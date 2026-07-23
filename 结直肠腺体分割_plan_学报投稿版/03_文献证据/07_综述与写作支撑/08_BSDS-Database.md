# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [x] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `BSDS source paper`
- `human segmented natural images`
- `GCE / LCE`
- `segmentation benchmark origin`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`07_综述与写作支撑`

- 本篇是 `BSDS / human-segmented natural images` 数据库的源头论文之一，最适合补“为什么 segmentation 可以和多人类标注直接量化比较”的最原始出处
- 对当前项目最重要的不是方法结构，而是数据库建设口径、`GCE/LCE` 的定义逻辑，以及 human-vs-algorithm 评价思路
- 本篇至少完成：`1-3, 9, 13-17`

---

## 1. 论文信息

- 论文名：`A Database of Human Segmented Natural Images and its Application to Evaluating Segmentation Algorithms and Measuring Ecological Statistics`
- 作者/团队：`David Martin, Charless Fowlkes, Doron Tal, Jitendra Malik`
- 发表年份/会议/期刊：`2001, ICCV`
- DOI / arXiv ID：`10.1109/ICCV.2001.937655`
- BibTeX key：`martin2001bsds`
- PDF 路径：`结直肠腺体分割_pdf库/07_综述与写作支撑/A_Database_of_Human_Segmented_Natural_Images_and_its_Application_to_Evaluating_Segmentation_Algorithms_2001.pdf`
- 当前定位：`07` 目录中最关键的数据集/评价协议源头文献之一，主要用于支撑 `BSDS`、`human segmented natural images`、`GCE/LCE`、以及 segmentation benchmark 的历史来源
- 与已提取论文的关系：
  - 与 [07_Boundary-Detection-Brightness-Texture.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/07_Boundary-Detection-Brightness-Texture.md) 衔接：后者用人工标注边界做 `precision-recall / F-measure`，本篇则提供这些多人类分割 ground truth 的数据库基础
  - 与 [06_Contour-Hierarchical-Segmentation.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/06_Contour-Hierarchical-Segmentation.md) 衔接：后者的 `BSDS300/500` benchmark 体系正是建立在这条数据库与人工标注评价传统之上
  - 与 [05_Active-Contour-Metrics.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/05_Active-Contour-Metrics.md) 互补：前者解释 classic segmentation metric，本篇解释为什么 benchmark 本身可以由多人类分割构成

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者认为 segmentation 不一定只能在具体下游任务中评估，也可以通过与 `multiple human observers` 的分割结果比较来直接评价
  - 用途：`评价协议动机`
  - 页码：`p.2-p.3`
- 句子/事实 2：虽然不同 human segmentations 并不完全相同，但在允许 `refinement` 的一致性度量下，同一图像上的不同人类分割具有相当高的一致性
  - 用途：`human ground truth 合理性`
  - 页码：`p.2-p.3, p.5-p.6`

#### 1.1.2 related work 可引用句

- 句子/事实 1：论文构建了一个包含 `groundtruth segmentations produced by humans` 的自然图像数据库，并用其评估 segmentation algorithms
  - 用途：`BSDS 来源`
  - 页码：`p.1-p.2`
- 句子/事实 2：作者提出 `GCE` 与 `LCE`，并明确这些 error measures 对 segmentation granularity 的 `refinement` 具有容忍性，因此适合比较不同粒度的人工或算法分割
  - 用途：`GCE/LCE 定义`
  - 页码：`p.6-p.7`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| DOI | `10.1109/ICCV.2001.937655` | 文献信息 | `题录` |
