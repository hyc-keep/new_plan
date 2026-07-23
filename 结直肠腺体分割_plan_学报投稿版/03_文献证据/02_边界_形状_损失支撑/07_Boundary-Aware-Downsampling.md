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

- `boundary-driven adaptive downsampling`
- `efficient segmentation support module`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`02_边界_形状_损失支撑`

- 虽然本篇更偏高效分割结构策略，但其动机和收益直接围绕 semantic boundaries 与 small objects，所以保留在本文件夹
- 本篇至少完成：`1, 2, 3, 4, 6, 8, 9, 10, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`Efficient Segmentation: Learning Downsampling Near Semantic Boundaries`
- 作者/团队：`Dmitrii Marin, Zijian He, Peter Vajda, Priyam Chatterjee, Sam Tsai, Fei Yang, Yuri Boykov`
- 发表年份/会议/期刊：`2019, arXiv preprint / efficient semantic segmentation`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:1907.07156`
- BibTeX key：`marin2019efficient`
- PDF 路径：`结直肠腺体分割_pdf库/02_边界_形状_损失支撑/Efficient_Segmentation_Learning_Downsampling_Near_Semantic_Boundaries_2019.pdf`
- 当前定位：`边界驱动的高效下采样策略来源论文；核心不是新 loss，而是让下采样在 semantic boundaries 附近保留更多采样点，从而在有限计算预算下同时改善 boundary precision 与 small-object support`
- 与已提取论文的关系：
  - 与 `Boundary-DoU-Loss_2023`、`Boundary-Loss_2019` 互补：它不是直接改 loss，而是从输入采样阶段提升边界质量
  - 与 `FPN_2017` 的多尺度思想互补：前者是多尺度特征融合，这篇是前端采样密度重分配
  - 可为腺体任务里“边界附近保留更高分辨率信息”提供结构动机

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：为了提速，语义分割常对输入做 downsampling，但这会带来 missed small objects 与 reduced accuracy at semantic boundaries 的代价
  - 用途：`背景 / 痛点`
  - 页码：`Abstract, p.1; Intro, p.1`
- 句子/事实 2：uniform downsampling 是 sub-optimal，更合理的做法是让更多采样点分布在 semantic boundaries 附近
  - 用途：`方法动机`
  - 页码：`Intro, p.1-p.2`
