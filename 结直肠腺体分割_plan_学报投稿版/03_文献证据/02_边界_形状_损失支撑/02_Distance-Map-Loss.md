# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [x] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `shape-aware loss`
- `distance-transform based penalty term`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`02_边界_形状_损失支撑`

- 按模板要求，本篇至少完成：`1, 2, 4, 5, 8, 9, 13, 14, 15`
- 因为原文同时给出数据划分、训练设置和后处理，所以额外补全：`6, 7, 16`

---

## 1. 论文信息

- 论文名：`Distance Map Loss Penalty Term for Semantic Segmentation`
- 作者/团队：`Fernando Caliva, Cristian Iriondo, Adriana M. Martinez, Sharmila Majumdar, Valentina Pedoia`
- 发表年份/会议/期刊：`2019, arXiv preprint`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:1908.03679`
- BibTeX key：`caliva2019distancemap`
- PDF 路径：`结直肠腺体分割_pdf库/02_边界_形状_损失支撑/Distance_Map_Loss_Penalty_Term_for_Semantic_Segmentation_2019.pdf`
- 当前定位：`距离图驱动的边界惩罚损失；核心不是换 backbone，而是在现有分割损失外引入一个按 boundary proximity 加权的 penalty term，让网络在 hard-to-segment boundary regions 上受到更强约束`
- 与已提取论文的关系：
  - 与 `Gated-SCNN` 互补：`Gated-SCNN` 是结构侧显式边界流，这篇是损失侧的 boundary-aware weighting
  - 与后续 `Boundary loss 2019` 形成同类对照：都是 boundary-aware supervision，但目标与形式不同
  - 可与 `Shape-Aware SDM 2020` 组成 `distance map / signed distance map` 路线

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：论文提出用 ground-truth masks 生成 distance maps，构造 loss penalty term，引导网络关注 hard-to-segment boundary regions
  - 用途：`边界损失动机`
  - 页码：`Abstract, p.1`
- 句子/事实 2：大多数分割误差集中在 object boundaries 附近，因此边界附近像素应在训练中被更强惩罚
  - 用途：`痛点描述`
  - 页码：`Sec.1, p.1-p.2`
- 句子/事实 3：该方法不仅提升 segmentation quality，还改善 shape preservation，尤其在 partial volume 区域更明显
  - 用途：`边界/形状价值`
  - 页码：`Abstract, p.1; Sec.3, p.3`

#### 1.1.2 related work 可引用句

- 句子/事实 1：论文明确提到该方法与 `Boundary loss` 相似，但不同点在于它从训练一开始就使用 distance-based penalty，而不是采用类似 fine-tuning 的策略
  - 用途：`同类方法差异`
  - 页码：`Sec.1, p.2`
- 句子/事实 2：作者强调他们的关注点不是 highly imbalanced segmentation，而是 accurate segmentation of object boundaries
  - 用途：`研究问题定位`
  - 页码：`Sec.1, p.2`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 数据集 | `OAI / Osteoarthritis Initiative` | 数据来源 | `p.2` |
| 手工标注病例数 | `40` | 数据规模 | `p.2` |
| 数据划分 | `25/5/10 train/valid/test` | 划分协议 | `p.2` |
| backbone | `V-Net` | 基础网络 | `p.1-p.2` |
| optimizer | `Adam` | 训练设置 | `p.2` |
| 学习率 | `1e-4` | 训练设置 | `p.2` |
| 数据增强 | `random in-plane rotations` | 数据增强 | `p.2` |
| boundary 指标 | `B-DSC 28.83±4.45%` | 主结果 | `p.3` |
| global 指标 | `G-DSC 96.42±0.80%` | 主结果 | `p.3` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 标准区域型损失即使能得到较高整体分割精度，错误仍往往集中在目标边界附近
- 对医学图像而言，边界与形状保真度直接影响 morphology / shape biomarkers 的可靠提取
- partial volume 区域和边界模糊区域尤其难分，普通 Dice 或 CE 对这些位置的针对性不足
- 需要一种简单、可插拔、能直接施加到现有分割网络上的 boundary-aware penalization 机制

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.2`
- `Sec.3, p.3`

### 2.2 核心思路（一段话概括解法方向）

- 论文从 GT segmentation mask 生成 distance map `Φ`，使得靠近目标边界的像素具有更高惩罚权重，并把该图直接乘到基础多类 cross-entropy 上，形成 `distance map loss penalty`。这样网络在训练时会更关注 hard boundary regions；作者用 V-Net 在 3D MRI bone segmentation 上验证，发现相较 Dice、focal loss 与 confident predictions penalizing loss，边界 Dice 和整体 Dice 都有所提升。

