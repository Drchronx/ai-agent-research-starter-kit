import json


def main() -> None:
    import torch

    from transformer_labeling_common import detect_torch_runtime

    runtime = detect_torch_runtime(torch)
    print(json.dumps(runtime, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