| 图像总数目标 | `1000` | 数据库规模 | `p.4, p.11` |
| 图像尺寸 | `481 x 321 RGB` | 数据库规格 | `p.4` |
| 图像来源 | `Corel` image database | 数据库来源 | `p.4` |
| 已收集分割数 | `3000` | 数据收集进度 | `p.5` |
| 已参与者 | `25` | 数据收集进度 | `p.5` |
| 已覆盖图像 | `800` | 数据收集进度 | `p.5` |
| 目标标注密度 | 每图至少 `4` gray + `4` color | 数据库规划 | `p.5, p.11` |
| NCuts 平均误差 | `22% LCE`, `28% GCE` | benchmark 结果 | `p.8` |
| human 平均误差 | `7% LCE`, `11% GCE` | benchmark 参照 | `p.8` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- segmentation 研究长期缺少像 recognition 那样统一、可量化的 benchmark
- 过去很多分割论文主要靠“展示几张看起来不错的图”来说明效果，评价高度主观
- 难点在于“什么是正确分割”比“分类对不对”更微妙
- 作者反对“分割只能放到具体下游任务里评估”的极端看法，提出可以直接把 segmentation 作为 segmentation 来比较
- 核心前提是：同一图像上，多个人类观察者的分割虽然粒度不同，但在合适的一致性度量下具有足够高的一致性

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 作者构建一个由人类对自然图像进行分割得到的大规模数据库，并设计 `GCE` 与 `LCE` 两种对 `refinement` 容忍的一致性/误差度量，用以比较不同粒度的 segmentation。随后，作者用该数据库评估 `NCuts`，将算法与 human observers 的一致性直接做对照，从而建立了一条非常重要的 segmentation benchmark 传统：不是仅凭主观视觉印象，也不是必须依赖某个下游任务，而是可以把人工分割作为 gold standard，直接量化算法与人类的差距。

关键页码：

- `p.1-p.3`
- `p.6-p.8`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 本篇不是提出一个新分割网络
- 它的核心工作由三部分组成：
  1. 构建 `human segmented natural images` 数据库
  2. 提出 `GCE / LCE` consistency measures
  3. 用数据库 benchmark `NCuts`

### 3.2 关键模块详细描述

**模块 1：`Image Segmentation Database`**

- 从 `Corel` 数据库中选择 `1000` 张具有代表性的自然图像
- 图像规格为 `481 x 321 RGB`
- 作者强调图像应包含至少一个可辨识对象，避免纯纹理或不适合 recognition/segmentation 任务的图像
- 页码：`p.4`

**模块 2：`Human Segmentation Collection Tool`**

- 作者开发了 Java segmentation tool 以方便大量用户通过网络参与标注
- 这保证了：
  - 可扩展的人类分割收集
  - 显式的像素分区结果
  - 服务端分配任务
- 页码：`p.4-p.5`

**模块 3：`GCE / LCE`**

- `Global Consistency Error (GCE)` 强制所有 local refinement 在同一方向上
- `Local Consistency Error (LCE)` 允许在图像不同区域中出现不同方向的 refinement
- 两者都容忍 segmentation granularity 不同，因此更适合比较不同观察者或不同算法输出
- 页码：`p.6-p.7`

**模块 4：`NCuts Benchmark`**

- 作者用该数据库和 error measures benchmark `Normalized Cuts`
- 结果清楚表明：
  - `NCuts` 比 humans 差
  - 但又明显优于“random”式无关分割
- 页码：`p.8`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

- 本篇不适用逐层参数表
- 但可以提炼成“组成-作用”表：

| 组成 | 作用 | 写作价值 |
|------|------|---------|
| human-segmented image database | 提供 segmentation gold standard | benchmark 来源 |
| `GCE` | 全局一致性误差 | classic metric 来源 |
| `LCE` | 局部一致性误差 | classic metric 来源 |
| `NCuts benchmark` | 演示数据库可用于算法比较 | human-vs-algorithm 对照模板 |

---

## 4. 公式与推导

### 4.1 核心公式

- 本篇最重要的不是复杂模型公式，而是 `GCE / LCE` 的定义逻辑
- 两者都基于 `refinement error`
- 核心思想：
  - 若一个 segmentation 是另一个的细化，不应被重罚
  - 因为不同观察者可能只是分割粒度不同，而不是 perceptual organization 完全矛盾
- 对当前项目来说，最重要的是理解：
  - `GCE` 更严格
  - `LCE` 更宽容

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 不适用

---

## 5. 损失函数

### 5.1 各监督项

- 本篇不讨论训练 loss

### 5.2 总损失公式

- 不适用

### 5.3 权重配置与调度策略

- 不适用

---

## 6. 训练协议

### 6.1 数据集与划分

- `1000` 张代表性自然图像
- `481 x 321 RGB`
- 来源于 `Corel`
- 当时数据收集进展为：
  - `3000` 个分割
  - `25` 位参与者
  - `800` 张图像
- 最终目标：
  - 每图至少 `4` 份灰度分割
  - 每图至少 `4` 份彩色分割

