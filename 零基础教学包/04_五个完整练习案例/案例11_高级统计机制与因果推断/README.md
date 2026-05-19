# 案例 11：高级统计机制与因果推断

目标：让新手学会判断什么时候用中介调节、SEM、多层模型、DID、PSM、IV、RDD、DML，什么时候只能说相关。

## 需要 Skills

```text
process-mediation-moderation
sem-cfa-path-latent
multilevel-longitudinal-modeling
causal-inference-design-audit
did-psm-iv-rdd-dml-event-study
statistical-results-tables
```

## 复制模块

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 因果 -Workspace "D:\你的项目路径"
```

## 提示词

```text
请审计我的研究设计是否支持因果、机制或边界条件结论。
变量：X=[写处理或自变量]，Y=[写因变量]，M=[中介]，W=[调节]，数据结构=[横截面/面板/实验/多层]。
请判断适合中介调节、SEM、多层模型、DID、PSM、IV、RDD、DML 还是只能做相关分析。
输出：可支持的结论、不能说的结论、模型公式、识别假设、稳健性、结果表结构和 Results 写法。
```

## 完成标准

- 有因果识别审计。
- 有模型选择理由。
- 有结果表结构。
- 有“能说/不能说”的论文语言边界。

