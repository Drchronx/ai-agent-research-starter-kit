from sklearn.linear_model import SGDClassifier

from sklearn_labeling_common import parse_common_args, run_sklearn_labeling


def main() -> None:
    args = parse_common_args("Run SGD text labeling on a labeled dataset.")
    run_sklearn_labeling(
        args,
        classifier_factory=lambda: SGDClassifier(
            loss="log_loss",
            penalty="l2",
            alpha=1e-4,
            max_iter=2000,
            tol=1e-3,
            random_state=42,
        ),
        method_name="sklearn_sgd",
    )


if __name__ == "__main__":
    main()
