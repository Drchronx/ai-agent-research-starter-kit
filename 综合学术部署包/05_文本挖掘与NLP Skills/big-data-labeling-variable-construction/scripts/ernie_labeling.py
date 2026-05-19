from transformer_labeling_common import parse_common_args, run_transformer_labeling


def main() -> None:
    args = parse_common_args("Fine-tune and evaluate an ERNIE-style text labeling model.")
    run_transformer_labeling(args, method_name="pretrained_ernie")


if __name__ == "__main__":
    main()
