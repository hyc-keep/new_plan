# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [x] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `gland orientation`
- `aggressive tumor identification`
- `early colon carcinoma`
- `computational pathology prognostic biomarker`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`08_病理意义_形态学与下游应用`

- 本篇是把“腺体形态学”从 general grading 推到“早期 colon carcinoma 复发风险分层”的关键病理扩展论文。
- 对当前项目最有价值的是：
  - 明确指出 gland orientation disorder 本身就是 aggressive tumor 的重要形态信号；
  - 用 `797` 个 gland morphometric features 做机器学习风险分层；
  - 把 computational pathology 输出与 `Ki67` 和 `CEA` 这些临床指标做相关性验证；
  - 说明腺体分割价值不仅在 `grade`，也在 early-stage recurrence risk prediction。
- 本篇至少完成：`1-4, 9, 12, 14-17`

---

## 1. 论文信息

- 论文名：`Glandular orientation and shape determined by computational pathology could identify aggressive tumor for early colon carcinoma: a triple-center study`
- 作者/团队：`Meng-Yao Ji, Lei Yuan, Shi-Min Lu, Meng-Ting Gao, Zhi Zeng, Na Zhan, Yi-Juan Ding, Zheng-Ru Liu, Ping-Xiao Huang, Cheng Lu, Wei-Guo Dong`
- 发表年份/会议/期刊：`2020, Journal of Translational Medicine`
- DOI / arXiv ID：`10.1186/s12967-020-02297-w`
- BibTeX key：`ji2020glandorientation`
- PDF 路径：`结直肠腺体分割_pdf库/08_病理意义_形态学与下游应用/Glandular_orientation_and_shape_determined_by_computational_pathology_could_identify_aggressive_tumor_for_early_colon_carcinoma_2020.pdf`
- 当前定位：`08` 目录里“腺体形态 -> 早期结肠癌高风险识别”的代表作，强调 orientation disorder 与 gland shape aberrance 可以作为 aggressive tumor 的客观影像标志。
- 与已提取论文的关系：
  - 直接承接 `02_Glandular-Morphometrics.md`：后者证明 gland morphology 可做客观分级，本篇进一步证明 orientation/shape 还可用于早期复发风险预测。
  - 与 `03_Segmentation-and-Grade-Prediction.md` 互补：后者强调 segmentation 驱动 grading，本篇更偏 prognostic classifier。
  - 与 `04_Automatic-Tumor-Grading-WSI.md` 形成上下游：本篇是 TMA / image-level 风险分层，本篇后的 WSI 工作则进一步做 slide-level 生存分析。

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：早期 colon adenocarcinoma 的整体复发率虽然低于 `20%`，但一旦复发，患者生存时间会显著缩短，因此仍需识别高风险亚群。
  - 用途：`临床动机`
  - 页码：`p.2`
