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

- `end-to-end pathology pipeline`
- `segmentation + detection + grading`
- `multi-institution validation`
- `radiomics + SVM ensemble`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`08_病理意义_形态学与下游应用`

- 本篇是 `08` 目录中把病理结构、腺体分割和跨机构分级验证连起来的关键论文
- 对当前项目最有价值的是：
  - 提供完整的 `segmentation -> detection -> grading` 流水线
  - 同时验证单机构内和跨机构间泛化
  - 明确哪些 gland / lumen / nuclei 形态特征在恶性识别中最有解释力
  - 证明组合多尺度特征与层级集成优于任何单一特征组
- 本篇至少完成：`1-9, 13-17`

---

## 1. 论文信息

- 论文名：`Segmentation and Grade Prediction of Colon Cancer Digital Pathology Images Across Multiple Institutions`
- 作者/团队：`Saima Rathore, Muhammad Aksam Iftikhar, Ahmad Chaddad, Tamim Niazi, Thomas Karasic, Michel Bilello`
- 发表年份/会议/期刊：`2019, Cancers`
- DOI / arXiv ID：`10.3390/cancers11111700`
- BibTeX key：`rathore2019seggrade`
- PDF 路径：`结直肠腺体分割_pdf库/08_病理意义_形态学与下游应用/Segmentation_and_Grade_Prediction_of_Colon_Cancer_Digital_Pathology_Images_Across_Multiple_Institutions_2019.pdf`
- 当前定位：`08` 目录里最完整的“腺体分割驱动下游检测与分级”流程论文之一，尤其重要的是它不仅做单数据集验证，还做了跨机构训练-测试互换
- 与已提取论文的关系：
  - 承接 [02_Glandular-Morphometrics.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/08_病理意义_形态学与下游应用/02_Glandular-Morphometrics.md)：前者强调 `BAM` 和 gland shape aberrance，本篇进一步整合 gland、patch、image 多尺度特征
  - 与 [01_CRC-Histological-Characteristics.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/08_病理意义_形态学与下游应用/01_CRC-Histological-Characteristics.md) 呼应：本篇算法使用的 gland formation、细胞核与 lumen 空间关系，本质上就是病理 grading 语言的量化
  - 与 [01_GlaS-Challenge.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md) 有直接连接：作者把 `GlaS` 作为跨机构验证数据之一

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：区分 benign / malignant、再进一步分级，是 colon histopathology 的核心任务，但 glandular architecture 和 size 在 benign 到 malignant 间连续变化，导致 pathologist 间 discordance 常见。
  - 用途：`研究动机`
  - 页码：`p.1`
