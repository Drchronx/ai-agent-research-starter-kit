# 案例 9：EEG/ERP 神经科学实验

目标：让新手掌握从脑电实验设计到预处理、ERP/频域分析和结果写作的完整路线。

## 需要 Skills

```text
eeg-experiment-planning
eeg-preprocessing-pipeline
erp-segmentation-analysis
eeg-frequency-connectivity
eeg-ml-classification
eeg-results-writing-figures
```

## 复制模块

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category EEG -Workspace "D:\你的项目路径"
```

## 提示词

```text
请围绕“AI agent 解释性如何影响用户信任的神经加工”设计一个 ERP 实验。
请输出：理论机制、实验范式、事件码、trial 结构、试次数、采样率、通道和参考方案、预处理流程、ERP 成分窗口、频域/时频备选分析、机器学习分类可行性、QC 表、图表计划和 Methods/Results 模板。
不要覆盖 raw EEG 数据，不要把探索性时间窗写成验证性结果。
```

## 完成标准

- 有实验范式和事件码表。
- 有预处理和 QC 计划。
- 有 ERP/频域/连接/机器学习分析路线。
- 有脑电论文图表和写作模板。