关键页码：

- `Abstract, p.1`
- `Sec.2, p.2`
- `Sec.3, p.3`

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
Dice = 2 Σi pi gi / (Σi p_i^2 + g_i^2)
```

符号说明：

- `pi`：预测体素概率
- `gi`：GT 体素标签
- 作用：作为作者实验中的一个重要 baseline
- 页码：`Eq.(1), p.1`

公式 2：

```text
L = (1 / N) Σi=1..N (1 + Φ) ⊙ Σj=1..K ( - yj log ŷj )
```

符号说明：

- `N`：样本数
- `K`：类别数
- `yj`：GT 类别标签
- `ŷj`：预测类别概率
- `Φ`：由 GT mask 生成的 distance map
- `⊙`：Hadamard product
- 含义：在标准多类 cross-entropy 外乘以距离图权重，对边界附近错误施加更强惩罚
- 页码：`Eq.(2), p.2`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 梯度特性：
  - `Φ` 越大，对应位置的 CE 梯度越大
  - 因此靠近边界的像素在反向传播中权重更高
- 关键实现细节：
  - 论文在损失中使用 `(1 + Φ)` 而不是只用 `Φ`
  - 作者明确说明加 `1` 是为了缓解 vanishing gradient 问题
- 适用条件：
  - 有较可靠的 GT mask，可从中计算 distance transform
  - 任务真正关心边界形状保真度，而不只看区域重叠
- 不适用场景：
  - 如果 GT 边界本身噪声大，距离图可能放大错误标注
  - 若目标极端稀疏且更需要 area imbalance 处理，这篇方法不是专门为该问题设计
- 页码：
  - `p.2`
  - `p.3`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `Base CE` | `Σ - yj log ŷj` | 多类语义分类 | segmentation output |
| `Distance Penalty` | `(1 + Φ)` | 强化 boundary-near pixels 的惩罚 | 逐像素/逐体素加权 |
| `Penalized CE` | `(1 + Φ) ⊙ CE` | 同时保持区域分类与边界关注 | 最终训练损失 |

### 5.2 总损失公式

```text
L_total = (1 / N) Σ (1 + Φ) ⊙ CE
```

说明：

- 这篇论文的核心很简单：不是再引入复杂多项式损失，而是把 `distance map` 作为一个 penalty factor 乘到原始 CE 上
- 好处是可插拔、实现直接、可迁移到 3D 和多类场景

### 5.3 权重配置与调度策略

- 各项权重：
  - 没有额外的手工 `λ` 加权
  - 核心权重来自 `distance map Φ`
- 是否衰减/动态调整：
  - 文中未报告动态调度
- 关键实现细节：
  - GT 外部和内部都计算距离图，再组合成最终 `Φ`
  - 不同骨结构的内部距离图分别计算，以缓解骨尺寸差异
- 页码：
  - `p.2`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `OAI / Osteoarthritis Initiative` | `25` | `10` | `5` | 共 `40` 个手工标注病例 |

### 6.2 数据增强

- 增强列表：
  - `random in-plane rotations`
- Patch 提取策略：`[待确认，当前摘录未见 patch 级设置]`
- 页码：`p.2`

### 6.3 优化器与超参数

- 框架：
  - `TensorFlow 1.12`
  - 距离图生成中使用 `MATLAB`
- 优化器：`Adam`
- 初始学习率：`1e-4`
- 学习率调度：`[待确认，文中摘录未见]`
- Batch size：`[待确认]`
- Epoch / Steps：`[待确认]`
- 权重初始化：`[待确认]`
- 预训练策略：`从头训练的可能性较高，但当前摘录未明确`
- 是否冻结部分层：`未见说明`
- 设备：`Intel Xeon Gold 6130 CPU, four GPUs, 376GB RAM`
- 页码：`p.2`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；3D MRI`
- 颜色空间转换：`不适用`
- resize / crop / pad 策略：`[待确认]`
- patch overlap：`[待确认]`
- 背景过滤策略：`无单独描述`
- 标签生成方式：
  - 从 GT segmentation masks 计算 distance transform
  - 对 mask 外部与内部都构造 distance map
  - 不同骨结构分别计算内部距离图后合并
- 类别不平衡处理：`不是本文主打问题`
- 随机种子/重复次数：`未明确`
- 数据泄漏风险点：`病例数较少，仅 40 例，后续复现时需严格固定 split`
- 页码：`p.2`

---

## 7. 推理与后处理

- 后处理步骤：
  1. 3D morphological closing
  2. 提取三个 largest connected components
