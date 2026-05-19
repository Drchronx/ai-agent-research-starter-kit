from sklearn.ensemble import RandomForestClassifier

from sklearn_labeling_common import parse_common_args, run_sklearn_labeling


def main() -> None:
    args = parse_common_args("Run Random Forest text labeling on a labeled dataset.")
    run_sklearn_labeling(
        args,
        classifier_factory=lambda: RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced",
        ),
        method_name="sklearn_random_forest",
    )


if __name__ == "__main__":
    main()
