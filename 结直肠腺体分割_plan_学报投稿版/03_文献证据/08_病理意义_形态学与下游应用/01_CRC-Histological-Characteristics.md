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

- `histology review`
- `CRC morphology background`
- `gland architecture and grading support`
- `writing support for pathology significance`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`08_病理意义_形态学与下游应用`

- 本篇是进入 `08` 目录后的病理基础起点，最重要的价值是把“腺体分割为什么重要”放回病理学语言里解释
- 对当前项目最有价值的是：
  - 给出正常结肠腺体的组织学基线
  - 给出 dysplasia 到 adenocarcinoma 的连续进展链
  - 给出 gland formation 分级口径
  - 给出 mucinous 等特殊亚型的组织学与临床差异
- 本篇至少完成：`1, 2, 9, 12, 14, 15, 16, 17`

---

## 1. 论文信息

- 论文名：`Classification and Histological Characteristics of Colorectal Cancer`
- 作者/团队：`Brooke Dubansky, Sally Lewis, Dale Telgenhoff`
- 发表年份/会议/期刊：`2024, Clinical Laboratory Science`
- DOI / arXiv ID：`10.29074/ascls.2022003206`
- BibTeX key：`dubansky2024crchistology`
- PDF 路径：`结直肠腺体分割_pdf库/08_病理意义_形态学与下游应用/Classification_and_Histological_Characteristics_of_Colorectal_Cancer_2024.pdf`
- 当前定位：`08` 目录里的病理基础总述文献，用于把 gland morphology、dysplasia、adenoma-carcinoma progression、grading 和 subtype 这些概念写得更病理化
- 与已提取论文的关系：
  - 与 [03_CRC-Diagnosis-Review-2022.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/03_CRC-Diagnosis-Review-2022.md) 互补：前者总结数字病理与 DL 任务版图，本篇补最基础的病理形态学定义
  - 与 [01_GlaS-Challenge.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md)、[04_MILD-Net.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md) 形成上游支撑：这些分割论文默认要识别的 gland architecture，在本篇里有病理定义
  - 与后续同目录的分级/形态测量论文互补：本篇先给标准病理语言，后续再接客观 grading 与 morphometrics

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：CRC 的分类与分期依赖病灶的 histological characteristics 和可预测的 morphology changes，而最常见类型是由 adenomatous polyp 进展而来的 adenocarcinoma。
  - 用途：`病理背景`
  - 页码：`p.1`