- TTA / Test-time refinement：`未见说明`
- 页码：`p.3`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | Proposed distance penalty vs Dice loss | B-DSC 与 G-DSC 均提升 | 距离图惩罚优于纯区域重叠优化 |
| `A2` | Proposed vs focal loss | Proposed 更优 | 边界附近的显式距离加权比 focal 式难例重加权更适合本任务 |
| `A3` | Proposed vs confident predictions penalizing loss | Proposed 更优 | 直接 shape-aware weighting 对边界更有效 |
| `A4` | relaxed B-DSC tolerance `1-4 voxels` | 附录多阈值下仍优 | 改善不是只出现在单一容差下 |

### 8.2 各模块贡献量化

- 主结果量化：
  - `B-DSC`：`28.83 ± 4.45%`
  - `Dice loss`：`26.73 ± 5.40%`
  - `Pereyra et al. 2017`：`25.81 ± 3.02%`
  - `Focal loss`：`26.70 ± 4.27%`
- 全局分割量化：
  - `G-DSC`：`96.42 ± 0.80%`
  - `Dice loss`：`96.34 ± 1.21%`
  - `Pereyra et al. 2017`：`95.96 ± 1.30%`
  - `Focal loss`：`95.00 ± 1.00%`
- 结论：
  - 方法不是靠牺牲全局分割换边界，而是同时改善边界与整体 Dice
- 页码：`p.3; Appendix A p.5`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `OAI knee MRI test` | `G-DSC 96.42±0.80%` | `B-DSC 28.83±4.45%` | `relaxed B-DSC (1-4 voxels) 持续领先` | compared with Dice / focal / confidence penalty |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `Proposed distance map loss` | `OAI` | `G-DSC 96.42±0.80%` | `B-DSC 28.83±4.45%` | `best` |
| `Dice loss` | `OAI` | `G-DSC 96.34±1.21%` | `B-DSC 26.73±5.40%` | baseline |
| `Pereyra et al. 2017` | `OAI` | `G-DSC 95.96±1.30%` | `B-DSC 25.81±3.02%` | confidence penalty |
| `Focal loss` | `OAI` | `G-DSC 95.00±1.00%` | `B-DSC 26.70±4.27%` | hard example reweighting |

### 9.3 公平对比条件确认

- 是否统一 backbone：`是，均基于 V-Net`
- 是否统一数据增强：`文中比较表述默认一致`
- 是否统一后处理：`是，统一使用 morphological closing + 3 largest components`
- 是否统一输入尺寸：`[待确认]`
- 结果来源：`原文 Figure 2 / Figure 3 / 结果段数字`
- 页码：`p.2-p.3`

### 9.4 评价协议与指标定义

- 数据划分来源：`作者自定义 25/5/10 split`
- 结果汇报层级：`test set`
- Dice 类型：
  - `G-DSC`：global Dice score coefficient
  - `B-DSC`：boundary Dice score coefficient
- relaxed B-DSC：
  - 对边界做一定 tolerance 扩展，再计算 boundary Dice
  - 文中附录报告 `1-4 voxels` tolerance
- 是否含后处理后再报结果：`是`
- 是否多 seed 平均：`未说明`
- 是否报告标准差 / 置信区间：`报告均值 ± 标准差`
- 页码：`p.3; Appendix A p.5`

---

## 13. 开源与复现

- 代码是否开源：`[待确认]`
- 代码仓库地址：`[待确认]`
- 框架/语言：`TensorFlow 1.12 + MATLAB`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：
  - 距离图构造细节对结果敏感
  - 数据集规模小，split 影响较大
  - 3D 医学数据的预处理和体素级后处理未完全展开

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `后续复现需固定并重复` | `中` |
| 验证集划分 | `是` | `25/5/10` | `低` |
| 推理阈值 | `否` | `需要结合 V-Net 输出实现确定` | `中` |
| 后处理细节 | `部分明确` | `保留 morphological closing + 3 largest CC` | `中` |
| 训练轮数停止准则 | `否` | `需额外确认` | `高` |
| 数据预处理 | `否` | `需在严格复现时补齐 MRI preprocessing` | `高` |

- 不确定但影响较大的点：
  - batch size、epoch、体素 spacing / resize 等未在当前摘录中明确
  - 距离图是否有额外归一化、裁剪或截断，当前摘录未展开

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文更像短篇方法说明，实验规模较小，主要验证在单一 3D bone segmentation 场景
- 论文强调 shape preservation，但并未给出更丰富的跨数据集泛化验证
- 页码：`p.1-p.3`

