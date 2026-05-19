---
name: ssci-literature-review
description: 基于Phillip Chong Ho Shon方法论系统解码SSCI论文各部分，提供结构化剖析与批判性解读；当用户需要分析学术论文、撰写文献综述、理解论文特定部分（摘要、引言、方法、结果、讨论等）或进行文献对话时使用
---

# SSCI论文文献综述解码专家

## 任务目标
- 本Skill用于：使用Shon方法论系统解码SSCI论文，提升学术文献阅读与综述写作能力
- 能力包含：论文部分提取、方法论剖析、批判性解读、文献综述构建
- 触发条件：用户上传论文文件并指定需要分析的论文部分，或询问如何阅读/分析学术论文

## 前置准备
- 用户需上传待分析的论文文件（PDF/DOCX/TXT格式）
- 明确指定需要提取和分析的论文部分（如摘要、引言、方法、结果、讨论等）

## 操作步骤

### 标准流程

**步骤0：展示Reading Codes参考表**

在开始分析前，向用户展示Shon Reading Codes体系，帮助用户理解解码框架：

**论文核心结构Codes**

| Code | 全称 | 位置 | 中文含义 |
|------|------|------|----------|
| **WTD** | What They Do | Introduction/Literature Review | 研究目的：作者声称要做什么，捕捉主要研究问题 |
| **SPL** | Summary of Previous Literature | Literature Review | 文献总结：总结已有研究结果，浓缩复杂思想 |
| **CPL** | Critique of Previous Literature | Literature Review | 文献批判：批判已有研究的局限性，为本研究提供正当性 |
| **GAP** | Gap | Literature Review | 研究空白：指出当前文献中缺失的要素 |
| **RAT** | Rationale | Literature Review/Introduction | 研究理据：论证为何此研究是必要且正当的 |
| **ROF** | Results of Findings | Results/Discussion | 研究发现：描述当前文章的主要结果 |
| **RCL** | Results Consistent with Literature | Discussion | 与文献一致：研究发现与已有文献一致 |
| **RTC** | Results To the Contrary | Discussion | 与文献相悖：研究发现与已有文献不一致 |
| **WTDD** | What They Did | Conclusion | 研究贡献：陈述已回答的研究问题及贡献 |
| **RFW** | Recommendations for Future Works | Conclusion | 未来建议：指出仍缺失的内容，建议未来研究 |

**批判性阅读策略Codes**

| Code | 全称 | 中文含义 |
|------|------|----------|
| **POC** | Point of Critique | 批判点：当前文章的缺陷，可用于未来批判 |
| **MOP** | Missed an Obvious Point | 遗漏点：作者错过与早期研究的明显联系 |
| **RPP** | Relevant Point to Pursue | 可追加点：可在未来论文中作为POC使用 |
| **WIL** | Will... | 逻辑验证：理论联系能否逻辑推演到结论 |

**标准论证链**：
```
引言：SPL → CPL → GAP → RAT → WTD
讨论：ROF → RCL/RTC → WTDD
结论：WTDD → RFW
```

---

**步骤1：文献读取与部分提取**
- 读取用户上传的论文文件
- 根据用户指定，精确定位并提取论文的特定部分
- 保留原文结构，确保内容完整性

**步骤2：方法论解码分析**
- 参考 [references/shon-methodology.md](references/shon-methodology.md) 中的方法论框架
- 根据提取的论文部分，应用相应的解码技巧：
  - **摘要**：识别研究问题、核心发现、理论贡献
  - **引言**：解析研究背景、问题提出、理论框架、研究目的
  - **文献综述**：梳理理论脉络、研究空白、理论对话
  - **方法**：评估研究设计、样本选择、数据分析策略
  - **结果**：解读数据呈现、主要发现、统计推断
  - **讨论**：分析结论推导、理论贡献、研究局限、未来方向

**步骤3：批判性剖析**
按照Shon方法论执行深度剖析：
1. **论证结构分析**：识别作者的论证逻辑链条
2. **理论框架评估**：评估理论基础的选择与运用
3. **方法论批判**：审视研究设计的合理性与局限
4. **证据链追踪**：从数据到结论的推理验证
5. **学术对话定位**：该研究在学科脉络中的位置

**步骤4：输出解码报告**
生成结构化的剖析报告，包含：
- 论文部分的原文提取（完整引用）
- 方法论解码要点
- 批判性分析结论
- 文献综述写作建议（如适用）

### 可选分支

**分支A：文献综述构建**
- 当用户需要撰写文献综述时
- 基于多篇论文的解码结果，进行主题整合
- 识别研究脉络、理论对话、研究空白
- 构建结构化的文献综述框架

**分支B：理论对话分析**
- 当用户关注理论框架时
- 提取论文的核心理论视角
- 分析不同论文之间的理论对话关系
- 识别理论发展脉络与争议点

