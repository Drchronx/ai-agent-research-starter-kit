# 实证资产定价论文模板

## 目录

1. 标题页格式
2. 摘要结构
3. 引言模板
4. 方法论模板
5. 实证结果模板
6. 结论模板
7. 表格与图形规范

---

## 1. 标题页格式

### 标准标题页

```
Empirical Asset Pricing via Machine Learning*

Shihao Gu
Booth School of Business, University of Chicago

Bryan Kelly
Yale University, AQR Capital Management, and NBER

Dacheng Xiu
Booth School of Business, University of Chicago

* 致谢内容...
```

### 标题命名规则

| 类型 | 示例 |
|------|------|
| 方法驱动 | "Machine Learning in Asset Pricing" |
| 发现驱动 | "Trees and Neural Networks Dominate Stock Return Prediction" |
| 问题驱动 | "Measuring Risk Premiums: A Machine Learning Approach" |

---

## 2. 摘要结构

### 标准摘要(250词)

```markdown
We perform a comparative analysis of machine learning methods for the 
canonical problem of empirical asset pricing: measuring asset risk premiums. 

[第一句:问题定义] We demonstrate large economic gains to investors using 
machine learning forecasts, in some cases doubling the performance of 
leading regression-based strategies from the literature. 

[第二句:核心发现] We identify the best-performing methods (trees and neural 
networks) and trace their predictive gains to allowing nonlinear predictor 
interactions missed by other methods. 

[第三句:稳健性/一致性] All methods agree on the same set of dominant 
predictive signals, a set that includes variations on momentum, liquidity, 
and volatility. 

(JEL C52, C55, C58, G0, G1, G17)
```

### 摘要句式库

**问题定义句式**:
- "We conduct a comparative analysis of..."
- "We investigate whether..."
- "This paper studies the effect of..."
- "We examine the relationship between..."

**发现描述句式**:
- "We find that..."
- "Our results indicate..."
- "We document that..."
- "Consistent with predictions, we observe..."

**贡献说明句式**:
- "Our contributions are threefold."
- "This paper makes two primary contributions."
- "We provide new evidence on..."

---

## 3. 引言模板

### 3.1 研究动机(Paragraph 1-2)

```markdown
[领域核心问题] Return prediction is economically meaningful. The fundamental 
goal of asset pricing is to understand the behavior of risk premiums. 

[研究挑战] But risk premiums are notoriously difficult to measure: market 
efficiency forces return variation to be dominated by unforecastable news 
that obscures risk premiums. 

[现有方法局限] Traditional prediction methods break down when the predictor 
count approaches the observation count or predictors are highly correlated.
```

### 3.2 研究贡献(Paragraph 3-4)

```markdown
Our primary contributions are twofold. 

First, we provide a new set of benchmarks for the predictive accuracy of 
machine learning methods in measuring risk premiums of the aggregate market 
and individual stocks. This accuracy is summarized two ways. The first is a 
high out-of-sample predictive R² relative to preceding literature. Second, 
and more importantly, we demonstrate large economic gains to investors 
using machine learning forecasts.

Second, we synthesize the empirical asset pricing literature with the field 
of machine learning. Relative to traditional empirical methods in asset 
pricing, machine learning accommodates a far more expansive list of potential 
predictor variables and richer specifications of functional form.
```

### 3.3 论文结构

```markdown
The remainder of this paper proceeds as follows. Section 2 describes the 
collection of machine learning methods. Section 3 presents our empirical 
analysis of U.S. equity returns. Section 4 concludes.
```

---

## 4. 方法论模板

### 4.1 模型设定

```markdown
In its most general form, we describe an asset's excess return as an 
additive prediction error model:

    ri,t+1 = Et(ri,t+1) + εi,t+1,

where Et(ri,t+1) = g*(zi,t). 

Stocks are indexed as i = 1,...,Nt and months by t = 1,...,T. Our objective 
is to isolate a representation of Et(ri,t+1) as a function of predictor 
variables that maximizes the out-of-sample explanatory power for realized 
ri,t+1. We denote those predictors as the P dimensional vector zi,t, and 
assume the conditional expected return g*(·) is a flexible function of 
these predictors.
```

### 4.2 变量定义表

| 变量 | 符号 | 定义 | 数据来源 |
|------|------|------|----------|
| 超额收益 | ri,t+1 | 股票i在t+1月的收益减无风险利率 | CRSP |
| 市值 | Size | log(股价×流通股数) | CRSP/Compustat |
| 账面市值比 | B/M | 股东权益/市值 | Compustat |
| 动量 | Mom | 过去12个月收益率 | CRSP |

### 4.3 样本划分

```markdown
We divide the 60 years of data into 18 years of training sample (1957–1974), 
12 years of validation sample (1975–1986), and the remaining 30 years 
(1987–2016) for out-of-sample testing. Because machine learning algorithms 
are computationally intensive, we avoid recursively refitting models each 
month. Instead, we refit once every year as most of our signals are updated 
once per year.
```