### 14.2 我们观察到的潜在问题

- 它本质上是对 CE 做距离加权，而不是直接优化可微分边界几何量，因此几何约束仍然较间接
- 距离图来自 GT mask，如果标注边界不稳定，会把噪声显式编码进损失
- 论文的主实验不是腺体分割，且 MRI 骨结构边界与病理切片边界统计特征差别很大
- 当前主表改进幅度在全局 Dice 上不大，收益主要集中在边界质量

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`未单列 failure case，但用 error maps 展示不同损失的边界误差`
- 典型失败场景：
  - partial voluming 区域边界更难分
  - 传统 Dice / focal 在边界附近的绝对距离误差更明显
- 对我们任务的映射：
  - 腺体任务中的黏连边界和细缝区域与本文的“hard boundary regions”高度相似
  - 但腺体内部纹理更复杂，distance penalty 可能要和区域损失或拓扑损失联合使用
- 页码：`p.3`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 从 GT mask 生成 distance map，作为边界难点区域的显式权重图
- 将 `distance penalty` 作为现有 CE/BCE 的外乘加权项，而不是强行替换整个 loss
- 同时报告 `global metric + boundary metric`，避免只看区域重叠

### 15.2 可以作为候选参数来源的

- 使用 `(1 + Φ)` 而不是 `Φ`，避免梯度过弱
- 边界内外同时计算距离图，而不是只看外边界
- 若目标尺寸差异大，可像文中一样按类别分别计算内部距离图再合并

### 15.3 不应照搬的（及原因）

- 直接把 `OAI` 的 3D MRI 设置迁移到腺体病理图像：
  - 原因：成像模态、边界统计、类别结构完全不同
- 只用 penalized CE 作为唯一损失：
  - 原因：腺体任务通常还需要 `Dice`、对象级约束或黏连分离监督
- 直接复用 morphological closing + 3 largest connected components：
  - 原因：病理图像中实例数量远多于三块骨结构，该后处理不适配

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界加权损失 | 用距离图对边界附近错误施加更强惩罚 | `强` |
| GT 派生监督图 | 直接从 mask 生成距离图，不需要额外人工标注 | `强` |
| shape-aware training | 说明边界质量可通过损失重加权改善，而非必须改 backbone | `强` |
| 指标设计 | 强调 `B-DSC` 等边界指标的重要性 | `中` |
| 复杂结构分离 | 对腺体黏连边界可作为 loss 候选，但需与区域 loss 联合 | `中` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`损失函数候选池`、`边界监督设计`
- [ ] 需要和哪篇论文交叉验证：`Boundary loss 2019`、`Shape-Aware SDM 2020`
- [ ] 待确认的问题：`距离图是否更适合作为 Dice/BCE 的辅助项，而非替代 CE`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 边界附近错误最集中、形状保真度对 biomarker 提取重要 | 作为 boundary-aware loss 动机 |
| related work | distance-transform based loss 路线 | 放在 boundary/shape-aware supervision 小节 |
| 方法 | `(1 + Φ) ⊙ CE` 的简单可插拔设计 | 作为辅助损失设计依据 |
| 实验设置 | `B-DSC` / relaxed B-DSC 的评价思路 | 用于补充边界指标设计 |
| 讨论 | 为什么全局 Dice 变化小但边界质量更好 | 用于解释结果差异 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.1-p.2` | GT segmentation 与 distance map 示意 | 说明损失输入来源 |
| `Eq.(2)` | `p.2` | penalized multi-class cross entropy 公式 | 回填 loss 设计 |
| `Figure 2` | `p.3` | 绝对距离误差图 | 定性展示边界误差改善 |
| `Figure 3` | `p.5` | Proposed vs Dice/focal 等多指标比较 | 数字与趋势引用 |

---

## 17. 提取质量自检

- [x] 关键数字已标注来源页码
- [x] 可直接引用卡片已填写
- [x] 核心公式与符号已解释
- [x] 训练设置已覆盖数据划分、optimizer、lr、augmentation
- [x] 标签与距离图生成逻辑已提取
- [x] 主结果数字已核对
- [x] 指标定义和评价协议已确认
- [x] 消融/对比结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/02_边界_形状_损失支撑/02_Distance-Map-Loss`
- `paper_type`: `planned_category:02_边界_形状_损失支撑`
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

- 记录字段：`paper_id=03_文献证据/02_边界_形状_损失支撑/02_Distance-Map-Loss`；`paper_type=planned_category:02_边界_形状_损失支撑`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/02_边界_形状_损失支撑/02_Distance-Map-Loss` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
