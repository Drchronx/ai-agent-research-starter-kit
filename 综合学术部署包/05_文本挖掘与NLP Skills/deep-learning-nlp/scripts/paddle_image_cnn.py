import argparse
import json
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp"}


def collect_images(root):
    root = Path(root)
    if root.is_file():
        return [(root, None)]
    if not root.exists():
        raise SystemExit(f"Input path not found: {root}")
    items = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            label = path.parent.name if path.parent != root else None
            items.append((path, label))
    if not items:
        raise SystemExit(f"No images found under: {root}")
    return items


class ImageFolderDataset:
    def __init__(self, root, labels=None, image_size=28):
        try:
            import paddle
        except ImportError as exc:
            raise SystemExit("Missing dependency: install paddlepaddle.") from exc
        self._base = paddle.io.Dataset
        self.root = Path(root)
        self.image_size = image_size
        raw_items = collect_images(self.root)
        folder_labels = sorted({label for _, label in raw_items if label is not None}, key=lambda x: int(x) if str(x).isdigit() else str(x))
        self.labels = labels or folder_labels
        self.label_to_id = {str(label): idx for idx, label in enumerate(self.labels)}
        self.items = []
        for path, label in raw_items:
            if label is None:
                continue
            if str(label) in self.label_to_id:
                self.items.append((path, self.label_to_id[str(label)]))
        if not self.items:
            raise SystemExit(f"No labeled images found under: {self.root}")

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        import numpy as np
        import paddle
        from PIL import Image

        path, label = self.items[idx]
        img = Image.open(path).convert("L").resize((self.image_size, self.image_size))
        arr = np.array(img).astype("float32") / 255.0
        arr = arr[None, :, :]
        return paddle.to_tensor(arr, dtype="float32"), paddle.to_tensor(label, dtype="int64")


def make_dataset_class():
    import paddle

    class Dataset(ImageFolderDataset, paddle.io.Dataset):
        pass

    return Dataset


def build_lenet(num_classes=10):
    import paddle

    class LeNet(paddle.nn.Layer):
        def __init__(self):
            super().__init__()
            self.conv1 = paddle.nn.Conv2D(in_channels=1, out_channels=6, kernel_size=5, stride=1, padding=2)
            self.relu1 = paddle.nn.ReLU()
            self.pool1 = paddle.nn.MaxPool2D(kernel_size=2, stride=2)
            self.conv2 = paddle.nn.Conv2D(in_channels=6, out_channels=16, kernel_size=5, stride=1, padding=0)
            self.relu2 = paddle.nn.ReLU()
            self.pool2 = paddle.nn.MaxPool2D(kernel_size=2, stride=2)
            self.flatten = paddle.nn.Flatten()
            self.linear1 = paddle.nn.Linear(400, 120)
            self.relu3 = paddle.nn.ReLU()
            self.linear2 = paddle.nn.Linear(120, 84)
            self.relu4 = paddle.nn.ReLU()
            self.linear3 = paddle.nn.Linear(84, num_classes)

        def forward(self, x):
            x = self.pool1(self.relu1(self.conv1(x)))
            x = self.pool2(self.relu2(self.conv2(x)))
            x = self.flatten(x)
            x = self.relu3(self.linear1(x))
            x = self.relu4(self.linear2(x))
            return self.linear3(x)

    return LeNet()


def evaluate(model, loader):
    import paddle

    correct = 0
    total = 0
    model.eval()
    with paddle.no_grad():
        for x, y in loader:
            logits = model(x)
            pred = paddle.argmax(logits, axis=1)
            correct += int((pred == y).astype("int64").sum().numpy())
            total += int(y.shape[0])
    return correct / total if total else 0.0


