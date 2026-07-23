# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [x] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `gland segmentation recent work`
- `attention + context fusion`
- `interpretability and uncertainty`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`04_腺体与病理近期相关工作`

- 本篇是近期直接针对结直肠腺体分割的 attention/context fusion 路线论文
- 本篇至少完成：`1, 2, 3, 6, 9, 13, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`Enhanced colorectal gland segmentation through multi-scale attention and contextual feature fusion`
- 作者/团队：`[待从正式文献信息页补全作者列表]`
- 发表年份/会议/期刊：`2026, Scientific Reports`
- DOI / arXiv ID：`10.1038/s41598-025-34548-5` / `[无 arXiv 信息]`
- BibTeX key：`macnet2026gland`
- PDF 路径：`结直肠腺体分割_pdf库/04_腺体与病理近期相关工作/Enhanced_colorectal_gland_segmentation_through_multi-scale_attention_and_contextual_feature_fusion_2026.pdf`
- 当前定位：`近期腺体分割直接方法论文；提出 `MAC-Net`，把 hierarchical feature extraction、attention refinement、multi-scale contextual fusion、hybrid boundary-aware loss、Grad-CAM 和不确定性分析放到同一系统`
- 与已提取论文的关系：
  - 与 `Attention_U-Net`、`VAN` 路线相连：都强调 attention，但本篇更贴近腺体病理分割任务
  - 与 `Boundary-Loss`、`Boundary-DoU` 互补：本篇不是纯 loss 论文，但显式加入 `Edge loss`
  - 与 `MILD-Net`、`DCAN` 等经典腺体分割方法形成“近期 attention/context fusion”对照组

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者提出 `MAC-Net`，融合 `multi-scale feature fusion`、`attention-guided contextual decoding` 与 `U-Net backbone`
  - 用途：`近期 related work 概括`
  - 页码：`Abstract, p.1`
- 句子/事实 2：普通 `U-Net` 的 skip connection 难以同时处理 varying gland sizes、染色伪影、intra-class variation 和复杂边界
  - 用途：`方法动机`
  - 页码：`p.2`
- 句子/事实 3：模型在 `EBHI-Seg` 训练并在 `GlaS` 上 cross-dataset 测试，得到 `95.08 Dice / 90.92 IoU` 的主结果，并在外部数据上保持约 `80%` 量级泛化
  - 用途：`结果概括`
  - 页码：`Abstract, p.1; p.8-p.10`

#### 1.1.2 related work 可引用句

- 句子/事实 1：MAC-Net 明确把 spatial、channel-level 与 contextual representation 同时融合，而不是只做单一路 attention 或 context branch
  - 用途：`方法差异化`
  - 页码：`p.2-p.3`
- 句子/事实 2：论文额外报告 `Grad-CAM` 与 `Monte Carlo Dropout`，说明其不仅追求分割分数，也强调可解释性与可靠性
  - 用途：`补充 discussion`
  - 页码：`p.3; p.6; p.12`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| input size | `256 x 256 x 3` | 训练设置 | `p.7` |
| batch size | `10` | 训练设置 | `p.7` |
| epochs | `100` | 训练设置 | `p.7` |
| optimizer | `Adam` | 训练设置 | `p.7` |
| EBHI-Seg split | `4:4:2` | train/val/test | `p.7` |
| train/val/test counts | `890 / 890 / 446` | EBHI-Seg 划分 | `p.7` |
| overall Dice / IoU | `95.08 / 90.92` | 主结果 | `p.8-p.9` |
| GlaS external Dice / IoU | `81.0 / 70.1` | cross-dataset | `p.9-p.10` |
| trainable parameters | `2.48M` | 轻量性 | `p.12` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 结直肠腺体病理图像中的 gland 具有：
  - 尺度变化
  - 边界不规则
  - 染色差异
  - 不同分化阶段的结构异质性
- 普通 encoder-decoder 尤其是简单 skip fusion 难以同时兼顾局部细节和全局上下文
- 需要一个既能保留 fine structural information、又能增强 context reasoning 和 boundary delineation 的轻量系统

对应原文依据（页码）：

- `Abstract, p.1`
- `p.2-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `MAC-Net`。该模型使用 4 级 encoder-decoder 主干，在 encoder 与 skip connection 上引入 channel attention，对特征进行动态重标定；在 bottleneck 处加入 multi-scale context aggregation，通过不同 pooling 粒度的上下文聚合增强全局结构建模；decoder 逐级融合 attention-refined encoder features 与上采样 decoder features；训练时采用 `Dice + Focal + Edge` 混合损失，以同时提升区域重叠、类别不平衡鲁棒性和边界清晰度。论文还额外引入 `Grad-CAM` 与 `MC Dropout` 来分析模型解释性和不确定性。

