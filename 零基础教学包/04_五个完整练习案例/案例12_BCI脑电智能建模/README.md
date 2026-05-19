# 案例 12：BCI 脑电智能建模

目标：让新手学会把 EEG/BCI 数据从“能跑模型”推进到“评价可信、能写论文”。重点不是堆深度学习模型，而是先避免数据泄漏，再谈准确率。

## 需要 Skills

```text
bci-data-structure
eeg-feature-engineering-bci
eeg-ml-classical-bci
eeg-deep-learning-bci
eeg-cross-subject-transfer-bci
eeg-model-evaluation-leakage
bci-online-decoding
eeg-model-interpretability-bci
bci-benchmark-datasets
bci-results-reporting
```

## 复制模块

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category BCI -Workspace "D:\你的项目路径"
```

## 第 1 步：建立 BCI 元数据表

```powershell
python "<本项目路径>\本地Skills功能分类库\15_BCI脑电智能建模Skills\bci-data-structure\scripts\create_bci_metadata_template.py" --out "D:\你的项目路径\data\bci_metadata_template.csv"
```

## 第 2 步：做防泄漏审计表

```powershell
python "<本项目路径>\本地Skills功能分类库\15_BCI脑电智能建模Skills\eeg-model-evaluation-leakage\scripts\create_bci_evaluation_audit.py" --out "D:\你的项目路径\output\bci_evaluation_leakage_audit.csv"
```

## 第 3 步：让 Agent 设计建模流程

提示词：

```text
请使用 BCI 脑电智能建模模块，围绕“运动想象 EEG 二分类”构建完整建模流程。
请先用 bci-data-structure 定义 subject/session/run/trial/window/label 和 split 单位。
再用 eeg-feature-engineering-bci 设计 band power、CSP/FBCSP 和 Riemannian 特征。
用 eeg-ml-classical-bci 设计 LDA、SVM、CSP+LDA 基线。
用 eeg-deep-learning-bci 设计 EEGNet 和 DeepConvNet 的训练流程。
用 eeg-model-evaluation-leakage 检查 trial-window 泄漏、subject split、标准化、CSP、PCA、特征选择和调参泄漏。
最后用 bci-results-reporting 给出 subject-wise table、balanced accuracy、AUC、F1、混淆矩阵、置信区间和论文 Results 模板。
不要把 trial-level random split 写成 cross-subject decoding。
```

## 完成标准

- 有 BCI 元数据表。
- 有特征工程路线。
- 有传统机器学习基线。
- 有深度学习训练计划。
- 有防泄漏审计表。
- 有 subject-wise 结果表和论文 Results 模板。