- 句子/事实 2：多数 CRC 起始于 polyp，早期发现并切除对改善 prognosis 很关键，这也说明 gland / polyp 相关结构在病理实践中有核心地位。
  - 用途：`临床意义`
  - 页码：`p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：正常 colon glands 是由单层 columnar cells 与大量 goblet cells 构成的单管状 invagination，后续 dysplasia 与 adenocarcinoma 的判断都以这种正常 gland architecture 为参照。
  - 用途：`形态学基线`
  - 页码：`p.2`
- 句子/事实 2：低分化程度的判断并不只看细胞异型性，还看 gland formation 的保留比例；well/moderate/poor differentiation 可分别对应 `>95%`、`50%-90%` 和 `<50%` 的 recognizable gland formation。
  - 用途：`分级标准`
  - 页码：`p.3`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| DOI | `10.29074/ascls.2022003206` | 文献信息 | `题录` |
| 文章页数 | `5` 页正文 | 文献规模 | `PDF` |
| adenocarcinoma 占比 | `~90%` | CRC 主类型背景 | `p.3` |
| tubular adenoma 占 benign adenomatous polyps | `~75%-80%` | polyp subtype 背景 | `p.3` |
| well differentiated gland formation | `>95%` | grading 定义 | `p.3` |
| moderately differentiated gland formation | `50%-90%` | grading 定义 | `p.3` |
| poorly differentiated gland formation | `<50%` | grading 定义 | `p.3` |
| mucinous adenocarcinoma 占 adenocarcinoma | `~10%` | 亚型背景 | `p.4` |
| signet ring adenocarcinoma 占 adenocarcinoma | `<1%` | 亚型背景 | `p.4` |
| signet ring 平均 5-year survival | `~30%` | 预后背景 | `p.4` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- CRC 的分类、分期和亚型识别都依赖稳定的组织学特征，而这些特征本质上是形态学问题。
- 大多数 CRC 来自 polyp 到 adenocarcinoma 的连续进展，因此需要明确：
  - 正常 gland 的基线长什么样
  - dysplasia 如何改变 gland architecture
  - 何时从 benign lesion 进入 invasive malignancy
- 仅用“癌/非癌”并不足以支撑病理报告，因为 subtype、grade、invasion 和 metastatic tendency 都与组织学结构有关。
- 因此本篇要用较短篇幅系统回顾：
  - benign polyps 的主要类型
  - adenocarcinoma 的分级标准
  - 常见特殊亚型的组织学与临床差异

对应原文依据（页码）：

- `p.1-p.4`

### 2.2 核心思路（一段话概括解法方向）

- 本文不是方法论文，而是一篇面向实验室/病理教育的短综述。它先从 colon 正常组织学与 polyp-carcinoma progression 讲起，再概括 benign polyps、CRC 主类型、adenocarcinoma grading 和 WHO 认可的主要亚型，最后强调形态学特征虽然定义了 grade 和 subtype，但 prognosis 往往还要结合分子特征共同判断。对我们来说，它最大的价值是为“gland segmentation 的病理意义”提供稳定、可直接写入论文的组织学语言。

关键页码：

- `p.1-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 本篇是病理综述，不是计算模型论文
- 不适用网络结构提取

### 3.2 关键模块详细描述

- 不适用

### 3.3 架构参数表（适用于基线对比论文 G 类型）

- 不适用

---

## 4. 公式与推导

### 4.1 核心公式

- 本篇无公式

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 不适用

---

## 5. 损失函数

### 5.1 各监督项

- 不适用

### 5.2 总损失公式

- 不适用

### 5.3 权重配置与调度策略

- 不适用

---

## 6. 训练协议

### 6.1 数据集与划分

- 本篇不是实验论文

### 6.2 数据增强

- 不适用

### 6.3 优化器与超参数

- 不适用

### 6.4 预处理与数据细节

- 不适用

---

## 7. 推理与后处理

- 不适用

---

## 8. 消融实验

- 不适用

---

## 9. 主表结果与对比

### 9.1 论文给出的核心病理结论

- 正常 colon gland 的组织学基线是：
  - 单层 columnar cells
  - 大量 goblet cells
  - 单管状 invagination 结构
- dysplasia 的关键形态变化包括：
  - stratification
  - hyperchromasia
  - nuclear elongation
  - gland architecture 丢失
- low-grade dysplasia 仍保留一定 gland architecture，而 high-grade dysplasia 出现更严重的细胞核异常和明显 gland architecture 丢失。
- adenomatous polyp 中：
  - tubular 最常见
  - villous / tubulovillous 更易恶变
- conventional adenocarcinoma 的 grade 可按 recognizable gland formation 比例来判定。

### 9.2 可直接用于正文的“病理标准句”

- 正常 gland architecture 是后续识别 dysplasia、polyp formation 和 invasive adenocarcinoma 的参照基线。
- 从 benign lesion 到 malignant lesion 更适合被理解为 continuum，而不是完全割裂的两个状态。
- 腺癌分级本质上与 gland formation 保留程度高度相关，因此腺体结构破坏不只是视觉现象，而是病理学意义上的分级信号。
- desmoplasia 和 dirty necrosis 是 conventional adenocarcinoma 的典型组织学特征。

### 9.3 特殊亚型要点

- `Mucinous adenocarcinoma`
  - 约占 adenocarcinoma 的 `10%`
  - 更常见于 `right-sided CRC`
  - 诊断时更高分期
  - 更常转移至 `peritoneum` 而非 `liver`
  - 常关联 `MSI`, `KRAS`, `BRAF`, `PI3K`