关键页码：

- `p.3-p.6`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`U-Net-like encoder-decoder with attention + context fusion`
- encoder：
  - 4 个 convolutional blocks
  - filters 依次为 `32, 64, 128, 256`
- bottleneck：
  - `multi-scale context aggregation`
- decoder：
  - 逐级上采样
  - 与 attention-refined encoder features 通过 lateral skip connection 融合
- output：
  - `1x1 conv + sigmoid` 得到二分类 gland mask

### 3.2 关键模块详细描述

**模块 1：`Hierarchical Feature Extraction`**

- 位置：`encoder`
- 操作流程：
  1. 每层由两层 `3x3 conv + ReLU`
  2. 后接 `Dropout`
  3. 前三层使用 `MaxPooling2D`
- 特点：
  - 从 `32` 通道逐步扩展到 `256`
  - 最深层不再池化，保留更高语义同时尽量保留细粒度信息
- 页码：`p.3-p.4`

**模块 2：`Multi-scale Context Aggregation`**

- 位置：`bottleneck`
- 操作流程：
  1. 对 deepest encoder feature 做 `2x2`、`4x4` 平均池化
  2. 经 `1x1 conv` 做维度压缩
  3. 双线性插值上采样回原尺寸
  4. 与原特征拼接
- 作用：
  - 强化 variable-sized tissue regions 的全局上下文建模
  - 提高对 overlapping glands 和 ill-defined margins 的鲁棒性
- 页码：`p.4`

**模块 3：`Decoder with Multi-scale Attention Fusion`**

- 位置：`decoder`
- 操作流程：
  1. 上采样粗尺度 decoder 输出
  2. 将对应 encoder 特征先经 channel attention 重加权
  3. 与上采样 decoder feature 拼接
  4. 再经卷积精炼
- 页码：`p.4-p.5`

**模块 4：`Channel Attention`**

- 位置：`encoder block 后和 skip connection 前`
- 操作流程：
  1. 先对每个通道做 global average pooling
  2. 两层全连接生成 channel weights
  3. 用 sigmoid 权重对原特征逐通道重标定
- 页码：`p.4-p.5`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| input | `256 x 256 x 3` | 模型输入 | `p.7` |
| conv kernel | `3x3` | encoder/decoder 主卷积 | `p.3-p.4` |
| encoder filters | `32, 64, 128, 256` | 分层特征提取 | `p.3` |
| pooling scales | `2x2, 4x4` | context aggregation | `p.4` |
| output head | `1x1 conv + sigmoid` | binary gland mask | `p.5` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：encoder block 输出

```text
F(l) = δ( D(W(l) * F(l-1) + b(l)) )
```

符号说明：

- `F(l-1)`：上一层输入特征
- `W(l), b(l)`：卷积核权重和偏置
- `D`：dropout
- `δ`：ReLU
- 页码：`Eq.(1), p.3-p.4`

公式 2：multi-scale context aggregation

```text
Fagg = Concat(
  F,
  Upsample(Conv1x1(AvgPool2x2(F))),
  Upsample(Conv1x1(AvgPool4x4(F)))
)
```

符号说明：

- `F`：最深层 encoder feature
- `Fagg`：融合多尺度上下文后的特征
- 页码：`Eq.(2), p.4`

公式 3：decoder 特征融合

```text
Dfi = Conv2D( Concat( Up(Dfi+1), A(Efi) ) )
```

符号说明：

- `Dfi+1`：更粗尺度 decoder 输出
- `Efi`：同尺度 encoder 特征
- `A(.)`：channel attention
- 页码：`Eq.(3), p.4`

公式 4：channel attention

```text
gc = (1 / HW) Σ_i Σ_j F(i,j,c)
e = σ( W2 · δ(W1 · g) )
F~(i,j,c) = ec · F(i,j,c)
```

符号说明：

