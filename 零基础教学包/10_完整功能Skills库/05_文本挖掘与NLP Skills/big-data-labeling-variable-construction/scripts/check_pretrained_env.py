import json


PYTORCH_HOME = "https://pytorch.org/"
PYTORCH_INSTALL = "https://pytorch.org/get-started/locally/"


def main() -> None:
    result = {
        "route": "pretrained_models",
        "pytorch_home": PYTORCH_HOME,
        "pytorch_install": PYTORCH_INSTALL,
        "torch_installed": False,
        "transformers_installed": False,
        "torch_version": None,
        "torch_cuda_version": None,
        "cuda_available": False,
        "device": "cpu",
        "status": "missing_dependencies",
        "message": "",
    }

    try:
        import torch  # type: ignore

        result["torch_installed"] = True
        result["torch_version"] = torch.__version__
        result["torch_cuda_version"] = torch.version.cuda
        result["cuda_available"] = bool(torch.cuda.is_available())
        result["device"] = "cuda" if result["cuda_available"] else "cpu"
    except Exception:
        pass

    try:
        import transformers  # type: ignore

        result["transformers_installed"] = True
        result["transformers_version"] = transformers.__version__
    except Exception:
        pass

    if result["torch_installed"] and result["transformers_installed"]:
        result["status"] = "ready"
        if result["cuda_available"]:
            result["message"] = "预训练模型环境已就绪，当前可使用 GPU。"
        else:
            result["message"] = "预训练模型环境已就绪，但当前将使用 CPU。"
    else:
        missing = []
        if not result["torch_installed"]:
            missing.append("torch")
        if not result["transformers_installed"]:
            missing.append("transformers")
        result["message"] = (
            "预训练模型路线缺少依赖："
            + ", ".join(missing)
            + "。请优先使用 PyTorch 官方安装页选择与你机器匹配的安装命令："
            + f"{PYTORCH_INSTALL}"
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