- `Signet ring adenocarcinoma`
  - 占比 `<1%`
  - 与 mucinous subtype 相关
  - 常见 `RCRC`, `MSI`, `BRAF/KRAS`
  - 平均 `5-year survival` 约 `30%`
- `Medullary adenocarcinoma`
  - 组织学上常见 solid sheets 和 prominent lymphocytic infiltrate
  - 虽 poorly differentiated，但预后可相对较好
- `Micropapillary adenocarcinoma`
  - 容易伴 lymphovascular invasion、淋巴结转移和较差预后
- `Serrated adenocarcinoma`
  - saw-toothed gland surface pattern
  - 可由 serrated adenoma 进展而来
  - 常与较差预后相关

### 9.4 评价协议与指标定义

- 本篇不是指标论文
- 但它提供了对后续实验解释很重要的“病理评价维度”：
  - gland architecture 是否保留
  - gland formation 比例高低
  - 是否出现 mucinous / signet ring / serrated 等特殊形态
  - 是否伴 desmoplasia、dirty necrosis、lymphovascular invasion
- 这意味着单纯像素级 overlap 并不能完全覆盖病理价值；如果后续要讨论结构保持、分级或亚型相关下游任务，本篇可作为上游论据

---

## 10. 计算量与效率

- 不适用

---

## 11. 分类体系与研究空白

### 11.1 本篇提供的分类框架

- benign colorectal polyps：
  - inflammatory
  - hamartomatous
  - hyperplastic
  - adenomatous
  - sessile serrated lesion
- WHO colorectal carcinoma 主类：
  - adenocarcinoma
  - adenosquamous carcinoma
  - spindle cell carcinoma
  - squamous cell carcinoma
  - undifferentiated carcinoma
- WHO adenocarcinoma 亚型：
  - cribriform-comedo
  - medullary
  - micropapillary
  - mucinous
  - serrated
  - signet ring

### 11.2 对我们写作最有用的空白提醒

- 本篇给了稳定的病理定义，但没有转化为数字病理可计算特征。
- 它指出 grade 与 subtype 不能只看宏观分期，但没有提供量化形态测量方法。
- 这正好为后续同目录的 `morphometrics / grading / multi-institution pathology AI` 文献留下承接空间。

---

## 12. 临床/病理标准

### 12.1 正常组织学基线

- 正常 colon glands 是由单层柱状上皮细胞和大量 goblet cells 构成的 tubular invagination。
- lamina propria 缺乏淋巴管，这也是早期局限性病变不易马上转移的重要组织学背景。

### 12.2 dysplasia 与 adenoma-carcinoma progression

- dysplasia 常表现为：
  - epithelial stratification
  - hyperchromasia
  - nuclear elongation
- low-grade dysplasia：
  - 仍可辨认 gland architecture
  - 上皮异常较轻
- high-grade dysplasia：
  - 细胞与核异常更重
  - gland architecture 丢失更明显
- 进一步突变可导致 polyp formation，再进一步穿破基底膜并侵入 submucosa，形成 invasive adenocarcinoma。

### 12.3 gland formation 分级标准

- `Well differentiated`：`>95%` 肿瘤区域仍可辨认 gland formation
- `Moderately differentiated`：`50%-90%`
- `Poorly differentiated`：`<50%`
- 这是本项目后续解释“为什么 gland morphology 破坏程度重要”的最直接病理依据。

### 12.4 特殊病理特征

- `Desmoplasia`：肿瘤间质的纤维增生反应
- `Dirty necrosis`：腺体腔内坏死碎屑
- 两者都是 conventional adenocarcinoma 常见且有辨识度的病理词汇

### 12.5 侧别与亚型差异

- `Right-sided CRC` 更常见：
  - 更高 grade / stage
  - 更大肿瘤
  - mucinous subtype
- 这说明 gland morphology 的变化还和解剖部位、分子背景及临床行为有系统关联。

---

## 13. 开源与复现

### 13.1 论文未报告但复现必需的信息

