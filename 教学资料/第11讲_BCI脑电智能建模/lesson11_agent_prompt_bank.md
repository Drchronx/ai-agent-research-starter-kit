# 第11讲 Agent Prompt Bank

## Prompt 1：建立 BCI 项目结构

```text
请使用 skills/bci-data-structure。基于 input/研究问题.md、data/raw、data/events、data/labels，生成 bci/bci_project_structure.md。定义 subject-session-run-trial-window 层级、metadata schema、label schema、split unit、class-balance audit 和 leakage risks。禁止覆盖 raw EEG。
```

## Prompt 2：选择 benchmark 数据集

```text
请使用 skills/bci-benchmark-datasets。我的任务是：[填写任务]。请生成 bci/bci_dataset_selection.md，比较 3-5 个候选公开数据集或自有数据是否可用，字段包括 subjects、sessions、channels、sampling_rate、labels、license、citation、split、限制。不要编造 URL、license 或 citation。
```

## Prompt 3：定义预测任务

```text
请生成 bci/bci_prediction_task.md。写清 prediction target、class labels、label source、prediction time、input unit、evaluation claim、class balance、chance level、exclusion criteria 和 cannot-claim boundary。
```

## Prompt 4：生成特征工程计划

```text
请使用 skills/eeg-feature-engineering-bci。生成 bci/bci_feature_engineering_plan.md。比较 band power、ERP、CSP/FBCSP、Riemannian、connectivity、time-window features。说明窗口、通道、频段、fit 位置、输出字段和泄漏风险。
```

## Prompt 5：生成 classical baseline 计划

```text
请使用 skills/eeg-ml-classical-bci。生成 bci/bci_classical_ml_plan.md。至少包括 chance、majority、LDA/logistic、SVM、CSP+LDA、Riemannian。写清 pipeline、nested CV、hyperparameter plan、metrics、subject-wise report、permutation test 和 model comparison。
```

## Prompt 6：判断 deep learning 是否适合

```text
请使用 skills/eeg-deep-learning-bci。基于数据量、split、baseline 和任务，生成 bci/bci_deep_learning_plan.md。候选 EEGNet、DeepConvNet、ShallowConvNet、CNN-LSTM、TCN、Transformer。必须给出是否建议使用 deep learning、tensor schema、augmentation、early stopping、metrics、failure risks。
```

## Prompt 7：跨被试迁移计划

```text
请使用 skills/eeg-cross-subject-transfer-bci。生成 bci/bci_cross_subject_transfer_plan.md。说明 target deployment、validation、source/target split、adaptation method、calibration policy、subject-wise metrics、failure-case analysis。
```

## Prompt 8：在线或伪在线计划

```text
请使用 skills/bci-online-decoding。生成 bci/bci_online_decoding_plan.md。说明 offline/pseudo-online/real online、window length、step size、causal preprocessing、decision rule、latency budget、online metrics、offline-online gap 和 deployment risks。
```

## Prompt 9：泄漏审计

```text
请使用 skills/eeg-model-evaluation-leakage。读取 bci/ 下全部计划，生成 qc/bci_leakage_audit.md。逐项检查 window、subject、session、normalization、CSP/PCA/feature selection、hyperparameter tuning、target test label、augmentation、benchmark comparability。每项给 pass/revise/fail 和 required fix。
```

## Prompt 10：模型解释审计

```text
请使用 skills/eeg-model-interpretability-bci。生成 qc/bci_model_interpretability_audit.md。说明可用解释方法、适合解释的层级、不能支持的神经机制 claim、需要的人类核验项和论文写作边界。
```

## Prompt 11：结果报告

```text
请使用 skills/bci-results-reporting。生成 bci/bci_results_report.md。必须先报告 split，再报告 baseline、chance level、subject-wise metrics、aggregate metrics with uncertainty、confusion matrix、class-level metrics、leakage safeguards、failed subjects、limitations 和 claim boundary。没有真实结果时，输出表格模板，不要编造指标。
```
