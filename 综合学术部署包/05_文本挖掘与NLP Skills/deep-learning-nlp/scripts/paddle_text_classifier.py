import argparse
import json
from collections import Counter
from pathlib import Path


PAD = "<PAD>"
UNK = "<UNK>"


def load_table(path, text_column=None):
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas.") from exc
    suffix = Path(path).suffix.lower()
    if suffix == ".txt":
        return pd.DataFrame({"text": [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]}), "text"
    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise SystemExit(f"Unsupported input: {path}")
    col = text_column or ("text" if "text" in df.columns else None)
    if not col or col not in df.columns:
        raise SystemExit(f"Specify --text-column. Available columns: {list(df.columns)}")
    return df, col


def tokenize(text):
    try:
        import jieba
    except ImportError as exc:
        raise SystemExit("Missing dependency: install jieba.") from exc
    return [t.strip() for t in jieba.lcut(str(text)) if t.strip()]


def build_vocab(texts, min_freq, max_vocab):
    counter = Counter()
    for text in texts:
        counter.update(tokenize(text))
    vocab = {PAD: 0, UNK: 1}
    for word, count in counter.most_common(max_vocab):
        if count >= min_freq and word not in vocab:
            vocab[word] = len(vocab)
    return vocab


def encode(text, vocab, max_len):
    ids = [vocab.get(token, vocab[UNK]) for token in tokenize(text)[:max_len]]
    if len(ids) < max_len:
        ids += [vocab[PAD]] * (max_len - len(ids))
    return ids


def make_arrays(texts, labels, vocab, label_to_id, max_len):
    import numpy as np
    x = np.array([encode(t, vocab, max_len) for t in texts], dtype="int64")
    y = np.array([label_to_id[str(label)] for label in labels], dtype="int64")
    return x, y


def create_dataset(x, y=None):
    import paddle

    class TextDataset(paddle.io.Dataset):
        def __init__(self, features, labels=None):
            self.features = features
            self.labels = labels

        def __len__(self):
            return len(self.features)

        def __getitem__(self, idx):
            if self.labels is None:
                return self.features[idx]
            return self.features[idx], self.labels[idx]

    return TextDataset(x, y)