- `g`：通道描述向量
- `e`：学习到的 channel weights
- `F~`：重加权后的特征
- 页码：`Eq.(4)-(6), p.4-p.5`

公式 5：输出与阈值化

```text
S = Conv1x1(Fdec)
Y^(i,j) = σ(S(i,j))
Yij = 1 if Y^(i,j) >= 0.5 else 0
```

符号说明：

- `Fdec`：最终 decoder feature
- `Y^`：像素级 gland 概率
- `Y`：二值分割结果
- 页码：`Eq.(7)-(9), p.5`

公式 6：混合损失

```text
LDice = 1 - (2 Σ Yi Y^i + ε) / (Σ Yi + Σ Y^i + ε)

LFocal = -(1/N) Σ [ α(1-Y^i)^γ Yi log(Y^i)
                  + (1-α)(Y^i)^γ (1-Yi) log(1-Y^i) ]

LEdge = (1/N) Σ || EYi - EY^i ||

LHybrid = α LDice + β LFocal + γ LEdge
```

符号说明：

- `LDice`：处理 overlap 和 class imbalance
- `LFocal`：强调 hard pixels，尤其是边界和不确定区域
- `LEdge`：通过 Sobel 边缘一致性强化 boundary delineation
- 论文设置 `α = β = γ = 0.3`
- 页码：`Eq.(10)-(13), p.5`

### 4.2 推导过程或梯度行为

- 论文对损失项的直觉解释：
  - `Dice` 强化整体重叠
  - `Focal` 聚焦难分类像素
  - `Edge` 强化边界清晰度
- 模型结构上的职责分工：
  - hierarchical encoder 保留多层次局部结构
  - context aggregation 补充 global context
  - attention skip fusion 在解码时抑制噪声、突出 gland-relevant channels
- 页码：`p.3-p.6`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `Dice loss` | `Eq.(10)` | 区域重叠与类别不平衡 | segmentation output |
| `Focal loss` | `Eq.(11)` | 聚焦 hard pixels / boundary pixels | segmentation output |
| `Edge loss` | `Eq.(12)` | 对齐预测边界与 GT 边界 | segmentation output |

### 5.2 总损失公式

```text
LHybrid = α LDice + β LFocal + γ LEdge
```

说明：

- 论文显式给出 `Dice + Focal + Edge` 的三项混合目标
- 该设计直接服务于小结构、类不平衡和边界质量

### 5.3 权重配置与调度策略

- `α = 0.3`
- `β = 0.3`
- `γ = 0.3`
- 剩余 `0.1` 留作 regularization / minor adjustments
- 页码：`p.5`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `EBHI-Seg` | `890 train` | `446 test` | `890 val` | `4:4:2` stratified split |
| `GlaS` | `165` | `external test` | `cross-dataset` | 外部泛化验证 |
| `PanNuke` | `zero-shot external` | `test` | `附加外部泛化` | 非结直肠器官 |
| `Amgad breast gland` | `zero-shot external` | `test` | `附加外部泛化` | 乳腺腺体 |

### 6.2 数据增强

- `random rotation` up to `10°`
- `width/height shift` up to `5%`
- `shear` up to `5%`
- `zoom` within `5%`
- `random horizontal flip`
- `nearest-fill mode`
- 页码：`p.7`

### 6.3 优化器与超参数

- 框架：`TensorFlow 2.12.0`
- 训练环境：`Google Colab + Tesla T4 16GB`
- optimizer：`Adam`
- batch size：`10`
- epochs：`100`
- input size：`256 x 256 x 3`
- 归一化：`min-max scaling to [0,1]`
- early stopping：
  - `patience = 10`
- reduce LR on plateau：
  - `factor = 0.1`
  - `patience = 5`
  - `min lr = 1e-4`
- 页码：`p.7`

### 6.4 预处理与数据细节

- 固定随机种子，保证 augmentation 一致性
- EBHI-Seg 使用 benchmark 约定切分，保证可复现比较
- cross-dataset generalization 直接用 EBHI-Seg 训练权重推理 GlaS，不额外 fine-tune
- 页码：`p.7-p.10`

---

## 7. 推理与后处理

- 推理输出为 probability map，再以 `0.5` 阈值二值化
- 额外 reliability 分析：
  - `Grad-CAM` 显示决策关注区域
  - `MC Dropout` 在推理阶段保持启用，做 `T=10` 次随机前向
