# Scenario Experiment Analysis Report


Data: `.\零基础教学包\04_五个完整练习案例\案例7_情景实验设计分析汇报\data\scenario_experiment_sample.csv`

Rows: 24, Columns: 11

DV: `adoption_intention`

IVs: explainability


## Reliability
Created composite scale columns from `--scale` specifications. See `reliability.csv`.


## Primary Model
Formula: `adoption_intention ~ explainability`

R-squared: 0.778

Cohen's d for `explainability` groups on `adoption_intention`: 3.587


## Manipulation Check: `mc_explainability`
Formula: `mc_explainability ~ explainability`; R-squared: 0.983


## Manipulation Check: `realism_check`
Formula: `realism_check ~ explainability`; R-squared: 0.052


## Mediation: `explainability` -> `trust` -> `adoption_intention`

Bootstrap indirect effect = -1.4729, 95% CI [-1.7093, -1.2464]


## Moderation: `expertise`
Formula: `adoption_intention ~ explainability * expertise`; R-squared: 0.993


## Notes
Review all outputs manually. This script is a first-pass helper and does not replace preregistered analysis decisions.