- 句子/事实 3：boundary-aware non-uniform downsampling 带来两类好处：减少 boundary quantization error，并隐式平衡 scale variation，对小目标更友好
  - 用途：`核心贡献概括`
  - 页码：`Intro, p.1-p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者不是用 image edges 决定采样位置，而是通过 semantic boundaries 学习 sampling locations
  - 用途：`与传统基于边缘的采样方法区分`
  - 页码：`Sec.2, p.2-p.3`
- 句子/事实 2：方法可作为任意现有 segmentation model 的前后处理模块接入，不限制 base segmentation model
  - 用途：`模块可插拔性`
  - 页码：`Sec.3, p.3-p.4`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 采样张量初始大小 | `(2, 8, 8)` | 辅助网络输出 | `p.5` |
| λ | `1` | boundary-driven sampling energy | `p.5` |
| auxiliary / segmentation optimizer | `Adam` | 实现细节 | `p.5` |
| ApolloScape lr / epochs | `1e-5 / 33` | sampler & segmentation 训练 | `p.5` |
| Supervisely lr / epochs | `1e-4 / 1000` | 训练设置 | `p.5` |
| Synthia lr / epochs | `1e-4 / 500` | 训练设置 | `p.5` |
| batch size vs resolution | `16-64:128, 128:32, 256:24, 512:12` | 训练设置 | `p.5` |
| 训练 crop | `largest square random crop` | 训练设置 | `p.5` |
| 测试 crop | `central largest square` | 测试设置 | `p.5` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 高效语义分割常需对输入图像做下采样，但 uniform downsampling 会损失边界定位精度
- 小目标在均匀采样后可能被完全错过
- 传统 uniform grid 对 boundary quantization error 不友好，且对大目标/小目标一视同仁
- 需要一种在相同计算预算下，自动把更多采样密度分配到 semantic boundaries 附近的策略

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `boundary-driven adaptive downsampling`。先从 GT semantic labels 计算 boundary map，再利用距离变换为每个位置找到最近 boundary 点，定义一个采样张量 `φ` 的优化能量：既要求采样点靠近 semantic boundaries，又要求采样网格不要过度扭曲。然后训练一个轻量 auxiliary network 预测该 sampling tensor，使用它对原图做 non-uniform downsampling；再将任意现有 segmentation model 应用于该下采样图，最后通过 non-uniform upsampling 把稀疏分类结果恢复到原分辨率。

关键页码：

- `Sec.3, p.3-p.4`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`adaptive downsampling block + arbitrary segmentation model + non-uniform upsampling`
- Backbone：
  - segmentation 部分可接 `U-Net / PSP-Net / DeepLabv3+` 等任意模型
  - sampling 部分使用 `double U-Net auxiliary network`
- 输入尺寸：`高分辨率原图`
- 输出头：
  - `sampling tensor`
  - `downsampled image`
  - `upsampled full-resolution segmentation`

### 3.2 关键模块详细描述

**模块 1：`Boundary-Driven Sampling Tensor`**

- 位置：`前端非均匀下采样模块`
- 操作流程：
  1. 从 GT labels 生成 boundary map
  2. 对每个均匀网格点 `uij` 找到最近 boundary 点 `b(uij)`
  3. 通过能量函数求解 sampling tensor `φ`
  4. 用 `φ` 在原图上采样形成下采样图
- 页码：`Sec.3.1, p.3-p.4`

**模块 2：`Auxiliary Sampling Network`**

- 位置：`学习预测 sampling tensor`
- 操作流程：
  1. 输入原始图像
  2. 通过 stacked double U-Net 预测 sampling tensor
  3. 用 L2 loss 拟合由优化问题生成的 proposal tensor `φ̃`
- 页码：`Sec.3.1, p.3-p.4; Fig.6`

**模块 3：`Segmentation Model`**

- 位置：`中间主分割网络`
- 操作流程：
  1. 处理 non-uniformly downsampled image
  2. 生成低分辨率稀疏分类结果
  3. 不对主 segmentation model 做额外结构限制
- 页码：`Sec.3.2, p.4`

**模块 4：`Non-uniform Upsampling`**

- 位置：`后端恢复原分辨率`
- 操作流程：
  1. 将低分辨率分类结果视作原图坐标系中的 sparse classifications
  2. 利用网格拓扑保持性质做高效插值
  3. 输出 full-resolution segmentation
- 页码：`Sec.3.3, p.4-p.5`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| sampling tensor | `(2, h, w)` | 非均匀采样位置 | `p.3` |
| initial predicted tensor size | `(2, 8, 8)` | auxiliary net 输出 | `p.5` |
| auxiliary network | `stacked double U-Net` | 预测 sampling tensor | `p.4-p.5` |
| per-block channels | `256 except first/last` | 提高效率 | `Fig.6, p.5` |
| segmentation model | `U-Net / PSP-Net / DeepLabv3+` | 主分割网络 | `p.4-p.6` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
Jij := I[φij^0, φij^1]
```

符号说明：

- `I`：原始图像
- `φ`：sampling tensor
- `J`：非均匀下采样后的图像
- 含义：用 sampling tensor 在原图上采样
- 页码：`Eq.(1), p.3`

公式 2：

```text
E(φ) = Σi,j ||φij - b(uij)||^2
     + λ Σ|i-i'|+|j-j'|=1 ||φij - φi'j'||^2
```

符号说明：

- `uij`：均匀网格位置
- `b(uij)`：离 `uij` 最近的 semantic boundary 点
- 第一项：把采样点拉向 boundary
- 第二项：约束相邻采样点的空间平滑，避免网格过度扭曲
- `λ`：控制 boundary attraction 与 grid regularity 的平衡
- 页码：`Eq.(2), p.3-p.4`

公式 3：

```text
φ ∈ [0,1]^(2×h×w)
φ1j^0 = 0, φhj^0 = 1
φi1^1 = 0, φiw^1 = 1
```

符号说明：

- 这些 covering constraints 保证采样位置覆盖整幅图像
- 页码：`Eq.(3), p.3-p.4`

### 4.2 推导过程或梯度行为

- 直觉推导：
  - uniform sampling 下 boundary localization error 约为 `O(D / √N)`
  - 若采样点均匀分布在 boundary 附近，误差界下降更快，可达 `O(κ l^2 / N^2)` 级别