def train(args):
    try:
        import numpy as np
        import paddle
    except ImportError as exc:
        raise SystemExit("Missing dependency: install paddlepaddle and numpy.") from exc

    paddle.seed(args.random_state)
    Dataset = make_dataset_class()
    train_ds = Dataset(args.train_dir, image_size=args.image_size)
    test_ds = Dataset(args.test_dir, labels=train_ds.labels, image_size=args.image_size) if args.test_dir else None
    train_loader = paddle.io.DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    test_loader = paddle.io.DataLoader(test_ds, batch_size=args.batch_size) if test_ds else None

    model = build_lenet(num_classes=len(train_ds.labels))
    optimizer = paddle.optimizer.Adam(learning_rate=args.learning_rate, parameters=model.parameters())
    loss_fn = paddle.nn.CrossEntropyLoss()
    history = []

    for epoch in range(1, args.epochs + 1):
        model.train()
        losses = []
        for x, y in train_loader:
            logits = model(x)
            loss = loss_fn(logits, y)
            loss.backward()
            optimizer.step()
            optimizer.clear_grad()
            losses.append(float(loss.numpy()))
        row = {"epoch": epoch, "loss": float(np.mean(losses))}
        if test_loader:
            row["test_accuracy"] = float(evaluate(model, test_loader))
        history.append(row)
        print(json.dumps(row, ensure_ascii=False))

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paddle.save(model.state_dict(), str(out / "model.pdparams"))
    (out / "labels.json").write_text(json.dumps(train_ds.labels, ensure_ascii=False, indent=2), encoding="utf-8")
    config = {"image_size": args.image_size, "num_classes": len(train_ds.labels), "architecture": "LeNet"}
    (out / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "metrics.json").write_text(json.dumps({"history": history}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "labels": train_ds.labels, "history": history}, ensure_ascii=False, indent=2))


def load_image_tensor(path, image_size):
    import numpy as np
    import paddle
    from PIL import Image

    img = Image.open(path).convert("L").resize((image_size, image_size))
    arr = np.array(img).astype("float32") / 255.0
    arr = arr[None, None, :, :]
    return paddle.to_tensor(arr, dtype="float32")


def predict(args):
    try:
        import pandas as pd
        import paddle
    except ImportError as exc:
        raise SystemExit("Missing dependency: install paddlepaddle and pandas.") from exc

    model_dir = Path(args.model_dir)
    labels = json.loads((model_dir / "labels.json").read_text(encoding="utf-8"))
    config = json.loads((model_dir / "config.json").read_text(encoding="utf-8"))
    model = build_lenet(num_classes=len(labels))
    model.set_state_dict(paddle.load(str(model_dir / "model.pdparams")))
    model.eval()

    rows = []
    with paddle.no_grad():
        for path, true_label in collect_images(args.input):
            logits = model(load_image_tensor(path, config["image_size"]))
            probs = paddle.nn.functional.softmax(logits, axis=1).numpy()[0]
            pred_id = int(probs.argmax())
            row = {
                "path": str(path),
                "predicted_label": labels[pred_id],
                "confidence": float(probs[pred_id]),
            }
            if true_label is not None:
                row["true_label"] = true_label
                row["correct"] = str(true_label) == str(labels[pred_id])
            rows.append(row)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False, encoding="utf-8-sig")
    summary = {"rows": len(rows), "output": str(output)}
    if rows and "correct" in rows[0]:
        summary["accuracy"] = sum(1 for row in rows if row["correct"]) / len(rows)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Train or predict the course LeNet CNN image classifier.")
    sub = parser.add_subparsers(dest="command", required=True)

    train_p = sub.add_parser("train")
    train_p.add_argument("--train-dir", required=True)
    train_p.add_argument("--test-dir")
    train_p.add_argument("--output-dir", required=True)
    train_p.add_argument("--epochs", type=int, default=1)
    train_p.add_argument("--batch-size", type=int, default=128)
    train_p.add_argument("--learning-rate", type=float, default=0.001)
    train_p.add_argument("--image-size", type=int, default=28)
    train_p.add_argument("--random-state", type=int, default=42)
    train_p.set_defaults(func=train)

    pred_p = sub.add_parser("predict")
    pred_p.add_argument("--model-dir", required=True)
    pred_p.add_argument("--input", required=True)
    pred_p.add_argument("--output", required=True)
    pred_p.set_defaults(func=predict)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