**分支C：研究方法比较**
- 当用户关注方法论时
- 比较不同论文的研究设计
- 评估方法论选择的适用性
- 提炼方法论创新点

**分支D：逐句解读分析与写作示范**

当用户需要深入理解文本细节或学习学术写作时，执行以下三阶段自动流程：

**阶段1：逐句解码**
- 对指定部分进行逐句剖析，每句标注Reading Code
- 从三个维度解读每句话：
  - **作用**：这句话在论证结构中的功能定位（用Reading Code标注）
  - **意图**：作者通过这句话想要达到的目的
  - **表达方式**：作者使用的修辞策略与语言技巧
- 每句英文原文后提供中文翻译
- 解码完成后，自动进入阶段2

**阶段2：用户选题交互**
- 智能体询问：**"您的研究主题或研究目的是什么？请简要描述您想研究的核心问题。"**
- 等待用户提供：研究主题、研究目的或论文选题
- 收到用户回复后，自动进入阶段3

**阶段3：写作示范**
- 根据用户研究主题，逐段撰写示范文本
- 写作规范：
  - 正文使用英文
  - 每个句子后添加（）注释：**(Code: 中文含义)**
  - 每个英文句子后提供中文翻译
  - 示例：*Previous studies have demonstrated that digital transformation significantly enhances operational efficiency (Chen, 2020; Li, 2021). (SPL: 总结已有研究，表明数字化转型能显著提升运营效率)*

  **中文**：先前的研究表明，数字化转型能显著提升运营效率。
- 参考 [references/shon-methodology.md](references/shon-methodology.md) 中的"逐句解读方法论"章节

## 资源索引
- 方法论框架：见 [references/shon-methodology.md](references/shon-methodology.md)（Shon方法论完整解读，包含各论文部分的解码技巧）

## 注意事项
- 在应用方法论时，优先读取references中的方法论框架，确保分析的系统性
- 剖析应保持学术客观性，既要识别论文贡献，也要指出局限
- 批判性分析应基于证据，避免主观臆断
- 文献综述应体现理论对话与研究脉络，避免简单罗列
- 充分利用智能体的文本理解与推理能力，无需借助外部工具

## 使用示例

### 示例1：单部分深度解码
**用户请求**："分析这篇论文的引言部分"
**执行方式**：智能体读取论文 → 提取引言 → 应用Shon方法论解码 → 输出剖析报告
**输出包含**：
- 研究背景的构建方式
- 研究问题的提出逻辑
- 理论框架的选择依据
- 研究目的与假设的论证链条

### 示例2：方法论部分批判
**用户请求**："评估这篇论文的研究方法"
**执行方式**：智能体读取方法部分 → 应用方法论评估框架 → 输出批判性分析
**关键分析点**：
- 研究设计的类型与适用性
- 样本选择的合理性
- 数据收集与分析方法的严谨性
- 方法论的局限与改进建议

### 示例3：文献综述构建
**用户请求**："为这3篇论文撰写文献综述"
**执行方式**：智能体分别解码各论文 → 识别共同主题 → 构建综述框架
**输出结构**：
- 研究主题的理论脉络
- 各研究的贡献与局限
- 研究空白与未来方向
- 整合性结论

### 示例4：逐句解读分析与写作示范
**用户请求**："逐句解读这篇论文的引言部分"
**执行方式**：智能体读取论文 → 识别Reading Codes → 逐句剖析 → 询问用户选题 → 撰写示范文本

---

**阶段1：逐句解码**

**【第1句】**

**原文**：
> Previous studies have shown that organizational learning positively influences innovation performance (Smith, 2018; Johnson, 2019).

**中文翻译**：先前的研究表明，组织学习正向影响创新绩效（Smith, 2018; Johnson, 2019）。

**Reading Code**：**SPL** (Summary of Previous Literature)

**位置**：Introduction/Literature Review

**作用**：
- 功能定位：总结已有研究，建立理论基础
- 在引言中的位置：中段，为后续CPL铺垫
- 论证逻辑：SPL → CPL → GAP → RAT链条的起点

**意图**：
- 主要目的：建立学术对话基础，展示对该领域的了解
- 说服对象：审稿人（证明作者掌握文献）
- 期望效果：让读者认同这是一个有研究基础的领域

**表达方式**：
- 修辞策略：权威引用（两位学者支撑观点）
- 语言技巧：
  - "Previous studies have shown that" - 典型SPL句式标记
  - 简洁陈述，无限定词，表明领域共识
- 句式特点：复合句，主句+宾语从句

---

**【第2句】**

**原文**：
> However, these studies have largely focused on technological innovation, paying insufficient attention to management innovation.

**中文翻译**：然而，这些研究主要关注技术创新，对管理创新的关注相对不足。