- 机制意义：
  - 边界附近更多采样点减少 boundary quantization error
  - 大区域在下采样图中的占比被压缩，小目标可见采样点增加，形成 implicit scale equalization
- 实践取舍：
  - `λ = 0` 时极度贴边界
  - `λ -> +∞` 时退化为均匀采样
  - 中间 `λ` 产生更实用的折中
- 页码：
  - `Intro, p.1-p.2`
  - `Sec.3.1, p.3-p.4`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `sampling tensor regression` | `L2(φ_pred, φ̃)` | 让 auxiliary net 学会预测 boundary-aware sampling tensor | auxiliary network |
| `softmax-entropy loss` | `[标准 CE]` | 监督 segmentation network | segmentation output |

### 5.2 总损失公式

```text
L_total = L2_sampling + CE_segmentation
```

说明：

- 论文不是提出新的 segmentation loss
- 创新点在前端 non-uniform downsampling 和后端对应 upsampling

### 5.3 权重配置与调度策略

- `λ = 1` 用于生成 sampling proposal
- auxiliary net 用 squared `L2 loss`
- segmentation network 用 `softmax-entropy loss`
- 页码：`p.3-p.5`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `ApolloScape` | `~105K` | `8K val` | `validation set` | 22 classes, 3384×2710 |
| `CityScapes` | `[待确认原始划分]` | `val` | `validation set` | 用于 PSP-Net / DeepLabv3+ |
| `Synthia` | `13K HD images` | `[待确认]` | `官方划分/实验划分` | synthetic city scenes |
| `Supervisely Person` | `5140` | `571` | `随机划分` | person vs background |

### 6.2 数据增强

- 增强列表：
  - `random left-right flipping`
  - `adjusting contrast`
  - `brightness`
  - `salt-and-pepper noise`
- Patch 提取策略：
  - 训练时随机裁剪最大正方形
  - 测试时取 central largest square
- 页码：`p.5-p.6`

### 6.3 优化器与超参数

- 框架：`Caffe2`
- 优化器：`Adam`
- 初始学习率 / epochs：
  - `ApolloScape: 1e-5 / 33`
  - `Supervisely: 1e-4 / 1000`
  - `Synthia: 1e-4 / 500`
- 学习率调度：`exponential policy`
- Batch size：
  - input resolution `16/32/64 -> 128`
  - `128 -> 32`
  - `256 -> 24`
  - `512 -> 12`