### 6.2 数据增强

- 不适用

### 6.3 优化器与超参数

- 不适用

### 6.4 预处理与数据细节

- 图像选择标准偏向“自然场景且至少有一个可辨识对象”
- 作者明确避免无对象的纯纹理场景作为主体样本
- 这使数据库更适合支持 segmentation / grouping / recognition 研究

---

## 7. 推理与后处理

- 本篇主要讲数据库和评估，不涉及统一推理流程
- 唯一可提炼的“流程性”内容是：
  - 收集多人分割
  - 计算 segmentation consistency
  - 用同一误差度量评价 human-human 与 algorithm-human

---

## 8. 消融实验

### 8.1 消融设计

- 不是传统 ablation paper
- 但它通过 human-human 与 NCuts-human 的对照，形成了一种非常强的 benchmark 分析框架

### 8.2 各模块贡献量化

- 贡献不在模型增益，而在 benchmark 基础设施：
  - 让 segmentation 能像 recognition 一样被定量比较
  - 让不同 granularity 的分割仍可在一致性框架下比较
  - 让 algorithm-human gap 被清楚量化

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 项目 | 结论 | 页码 |
|------|------|------|
| 数据库目标 | 建立 `human segmented natural images` database | `p.1-p.2` |
| 核心主张 | segmentation 可通过与 multiple human observers 的结果比较直接评价 | `p.2-p.3` |
| 数据库规格 | `1000` 张 `481x321 RGB` Corel 图像 | `p.4` |
| 收集进度 | `3000` segmentations, `25` people, `800` images | `p.5` |
| error measures | 提出 `GCE` 与 `LCE` | `p.6-p.7` |
| human consistency | humans 在同图像上高度一致 | `p.5-p.6` |
| NCuts benchmark | `22% LCE`, `28% GCE` | `p.8` |
| human benchmark | `7% LCE`, `11% GCE` | `p.8` |

### 9.2 与其他方法的对比

- 论文主要比较的不是多种现代 segmentation 模型，而是：
  - human vs human
  - algorithm vs human
  - same-image vs different-image segmentation pairs
- 这使它更像一篇 benchmark 基础设施论文，而非单纯方法对比文

### 9.3 公平对比条件确认

- 所有比较都基于同一套 human segmentation database
- 误差度量统一采用 `GCE / LCE`
- 对人类与算法使用同一评价尺度
- 这是本篇最重要的公平性来源

### 9.4 评价协议与指标定义

- 本篇对你最重要的贡献是评价协议而非模型
- 它支撑以下写法：
  - segmentation 可以直接和多人类标注进行量化比较
  - 不同 granularity 的分割不应一概视为错误
  - 因此需要对 refinement tolerant 的指标
- 如果后面你要解释 `GCE / LCE`，本篇就是最直接的源头文献之一
- 如果你要解释为什么早期 boundary/segmentation benchmark 会依赖多人类标注，本篇同样是关键出处

---

## 10. 计算量与效率

- 本篇不以算法效率为重点
- 对当前项目而言，最重要的是数据集和评价框架，不是运行速度

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

- 本篇不是综述
- 但它实际上解决了一个长期空白：
  - segmentation 缺少像 recognition 那样统一可量化的 benchmark
- 作者给出的解决方式是：
  - 公开数据集
  - 多人类标注
  - refinement-tolerant metrics

---

## 12. 临床/病理标准（病理临床 D 类型专用）

- 本篇不涉及病理标准
- 但它对病理图像研究的启发很直接：
  - 多观察者标注差异并不等于 benchmark 不可用
  - 关键是用合适的一致性/误差定义去比较不同 granularity 或不同风格的标注

---

## 13. 开源与复现

- 代码是否开源：`当前抽取片段未记录`
- 代码仓库地址：`未记录`
- 框架/语言：`含 Java segmentation tool`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`低到中`
- 复现障碍：
  - 真正的价值不在复现某个模型，而在复用其 benchmark 思路
  - 若完全复现实验，需要访问原数据库、分割工具与 NCuts 实现

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 当前可直接下载的数据库入口 | 当前抽取片段未保留 | 只提数据库与评价思想 | 中 |
| Java 工具现成运行方式 | 未保留 | 不做完整复现 | 低 |
| 与现代病理任务的直接映射 | 否 | 作为 benchmark 历史来源使用 | 低 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文承认 segmentation 的“正确答案”本身比分类更微妙
- 不同观察者之间并非完全一致
- 因此作者专门设计 refinement-tolerant measures，而不是假设唯一绝对分割