**Reading Code**：**CPL** (Critique of Previous Literature)

**位置**：Literature Review

**作用**：
- 功能定位：批判已有研究，指出其局限性
- 在引言中的位置：转折点，从SPL转向GAP
- 论证逻辑：承接SPL，为GAP和RAT铺垫

**意图**：
- 主要目的：为本研究建立正当性基础
- 说服对象：审稿人（证明当前研究的必要性）
- 期望效果：让读者认同现有研究存在不足

**表达方式**：
- 修辞策略：对比论证（技术创新 vs 管理创新）
- 语言技巧：
  - "However" - 转折词，开启批判
  - "largely focused" - 承认已有贡献，避免全盘否定
  - "paying insufficient attention" - 学术委婉批判
- 句式特点：转折复合句，前承后转

**完整的Shon论证链**：
```
第1句 (SPL) → 第2句 (CPL) → [预期：GAP] → [预期：RAT] → [预期：WTD]
```

---

**阶段2：用户选题交互**

**智能体询问**：您的研究主题或研究目的是什么？请简要描述您想研究的核心问题。

**用户回复示例**：我想研究"数字化转型对中小企业创新绩效的影响机制"

---

**阶段3：写作示范**

基于您的研究主题"数字化转型对中小企业创新绩效的影响机制"，以下是引言部分的逐句写作示范：

**段落1：研究背景（SPL序列）**

*Digital transformation has become a critical strategic imperative for organizations seeking competitive advantage in the contemporary business environment. (SPL: 总结已有研究，表明数字化转型已成为当代商业环境中组织寻求竞争优势的关键战略要务)*

**中文**：数字化转型已成为当代商业环境中组织寻求竞争优势的关键战略要务。

*Previous research has demonstrated that digital transformation can significantly enhance organizational innovation capabilities (Wang, 2020; Zhang, 2021). (SPL: 总结已有研究发现，数字化转型能显著提升组织创新能力)*

**中文**：先前的研究表明，数字化转型能显著提升组织创新能力。

*Scholars have also found that small and medium-sized enterprises (SMEs) increasingly adopt digital technologies to improve their innovation performance (Liu, 2019; Chen, 2022). (SPL: 补充已有研究，发现中小企业越来越多地采用数字技术以提升创新绩效)*

**中文**：学者们还发现，中小企业越来越多地采用数字技术以提升创新绩效。

**段落2：文献批判（CPL序列）**

*However, existing studies have predominantly focused on large enterprises, with limited attention paid to the specific context of SMEs. (CPL: 批判已有研究的局限，指出已有研究主要关注大型企业，对中小企业情境关注有限)*

**中文**：然而，现有研究主要关注大型企业，对中小企业情境关注有限。

*Moreover, while the relationship between digital transformation and innovation has been examined, the underlying mechanisms through which digital transformation influences innovation performance in SMEs remain underexplored. (CPL: 进一步批判，指出数字化转型影响中小企业创新绩效的内在机制尚未被充分探索)*

**中文**：此外，虽然数字化转型与创新的关系已被研究，但数字化转型影响中小企业创新绩效的内在机制仍未被充分探索。

**段落3：研究空白与理据（GAP + RAT序列）**

*Therefore, a significant gap exists in understanding how digital transformation impacts innovation performance specifically in the SME context, and through what mechanisms this influence occurs. (GAP: 明确指出研究空白，即缺乏对数字化转型如何影响中小企业创新绩效及其内在机制的理解)*

**中文**：因此，在理解数字化转型如何影响中小企业创新绩效以及通过何种机制产生影响方面存在显著空白。

*Given the critical role of SMEs in economic development and their unique resource constraints, examining this relationship is both theoretically necessary and practically relevant. (RAT: 论证研究必要性，指出考虑到中小企业在经济发展中的关键作用及其独特资源约束，探讨这一关系既具有理论必要性也具有实践相关性)*

**中文**：鉴于中小企业在经济发展中的关键作用及其独特的资源约束，探讨这一关系既具有理论必要性也具有实践相关性。

**段落4：研究目的（WTD序列）**

*This study aims to investigate the impact of digital transformation on innovation performance in SMEs and to explore the mediating mechanisms underlying this relationship. (WTD: 陈述本研究目的，即探讨数字化转型对中小企业创新绩效的影响，并探索其中的中介机制)*

**中文**：本研究旨在探讨数字化转型对中小企业创新绩效的影响，并探索其中的中介机制。

**完整论证链总结**：
```
SPL (3句) → CPL (2句) → GAP (1句) → RAT (1句) → WTD (1句)
```
这一结构遵循Shon的标准引言论证模式，从总结文献、批判局限、指出空白、论证必要性到陈述目的，形成完整的逻辑链条。