- 权重初始化：`PSP-Net / DeepLabv3+` 用公开实现默认参数
- 预训练策略：`沿用 public implementations 默认设置`
- 是否冻结部分层：`未强调`
- 设备：`[待确认]`
- 页码：`p.5`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；自然图像`
- 颜色空间转换：`未强调`
- resize / crop / pad 策略：
  - 辅助网络先预测 `(2,8,8)` sampling tensor，再 resize 到目标 downsampling resolution
- patch overlap：`不适用`
- 背景过滤策略：`不适用`
- 标签生成方式：
  - 从 GT semantic labels 计算 semantic boundary map
  - 再基于最近 boundary 点与能量优化得到 proposal sampling tensor
- 类别不平衡处理：
  - 通过对 target classes 的 boundary 附近增加采样点来隐式平衡小目标
- 随机种子/重复次数：`未明确`
- 数据泄漏风险点：`需遵循各 benchmark 官方 split`
- 页码：`p.3-p.6`

---

## 7. 推理与后处理

- 推理流程：
  1. auxiliary net 预测 sampling tensor
  2. 非均匀下采样图像
  3. segmentation model 预测低分辨率分类
  4. non-uniform upsampling 恢复到原分辨率
- 关键点：
  - adaptive downsampling 保持 grid topology，因此 upsampling 可跳过复杂 triangulation
  - 训练 segmentation network 时不包含 upsampling stage，而是直接下采样 label map
- 页码：`p.4-p.5`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | uniform downsampling vs adaptive downsampling | 各 backbone、各数据集一致提升 | 非均匀采样优于均匀采样 |
| `A2` | 不同 downsampling resolutions | 固定 FLOPs 下 proposed 更优 | 同等成本下更高质量 |
| `A3` | all classes vs target classes | target classes 收益更大 | 小目标和边界类受益最明显 |
| `A4` | object size bins | smaller objects 上提升更大 | 证实 implicit scale equalization |
| `A5` | trimap boundary evaluation | boundary 附近提升最明显 | 证明改进确实来自 boundary precision |

### 8.2 各模块贡献量化

- ApolloScape：
  - 对 target classes 的 `mIoU` 提升约 `3% - 5%`
  - overall `mIoU` 提升最高约 `2%`
- CityScapes：
  - PSP-Net / DeepLabv3+ 在相同 FLOPs 下均优于 uniform baseline
  - 整体提升可达 `up to 4%`
- Synthia：
  - target classes 提升约 `1.5% - 3%`
- Supervisely Person：
  - absolute `mIoU` 提升最高 `5.8%`
- 页码：`p.5-p.7`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `ApolloScape` | `overall mIoU up to +2%` | `target classes +3%~5%` | `same cost better quality` | boundary-aware sampling |
| `CityScapes` | `up to +4%` | `same computational cost` | `better boundary precision` | PSP-Net / DeepLabv3+ |
| `Synthia` | `target classes +1.5%~3%` | `all classes tie or improve` | `negligible cost` | U-Net backbone |
| `Supervisely` | `absolute mIoU +5.8%` | `better person segmentation` | `same budget` | person vs background |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `uniform baseline` | `ApolloScape` | `lower mIoU` | `target classes worse` | `same FLOPs` |
| `adaptive downsampling` | `ApolloScape` | `higher mIoU` | `target classes +3~5%` | `same FLOPs` |
| `uniform PSP-Net/DeepLabv3+` | `CityScapes` | `lower mIoU` | `same cost` | `worse boundaries` |
| `adaptive PSP-Net/DeepLabv3+` | `CityScapes` | `better mIoU` | `up to +4%` | `better boundary precision` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`是，同一 backbone 仅替换 uniform/adaptive downsampling`
- 是否统一数据增强：`是，共享同一训练流程`
- 是否统一后处理：`是，共享同一插值/输出框架`
- 是否统一输入尺寸：`是，在相同 downsampling resolution 和 FLOPs 下比较`
- 结果来源：`原文 cost-performance curves 与表格`
- 页码：`p.5-p.7`

### 9.4 评价协议与指标定义

- 主要指标：`mIoU`
- 额外分析：
  - target classes IoU
  - trimap boundary accuracy
  - object-wise recall 按大小分箱
- 结果汇报层级：`validation / held-out test，按数据集设置`
- 是否含后处理后再报结果：`包含统一 non-uniform upsampling`
- 是否多 seed 平均：`未说明`
- 页码：`p.5-p.7`

---

## 10. 计算量与效率

- 论文核心卖点之一：
  - 在固定计算预算下优于 uniform baseline
  - computational overhead negligible / small
- 结构定位：
  - 介于单阶段 segmentation 与两阶段 object-centric approaches 之间
  - 目标是在不显著增加成本的前提下提升 boundary precision 和 small-object support
- 对我们项目的意义：
  - 边界相关提升不一定只能靠 loss；采样策略本身也能改变精度-成本平衡
- 页码：`Abstract, p.1`
- `Sec.4.2, p.5-p.7`

---

## 13. 开源与复现

- 代码是否开源：`[待确认]`
- 代码仓库地址：`[待确认]`
- 框架/语言：`Caffe2`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中-高`
- 复现障碍：
  - non-uniform sampling + non-uniform upsampling 需要完整复现前后端流程
  - auxiliary net 与 segmentation net 需分阶段训练
  - 各 benchmark 数据预处理和 resolution/FLOPs 对齐要求较细

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `后续复现需固定` | `中` |
| 验证集划分 | `部分明确` | `遵循 benchmark 官方 split 或文中拆分` | `中` |
| 推理阈值 | `不适用` | `分割网络默认 argmax` | `低` |
| 后处理细节 | `部分明确` | `保留 non-uniform upsampling` | `高` |
| 训练轮数停止准则 | `是` | `各数据集 epochs 已给出` | `低` |
| 数据预处理 | `部分明确` | `largest-square crop + augmentations` | `中` |

- 不确定但影响较大的点：
  - auxiliary network 的完整深度配置和分辨率适配细节需要结合图和实现
  - target classes 的具体定义在不同数据集下需要回实现确认

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 该方法针对高分辨率 segmentation 的边界/小目标问题，非常依赖 adaptive sampling tensor 学得合理
- 更适合作为效率-精度折中模块，而不是单独替代 segmentation backbone

