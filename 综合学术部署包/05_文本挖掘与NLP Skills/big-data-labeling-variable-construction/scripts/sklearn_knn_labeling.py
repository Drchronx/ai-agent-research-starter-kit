from sklearn.neighbors import KNeighborsClassifier

from sklearn_labeling_common import parse_common_args, run_sklearn_labeling


def main() -> None:
    args = parse_common_args("Run KNN text labeling on a labeled dataset.")
    run_sklearn_labeling(
        args,
        classifier_factory=lambda: KNeighborsClassifier(n_neighbors=3, weights="distance"),
        method_name="sklearn_knn",
    )


if __name__ == "__main__":
    main()
