# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [x] C - 综述论文（Survey / Review）
- [x] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `systematic review`
- `CRC diagnosis`
- `medical + technical viewpoints`
- `MSI / prognosis / TME writing support`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`07_综述与写作支撑`

- 本篇是 CRC 病理 DL 综述的更新版，最重要的价值是把你的写作支撑从 `2020` 续到 `2022`，并显著扩展到 `MSI / molecular phenotypes / prognosis / metastasis`
- 本篇至少完成：`1-3, 9, 11-16`

---

## 1. 论文信息

- 论文名：`Deep Learning on Histopathological Images for Colorectal Cancer Diagnosis: A Systematic Review`
- 作者/团队：`Athena Davri, Effrosyni Birbas, Theofilos Kanavos, Georgios Ntritsos, Nikolaos Giannakeas, Alexandros T. Tzallas, Anna Batistatou`
- 发表年份/会议/期刊：`2022, Diagnostics`
- DOI / arXiv ID：`10.3390/diagnostics12040837`
- BibTeX key：`davri2022crcdiag`
- PDF 路径：`结直肠腺体分割_pdf库/07_综述与写作支撑/Deep_Learning_on_Histopathological_Images_for_Colorectal_Cancer_Diagnosis_A_Systematic_Review_2022.pdf`
- 当前定位：`07` 目录中 CRC 病理综述时间线的更新节点，相比 2020 版更强调临床转化、分子表型、MSI、预后和技术视角
- 与已提取论文的关系：
  - 与 [01_CRC-AI-Review.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/01_CRC-AI-Review.md) 形成前后衔接：前者总结到 2020，本篇扩展到 2021 年底并将纳入量提升到 `82` 篇
  - 与 [03_Cerberus.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/06_半监督_拓扑_扩展工作/03_Cerberus.md) 相呼应：本篇证明 CRC histopathology DL 已从单纯 gland segmentation 扩展到 TME、MSI、survival、metastasis
  - 与 [01_GlaS-Challenge.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md)、[03_DCAN.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/03_DCAN.md) 等方法论文互补：这些是本篇“技术视角”树状框架中的具体节点

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：CRC 病理诊断不仅需要明确诊断，还需要同步提供 prognostic / predictive biomarker 信息，因此病理科的工作负荷和一致性压力都在上升。
  - 用途：`临床背景`
  - 页码：`p.1-p.2`