- 句子/事实 2：H&E 仍是结肠癌预后评估金标准之一，但人工病理判读存在明显 intra-/inter-observer variability。
  - 用途：`为什么要 computational pathology`
  - 页码：`p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者明确指出 gland shape、size、orientation 和 spatial relationship 的量化特征与肿瘤分级、转移和复发有关，但在 colon cancer 中此前缺少系统的定量研究。
  - 用途：`研究空白`
  - 页码：`p.2`
- 句子/事实 2：本篇不是直接依赖分子 assay，而是尝试用普通 H&E 中的 gland morphology 建立更便宜、更可重复的 recurrence risk marker。
  - 用途：`方法定位`
  - 页码：`p.1-p.2`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 总患者数 | `532` | 队列规模 | `p.1, p.5` |
| TCGA 验证集 | `113` | 外部验证 | `p.1` |
| TMA 数 | `4` | 样本组织形式 | `p.1-p.2` |
| 特征总数 | `797` | gland morphometric feature pool | `p.1, p.3` |
| 入模特征数 | `5` | MRMR 选择结果 | `p.1, p.4` |
| 主分类器 | `SVM` | 最优分类器 | `p.4, p.6` |
| cross-validation | `5-fold` | 训练稳健性 | `p.4` |
| 主结果 accuracy | `88.1%` | recurrence prediction | `p.1, p.6` |
| DSS hazard ratio | `9.65 (95% CI 2.15-43.12)` | 独立预后价值 | `p.1, p.7` |
| D1 / D2-D3 / D4 | `263 / 223 / 46` | 内部分层验证 | `p.1, p.5` |
| recurrence 总数 | `112 / 532` | 事件比例 | `p.5` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 早期 colon adenocarcinoma 患者整体预后较好，但仍有一小部分会复发，需要更细粒度的高风险识别。
- 分子检测如 recurrence score 虽然有效，但成本高、组织破坏性更强。
- H&E 中 gland morphology 长期被病理学用于判断恶性程度，但缺少可重复、可量化、可机器学习建模的风险指标。
- 因此作者要回答的问题是：
  - 仅基于 H&E gland morphology，能否识别 aggressive tumor？
  - gland orientation disorder 和 gland shape irregularity 是否可作为 early-stage recurrence marker？

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文先对 H&E 图像中的 individual glands 做自动分割，然后从每个 gland 提取 orientation、shape、size、texture、density 和 architecture 等共 `797` 个定量特征，再用 `MRMR` 从训练集筛出最有信息量的 `5` 个特征，分别尝试 `SVM / RF / DAC` 三种分类器预测 recurrence risk。最终锁定 `SVM` 形成 `ECAHBC` 图像分类器，并在独立验证集、TCGA 队列以及 `Ki67`/`CEA` 相关性、生存分析中验证其临床意义。

关键页码：

- `p.1-p.4`
- `p.6-p.10`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 总体流程：
  1. 自动 gland segmentation
  2. gland-level morphometric feature extraction
  3. `MRMR` 筛选 top-5 特征
  4. 构建 `SVM / RF / DAC`
  5. 锁定最优分类器 `ECAHBC`
  6. recurrence prediction
  7. DSS survival validation
  8. `Ki67` 与 `CEA` 相关性分析

### 3.2 关键模块详细描述

**模块 1：`Automatic Gland Segmentation`**

- 作用：
  - 为下游 orientation/shape 特征提取提供 gland contour。
- 论文写法：
  - gland 由前置自动分割算法得到，本文不把分割网络本身作为主要贡献。
- 页码：`p.3`

**模块 2：`797 Gland Histomorphometric Features`**

- 特征大类包括：
  - gland orientation
  - gland shape/size
  - texture
  - density
  - gland architecture descriptors
- 页码：`p.3-p.4`, `p.7-p.9`

**模块 3：`MRMR Feature Selection`**

- 作用：
  - 从 `797` 个候选特征里选出信息量最大且冗余最小的少数特征。
- 结果：
  - 最终保留 `5` 个特征建模，以避免过拟合。
- 页码：`p.4`

**模块 4：`Machine Learning Classifier`**

- 候选模型：
  - `SVM`
  - `RF`
  - `DAC`
- 训练策略：
  - `5-fold cross-validation`
- 最终最佳：
  - `SVM`
- 页码：`p.4-p.6`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 组件 | 作用 | 关键细节 |
|------|------|---------|
| gland segmentation | 生成 gland contour | 前置自动分割 |
| 797 features | 提取形态学定量描述 | orientation/shape/size/density 等 |
| MRMR | 降维筛特征 | 选出 `5` 个最优特征 |
| SVM/RF/DAC | recurrence classifier | 最终锁定 `SVM` |
| ECAHBC | 风险分层器 | aggressive vs indolent tumor |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：`MRMR` 思想

```text
select features with maximum relevance to recurrence label
while minimizing redundancy among selected features
```

符号说明：
- 本篇未把 `MRMR` 数学式完整展开到正文抽取片段；
- 但其核心就是高相关、低冗余的 feature subset selection。

公式 2：风险分层流程

```text
gland segmentation -> 797 features -> MRMR top-5 -> SVM -> ECAHBC risk label
```

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇不是深度网络新结构论文，关键不在梯度推导。
- 真正重要的是病理逻辑：
  - aggressive tumor 的 gland 更无序；
  - orientation disorder 和 shape irregularity 可被数值化；
  - 少量高信息量 morphometric features 就足以形成有效的 recurrence classifier。

---

## 5. 损失函数

### 5.1 各监督项

- 本篇主体不是 end-to-end 深度训练论文，主 classifier 是传统机器学习模型。
- 核心“监督”来源是 recurrence label，而不是 segmentation loss 设计。

### 5.2 总损失公式

```text
不适用；正文重点是 feature selection + machine learning classification
```

### 5.3 权重配置与调度策略

- 文中未强调分类损失函数细节。
- 主要关注：
  - feature screening
  - cross-validation
  - classifier selection

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集/子集 | 数量 | 备注 |
|------------|------|------|
| 总患者数 | `532` | 来自 `2` 个独立中心 |
| D1 | `263` | 训练/筛特征主集 |
| D2/D3 | `223` | 验证与相关性分析 |
| D4 | `46` | 额外独立验证 |
| D5 / TCGA | `113` | 外部验证 |

### 6.2 数据增强

- 当前抽取正文未强调图像增强。
- 说明本文主焦点不是 end-to-end CNN 训练，而是 segmentation 后的 morphometric machine learning。

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| feature selection | `MRMR` |
| candidate classifiers | `SVM / RF / DAC` |
| validation | `5-fold cross-validation` |
| final best classifier | `SVM` |

### 6.4 预处理与数据细节

- 样本形式：`4` 个 TMA
- 研究对象：early colon adenocarcinoma
- recurrence 定义：术后至复发诊断或随访终点
- follow-up 截止：`2017-12-31`
- 病理/临床信息完整性是纳入条件之一。

---

## 7. 推理与后处理

- 先由自动 gland segmentation 提取 gland contour。
- 再生成：
  - gland contour
  - gland orientation map
  - gland shape underlying distribution
- 最终由分类器直接输出：
  - `C+` recurrence risk
  - `C-` non-recurrence risk

---

## 8. 消融实验

### 8.1 候选分类器比较

- 候选：
  - `SVM`
  - `DAC`
  - `RF`
- 结果：
  - `SVM` 表现最好，因此被锁定为 `ECAHBC`。

### 8.2 各模块贡献量化

- 文中可明确的主要贡献量化是“特征类别”而不是“网络模块”：
  - top-5 里 `3/5` 与 gland orientation disorder 相关；
  - `2/5` 与 gland shape/size 相关。
- 这说明 orientation disorder 是 aggressive tumor 的主导信号之一。

### 8.3 与人工阅读比较

- 论文专门评估了两位病理专家在 D1 / D2 上的人工估计一致性与性能。
- 这一步的意义是把机器风险分层与传统人工分级放在同一评价框架下。

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 指标 | 数值 | 页码 |
|------|------|------|
| recurrence prediction accuracy | `0.881` | `p.6` |
| DSS hazard ratio | `9.65` | `p.1, p.7` |
| 95% CI | `2.15-43.12` | `p.1, p.7` |
| P value | `0.003` | `p.1, p.7` |

### 9.2 结果解释

- `ECAHBC-positive` 患者 recurrence risk 明显更高，且 DSS 更差。
- orientation disorder 和 gland shape irregularity 在 aggressive tumor 中更明显。
- 作者还观察到 `ECAHBC-positive` 与 `Ki67` 阳性、`CEA` 升高存在显著相关。

### 9.3 公平对比条件确认

- 本篇不是和 segmentation SOTA 做统一主表竞争，而是做病理风险建模。
- 所以公平性重点在：
  - 多中心验证；
  - 外部 TCGA 验证；
  - 与人工病理估计和临床指标同时比较。

### 9.4 评价协议与指标定义

- 分类/预后指标主要包括：
  - accuracy
  - PPV
  - NPV
  - Kaplan-Meier
  - log-rank
  - Cox proportional hazards

---

## 10. 计算量与效率

- 本篇主要价值在于病理可解释性，不在部署效率。
- 但相比昂贵分子 assay，它强调：
  - 基于常规 H&E；
  - 非破坏性；
  - 成本更低；
  - 可重复性更强。

---

## 11. 分类体系与研究空白

### 11.1 本篇的方法学定位

- 不是 end-to-end grading CNN；
- 也不是仅做 segmentation；
- 而是 `segmentation-driven morphometric prognostic modeling`。

### 11.2 论文指出的研究空白 / Open Problems

- colon cancer 文献里此前缺少系统的 gland orientation / shape 定量预后分析。
- 手工病理 grading 受主观性影响大。
- 分子 assay 虽强，但不适合所有临床场景。

### 11.3 对后续研究的启示

- gland segmentation 的下游价值不止于 `grade classification`，还包括 recurrence risk prediction。
- orientation 特征值得在今后 morphology-aware 模块设计与分析中重点关注。

---

## 12. 临床/病理标准

### 12.1 涉及的病理分级标准

- 论文使用 in-house two-tiered grading 口径：
  - `>=50%` tumor glandular -> low grade
  - `<50%` tumor glandular -> high grade
- 本质上仍是 gland formation 驱动的病理标准。

### 12.2 涉及的生物标志物

- `Ki67 labeling index`
- `serum CEA`

### 12.3 临床意义

- 本篇提供的临床桥接非常强：
  - 从 routine H&E 中提取 gland morphology；
  - 形成 recurrence risk classifier；
  - 并与 `Ki67`、`CEA` 做一致性验证；
  - 因而不是只停留在视觉漂亮的形态描述。

---

## 13. 开源与复现

- 代码是否开源：`正文未见稳定公开仓库`
- 代码仓库地址：`未提供`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`中高`

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 前置 gland segmentation 模型细节 | 部分 | 只确认存在自动分割 | 高 |
| 797 特征的完整数学定义 | 部分 | 依赖补充材料 | 高 |
| SVM 核函数与参数 | 否 | 不脑补 | 高 |
| TCGA 验证具体预处理 | 否 | 仅记录外部验证存在 | 中 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 主样本仍以 TMA 为主，不是全量 WSI。
- 多中心数量仍有限，需更大规模独立验证。

### 14.2 我们观察到的潜在问题

- 强依赖前置 gland segmentation 质量。
- 如果 gland contour 出错，orientation / shape 特征会直接失真。
- 以 recurrence 为终点时，类别不平衡和事件数不足都可能影响稳定性。

### 14.3 失败案例 / 定性分析

- aggressive tumor 与 indolent tumor 的差异被可视化为：
  - gland contour 更不规则；
  - orientation map 更混乱；
  - underlying distribution 更离散。
- 但如果是 mixed morphology 样本，单一少数特征可能仍难完全覆盖异质性。

---

## 15. 对我们项目的落地价值

### 15.1 最直接的启发

- 这篇极适合支撑“为什么 gland segmentation 不只是做 mask，而是为更高层病理风险建模服务”。
- 它把 `orientation disorder` 从病理直觉变成了机器可量化特征。

### 15.2 对特征工程和下游任务的启发

- 从分割结果中可进一步派生：
  - gland orientation entropy
  - local tensor contrast
  - circularity entropy
  - fractal dimension dispersion
- 如果后续扩展 morphology-aware 下游任务，可把本篇当作 orientation 路线的关键入口。

### 15.3 对实验设计的提醒

- 若未来做分割到风险建模的扩展，应优先避免：
  - 只追求 Dice，不验证形态可用性；
  - 只做单中心验证；
  - 不做临床指标相关性检查。

### 15.4 在整套文献链中的位置

- 在 `08` 目录中，本篇最适合放在：
  - `02_Glandular-Morphometrics.md` 之后；
  - `03_Segmentation-and-Grade-Prediction.md` 与 `04_Automatic-Tumor-Grading-WSI.md` 之前。
- 它的角色是“从 morphology grading 走向 prognostic stratification”的中间桥梁。

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`引言/讨论中的临床价值说明`
- [ ] 需要和哪篇论文交叉验证：`02_Glandular-Morphometrics.md`, `03_Segmentation-and-Grade-Prediction.md`
- [ ] 待确认的问题：`如果后续做 morphology-aware metrics，是否要显式加入 orientation disorder 分析`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 早期结肠癌高风险识别需求 | 临床动机 |
| related work | gland orientation / shape risk modeling | 病理下游小节 |
| 讨论 | segmentation 价值延伸到 recurrence prediction | 应用价值 |
| 展望 | 与 `Ki67/CEA` 的桥接 | 多模态/临床结合 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.3` | 整体 workflow 图 | 方法总览 |
| `Fig. 2` | `p.5` | recurrence 与 non-recurrence 的 gland contour / orientation map 对比 | 形态学直观证据 |
| `Table 1` | `p.5` | 患者临床病理特征统计 | 队列说明 |
| `Fig. 4` | `p.8` | Kaplan-Meier / 风险分层结果 | 预后价值 |
| `Table 2` | `p.7` | DSS 生存分析 | 独立预后价值 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（前置分割与 SVM 超参数仍缺）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文摘要/结果段一致
- [x] 指标定义和评价协议已确认
- [ ] 消融实验的结论已量化（本文更偏 classifier 比较，不是模块消融）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注而未脑补

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/08_病理意义_形态学与下游应用/05_Gland-Orientation-Aggressive-Tumor`
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

- 记录字段：`paper_id=03_文献证据/08_病理意义_形态学与下游应用/05_Gland-Orientation-Aggressive-Tumor`；`paper_type=planned_category:08_病理意义_形态学与下游应用`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/08_病理意义_形态学与下游应用/05_Gland-Orientation-Aggressive-Tumor` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