- 本篇为综述，不涉及可复现实验
- 但如果要把本篇转化为数字病理研究设计，仍缺少：
  - gland formation 的像素级或实例级量化定义
  - desmoplasia / dirty necrosis / mucin pools 的标注口径
  - subtype 区分所需的最小视野尺度
  - gland disruption 与 grade 的可计算映射方式

### 13.2 数据与代码

- 无开源代码
- 无统一实验数据

---

## 14. 局限性与失败案例

- 本篇篇幅较短，更像病理教育型综述，而不是系统综述。
- 它没有提供数字病理任务中的 dataset、annotation protocol 或 quantitative benchmark。
- 对特殊亚型的覆盖是概览式的，适合写背景，不足以单独支撑精细 subtype discrimination 方法设计。
- 文中也明确暗示：形态学虽然定义了 grade 和 subtype，但 prognosis 往往还要结合 molecular characteristics，不能把 morphology 当作唯一依据。

---

## 15. 对我们项目的落地价值

### 15.1 能直接支持什么写法

- 引言里可更病理化地说明：腺体分割不是单纯轮廓提取，而是服务于对 gland architecture、dysplasia progression 和 adenocarcinoma grading 的结构化观察。
- 讨论里可写：模型若只能给出区域覆盖，而不能较好保留 gland formation 与 lumen/boundary 结构，就难以服务真正的病理分级与亚型判断。
- 临床意义部分可写：mucinous、signet ring、medullary 等亚型并非纯命名差异，而对应不同的组织学模式、转移倾向和预后背景。

### 15.2 对模型设计的启发

- 应优先保留：
  - gland contour 完整性
  - lumen 形态
  - gland-to-gland separation
  - 结构破坏区域的局部细节
- 后续若做下游任务，可考虑从分割结果中提取：
  - gland formation 比例
  - gland density / size / irregularity
  - lumen morphology
  - 黏液样区域比例

### 15.3 在整套文献链中的位置

- 这是 `08` 目录的病理基础锚点
- 后续最自然的承接是：
  - `Glandular_Morphometrics_for_Objective_Grading_of_Colorectal_Adenocarcinoma_Histology_Images_2017`
  - `Automatic_Tumor_Grading_on_Colorectal_Cancer_Whole-Slide_Images_2022`
  - `Segmentation_and_Grade_Prediction_of_Colon_Cancer_Digital_Pathology_Images_Across_Multiple_Institutions_2019`

---

## 16. 关键图表索引

- `Figure 1`
  - 内容：colon 解剖分区与 `RCRC/LCRC` 示意
  - 用途：写侧别差异时的背景图参考
  - 页码：`p.2`
- `Table 1`
  - 内容：benign colorectal polyps 的基本分类和形态特征
  - 用途：写 adenoma subtype 与 malignant risk
  - 页码：`p.3`
- `Table 2`
  - 内容：CRC 主类型与 adenocarcinoma subtypes 列表
  - 用途：写 subtype taxonomy
  - 页码：`p.4`

---

## 17. 提取质量自检

- 本篇正文较短，全文已基本通读并结合关键词核对，核心病理事实提取完整度较高。
- 重点保留了对当前项目最有用的几类证据：
  - 正常 gland 组织学基线
  - dysplasia 到 adenocarcinoma 的连续进展
  - gland formation grading
  - mucinous / signet ring 等特殊亚型特征
- 未逐条展开所有参考文献的上游原始证据，尤其 subtype 细节更多是该综述的二次总结。
- 这篇更适合作为病理写作支撑锚点，而不是单独作为某一亚型的最终证据终点。

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/08_病理意义_形态学与下游应用/01_CRC-Histological-Characteristics`
- `paper_type`: `planned_category:08_病理意义_形态学与下游应用`
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

- 记录字段：`paper_id=03_文献证据/08_病理意义_形态学与下游应用/01_CRC-Histological-Characteristics`；`paper_type=planned_category:08_病理意义_形态学与下游应用`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/08_病理意义_形态学与下游应用/01_CRC-Histological-Characteristics` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