- 句子/事实 2：CRC 病理仍以 histopathological examination 为 gold standard，但 pathologists 对诊断、分级和 biomarker 评估存在显著 intra-/inter-observer variability，这为可靠的机器辅助方法提供了现实需求。
  - 用途：`研究动机`
  - 页码：`p.1-p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者从 `medical viewpoint` 和 `technical viewpoint` 两个维度同时整理 CRC histopathology DL 文献，这是本综述相较以往工作的主要特色。
  - 用途：`综述结构`
  - 页码：`p.4-p.6`
- 句子/事实 2：截至检索时，CRC histopathology DL 的研究范围已扩展到 `diagnosis`、`tumor tissue classification`、`tumor microenvironment`、`prognosis/metastasis/survival` 和 `microsatellite instability`
  - 用途：`任务版图`
  - 页码：`p.5-p.10`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| DOI | `10.3390/diagnostics12040837` | 文献信息 | `p.1` |
| 检索数据库 | `PubMed` | 系统综述方法 | `p.5` |
| 检索截止 | `2021-12-31` | 系统综述方法 | `p.5` |
| 初始检索 | `166` 篇 | 综述方法 | `p.5-p.6` |
| 全文筛选 | `92` 篇 | 综述方法 | `p.5-p.6` |
| 最终纳入 | `82` 篇 | 综述方法 | `p.5-p.6` |
| WHO CRC 主类 | `4` 类 | 病理背景 | `p.2` |
| colorectal ADC 占比 | `90%` | 病理背景 | `p.2` |
| CIN tumors | `~84%` | 分子背景 | `p.2` |
| hypermutated / MSI | `~13-16%` | 分子背景 | `p.2` |
| Lynch syndrome in CRC | `~2-3%` | 分子背景 | `p.2` |
| WSI 40x pixel edge | `227 nm` | 数字病理背景 | `p.3` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- CRC 发病率仍在上升，病理诊断负担很重。
- 现代 CRC pathology report 不只需要判定“是不是癌”，还需要报告：
  - histologic subtype
  - grade
  - TNM
  - lymphovascular / perineural invasion
  - tumor budding
  - 乃至分子与免疫相关信息
- 这些评估既耗时，又容易受 pathologist 主观解释影响。
- 同时，数字病理与 WSI 已成为可大规模计算分析的基础，因此需要系统回顾 DL 在 CRC histopathology 中究竟能覆盖哪些任务与临床目标。

对应原文依据（页码）：

- `p.1-p.4`

### 2.2 核心思路（一段话概括解法方向）

- 本综述依照 PRISMA 流程系统检索至 2021 年底的 CRC histopathology DL 研究，并创新性地从 `medical viewpoint` 与 `technical viewpoint` 两条主线同时组织文献：前者按临床任务分为诊断、组织分类、微环境、预后/转移/生存、MSI；后者按网络范式与技术实现分为 CNN、GAN、自定义架构、预训练/迁移学习、popular CNN modifications、ensemble 和组合方法。该双视角结构非常适合直接转化为论文中的 related work 与 discussion 框架。

关键页码：

- `p.4-p.6`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 本篇是系统综述，不是单一模型论文
- 核心双框架：
  - `Medical Viewpoint`
  - `Technical Viewpoint`

### 3.2 关键模块详细描述

**框架 1：`Medical Viewpoint`**

- 任务分类：
  1. `Diagnosis`
  2. `Tumor tissue classification`
  3. `Tumor microenvironment`
  4. `Prognosis / metastasis / survival`
  5. `Microsatellite instability`
- 这是本篇最适合直接回填论文写作结构的部分
- 页码：`p.5-p.10`

**框架 2：`Technical Viewpoint`**

- 技术分类：
  - `CNNs`
  - `GANs`
  - `custom architectures`
  - `pretrained architectures & transfer learning`
  - `popular CNN modifications`
  - `method combinations`
  - `ensemble methods`
- 页码：`p.6, p.10+`

**模块 1：`Diagnosis`**

- 主要做 cancer/not-cancer、benign/colon ADC 等二分类
- 也包含 tumor localization、WSI tumor region detection
- 部分工作达到与 pathologists 类似表现
- 页码：`p.6-p.7`

**模块 2：`Tumor Tissue Classification`**

- 关注正常/腺瘤/癌、多级别分级、组织结构与细胞特征
- 文中还提到跨器官迁移学习到 poorly differentiated colorectal biopsy WSIs
- 页码：`p.7-p.8`

**模块 3：`TME / Prognosis / Metastasis / Survival`**

- 从细胞分布、炎症浸润、stroma 比例到生存风险建模
- 体现了 CRC histopathology DL 已从“识别病灶”扩展到“解释病理生态与预后”
- 页码：`p.8-p.10`

**模块 4：`MSI / Molecular Phenotype`**

- 是相较 2020 综述最值得强调的新重点之一
- 包括：
  - MSI / MSS
  - CMS
  - TMB-H
  - 相关 transcriptomic / genomic profiles
- 页码：`p.9-p.10`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

- 本篇不适用逐层网络参数表
- 但可以直接借用其“任务-技术”二维框架：

| 维度 | 类别 | 写作价值 |
|------|------|---------|
| Medical | diagnosis / tissue class / TME / prognosis / MSI | 适合 `related work` 的任务层次 |
| Technical | CNN / GAN / transfer learning / ensemble / custom arch | 适合 `方法综述` 的技术层次 |

---

## 4. 公式与推导

### 4.1 核心公式

- 本篇是综述，无统一公式推导
- 重点不在公式，而在：
  - 临床任务定义
  - 数字病理成像背景
  - 研究组织框架

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 不适用

---

## 5. 损失函数

### 5.1 各监督项

- 综述未统一总结 loss 体系
- 更侧重任务目标与技术路线

### 5.2 总损失公式

- 不适用

### 5.3 权重配置与调度策略

- 不适用

---

## 6. 训练协议

### 6.1 数据集与划分

- 本篇纳入研究范围覆盖：
  - biopsy tissues
  - surgical histology sections
  - WSIs
  - H&E
  - IHC / ISH
- 数字病理背景部分给出关键事实：
  - 组织切片厚度通常 `4 um`
  - 常见扫描倍率 `20x / 40x`
  - 40x 下某些扫描仪的 pixel edge 约 `227 nm`
- 综述方法：
  - PubMed 检索至 `2021-12-31`
  - 采用 PRISMA
  - 最终纳入 `82` 篇原始研究

### 6.2 数据增强

- 本篇不统一总结 augmentation

### 6.3 优化器与超参数

- 本篇不统一总结 optimizer / lr / batch size

### 6.4 预处理与数据细节

- 作者特别强调 WSI 数字化和像素物理尺寸背景，这对于解释：
  - tile extraction
  - magnification
  - cross-study comparability
  非常有帮助

---

## 7. 推理与后处理

- 本篇不提供统一推理流程
- 但可提炼的流程级观点包括：
  - WSI -> patch / tile -> classification / localization
  - patch aggregation / cluster aggregation
  - WSI-level inference increasingly important for clinical use

---

## 8. 消融实验

### 8.1 消融设计

- 综述论文，不做统一消融

### 8.2 各模块贡献量化

- 可量化的不是模块增益，而是研究版图扩展：
  - 从单纯 diagnosis / segmentation 走向 `TME / prognosis / MSI / molecular phenotypes`
- 对你写作最有价值的变化是：
  - 2022 年时，CRC histopathology DL 已明显不再局限于 gland segmentation 主线

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 项目 | 结论 | 页码 |
|------|------|------|
| 综述规模 | 共纳入 `82` 篇 | `p.5-p.6` |
| 组织方式 | 同时从 `medical` 和 `technical` 视角归类 | `p.4-p.6` |
| 新扩展任务 | `MSI / prognosis / metastasis / survival / TME` 已成为重要方向 | `p.5-p.10` |
| 临床价值 | DL 可辅助诊断、预测分子表型与 MSI、识别与预后相关组织特征 | `p.1` |

### 9.2 与其他方法的对比

- 作为综述，它不像 2020 那样重点做 gland segmentation rank-sum 排名
- 更强调整个领域的扩展方向和可转化场景：
  - diagnosis
  - tissue classification
  - TME
  - survival / metastasis
  - MSI / TMB / CMS

### 9.3 公平对比条件确认

- 不同任务的数据集、标签、终点和评价指标差异很大
- 因此更适合把本篇作为“任务地图”和“问题空间定义”，而不是严格 SOTA 排名依据

### 9.4 评价协议与指标定义

- 综述中涉及的指标很多，依任务而变：
  - `accuracy`
  - `sensitivity / specificity`
  - `AUC`
  - `F1`
  - detection precision / recall
  - survival-related risk metrics
- 写作上最重要的是：不同临床终点对应不同评价体系，不能把所有研究压缩到单一 metric

---

## 10. 计算量与效率

- 本篇不统一报告计算量
- 但多次强调：
  - pathology laboratory diagnostic load 很高
  - AI 的现实意义不仅在 accuracy，也在帮助减轻时间负担和提升一致性

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- `Medical viewpoint`：
  - diagnosis
  - tumor tissue classification
  - TME
  - prognosis / metastasis / survival
  - MSI
- `Technical viewpoint`：
  - CNN
  - GAN
  - custom architectures
  - pretrained / transfer learning
  - method combinations
  - ensemble methods

### 11.2 论文指出的研究空白 / Open Problems

- 临床落地仍需要更可靠、更高质量、更大规模的数据
- challenging cases 依旧存在，如：
  - small adenomatous glands
  - difficult benign vs malignant discrimination
  - misclassified MSI patches
- 有些大数据训练并不必然带来更高 generalization accuracy
- 不同任务之间标签定义、终点与评价方式并不统一

### 11.3 对我们选题的启示

- 你的 gland segmentation 主线仍然合理，因为 CRC ADC 本身以 glandular differentiation 为核心
- 但在论文写作上，完全可以把工作挂到更大的临床任务链条中：
  - diagnosis
  - subtype / grade
  - TME
  - MSI / CMS / TMB
  - prognosis
- 这会让你的论文意义不只停留在“分得更准”，而是“为更完整的 CRC pathology decision pipeline 提供基础”

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 文中明确写到完整 pathology report 应关注：
  - histologic subtype
  - histologic grade
  - TNM
  - lymphovascular invasion
  - perineural invasion
  - tumor budding
- 还提到：
  - WHO CRC main categories
  - TCGA molecular groups
  - CMS1-4 分类

### 12.2 涉及的生物标志物

- `MMR proteins`: `MLH1`, `MSH2`, `MSH6`, `PMS2`
- `MSI`
- `CIMP`
- `TMB-H`
- `EGFR`
- `PD-L1` 相关免疫背景可在更广泛 CRC 讨论中承接

### 12.3 临床意义

- 病理不仅要诊断肿瘤，还要为 personalized treatment 提供分子与预后信息
- 因而 CRC histopathology DL 的意义已从简单检测扩展到：
  - biomarker screening
  - MSI inference
  - survival prediction
  - metastasis risk assessment

---

## 13. 开源与复现

- 代码是否开源：`不适用（综述）`
- 代码仓库地址：`不适用`
- 框架/语言：`不适用`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`低`
- 复现障碍：
  - 不涉及单一模型复现
  - 真正难点在于跨任务、跨终点研究之间缺乏统一协议

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 各任务统一 benchmark | 否 | 仅按任务框架整理 | 高 |
| 各研究统一 validation 协议 | 否 | 不强行汇总 | 中 |
| 统一 annotation protocol | 否 | 记录为领域问题 | 中 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 本篇当前抽取片段中未见集中列出“本综述局限性”段落
- 但全篇持续暗示：
  - 数据规模
  - challenging cases
  - generalization
  - clinical implementation
  仍是关键瓶颈

### 14.2 我们观察到的潜在问题

- 任务范围更广，但也因此更难做直接 quantitative comparison
- 与 2020 综述相比，本篇更像“扩展版地图”，不是 gland segmentation 的严格排名综述

### 14.3 失败案例 / 定性分析

- 文中明确提到的困难包括：
  - challenging tiles with small adenomatous glands
  - MSI 误判常出现在 necrotic 或 lymphocyte-rich 区域
  - larger training sets 并不总是带来更高 generalization

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- CRC pathology DL 的更新版上位框架
- 医学视角 + 技术视角的双重 related work 写法
- 从 gland segmentation 过渡到 MSI / prognosis / TME 的叙事支撑

### 15.2 可以作为候选参数来源的

- 不主要提供超参数
- 更主要提供：
  - WSI 数字化背景
  - magnification / pixel size
  - 任务层次划分

### 15.3 不应照搬的（及原因）

- 不应把这篇当作 gland segmentation 的专门 benchmark 综述
  - 原因：它更关注整个 CRC histopathology 任务空间
- 不应把不同临床终点的结果直接并列比较
  - 原因：任务定义和指标差异很大

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 论文引言背景 | 病理负担重、observer variability、personalized treatment 需求 | 强 |
| related work 结构 | medical + technical dual viewpoint | 强 |
| 任务意义拔高 | gland segmentation 可支撑 MSI / prognosis / TME 上游分析 | 强 |
| discussion | clinical translation 仍受 generalization 与 challenging cases 限制 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`论文写作_引言与相关工作素材`
- [ ] 需要和哪篇论文交叉验证：`01_CRC-AI-Review.md`, `03_Cerberus.md`, `01_GlaS-Challenge.md`
- [ ] 待确认的问题：`后续是否再补 Metrics Reloaded 作为评估协议支撑`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | personalized treatment、pathology workload、observer variability | 临床背景 |
| related work | 双视角任务-技术框架 | 综述主线 |
| 讨论 | challenging tiles、MSI misclassification、generalization limits | 局限性 |
| 展望 | 从 gland/task-level 到 molecular phenotype/prognosis | 研究意义拓展 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.3` | WSI 数字化与像素尺度示意 | 数字病理背景 |
| `Fig. 2` | `p.5-p.6` | PRISMA 流程图 | 综述方法 |
| `Fig. 3` | `p.6` | Medical + Technical viewpoint 树状图 | 综述结构 |
| `Table 1` | `p.5+` | 纳入研究的 medical scope / technical method / dataset / metrics | 总索引 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 双视角综述框架已明确
- [x] 临床与病理背景已单独提炼
- [x] 与我们项目的关联已具体到写作和意义拔高层面
- [ ] 训练参数足够完全复现（综述文不适用）
- [x] 重要局限和 challenging case 已记录
- [x] 不确定的内容已标注而未脑补

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/07_综述与写作支撑/03_CRC-Diagnosis-Review-2022`
- `paper_type`: `planned_category:07_综述与写作支撑`
- `evidence_status`: `unverified`
- 本区为本轮结构化补齐记录，不替代正文中的原文事实、公式、页码、数字或已有待确认标记；发现 `待确认`、`待填` 或空白证据字段时保持 `unverified`，不自动补数字。
- 文献原文数字、公式和结论默认按 `quoted_from_original_paper/reference_only` 处理；它们不是本项目结果，也不是 `reproduced`。
- `formal_result`: `not_run`
- `result_eligibility`: `false`
- 本篇不得被当作 current journal 结果、current protocol、Gate 或结果主表的替代证据。

## 代码落地接口

- 参考代码核验状态：`code_unverified`；本轮未对每篇论文的仓库、commit/tag 和关键文件逐项核验。
- 若正文已有开源代码信息，后续必须逐项补记 `repository/commit_or_tag/key_files`，并保持未核验前不称为 `strict replication basis`。
- 若正文没有可核验的参考实现，辅助接口状态：`planned_not_created`；本轮不创建代码、不授予复现权限。

## 运行记录字段与 lineage

- 记录字段：`paper_id=03_文献证据/07_综述与写作支撑/03_CRC-Diagnosis-Review-2022`；`paper_type=planned_category:07_综述与写作支撑`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
- `source_stage`: `s03_literature_evidence`
- `source_manifest`: `unverified`
- `source_protocol_version`: `unverified`
- `source_run_name`: `reference_only`
- `consumer_stage`: `unverified`
- `consumer_file`: `unverified`
- `consumption_boundary`: `literature_evidence_only_no_current_result`
- 本轮没有生成实验 run、manifest、metrics 或 current result lineage。

## 独立回退条件

- PDF 路径、页码、公式、数字、指标 identity、split 或代码状态无法核验时，标记 `unverified/blocked`。
- 处于 `unverified/blocked` 的内容不得进入 current protocol、Gate、结果主表或投稿结果；应回退到逐项人工来源复核。
- 本轮不改变正文已有事实，不把待确认字段改成已确认，也不以第三方转述替代原文核验。

## 冲突裁决记录

- 原文：保留单篇正文已有的原文事实、公式、页码和数字；未逐项复核者仍为 `unverified`。
- 第三方转述：仅作辅助线索，不能覆盖原文，也不能升格为 verified。
- 当前协议：只决定本项目消费边界，不改写论文方法、指标 identity、split 或结果。
- 历史 provenance：仅作历史来源记录，不得作为 current journal 结果或当前 Gate 证据。

## 文件质量自检

- [x] 原有正文、公式、页码、数字和已有待确认内容保留，未新增虚构来源、commit、metrics 或结论。
- [x] 基本章节存在不等于证据复核完成；本篇仍明确为 `unverified`。
- [x] `待确认`、`待填` 或空白证据字段没有被自动填值，仍需人工来源复核。
- [x] 原文引用值与本项目重跑结果分离；本篇不是本项目结果。
- [x] `formal_result=not_run`、`result_eligibility=false` 已明确；未生成实验结果。
- [x] 七字段 lineage 全部出现，且消费边界限制为 literature evidence only。
- [x] 代码接口仅记录参考代码核验边界，未创建不存在的辅助接口。
- [x] PDF、页码、公式、数字、指标 identity、split 或代码状态无法核验时的回退边界已独立写明。

## Diagnostics 闭环

- 本轮执行的是结构化补齐，不是逐篇 PDF 复核。
- 实际状态：`partial_pending_manual_source_review`；不能写 `pass`。
- 本轮未启动实验、未生成运行记录、未生成 metrics、未改变 current protocol 或 Gate 状态。
- 后续逐篇人工核验应复查正文落点、来源页码、指标 identity、split、代码状态与本区字段的一致性。

## 审计对表

| 已读文件 | 正文落点 | 自检落点 | diagnostics | 当前缺口 | 修复状态 |
|---|---|---|---|---|---|
| `03_文献证据/07_综述与写作支撑/03_CRC-Diagnosis-Review-2022` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
| `03_文献证据/00_通用文献深提取模板.md` | 状态、lineage、回退和消费边界 | 文件质量自检 | `partial_pending_manual_source_review` | 模板字段不等于逐篇来源复核 | 已映射本篇收尾字段 |


## 来源资产核验

- `pdf_path_status=exists`：对应原文 `PDF 路径` 字段已存在，且本地 PDF 文件真实存在。本节不虚构绝对路径、hash 或页码。
- `paper_identity_status=not_independently_rechecked`：本轮没有逐篇人工核对标题、DOI 与正文一致性。
- `page_formula_metric_split_status=manual_review_pending`：页码、公式、数字、split 与指标 identity 仍需人工逐篇与 PDF 核验。
- `code_repository_status=manual_review_pending`：代码 repository、commit、tag 与 key files 未逐篇核验。
- `evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`。
- `diagnostics_status=partial_pending_manual_source_review`。

### 回退规则
PDF 路径失效、身份不一致、页码/公式/数字/指标/split/代码核验失败时，保持 `unverified/blocked`，不得进入 current protocol、Gate、结果表或投稿。

### 审计对表

| 证据项 | 当前事实 | 状态 | 下游消费边界 |
|---|---|---|---|
| PDF 路径与本地文件 | `PDF 路径` 字段存在且本地 PDF 文件真实存在 | `exists` | 仅允许作为待人工复核的来源入口 |
| 论文身份 | 本轮未逐篇人工核对标题、DOI、正文一致性 | `not_independently_rechecked` | 不得作为身份一致性结论消费 |
| 页码/公式/数字/split/指标 | 尚未逐篇与 PDF 对照 | `manual_review_pending` | 不得进入结果表、Gate 或投稿 |
| 代码仓库资产 | repository/commit/tag/key files 未逐篇核验 | `manual_review_pending` | 不得进入复现实验或 current protocol |
| 证据与正式结果 | 未完成来源人工复核，未运行正式结果 | `unverified`; `not_run` | `result_eligibility=false`，保持 blocked |
