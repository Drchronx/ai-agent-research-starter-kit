# BCI Model Plan Template

## 1. Prediction Task

- Target:
- Label source:
- Prediction time:
- Classes or regression target:
- Input unit:
- Evaluation claim:

## 2. Data Structure

- Subjects:
- Sessions:
- Runs:
- Trials:
- Windows:
- Metadata file:

## 3. Split Design

- Split unit:
- Train:
- Validation:
- Test:
- Nested CV:
- Claim supported:
- Claim not supported:

## 4. Feature Engineering

| Feature | Window | Channels | Frequency | Fit inside fold | Output |
|---|---|---|---|---|---|
| band power |  |  |  | yes/no |  |
| ERP |  |  |  | yes/no |  |
| CSP/FBCSP |  |  |  | yes/no |  |
| Riemannian |  |  |  | yes/no |  |

## 5. Models

- Chance:
- Majority:
- LDA/logistic:
- SVM:
- CSP+LDA:
- Riemannian:
- Deep learning, if justified:

## 6. Metrics

- Accuracy:
- Balanced accuracy:
- AUC:
- F1:
- Confusion matrix:
- Subject-wise:
- Uncertainty:

## 7. Risks

- Leakage:
- Class imbalance:
- Failed subjects:
- Overfitting:
- Online gap:
