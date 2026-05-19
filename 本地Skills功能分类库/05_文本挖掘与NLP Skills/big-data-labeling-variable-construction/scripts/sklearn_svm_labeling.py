from sklearn.svm import LinearSVC

from sklearn_labeling_common import parse_common_args, run_sklearn_labeling


def main() -> None:
    args = parse_common_args("Run SVM text labeling on a labeled dataset.")
    run_sklearn_labeling(
        args,
        classifier_factory=lambda: LinearSVC(random_state=42),
        method_name="sklearn_svm",
    )


if __name__ == "__main__":
    main()