- `MC Dropout` 的像素方差用于构建 uncertainty map
- 页码：`p.5-p.6; p.12`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | baseline U-Net | `92.25 Dice` | 基线 |
| `A2` | `+H` | `92.43 Dice` | hierarchical extraction 有益 |
| `A3` | `+A` | `92.69 Dice` | attention refinement 有益 |
| `A4` | `+M` | `92.62 Dice` | multi-scale context 有益 |
| `A5` | `+H+A+M = MAC-Net` | `95.08 Dice` | 三者组合最强 |

### 8.2 各模块贡献量化

- `Baseline`: Dice `92.25`, IoU `87.57`
- `Baseline + H`: Dice `92.43`, IoU `87.89`
- `Baseline + A`: Dice `92.69`, IoU `87.27`
- `Baseline + M`: Dice `92.62`, IoU `88.18`
- `Baseline + H + A`: Dice `92.72`, IoU `88.30`
- `Baseline + H + M`: Dice `92.56`, IoU `88.05`
- `Baseline + A + M`: Dice `92.78`, IoU `88.41`
- `MAC-Net`: Dice `95.08`, IoU `90.92`, Precision `95.83`, Recall `94.65`
- 页码：`Table 5, p.12-p.13`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `EBHI-Seg` | `Dice 95.08` | `IoU 90.92` | `Precision 95.83 / Recall 94.65` | overall |
| `GlaS` | `Accuracy 80.1` | `Dice 81.0` | `IoU 70.1` | zero-shot external test |
| `PanNuke` | `Accuracy 59.80` | `Dice 34.46` | `IoU 22.48` | organ/domain shift |
| `Amgad breast gland` | `Accuracy 60.79` | `Dice 20.55` | `IoU 12.73` | larger domain mismatch |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `U-Net` | `EBHI-Seg` | 较低 Dice/IoU | baseline | 对照 |
| `MedT` | `EBHI-Seg` | baseline-level | 复杂区域更弱 | 对照 |
| `DMoC-UNet` | `EBHI-Seg` | 强基线 | 仍弱于 MAC-Net | 近期对照 |
| `MAC-Net` | `EBHI-Seg` | best Dice / IoU | strongest fair-split result | 本文 |

### 9.3 公平对比条件确认

- Table 2 只比较同样 `4:4:2` 划分下训练测试的方法
- Table 3 额外文献对比仅作补充趋势参考，不是严格公平对比
- cross-dataset 测试不做 fine-tune，直接用 EBHI-Seg 训练权重推理 GlaS
- 页码：`p.8-p.10`

### 9.4 评价协议与指标定义

- `Dice Score`
- `IoU`
- `Precision`
- `Recall`
- `Conformity Coefficient`
- 论文给出了上述公式定义
- 页码：`Eq.(18)-(22), p.7-p.8`

---

## 10. 计算量与效率

- 模型参数量：`2.48M`
- 大小约：`9.46 MB`
- 定位：
  - 相比多数 attention-driven segmentation model 更轻量
  - 适合资源受限临床环境的部署讨论
- 代价：
  - 虽然参数量小，但完整系统包含 attention、context aggregation、解释性与不确定性分析
- 页码：`p.12`

---

## 13. 开源与复现

- 代码是否开源：`文中未明确提供公开仓库`
- 代码仓库地址：`[待确认]`
- 框架/语言：`TensorFlow 2.12.0`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：
  - 论文来自较新期刊文章，可能无完整公开代码
  - Edge loss、attention skip fusion、uncertainty inference 需自行组合实现

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 学习率初始值 | `未清楚写出` | `需后续复现时搜索补充` | `中` |
| dropout 具体位置和比例完整表 | `部分明确` | `按文中描述重建` | `中` |
| 完整代码 | `未确认` | `需自行实现` | `中-高` |
| EBHI-Seg benchmark 切分脚本 | `未提供` | `按 4:4:2 复现` | `中` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 实验主要依赖两个 colorectal datasets
- 模型在跨器官/跨任务数据上的 zero-shot 表现明显下降
- domain shift 仍然是病理 AI 系统的重要障碍

### 14.2 我们观察到的潜在问题