### 14.2 我们观察到的潜在问题

- 这篇主要基于自然场景语义分割，边界统计与腺体病理图像不同
- 对病理 patch 来说，semantic boundaries 不一定像道路/器官那样有稳定尺度结构
- 系统复杂度高于单纯替换一个 loss；若你的目标不是推理效率，而是离线高精度，收益可能不如直接提分辨率或改 backbone/loss

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`通过 trimap 和 object-size 分析展示 uniform baseline 的问题`
- 典型失败场景：
  - uniform downsampling 更容易漏掉 smaller objects
  - boundary 附近出现更明显的 localization errors
- 对我们任务的映射：
  - 若腺体边界细而复杂，训练时保留边界附近更多像素可能有意义
  - 但若图像本身已是 patch 级高分辨率，额外的 non-uniform sampler 未必划算
- 页码：`p.6-p.7`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- “边界附近采样更密、内部采样可更稀” 的设计理念
- 把 boundary-aware 思路放到输入/采样阶段，而不仅是 loss 阶段
- 用 trimap boundary accuracy 和 small-object recall 来分析方法收益来源

### 15.2 可以作为候选参数来源的

- `λ = 1`
- sampling tensor 先从 `(2,8,8)` 预测再 resize
- `largest-square crop`
- `Adam + exponential lr`

### 15.3 不应照搬的（及原因）

- 直接整套移植到腺体分割训练流程：
  - 原因：工程复杂度高，且你当前任务更偏离线高精度而非移动端高效推理
- 直接照搬自然场景 target classes：
  - 原因：病理图像没有同样的类间尺度和几何先验

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界优先采样 | 理论与实验都支持边界附近保留更多像素 | `强` |
| 小目标保留 | adaptive downsampling 对小目标 recall 更友好 | `强` |
| 高效分割设计 | 在固定 FLOPs 下提高 mIoU 的思路 | `中` |
| 腺体分割主模型 | 更像启发式结构策略，不是直接主模块 | `中` |
| 损失函数设计 | 不直接提供 loss 公式 | `弱` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`边界保留策略`、`高效推理备选方案`
- [ ] 需要和哪篇论文交叉验证：`Boundary-DoU-Loss_2023`、`FPN_2017`
- [ ] 待确认的问题：`腺体任务是否真的需要 non-uniform input sampling，而不是更高分辨率 patch`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | uniform downsampling 对边界和小目标有天然缺陷 | 作为边界保留动机 |
| related work | boundary-driven efficient segmentation 路线 | 放在高效分割/采样策略小节 |
| 方法 | boundary-aware sampling tensor 的概念 | 作为可选结构启发 |
| 实验设置 | trimap / object-size recall 分析框架 | 用于解释边界改进来源 |
| 讨论 | 提升边界不一定只能改 loss，采样策略同样重要 | 用于扩展讨论 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.1` | GT 边界与 adaptive sampling locations 示意 | 写方法动机 |
| `Figure 2` | `p.2-p.3` | 完整高效分割框架 | 回填系统结构 |
| `Eq.(2)` | `p.3-p.4` | sampling tensor 能量函数 | 回填核心公式 |
| `Figure 3` | `p.3-p.4` | 不同 λ 下的采样效果 | 解释超参数作用 |
| `Figure 6` | `p.5` | double U-Net auxiliary network | 回填模块设计 |
| `Table 2-5` | `p.6-p.7` | ApolloScape / CityScapes / Synthia / Supervisely 结果 | 数字引用 |
| `Figure 12-14` | `p.7` | boundary trimap 和 object-size recall 分析 | 解释为何对小目标与边界更好 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] 公式符号都有解释
- [x] 训练参数已覆盖 optimizer、lr、epochs、batch、crop、augment
- [x] adaptive sampling / upsampling 逻辑已记录
- [x] 主结果与关键趋势已核对
- [x] 指标定义和评价协议已确认（mIoU / target IoU / trimap / recall）
- [x] 边界与小目标收益已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/02_边界_形状_损失支撑/07_Boundary-Aware-Downsampling`
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

- 记录字段：`paper_id=03_文献证据/02_边界_形状_损失支撑/07_Boundary-Aware-Downsampling`；`paper_type=planned_category:02_边界_形状_损失支撑`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/02_边界_形状_损失支撑/07_Boundary-Aware-Downsampling` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