def build_model(model_type, vocab_size, num_classes, embed_dim, hidden_size, num_filters, max_len):
    import paddle
    import paddle.nn as nn
    import paddle.nn.functional as F

    class DNNClassifier(nn.Layer):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
            self.fc1 = nn.Linear(embed_dim, hidden_size)
            self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
            self.out = nn.Linear(hidden_size // 2, num_classes)

        def forward(self, x):
            emb = self.embedding(x)
            mask = (x != 0).astype("float32").unsqueeze(-1)
            denom = paddle.maximum(mask.sum(axis=1), paddle.ones([x.shape[0], 1], dtype="float32"))
            pooled = (emb * mask).sum(axis=1) / denom
            h = F.relu(self.fc1(pooled))
            h = F.relu(self.fc2(h))
            return self.out(h)

    class TextCNN(nn.Layer):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
            self.convs = nn.LayerList([nn.Conv1D(embed_dim, num_filters, k) for k in [3, 4, 5] if k <= max_len])
            self.out = nn.Linear(len(self.convs) * num_filters, num_classes)

        def forward(self, x):
            emb = self.embedding(x).transpose([0, 2, 1])
            pools = []
            for conv in self.convs:
                h = F.relu(conv(emb))
                pools.append(F.max_pool1d(h, kernel_size=h.shape[2]).squeeze(-1))
            return self.out(paddle.concat(pools, axis=1))

    class RNNClassifier(nn.Layer):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
            self.gru = nn.GRU(embed_dim, hidden_size)
            self.out = nn.Linear(hidden_size, num_classes)

        def forward(self, x):
            emb = self.embedding(x)
            _, final_state = self.gru(emb)
            h = final_state[-1]
            return self.out(h)

    if model_type == "dnn":
        return DNNClassifier()
    if model_type == "cnn":
        return TextCNN()
    if model_type == "rnn":
        return RNNClassifier()
    raise SystemExit(f"Unsupported model type: {model_type}")


def evaluate(model, loader):
    import paddle
    correct = 0
    total = 0
    model.eval()
    with paddle.no_grad():
        for batch_x, batch_y in loader:
            logits = model(batch_x)
            pred = paddle.argmax(logits, axis=1)
            correct += int((pred == batch_y).astype("int64").sum().numpy())
            total += int(batch_y.shape[0])
    return correct / total if total else 0.0


def train(args):
    try:
        import numpy as np
        import paddle
        import pandas as pd
        from sklearn.model_selection import train_test_split
    except ImportError as exc:
        raise SystemExit("Missing dependency: install paddlepaddle, numpy, pandas, and scikit-learn.") from exc

    df, text_col = load_table(args.input, args.text_column)
    if args.label_column not in df.columns:
        raise SystemExit(f"Label column not found. Available columns: {list(df.columns)}")
    data = df[[text_col, args.label_column]].dropna()
    labels = sorted(str(x) for x in data[args.label_column].astype(str).unique())
    label_to_id = {label: idx for idx, label in enumerate(labels)}
    stratify = data[args.label_column] if data[args.label_column].value_counts().min() >= 2 else None
    train_df, val_df = train_test_split(data, test_size=args.test_size, random_state=args.random_state, stratify=stratify)

    vocab = build_vocab(train_df[text_col].astype(str).tolist(), args.min_freq, args.max_vocab)
    x_train, y_train = make_arrays(train_df[text_col].astype(str), train_df[args.label_column].astype(str), vocab, label_to_id, args.max_len)
    x_val, y_val = make_arrays(val_df[text_col].astype(str), val_df[args.label_column].astype(str), vocab, label_to_id, args.max_len)
    train_loader = paddle.io.DataLoader(create_dataset(x_train, y_train), batch_size=args.batch_size, shuffle=True)
    val_loader = paddle.io.DataLoader(create_dataset(x_val, y_val), batch_size=args.batch_size)

    paddle.seed(args.random_state)
    model = build_model(args.model_type, len(vocab), len(labels), args.embed_dim, args.hidden_size, args.num_filters, args.max_len)
    optimizer = paddle.optimizer.Adam(learning_rate=args.learning_rate, parameters=model.parameters())
    loss_fn = paddle.nn.CrossEntropyLoss()
    history = []

    for epoch in range(1, args.epochs + 1):
        model.train()
        losses = []
        for batch_x, batch_y in train_loader:
            logits = model(batch_x)
            loss = loss_fn(logits, batch_y)
            loss.backward()
            optimizer.step()
            optimizer.clear_grad()
            losses.append(float(loss.numpy()))
        val_acc = evaluate(model, val_loader)
        history.append({"epoch": epoch, "loss": float(np.mean(losses)), "val_accuracy": float(val_acc)})
        print(json.dumps(history[-1], ensure_ascii=False))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paddle.save(model.state_dict(), str(output_dir / "model.pdparams"))
    (output_dir / "vocab.json").write_text(json.dumps(vocab, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "labels.json").write_text(json.dumps(labels, ensure_ascii=False, indent=2), encoding="utf-8")
    config = {
        "model_type": args.model_type,
        "max_len": args.max_len,
        "embed_dim": args.embed_dim,
        "hidden_size": args.hidden_size,
        "num_filters": args.num_filters,
        "vocab_size": len(vocab),
        "num_classes": len(labels),
    }
    (output_dir / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "metrics.json").write_text(json.dumps({"history": history, "labels": labels}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output_dir": str(output_dir), "vocab_size": len(vocab), "labels": labels}, ensure_ascii=False, indent=2))


def predict(args):
    try:
        import numpy as np
        import paddle
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install paddlepaddle, numpy, and pandas.") from exc

    model_dir = Path(args.model_dir)
    config = json.loads((model_dir / "config.json").read_text(encoding="utf-8"))
    vocab = json.loads((model_dir / "vocab.json").read_text(encoding="utf-8"))
    labels = json.loads((model_dir / "labels.json").read_text(encoding="utf-8"))
    df, text_col = load_table(args.input, args.text_column)
    x = np.array([encode(t, vocab, config["max_len"]) for t in df[text_col].fillna("").astype(str)], dtype="int64")
    loader = paddle.io.DataLoader(create_dataset(x), batch_size=args.batch_size)
    model = build_model(config["model_type"], config["vocab_size"], config["num_classes"], config["embed_dim"], config["hidden_size"], config["num_filters"], config["max_len"])
    model.set_state_dict(paddle.load(str(model_dir / "model.pdparams")))
    model.eval()
    preds = []
    confs = []
    with paddle.no_grad():
        for batch_x in loader:
            logits = model(batch_x)
            probs = paddle.nn.functional.softmax(logits, axis=1).numpy()
            idx = probs.argmax(axis=1)
            preds.extend([labels[int(i)] for i in idx])
            confs.extend([float(row.max()) for row in probs])
    out = df.copy()
    out["predicted_label"] = preds
    out["confidence"] = confs
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(json.dumps({"rows": len(out), "output": str(output_path)}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Train or predict Paddle DNN/CNN/RNN text classifiers.")
    sub = parser.add_subparsers(dest="command", required=True)

    train_p = sub.add_parser("train")
    train_p.add_argument("--input", required=True)
    train_p.add_argument("--text-column")
    train_p.add_argument("--label-column", required=True)
    train_p.add_argument("--model-type", choices=["dnn", "cnn", "rnn"], required=True)
    train_p.add_argument("--output-dir", required=True)
    train_p.add_argument("--max-len", type=int, default=128)
    train_p.add_argument("--max-vocab", type=int, default=50000)
    train_p.add_argument("--min-freq", type=int, default=2)
    train_p.add_argument("--embed-dim", type=int, default=128)
    train_p.add_argument("--hidden-size", type=int, default=128)
    train_p.add_argument("--num-filters", type=int, default=128)
    train_p.add_argument("--batch-size", type=int, default=32)
    train_p.add_argument("--epochs", type=int, default=5)
    train_p.add_argument("--learning-rate", type=float, default=0.001)
    train_p.add_argument("--test-size", type=float, default=0.2)
    train_p.add_argument("--random-state", type=int, default=42)
    train_p.set_defaults(func=train)

    pred_p = sub.add_parser("predict")
    pred_p.add_argument("--model-dir", required=True)
    pred_p.add_argument("--input", required=True)
    pred_p.add_argument("--text-column")
    pred_p.add_argument("--output", required=True)
    pred_p.add_argument("--batch-size", type=int, default=64)
    pred_p.set_defaults(func=predict)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