- 这篇的主结果高度依赖 `EBHI-Seg`，与 `GlaS/CRAG` 主线对接价值存在数据域差异
- 虽然用了 hybrid loss 与 context fusion，但 external GlaS 结果明显低于内部测试，说明泛化仍有限
- 其 attention/context decoder 结构较重，更适合作为 related work 或上界参照，而不一定适合作为你当前的主线高性价比方案

### 14.3 失败案例 / 定性分析

- 论文指出最差案例通常发生在：
  - 复杂 stroma
  - gland boundaries 模糊
  - domain shift 明显的外部数据
- error map 显示大部分误差仍集中在不规则 gland 边界
- `MC Dropout` 结果表明高不确定性区域常与复杂边界和 stromal ambiguity 一致
- 页码：`p.8-p.13`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `attention + multi-scale context + edge-aware loss` 的近期腺体分割路线
- `Grad-CAM + uncertainty` 作为结果可信度补充分析
- cross-dataset generalization 作为评价模型稳健性的补充方式

### 15.2 可以作为候选参数来源的

- `input = 256 x 256`
- `batch size = 10`
- `epochs = 100`
- `Adam`
- `Dice + Focal + Edge`

### 15.3 不应照搬的（及原因）

- 直接照搬整个 `MAC-Net` 作为你当前主线模型：
  - 原因：结构较重，且其核心亮点偏近期模块堆叠而非高性价比主干
- 直接把 EBHI-Seg 上的高分数视为对 GlaS/CRAG 的同等保证：
  - 原因：外部 GIaS 测试已表明 domain shift 会明显拉低结果

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 近期相关工作补强 | 直接腺体分割近期方法 | `强` |
| attention/context fusion | 多尺度上下文与通道注意力路线 | `中-强` |
| 边界强化 | `Edge loss` 直接支持 boundary delineation | `中` |
| 泛化与可靠性分析 | cross-dataset + uncertainty | `中` |
| 主线 backbone 选择 | 更像对照路线，不是最强直接支撑 | `中-弱` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`近期 related work`、`可解释性与不确定性分析备选`
- [ ] 需要和哪篇论文交叉验证：`MILD-Net`、`Attention_U-Net`、`Boundary-DoU-Loss`
- [ ] 待确认的问题：`是否需要在你自己的实验里补一个轻量 edge-aware hybrid loss 对照`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 近期 CRC gland segmentation 仍依赖 attention/context fusion | 作为领域现状 |
| related work | MAC-Net 路线 | 放在 recent gland segmentation 小节 |
| 方法讨论 | hybrid loss + context fusion 的优缺点 | 用于对照我们不走重 decoder 的理由 |
| 实验分析 | cross-dataset + uncertainty | 作为泛化/可靠性分析参考 |
| 讨论 | 边界复杂区域仍是错误集中点 | 与我们的边界方法衔接 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1-2` | `p.1, p.3-p.4` | MAC-Net 概览与结构图 | 回填方法 |
| `Eq.(1)-(9)` | `p.3-p.5` | encoder/context/attention/output 公式 | 回填公式 |
| `Eq.(10)-(15)` | `p.5-p.6` | hybrid loss、Grad-CAM、uncertainty | 回填损失与解释性 |
| `Eq.(18)-(22)` | `p.7-p.8` | 指标定义 | 指标说明 |
| `Table 1-3` | `p.8-p.10` | 主结果与文献对比 | 数字引用 |
| `Table 4` | `p.12` | uncertainty summary | 可靠性引用 |
| `Table 5` | `p.12-p.13` | ablation study | 模块贡献 |
| `Figure 8-10` | `p.12-p.13` | Grad-CAM / ablation visuals | 解释性与定性分析 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] MAC-Net 架构和混合损失公式已覆盖
- [x] 训练设置与数据切分已记录
- [x] cross-dataset 与 uncertainty 分析已单独记录
- [x] 消融实验已补齐
- [x] 与我们项目的关联已具体到模块级别
- [x] 不确定内容已标注 `[待确认]`

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/04_腺体与病理近期相关工作/01_MAC-Net`
- `paper_type`: `planned_category:04_腺体与病理近期相关工作`
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

- 记录字段：`paper_id=03_文献证据/04_腺体与病理近期相关工作/01_MAC-Net`；`paper_type=planned_category:04_腺体与病理近期相关工作`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/04_腺体与病理近期相关工作/01_MAC-Net` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