---

## 5. 实证结果模板

### 5.1 基准回归表格

```
Table 1
Monthly out-of-sample stock-level prediction performance (percentage R²)

OLS with all covariates, OLS-3 (which preselects size, book-to-market, and 
momentum as the only covariates), PLS, PCR, elastic net (ENet), generalized 
linear model with group lasso (GLM), random forest (RF), gradient boosted 
regression trees (GBRT), and neural network architectures with one to five 
layers (NN1,...,NN5).

                     (1)        (2)        (3)
OLS                 -3.46      ---        ---
OLS-3                0.16      0.21       0.18
PLS                  0.26      0.31       0.29
PCR                  0.27      0.32       0.30
ENet                 0.11      0.15       0.13
RF                   0.33      0.38       0.36
GBRT                 0.35      0.41       0.38
NN1                  0.34      0.39       0.37
NN2                  0.36      0.42       0.39
NN3                  0.40      0.45       0.42
NN4                  0.38      0.43       0.40
NN5                  0.35      0.40       0.38

Note: This table reports monthly out-of-sample R² (in %) for various 
prediction methods. Column (1) reports results for the full sample, 
columns (2) and (3) report results for the top-1000 and bottom-1000 
stocks by market value, respectively.
```

### 5.2 结果描述句式

```markdown
The first row of Table 1 reports R² for the entire pooled sample. The OLS 
model using all 920 features produces an R² of −3.46%, indicating it is 
handily dominated by applying a naive forecast of zero to all stocks in 
all months.

Regularizing the linear model via dimension reduction improves predictions 
even further. By forming a few linear combinations of predictors, PLS and 
PCR raise the out-of-sample R² to 0.26% and 0.27%, respectively.

When we expand the model to accommodate nonlinear predictive relationships 
via trees and neural networks, we find that these methods unambiguously 
improve predictions with monthly stock-level R² between 0.33% and 0.40%.
```

---

## 6. 结论模板

```markdown
Machine learning has great potential for improving risk premium measurement, 
which is fundamentally a problem of prediction. It amounts to best 
approximating the conditional expectation E(ri,t+1 | Ft), where ri,t+1 is 
an asset's return in excess of the risk-free rate, and Ft is the true and 
unobservable information set of market participants. This is a domain in 
which machine learning algorithms excel.

But these improved predictions are only measurements. The measurements do 
not tell us about economic mechanisms or equilibria. Machine learning 
methods on their own do not identify deep fundamental associations among 
asset prices and conditioning variables. When the objective is to understand 
economic mechanisms, machine learning still may be useful. It requires the 
economist to add structure—to build a hypothesized mechanism into the 
estimation problem.

A nascent literature is marrying machine learning to equilibrium asset 
pricing, and this remains an exciting direction for future research.
```

---

## 7. 表格与图形规范

### 7.1 表格模板

```latex
\begin{table}[htbp]
\centering
\caption{Monthly Out-of-Sample Prediction Performance}
\label{tab:prediction}
\begin{tabular}{lccc}
\hline\hline
Method & (1) Full Sample & (2) Top 1000 & (3) Bottom 1000 \\
\hline
OLS    & -3.46*** & ---    & ---    \\
OLS-3  & 0.16***  & 0.21*** & 0.18*** \\
PLS    & 0.26***  & 0.31*** & 0.29*** \\
PCR    & 0.27***  & 0.32*** & 0.30*** \\
ENet   & 0.11***  & 0.15*** & 0.13*** \\
RF     & 0.33***  & 0.38*** & 0.36*** \\
GBRT   & 0.35***  & 0.41*** & 0.38*** \\
NN3    & 0.40***  & 0.45*** & 0.42*** \\
\hline
\end{tabular}
\caption*{\small Note: This table reports monthly out-of-sample $R^2$ 
(in percentage) for various prediction methods. ***, **, * denote 
significance at the 1\%, 5\%, and 10\% levels, respectively.}
\end{table}
```

### 7.2 图形模板

```latex
\begin{figure}[htbp]
\centering
\caption{Model Complexity Over Time}
\label{fig:complexity}
% 图形内容
\end{figure}
```

---

## 附录:常用句式库

### 过渡句

| 场景 | 句式 |
|------|------|
| 引出新话题 | "We next turn to...", "Turning to...", "We now examine..." |
| 对比分析 | "In contrast, ...", "Conversely, ...", "However, ..." |
| 因果关系 | "As a result,...", "Consequently,...", "This leads to..." |
| 强调重要性 | "More importantly,...", "Crucially,...", "Most notably,..." |
| 引用文献 | "As shown in Smith (2020),...", "Consistent with Smith (2020),..." |

### 统计显著性表述

| 表达 | 含义 |
|------|------|
| "statistically significant at the 1% level" | p < 0.01 |
| "significant at conventional levels" | p < 0.05 |
| "marginally significant" | p < 0.1 |
| "cannot reject the null" | 不显著 |