### 14.2 我们观察到的潜在问题

- 这是自然图像数据库，不是病理图像数据库
- `GCE / LCE` 很适合写 classic segmentation benchmark 历史，但不一定是你当前实验的首选主指标
- 因此最合适的用法是：
  - 作为 benchmark 历史来源
  - 作为多人类标注一致性思路来源
  - 而不是直接当成当前腺体任务的主评价协议

### 14.3 失败案例 / 定性分析

- 文中最重要的“失败意识”是：
  - 一个算法可能通过极粗或极细分割来投机
  - 这就是为什么 error measure 必须显式讨论 refinement tolerance
- 作者也指出 degenerate segmentations 会影响度量解释，因此评价需要结合分布分析而非只看孤立样本

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `BSDS / human segmented natural images` 的源头出处
- segmentation 可与多人类标注直接比较的经典论证
- `GCE / LCE` 的来源和语义

### 15.2 可以作为候选参数来源的

- 本篇不给深度模型训练参数
- 它提供的是 benchmark 设计逻辑和人工标注一致性框架

### 15.3 不应照搬的（及原因）

- 不应把自然图像数据库的 benchmark 结论直接套到病理腺体分割
  - 原因：图像域、目标结构、标注习惯都不同
- 不应把 `GCE / LCE` 直接当成你当前实验必须报告的主指标
  - 原因：它更适合作为历史来源和评价思想补充
- 不应忽略这篇里“human granularity differences 合理存在”的前提
  - 原因：如果脱离这一点，`GCE / LCE` 的设计动机就会被误解

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| benchmark 历史来源 | `BSDS` 与 human segmentation database 的源头 | 强 |
| 指标解释 | `GCE / LCE` 的定义动机与语义 | 强 |
| discussion | 多观察者标注差异不应简单视为噪声 | 强 |
| related work | segmentation 从主观展示走向定量 benchmark 的历史转折 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`论文写作_实验指标历史与benchmark来源`
- [ ] 需要和哪篇论文交叉验证：`06_Contour-Hierarchical-Segmentation.md`, `07_Boundary-Detection-Brightness-Texture.md`
- [ ] 待确认的问题：`正文是否需要显式提 GCE/LCE，还是只在 related work / 附录中说明 BSDS 的历史来源`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| related work | segmentation benchmark 的历史来源 | 背景脉络 |
| 方法/实验 | human-labeled segmentation 作为 gold standard 的依据 | 指标背景 |
| discussion | 多观察者差异与 refinement tolerance | 评价局限讨论 |
| 附录 | `GCE / LCE` 的出处说明 | 术语补充 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.1-p.2` | 数据库示例图与多人类分割 | 直观说明 human variability |
| `Figure 3` | `p.2-p.3` | refinement tolerant 度量动机示意 | 解释 `GCE/LCE` |
| `Figure 4` | `p.3-p.4` | human-human 的 `GCE/LCE` 分布 | 说明一致性 |
| `Figure 8` | `p.8` | `NCuts vs human` 的 `GCE/LCE` 分布 | benchmark 结果 |
| `Figure 9` | `p.8` | 每图 `human vs human` 与 `NCuts vs human` 误差对比 | algorithm-human gap |

---

## 17. 提取质量自检

- [x] 已明确本篇是 `BSDS / human segmented images` 的源头论文
- [x] 已写清 `GCE / LCE` 的设计动机
- [x] 已记录 `1000 images / 481x321 / Corel` 等数据库规格
- [x] 已记录 `3000 segmentations / 25 people / 800 images` 的收集进度
- [x] 已记录 `NCuts 22%/28%` 与 `human 7%/11%` 的关键对比
- [x] 已明确它在我们项目中更适合做 benchmark 历史与评价思想支撑
- [ ] 所有公式逐项抄录校对（当前不需要）

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/07_综述与写作支撑/08_BSDS-Database`
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

- 记录字段：`paper_id=03_文献证据/07_综述与写作支撑/08_BSDS-Database`；`paper_type=planned_category:07_综述与写作支撑`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/07_综述与写作支撑/08_BSDS-Database` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
