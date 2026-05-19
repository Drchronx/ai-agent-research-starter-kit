# 案例 7：情景实验设计、分析和结果汇报

目标：让完全新手照着做一遍顶刊风格情景实验流程。这个案例不是只写问卷题，而是练习“真实论文范式学习 -> 实验设计 -> 预实验计划 -> 主实验分析 -> 结果汇报”。

## 你要用到的 Skills

```text
scenario-experiment-benchmark-mining
scenario-experiment-design
scenario-experiment-analysis
scenario-experiment-reporting
citation-management
scientific-critical-thinking
```

## 第 1 步：复制情景实验模块

```powershell
cd "<本项目路径>\本地Skills功能分类库"
powershell -ExecutionPolicy Bypass -File .\00_工具脚本\copy_skill_to_workspace.ps1 -Category 情景 -Workspace "D:\你的项目路径"
```

## 第 2 步：让 Agent 学真实顶刊范式

提示词：

```text
请使用 scenario-experiment-benchmark-mining，围绕“AI agent 解释性、用户信任和采纳意愿”检索并核验真实情景实验论文。
优先关注 JCR、JCP、JM、JMR、ISR、MISQ、JAP、OBHDP、JPSP、Psychological Science 等期刊。
输出一个范式矩阵：论文、期刊、年份、DOI/URL、理论、实验设计、操纵、样本、操纵检验、DV、中介/调节、分析模型、报告方式、可借鉴点。
不要编造引用；无法核验的放入待核验列表。
```

## 第 3 步：设计实验

提示词：

```text
请使用 scenario-experiment-design，把研究问题设计成一个 2 x 2 情景实验。
主题：AI agent 解释性如何影响用户信任和采纳意愿。
请输出：理论机制、实验条件、每个条件的刺激文本、操纵检验、真实感检验、混淆检验、注意力检查、主要量表、预实验方案、主实验样本量和分析计划。
```

## 第 4 步：用示例数据练分析

示例数据在：

```text
data/scenario_experiment_sample.csv
```

运行示例：

```powershell
python "<本项目路径>\本地Skills功能分类库\10_情景实验与行为研究Skills\scenario-experiment-analysis\scripts\analyze_scenario_experiment.py" `
  --data "<本项目路径>\零基础教学包\04_五个完整练习案例\案例7_情景实验设计分析汇报\data\scenario_experiment_sample.csv" `
  --dv adoption_intention `
  --ivs explainability `
  --mediators trust `
  --moderators expertise `
  --checks mc_explainability realism_check `
  --scale trust:trust1,trust2,trust3 `
  --outdir "<本项目路径>\零基础教学包\04_五个完整练习案例\案例7_情景实验设计分析汇报\output"
```

如果环境提示缺少依赖，先让 Agent 检查 `pandas`、`numpy`、`statsmodels`、`scipy` 的版本，不要自己乱改环境。

## 第 5 步：写 Method 和 Results

提示词：

```text
请使用 scenario-experiment-reporting，读取 output 中的分析结果，把本案例写成论文中的 Method 和 Results。
必须报告：样本、随机分配、排除规则、操纵检验、真实感检验、量表信度、主效应、中介或调节结果、效应量、精确 p 值、95% CI、图表建议和透明性说明。
不要把模拟数据当成真实研究结论。
```

## 完成标准

你应该得到：

- 一个顶刊情景实验范式矩阵。
- 一套 2 x 2 或中介/调节情景实验设计。
- 一个预实验和主实验执行计划。
- 一份分析输出文件夹。
- 一段可放进论文草稿的 Method/Results 模板。