- 句子/事实 2：结直肠癌计算机辅助诊断必须同时考虑 cellular architecture、gland formation 和 stromal components，而不是只看全图粗粒度纹理。
  - 用途：`病理结构背景`
  - 页码：`p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者提出 end-to-end computational pathology pipeline，把 gland segmentation、cancer detection 和 cancer grading 放进单一自动化流程。
  - 用途：`方法定位`
  - 页码：`p.1-p.3`
- 句子/事实 2：训练一个机构、测试另一个机构后，cancer detection 仍可达到 `93.7%-94.5%`，grading 仍达 `95%`，说明模型并非只在单中心数据上成立。
  - 用途：`泛化能力`
  - 页码：`p.8`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| DOI | `10.3390/cancers11111700` | 文献信息 | `p.1` |
| RMC 图像数 | `174` | 数据规模 | `p.1`, `p.10` |
| GlaS 图像数 | `165` | 数据规模 | `p.1`, `p.10` |
| RMC slides / patients | `68 / 68` | 数据来源 | `p.10` |
| GlaS slides / patients | `16 / 16` | 数据来源 | `p.10` |
| RMC magnification | `10x` | 成像设置 | `p.10` |
| GlaS magnification | `20x` | 成像设置 | `p.10` |
| segmentation accuracy | `87.5% (RMC), 88.4% (GlaS)` | 分割结果 | `p.1`, `p.6` |
| meta-classifier detection acc | `97.6% (RMC), 98.3% (GlaS)` | 主结果 | `p.1`, `p.7` |
| meta-classifier grading acc | `98.6% (RMC), 98.6% (GlaS)` | 主结果 | `p.1`, `p.7` |
| cross-dataset detection acc | `94.5%, 93.7%` | 跨机构结果 | `p.1`, `p.8` |
| cross-dataset grading acc | `95%, 95%` | 跨机构结果 | `p.1`, `p.8` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 结肠病理诊断至少包含三个层次：
  - gland segmentation
  - benign vs malignant detection
  - malignant grading
- 既往工作常把这三件事拆开做，缺少真正连贯的端到端流程。
- 只依赖 global image features 容易漏掉局部 gland / lumen / nuclei 细节。
- 同时，单中心实验不能说明方法能否跨机构泛化。
- 因而本文要解决的是：
  - 如何分割 gland 及其内部结构
  - 如何融合 image / patch / gland 三尺度特征
  - 如何验证跨数据集、跨机构是否仍稳健

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 论文构建了一条多步式 computational pathology pipeline：先通过几何和形态学规则驱动的 gland segmentation 方法，把 gland boundary 以及内部的 epithelial cells、nuclei、lumen 分开；再在 image、local patch、individual gland 三个尺度上提取 radiomic / morphometric 特征；随后用分层 SVM 框架完成第一层概率估计，并在第二层用 linear / RBF / sigmoid SVM 做 meta-classifier，再通过 majority voting 给出最终的 cancer detection 和 grading 结果。与前一篇基于 `BAM + SVM` 的工作相比，这篇的关键提升是多尺度特征集成和跨机构验证。

关键页码：

- `p.1-p.3`
- `p.10-p.13`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 总体五步：
  1. colon histology image input
  2. multi-step gland segmentation
  3. tissue morphology quantification
  4. first-level classification
  5. second-level meta-classification with majority voting
- 最终任务：
  - 二分类：`normal vs malignant`
  - 三分类：`well / moderate / poor` 或对应等价 grade 分组

### 3.2 关键模块详细描述

**模块 1：`Multi-step Gland Segmentation`**

- 位置：整条 pipeline 的入口
- 目标：
  - 不只分 gland boundary
  - 还要分 gland 内部的 epithelial cells、nuclei、lumen
- 核心步骤：
  1. `K-means` 把图像聚成 white / pink / purple 三类组织成分
  2. ellipse fitting 定位 nuclei、epithelial cytoplasm、lumen
  3. hierarchical clustering 区分 true gland components 与 false positives
  4. lumen detection
  5. internal gland region formation
  6. 借助 radial lines 与层次聚类加入 boundary nuclei
  7. dilation 得到完整 gland region
- 页码：`p.11-p.12`

**模块 2：`Multi-scale Feature Extraction`**

- 三类特征：
  - `image-based`
  - `gland-based`
  - `local-patch-based`
- 设计动机：
  - image-based 看全局纹理
  - patch-based 捕捉中尺度局部异质性
  - gland-based 直连病理上最重要的结构解释
- 页码：`p.3`, `p.12-p.13`

**模块 3：`Gland-based Morphometrics`**

- 关键内容：
  - 选取 `5` 个最大和 `5` 个最小 glands
  - 计算 epithelial cells 和 nuclei 到 lumen centroid 的距离波动
  - 计算 lumen / epithelial / nuclei 面积比例与两两比值
  - 计算 area、compactness、convex area、eccentricity、Euler number、major/minor axis、orientation、perimeter
- 这是最贴近病理 gland formation 与结构破坏的特征层
- 页码：`p.12-p.13`

**模块 4：`Hierarchical SVM Classification`**

- 第一层：
  - image-based 特征 -> RBF SVM -> `ProbabilityScore_1`
  - patch-based 特征 -> 多个 RBF SVM weak classifiers -> 选最高置信度 -> `ProbabilityScore_2`
  - gland-based 特征 -> RBF SVM -> `ProbabilityScore_3`
- 第二层：
  - 用 `ProbabilityScore_1/2/3` 作为输入
  - 建 linear / RBF / sigmoid SVM weak classifiers
  - 用 majority voting 输出最终分类
- 页码：`p.3`, `p.13`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 组件 | 作用 | 关键细节 |
|------|------|---------|
| K-means clustering | 初步分离组织成分 | white / pink / purple |
| ellipse fitting | 识别基础对象 | nuclei / epithelial cytoplasm / lumen |
| hierarchical clustering | 过滤伪目标 | true vs false gland components |
| radiomic features | 量化 morphology 和 texture | image / patch / gland 三尺度 |
| first-level RBF SVM | 生成各类特征概率估计 | `ProbabilityScore_1/2/3` |
| meta-classifier | 集成不同特征流 | linear + RBF + sigmoid + voting |

---

## 4. 公式与推导

### 4.1 核心公式

- 本篇不以单一公式创新为主
- 关键是多步处理与分层分类框架，而不是某个新的损失或解析公式

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 不适用

---

## 5. 损失函数

### 5.1 各监督项

- 本篇主干不是 end-to-end deep learning
- segmentation 也不是通过统一训练的深网络完成，而是多步 image processing / clustering / heuristics
- 分类使用 SVM，不存在深度网络式总损失设计

### 5.2 总损失公式

- 不适用

### 5.3 权重配置与调度策略

- 不适用

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `RMC` | `174` 张图像 | 通过 `10-fold CV` 轮换 | `10-fold cross-validation` | `68` slides / `68` patients, `10x` |
| `GlaS` | `165` 张图像 | 通过 `10-fold CV` 轮换 | `10-fold cross-validation` | `16` slides / `16` patients, `20x` |

补充类别分布：

- `RMC`
  - `82 normal`
  - `92 malignant`
  - malignant further:
    - `44 well`
    - `25 moderate`
    - `23 poor`
- `GlaS`
  - `74 normal`
  - `91 malignant`
  - malignant further:
    - `47 moderate`
    - `20 moderate-to-poor`
    - `24 poor`
  - 文中为对齐两数据集，将其转成 `well / moderate / poor` 近似分组

### 6.2 数据增强

- 未报告典型深学习 augmentation 流程
- segmentation 主要依赖多步图像处理，不是数据增强驱动
- patch-based branch 采用 random subset of fixed-size patches

### 6.3 优化器与超参数

- 分类器：
  - first-level：`RBF SVM`
  - second-level：`linear`, `RBF`, `sigmoid` SVM
- 参数调节：
  - `grid search`
- 验证：
  - `10-fold cross-validation`
- 页码：`p.13`

### 6.4 预处理与数据细节

- contrast enhancement 用于降低 imaging artifacts
- 之后转为 gray-scale 进行后续分析
- 两个数据集倍率不同：
  - `RMC = 10x`
  - `GlaS = 20x`
- 这是跨机构验证里很重要的 domain shift 来源

---

## 7. 推理与后处理

- segmentation 本身就是推理型 multi-step 流程：
  - 聚类
  - ellipse fitting
  - clustering for true/false objects
  - morphological dilation
- 分类推理是两层：
  - 先各特征流给 probability estimate
  - 再由 meta-classifier majority voting 得到最终结论
- 这使整个流程虽然不是 end-to-end deep network，但具有较强可解释性

---

## 8. 消融实验

### 8.1 单特征组比较

- 对 `cancer detection`
  - gland-based 略优于 patch-based 和 image-based
- 对 `cancer grading`
  - gland-based 仍是三者中最好
- 说明和病理结构最直接对应的 gland-level 特征最有信息量

### 8.2 meta-classifier 相比单特征/单分类器提升

- 集成后：
  - detection 提升到 `97.6%-98.3%`
  - grading 提升到 `98.6%`
- 文中明确指出该提升在 `95% CI` 下具有统计显著性，`p < 0.01`

### 8.3 跨机构验证

- 训练 `RMC` 测试 `GlaS`
  - detection `94.5%`
  - grading `95.0%`
- 训练 `GlaS` 测试 `RMC`
  - detection `93.7%`
  - grading `95.0%`
- 这是本篇相对同类论文最重要的加分项之一

---

## 9. 主表结果与对比

### 9.1 gland segmentation 结果

| 指标 | RMC | GlaS | 页码 |
|------|-----|------|------|
| Segmentation accuracy | `87.50` | `88.40` | `p.6` |
| Jaccard index | `0.86` | `0.89` | `p.6` |
| Dice similarity | `0.84` | `0.87` | `p.6` |
| Sensitivity | `0.90` | `0.92` | `p.6` |
| Specificity | `0.82` | `0.88` | `p.6` |
| F-Score | `0.88` | `0.89` | `p.6` |

### 9.2 individual feature 结果

| 任务 | 最佳单特征组 | GlaS | RMC | 页码 |
|------|-------------|------|-----|------|
| Cancer detection | gland-based | `93.7%` | `92.1%` | `p.6-p.7` |
| Cancer grading | gland-based | `90.5%` | `92.5%` | `p.6-p.7` |

补充：

- patch-based：
  - detection `93.1 / 91.5`
  - grading `89.5 / 91.5`
- image-based：
  - detection `92.5 / 90.9`
  - grading `89.7 / 90.7`

### 9.3 meta-classifier 主结果

| 任务 | GlaS ensemble | RMC ensemble | 页码 |
|------|---------------|--------------|------|
| Cancer detection accuracy | `98.3%` | `97.6%` | `p.7` |
| Cancer detection sensitivity | `97.8%` | `98.9%` | `p.7` |
| Cancer detection specificity | `98.8%` | `95.9%` | `p.7` |
| Cancer detection MCC | `96.5` | `95.1` | `p.7` |
| Cancer grading accuracy | `98.6%` | `98.6%` | `p.7` |
| Cancer grading sensitivity | `97.3%` | `97.4%` | `p.7` |
| Cancer grading specificity | `99.0%` | `99.0%` | `p.7` |
| Cancer grading MCC | `96.4` | `96.4` | `p.7` |

### 9.4 AUC 与跨机构结果

- `AUC`
  - detection：
    - `0.95` on `RMC`
    - `0.99` on `GlaS`
  - grading：
    - `0.98` on `RMC`
    - `0.96` on `GlaS`
- 跨机构 meta-classifier：
  - Train `RMC` -> Test `GlaS`
    - detection `94.5%`
    - grading `95.0%`
  - Train `GlaS` -> Test `RMC`
    - detection `93.7%`
    - grading `95.0%`

### 9.5 解释性特征

- 正常组织相对恶性组织表现为：
  - lower entropy
  - lower contrast
  - nuclei 到 lumen centroid 的距离波动更小
  - higher eccentricity
  - higher compactness
- 这些特征恰好与 pathologist 的视觉判断逻辑一致

### 9.6 评价协议与指标定义

- segmentation：
  - accuracy
  - Jaccard
  - Dice
  - sensitivity
  - specificity
  - F-score
- classification：
  - accuracy
  - sensitivity
  - specificity
  - `MCC`
  - ROC / AUC
- 这篇同时覆盖 segmentation metrics 与 clinical decision metrics，特别适合作为“分割如何服务下游病理判断”的证据

---

## 10. 计算量与效率

- 作者强调其 segmentation 方法不依赖深度网络训练，因此：
  - 不需要预训练模型
  - 可在仅有 CPU 的 desktop 上运行
  - 处理时间低于计算昂贵的深学习方法
- 但文中未给出系统级 runtime 数字

---

## 11. 分类体系与研究空白

### 11.1 本篇的任务体系

- gland segmentation
- cancer detection
- cancer grading
- within-dataset validation
- cross-dataset validation

### 11.2 本篇的特色

- 把 segmentation 与 grading 真正放进同一流程
- 不只分 gland 边界，还分内部结构
- 特征跨三尺度
- 分类跨两层
- 泛化跨两机构

### 11.3 仍未解决的空白

- 极度去分化的 very poorly-differentiated specimens 仍难被准确量化
- 方法更适合 gland-focused morphology，不适合直接做 benign/malignant 区域分割
- 仍需 prospective validation
- 尚未连接 survival、molecular subtype 或 genomic aberration 等更下游结局

---

## 12. 临床/病理标准

- 本篇强调病理判读依赖：
  - cellular architecture
  - gland formation
  - stromal components
- 正常组织：
  - uniform glandular arrangement
- 恶性组织：
  - heterogenous disruption of histologic features
- grading 以 `well / moderate / poor` differentiation 为基础
- 这说明模型如果只做粗分割、不保留 gland 内部结构，将很难支撑真正病理相关的分级

---

## 13. 开源与复现

### 13.1 论文未报告但复现必需的信息

- 未给出 patch-based 分支的固定 patch size
- 未完整给出所有 radiomic 特征维度统计与筛选细节
- 未给出 SVM 具体超参数最终取值
- 未说明两个数据集在跨机构实验中的 stain normalization 是否额外做过对齐
- 未提供完整代码链接

### 13.2 复现与偏差风险

- 两数据集倍率不同（`10x` vs `20x`），虽然提升了泛化论证价值，但也增加复现复杂度
- grading 标签映射存在对齐过程：
  - `moderate-to-poor` 被转换到与另一数据集可比的分级体系
- segmentation 方法 heavily depends on a sequence of heuristic choices，复现实装时较容易出现细节偏差

### 13.3 数据与代码

- 文中未给出完整公开代码入口
- `GlaS` 可公开获取，但 `RMC` 为机构数据，不应默认可直接拿到

---

## 14. 局限性与失败案例

- segmentation 在极不规则 glands 上仍会 under-segment 或漏掉部分边界
- 方法不能直接做 benign / malignant 区域级分离
- 对 extremely deformed glands 的 morphometric decoding 不够准确
- 属于 retrospective study，尚缺 prospective clinical validation
- 虽然论文称之为 end-to-end pipeline，但实质上是多步手工分割 + radiomics + SVM，不是统一可训练的深度端到端框架

---

## 15. 对我们项目的落地价值

### 15.1 最可直接借用的结论

- 腺体分割如果能进一步区分 lumen / epithelial / nuclei，就能更自然服务 grading，而不只是生成轮廓 mask
- 多尺度特征融合明显优于单一尺度
- 跨机构验证是病理 AI 论文里非常值得强调的可信度来源

### 15.2 对我们后续实验的启发

- 可考虑从分割结果派生：
  - gland component ratios
  - nuclei-lumen spatial arrangement
  - compactness / eccentricity / perimeter
  - texture + morphology 联合特征
- 若未来做 morphology-aware downstream task，可把本篇当作经典 radiomics baseline

### 15.3 对论文写作的价值

- 在 discussion 中可引用这篇说明：
  - 分割不是终点，而是病理量化的前端
  - gland 内部结构信息对 grading 同样重要
  - 跨机构 generalization 是检验病理模型可靠性的必要条件

### 15.4 在文献链中的位置

- 这是 `08` 目录里最完整的“结构分割 -> 下游分级 -> 跨机构泛化”节点
- 下一篇最自然的承接目标是：
  - `Automatic_Tumor_Grading_on_Colorectal_Cancer_Whole-Slide_Images_2022`

---

## 16. 关键图表索引

- `Figure 1`
  - 内容：normal、moderate、moderate-to-poor、poor 示例
  - 用途：病理 grade 视觉对照
  - 页码：`p.2`
- `Figure 2`
  - 内容：整体 pipeline 示意图
  - 用途：写 methodology 总框架
  - 页码：`p.3`
- `Figure 3`
  - 内容：gland segmentation 可视化结果
  - 用途：展示正常与恶性样本分割效果
  - 页码：`p.5-p.6`
- `Figure 4`
  - 内容：ROC / AUC
  - 用途：说明 detection / grading 的可靠性
  - 页码：`p.7-p.8`
- `Figure 5`
  - 内容：normal vs malignant 的 top features boxplots
  - 用途：解释性分析
  - 页码：`p.8-p.9`
- `Figure 6`
  - 内容：multi-step gland segmentation workflow
  - 用途：写 segmentation 方法
  - 页码：`p.11`
- `Figure 7`
  - 内容：单 gland 内的 lumen / epithelial / nuclei 特征示意
  - 用途：写 gland-based features
  - 页码：`p.12-p.13`
- `Table 1`
  - 内容：segmentation performance
  - 用途：分割结果
  - 页码：`p.6`
- `Table 2`
  - 内容：单特征组分类结果
  - 用途：消融对照
  - 页码：`p.6-p.7`
- `Table 3`
  - 内容：meta-classifier within-dataset 结果
  - 用途：主结果
  - 页码：`p.7`
- `Table 4`
  - 内容：cross-institution 结果
  - 用途：泛化证据
  - 页码：`p.8`

---

## 17. 提取质量自检

- 本篇全文已抽取，并结合摘要、结果表、方法段和跨机构验证部分完成核对，主证据较完整。
- 重点保留了四类最关键的信息：
  - 完整 pipeline
  - segmentation 与 grading 主结果
  - cross-dataset generalization
  - 解释性 morphometric 特征
- 由于 PDF 文本抽取存在重复段和少量排版噪声，正式稿中优先保留经多处一致验证的数字和结论。
- 本篇非常适合作为 `08` 目录的核心支撑文献之一，但需要注意：它虽然称为 end-to-end pipeline，技术上并不是纯深度学习的一体化训练系统。

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/08_病理意义_形态学与下游应用/03_Segmentation-and-Grade-Prediction`
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

- 记录字段：`paper_id=03_文献证据/08_病理意义_形态学与下游应用/03_Segmentation-and-Grade-Prediction`；`paper_type=planned_category:08_病理意义_形态学与下游应用`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/08_病理意义_形态学与下游应用/03_Segmentation-and-Grade-Prediction` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
