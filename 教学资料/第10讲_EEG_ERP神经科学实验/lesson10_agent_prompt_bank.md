# 第10讲 Agent 提示词库

## 1. 实验设计

```text
请基于我的研究主题，生成 eeg/study_design.md。

包括研究问题、理论机制、行为假设、神经假设、目标 ERP 成分/频段/连接/分类指标、实验范式、trial 时序、事件码设计原则、EEG 记录设置、预处理路线、分析路线、伦理和风险。不要把 ERP 成分直接等同心理构念。
```

## 2. 事件码表

```text
请生成 eeg/event_marker_table.xlsx 的内容草稿。

字段包括 marker_code、event_name、condition、trial_phase、time_locking_role、expected_count、behavior_link、included_in_erp、included_in_frequency、notes。检查事件码重复、条件不可区分、无法 time-lock 和行为日志无法对齐的问题。
```

## 3. 数据结构

```text
请生成 eeg/data_structure.md。

设计 raw、behavior、events、derivatives、scripts、figures、qc 的文件夹和命名规范。要求原始数据只读保存，所有衍生文件有版本号，subject/session/task/run 命名一致。
```

## 4. 环境检查

```text
请生成 eeg/environment_check.md。

记录 Python/MATLAB、MNE/EEGLAB、关键包版本、数据格式支持、缺失依赖、可运行入口、风险和下一步。
```

## 5. 预处理计划

```text
请基于 study_design.md、event_marker_table.xlsx 和数据格式，生成 eeg/preprocessing_plan.md。

包括原始数据保护、导入、通道名、montage、采样率、滤波、重参考、坏道、ICA、事件码完整性、epoch 前检查、剔除规则、输出命名和 reviewer-facing 预处理段落。
```

## 6. 预处理 QC 表

```text
请生成 eeg/preprocessing_qc.xlsx 的内容草稿。

每个被试记录 raw_file、sampling_rate、bad_channels、interpolated_channels、rejected_ica_components、total_events、valid_events、total_epochs、retained_epochs、retention_rate、exclusion_reason、qc_decision。
```

## 7. ERP 分析计划

```text
请生成 eeg/erp_analysis_plan.md。

包括 time-locking event、epoch window、baseline window、artifact rejection、condition averaging、ERP component、ROI electrodes、time window、amplitude/latency metric、statistical model、figure plan、confirmatory/exploratory 标记。
```

## 8. ERP 成分表

```text
请生成 eeg/erp_component_table.xlsx 的内容草稿。

字段包括 component、time_locking_event、epoch_window、baseline_window、time_window、roi_electrodes、metric、conditions、statistical_model、literature_or_rationale、confirmatory_status、notes。
```

## 9. 频域/连接计划

```text
请生成 eeg/frequency_connectivity_plan.md。

包括目标频段、PSD/STFT/wavelet/ERSP/ITC/coherence/PLV/wPLI 方法、baseline、归一化、ROI、时间窗、频段、多重比较、图表计划和解释边界。强调连接不是因果方向。
```

## 10. EEG 机器学习计划

```text
请生成 eeg/eeg_ml_plan.md。

包括 prediction target、label 来源、feature 类型、被试内/跨被试/留一被试验证、train/validation/test 划分、防泄漏规则、baseline model、deep model 是否必要、metrics、permutation test/nested CV 和解释边界。
```

## 11. 结果写作模板

```text
请生成 eeg/eeg_results_template.md。

包括 Participants and exclusions、EEG recording、Preprocessing、ERP analysis、Frequency/time-frequency/connectivity analysis、ML analysis、QC disclosure、Figure plan、Table plan、Results paragraph template、Limitations and reviewer risks。
```

## 12. 审稿人式审计

```text
请以严格审稿人视角审计第10讲工作区，生成 qc/eeg_analysis_audit.md。

检查研究问题与 EEG 指标匹配、事件码完整性、行为和 EEG 对齐、预处理先验、ICA/坏道依据、ERP 窗口和 ROI、频域/连接解释、ML 泄漏、QC 透明和写作是否过度。输出 pass/revise/fail。
```
