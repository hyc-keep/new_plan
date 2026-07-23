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
- [x] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `F - 数据集/竞赛结果引用论文`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`01_经典基线与对比方法`

- 按模板要求，本篇至少完成：`1, 3, 6, 7, 9, 10, 13, 15, 16`
- 因为这篇是整个后续路线的根基基线，所以额外完成：`2, 4, 5, 8, 14`

---

## 1. 论文信息

- 论文名：`U-Net: Convolutional Networks for Biomedical Image Segmentation`
- 作者/团队：`Olaf Ronneberger, Philipp Fischer, Thomas Brox`
- 发表年份/会议/期刊：`2015, MICCAI 2015（论文同时有 arXiv 版本）`
- DOI / arXiv ID：`10.48550/arXiv.1505.04597` / `arXiv:1505.04597`
- BibTeX key：`ronneberger2015unet`
- PDF 路径：`结直肠腺体分割_pdf库/01_经典基线与对比方法/U-Net_2015.pdf`
- 当前定位：`整个医学分割 U 形编码器-解码器路线的标准起点，也是我们腺体分割首轮最小可复核基线的直接结构依据`
- 与已提取论文的关系：
  - 继承自：`FCN` 的 dense prediction 思路，但强化了定位与上下文结合
  - 被谁引用/改进：`UNet++`、`Attention U-Net`、`ResUNet`、`U-Net 3+`、`nnU-Net`、大量腺体分割方法
  - 互补论文：`GlaS Challenge_2017`、`MILD-Net_2018`、`UNet++_2018`、`Attention_U-Net_2018`

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：`生物医学任务通常拿不到成千上万张精标图像，因此网络必须在 very few training images 的条件下仍能训练成功`
  - 用途：`背景 / 痛点`
  - 页码：`p.1, p.3`
- 句子/事实 2：`U-Net 的关键不是只做 dense prediction，而是用 contracting path 获取 context、用 symmetric expanding path 做 precise localization`
  - 用途：`方法动机`
  - 页码：`p.1, p.3-p.4`
- 句子/事实 3：`强数据增强，尤其是 elastic deformation，是少样本医学分割训练成功的关键概念之一`
  - 用途：`实验设置动机`
  - 页码：`p.3, p.6`

#### 1.1.2 related work 可引用句

- 句子/事实 1：`U-Net 通过 skip connection 将 encoder 的高分辨率特征与 decoder 的上采样特征拼接，从而同时保留上下文和精确定位`
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.3-p.4`
- 句子/事实 2：`相比 sliding-window CNN，U-Net 避免了对每个 patch 单独前向计算造成的大量冗余`
  - 用途：`经典基线对比`
  - 页码：`p.2-p.3`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 输入 tile | `572×572 -> 388×388 输出` | 方法/实现说明 | `p.2, p.4` |
| Batch size | `1` | 实验设置 | `p.4` |
| Momentum | `0.99` | 实验设置 | `p.4` |
| 边界权重图参数 | `w0 = 10`, `sigma ≈ 5 pixels` | 边界监督设计 | `p.5` |
| 形变增强网格 | `3×3 coarse grid` | 数据增强 | `p.6` |
| 位移标准差 | `10 pixels` | 数据增强 | `p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 生物医学图像分割需要像素级定位，但可用标注数据通常很少，无法像自然图像分类那样依赖超大数据集
- 传统 sliding-window CNN 虽然能做像素分类，但推理很慢，而且 patch 越大越有上下文、越小越有定位精度，两者难兼顾
- FCN 虽然已经能做 dense prediction，但作者认为还需要更强的高分辨率定位信息回流，才能在少样本医学分割上得到更精细的边界
- 细胞/腺体这类 touching objects 的分离很难，仅做普通前景背景分类不够，需要专门强化分离边界

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 用一个对称的 `encoder-decoder` 结构替代 sliding-window 逐点分类：左侧 contracting path 逐步下采样提取上下文，右侧 expanding path 逐步上采样恢复分辨率，并把 encoder 对应层的高分辨率特征裁剪后拼接给 decoder；再结合 overlap-tile 推理和强 elastic deformation 增强，使网络在 very few training images 下也能稳定学到 precise localization。

关键页码：

- `p.1-p.4`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`encoder-decoder / symmetric U-shaped fully convolutional network`
- Backbone：`自定义 U-Net 主干`
- 输入尺寸：`示意架构用 572×572 输入，输出 388×388；最低分辨率示意为 32×32`
- 输出头：`1×1 convolution 输出每个像素的类别概率`

### 3.2 关键模块详细描述

**模块 1：`Contracting Path`**

- 位置：`网络左半部分`
- 操作流程：
  1. 每个 stage 执行两次 `3×3 unpadded convolution + ReLU`
  2. 然后执行 `2×2 max pooling, stride 2`
  3. 每下采样一次，通道数翻倍
- 页码：`p.4`

**模块 2：`Expansive Path`**

- 位置：`网络右半部分`
- 操作流程：
  1. 先对当前特征做上采样
  2. 再执行 `2×2 up-convolution`，把通道数减半
  3. 将其与 encoder 对应层裁剪后的特征图进行拼接
  4. 再执行两次 `3×3 convolution + ReLU`
- 页码：`p.4`

**模块 3：`Skip Connection + Cropping`**

- 位置：`每个 encoder-decoder 对应尺度之间`
- 操作流程：
  1. 从 encoder 复制高分辨率特征图
  2. 因为使用 unpadded convolution，特征图尺寸缩小，所以先 crop
  3. 再与 decoder 当前尺度特征进行 concatenation
- 页码：`p.2-p.4`

**模块 4：`Overlap-tile Strategy`**

- 位置：`推理阶段`
- 操作流程：
  1. 用较大的输入 tile 进行局部预测
  2. 只保留 valid convolution 对应的中心输出区域
  3. 对大图做重叠切块并拼接结果
  4. 图像边缘缺失上下文时使用 mirroring 外推
- 页码：`p.3-p.4`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| Input | image tile | `1` | `572×572` | 论文图示 |
| Encoder 1 | `conv 3×3 ×2` | `64` | `570×570 -> 568×568` | 后接 pooling |
| Encoder 2 | `conv 3×3 ×2` | `128` | `280×280 -> 278×278` | 图示中省略中间一步，实质为 valid conv 缩小 |
| Encoder 3 | `conv 3×3 ×2` | `256` | `136×136 -> 132×132` |  |
| Encoder 4 | `conv 3×3 ×2` | `512` | `64×64 -> 60×60` |  |
| Bottleneck | `conv 3×3 ×2` | `1024` | `28×28` 附近 | 图示最低层 |
| Decoder 4 | up-conv + concat + conv | `512` | `56×56 -> 52×52` | 与 encoder 4 crop 后拼接 |
| Decoder 3 | up-conv + concat + conv | `256` | `104×104 -> 100×100` |  |
| Decoder 2 | up-conv + concat + conv | `128` | `200×200 -> 196×196` |  |
| Decoder 1 | up-conv + concat + conv | `64` | `392×392 -> 388×388` |  |
| Output | `1×1 conv` | `2` | `388×388` | 图中示例为二分类 |

备注：

- 论文图给出了通道数和关键空间尺寸，足够作为 U-Net 原始结构的直接依据
- 腺体任务里若改成 `512×512` 输入，不再是论文图中的原始 valid-conv 尺寸链路，属于工程改写，不应冒充原文原值

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
E = \sum_{x \in \Omega} w(x) · log(p_{l(x)}(x))
```

符号说明：

- `x`：像素位置
- `Omega`：整张输出图的像素集合
- `l(x)`：像素 `x` 的真实类别
- `p_{l(x)}(x)`：像素 `x` 属于真实类别的 softmax 概率
- `w(x)`：像素权重图
- 说明：论文将其描述为 `pixel-wise softmax + cross entropy`，OCR 文本中可能缺少负号，但其含义是加权像素级交叉熵
- 页码：`p.4-p.5`

公式 2：

```text
w(x) = w_c(x) + w0 · exp(- (d1(x) + d2(x))^2 / (2 sigma^2))
```

符号说明：

- `w_c(x)`：类别频率平衡项
- `d1(x)`：像素 `x` 到最近细胞边界的距离
- `d2(x)`：像素 `x` 到第二近细胞边界的距离
- `w0`：边界强调强度
- `sigma`：边界衰减尺度
- 作用：给 touching objects 间的窄分离带更高权重
- 页码：`p.5`

公式 3：

```text
std = sqrt(2 / N)
```

符号说明：

- `std`：初始化高斯分布标准差
- `N`：当前神经元的输入连接数
- 作用：让不同路径的特征图初始方差接近单位方差，稳定深层训练
- 页码：`p.5`

### 4.2 推导过程或梯度行为

- 梯度特性：像素级加权交叉熵通过 `w(x)` 放大边界处和稀有类别像素的梯度，从而更强地推动网络学习相邻实例的分离带
- 适用条件：适合 touching objects 明显、实例分离困难的生物医学图像
- 不适用场景：如果任务主要是语义区域分割且不需要靠窄边界分离实例，原论文的 border-weighted CE 未必是最佳选择
- 页码：`p.5`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| pixel-wise softmax cross entropy | `见公式 1` | 像素分类 | 最终输出 |
| border-aware weight map | `见公式 2` | 强化 touching objects 间分离边界 | 作用于 loss 权重 |

### 5.2 总损失公式

```text
L_total = weighted pixel-wise softmax cross entropy
```

说明：

- 原论文没有多分支、多头、多项加权总损失
- 核心就是像素级 softmax 交叉熵，但通过 `w(x)` 改造成对边界更敏感的监督

### 5.3 权重配置与调度策略

- 各项权重：`w0 = 10`, `sigma ≈ 5 pixels`
- 是否衰减/动态调整：`否，论文未描述动态调度`
- 页码：`p.5`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| EM segmentation challenge | `30` 张 `512×512` 训练图 | 测试集公开但真值保密 | `未单列验证集` | 提交概率图给组织方评测 |
| PhC-U373 | `35` 张部分标注训练图 | challenge test | `未单列验证集` | 相差显微镜 |
| DIC-HeLa | `20` 张部分标注训练图 | challenge test | `未单列验证集` | DIC 显微镜 |

### 6.2 数据增强

- 增强列表：
  - `shift / rotation invariance`
  - `gray value variations`
  - `random elastic deformations`
  - `drop-out` 作为隐式增强
- Patch 提取策略：`large input tiles, batch = 1`
- 页码：`p.3, p.6`

### 6.3 优化器与超参数

- 框架：`Caffe`
- 优化器：`stochastic gradient descent`
- 初始学习率：`正文未明确给出 [待确认]`
- 学习率调度：`正文未明确给出 [待确认]`
- Batch size：`1`
- Epoch / Steps：`正文未明确给出 [待确认]`
- 权重初始化：`Gaussian with std = sqrt(2/N)`
- 预训练策略：`从头训练`
- 是否冻结部分层：`否`
- 设备：`NVidia Titan GPU (6 GB)`
- 页码：`p.4-p.6, p.8`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`未提到`
- 颜色空间转换：`未提到`
- resize / crop / pad 策略：`valid convolution；encoder 特征需 crop 后与 decoder 拼接；大图推理时 overlap-tile`
- patch overlap：`有，重叠切块推理`
- 背景过滤策略：`未提到`
- 标签生成方式：`原始 segmentation map；为 touching cells 人为引入 separation border 并构造权重图`
- 类别不平衡处理：`通过 w_c(x) 做 class-frequency balancing`
- 随机种子/重复次数：`未明确`
- 数据泄漏风险点：`论文未讨论；主要是 challenge 评测数据集`
- 页码：`p.3-p.6`

---

## 7. 推理与后处理

- 推理时输入尺寸：`以 large tile 方式推理；示意为 572×572 输入得到 388×388 有效输出`
- 概率阈值：`EM challenge 提交的是 membrane probability map；固定阈值细节未写`
- 后处理步骤：
  1. `对大图采用 overlap-tile strategy`
  2. `边界区域通过 mirroring 补足上下文`
  3. `EM 任务结果不依赖额外 pre/post-processing`
- TTA / Test-time refinement：`EM challenge 结果使用 7 个旋转版本平均`
- 页码：`p.3-p.4, p.6-p.7`

---

## 8. 消融实验

### 8.1 消融设计

> 论文没有后期常见的模块级 ablation table，但它通过和 prior best/sliding-window 方法以及不同 challenge 结果做了功能性验证。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | `U-Net` vs sliding-window CNN (`IDSIA`) on EM challenge | `warping error 0.000353 vs 0.000420`, `rand error 0.0382 vs 0.0504` | U-Net 在速度和精度上都优于逐 patch 分类路线 |
| 2 | 无强 post-processing 的 U-Net vs heavily tuned challenge pipelines | `PhC-U373 IOU 0.9203`, `DIC-HeLa IOU 0.7756` | 主干结构 + 强增强已经足以显著领先 |
| 3 | 不使用 elastic deformation 的隐含对照 | 论文未给表，但作者明确说 elastic deformation 是关键概念 | 少样本医学分割中强形变增强是核心经验 |

### 8.2 各模块贡献量化

- 模块 A 的独立贡献：`symmetric expanding path + skip connection` 解决了 FCN 语义强但定位弱的问题
- 模块 B 的独立贡献：`border-weighted loss` 用来分开 touching cells
- 页码：`p.3-p.6`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| EM challenge | `Warping error 0.0003529` | `Rand error 0.0382` | `Pixel error 0.0611` | 无额外 pre/post-processing |
| PhC-U373 | `IOU 0.9203` | - | - | ISBI cell tracking challenge 2015 |
| DIC-HeLa | `IOU 0.7756` | - | - | ISBI cell tracking challenge 2015 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| 本文方法 `U-Net` | EM challenge | `Warping error 0.000353` | `Rand error 0.0382` | `Pixel error 0.0611` |
| `IDSIA` sliding-window CNN | EM challenge | `Warping error 0.000420` | `Rand error 0.0504` | `Pixel error 0.0613` |
| 本文方法 `U-Net` | PhC-U373 | `IOU 0.9203` | - | - |
| second-best 2015 | PhC-U373 | `IOU 0.83` | - | - |
| 本文方法 `U-Net` | DIC-HeLa | `IOU 0.7756` | - | - |
| second-best 2015 | DIC-HeLa | `IOU 0.46` | - | - |

### 9.3 公平对比条件确认

- 是否统一 backbone：`不是严格同 backbone 消融，而是对 challenge/既有方法的外部比较`
- 是否统一数据增强：`否，challenge 对手可能不同`
- 是否统一后处理：`作者特别强调 U-Net 在 EM 结果里没有额外 pre/post-processing`
- 是否统一输入尺寸：`未完全统一`
- 结果来源：`原文数字`
- 页码：`p.6-p.7`

### 9.4 评价协议与指标定义

- 数据划分来源：`challenge 官方训练/测试设置`
- 结果汇报层级：`test/challenge leaderboard`
- 实例匹配规则：`不适用原文主表；主要是像素级和 challenge 专用指标`
- Dice 类型：`本篇主表未用 Dice`
- Hausdorff 类型：`未用`
- F1 类型：`未用`
- 是否含后处理后再报结果：`EM 主结果明确为无额外 pre/post-processing`
- 是否多 seed 平均：`未明确`
- 是否报告标准差 / 置信区间：`否`
- 是否和官方 challenge protocol 一致：`是`
- 页码：`p.6-p.7`

---

## 10. 计算量与效率

- 参数量（Params）：`正文未给出`
- 计算量（FLOPs / MACs）：`正文未给出`
- 推理时间（ms/image）：`512×512 图像分割小于 1 秒`
- 训练时间（总 GPU-hours）：`约 10 小时`
- 输入尺寸（计算量对应的）：`512×512` / `572×572 tile`
- 对比方法的效率数据：`未表格化给出`

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `U-Net` | `未报告` | `未报告` | `< 1 s / 512×512 image` |

- 页码：`p.1, p.8`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net`
- 框架/语言：`Caffe`
- 预训练权重是否提供：`论文称提供 trained networks`
- 复现难度评估：`中`
- 复现障碍：`原始实现基于 Caffe；正文未明确学习率、训练轮数、具体 stop criterion`

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不视为论文固定值 | 中 |
| 验证集划分 | 否 | 后续腺体实验单独工程划分 | 高 |
| 推理阈值 | 否 | 不把阈值当论文原值引用 | 中 |
| 后处理细节 | 部分 | 仅记录 overlap-tile 与 mirroring | 中 |
| 训练轮数停止准则 | 否 | 作为工程默认项单独设定 | 高 |
| 数据预处理 | 部分 | 只记录原文明确提到的 deformation / tiling / border handling | 中 |

- 不确定但影响较大的点：
  - `学习率`
  - `epoch / iteration`
  - `dropout 具体比例`

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 需要通过大 tile、batch=1、高动量来尽量榨干显存，说明内存限制对原始实现影响很大
- 使用 valid convolution 导致输入输出尺寸不一致，需要 crop 和 overlap-tile 额外处理
- 论文虽然强调通用性，但实验主要在细胞/EM 数据集上，并非病理腺体 benchmark
- 页码：`p.3-p.4, p.8`

### 14.2 我们观察到的潜在问题

- 原始 `U-Net` 的 loss 是 weighted softmax CE，不是今天病理分割里更常见的 `BCE + Dice`
- 原始网络尺寸链路建立在 `valid convolution` 上，现代实现大多改成 `same padding`，所以“结构继承”和“实现细节继承”不能混为一谈
- 原论文没有对象级指标，不足以直接支撑腺体分割最终评价协议

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`主要展示成功案例，没有系统化失败案例表`
- 典型失败场景：`论文动机明确指向 touching objects 分离困难、边界定位与上下文权衡困难`
- 页码：`p.3, p.5`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `U-shaped encoder-decoder + skip connection` 作为腺体分割首轮最小可复核基线
- 少样本医学分割必须重视强数据增强，尤其是形变增强
- 大图推理时使用 tile/overlap 的工程思想

### 15.2 可以作为候选参数来源的

- `batch size = 1` 的显存优先训练思路
- `SGD + high momentum` 的一种经典做法
- 边界权重图思想，可转化为边界分支/边界 loss 的动机来源

### 15.3 不应照搬的（及原因）

- `572×572 -> 388×388` 的原始 valid-conv 尺寸链路
  - 原因：现代病理分割工程多使用 `same padding` 和更规则的 `512×512`
- `weighted softmax CE` 作为唯一主损失
  - 原因：腺体任务更常需要 `Dice`、对象级稳定性和边界/分离能力联合优化
- EM / cell tracking challenge 的结果数字
  - 原因：数据模态、对象尺度、评价协议与 `GlaS/CRAG` 差异过大

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 是否先做纯 U-Net 基线 | 这是最直接、最经典的医学分割起点 | 强 |
| 为什么要保留 skip connection | 原文核心就是把高分辨率定位信息回流到 decoder | 强 |
| 为什么要做强增强 | 原文明确说 elastic deformation 是少样本训练关键 | 强 |
| 是否直接继承原始 loss | 只能作为边界分离动机，不适合直接固定到腺体任务 | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`01_实验执行/02_UNet流程验证/01_任务与默认配置.md`、`01_实验执行/02_UNet流程验证/02_训练步骤.md`
- [ ] 需要和哪篇论文交叉验证：`GlaS Challenge_2017`、`MILD-Net_2018`、`UNet++_2018`
- [ ] 待确认的问题：`在腺体任务上，是否要单独测试原始 weighted CE 风格边界权重图，还是只保留 U-Net 结构并改用 BCE + Dice`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 少样本医学分割、定位与上下文并重的经典动机 | 作为 U-Net 路线的原始出处 |
| related work | 医学分割 encoder-decoder 主线起点 | 放在方法脉络第一段 |
| 方法 | skip connection 与对称 decoder 的设计依据 | 可作为基线结构定义 |
| 实验设置 | 强增强、tile 推理、少样本训练理念 | 仅作为原则性依据，不夸大为参数原样复现 |
| 讨论 | 原始 U-Net 与现代 same-padding U-Net 的差异 | 用于解释“经典结构”和“现代工程实现”边界 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig.1` | `p.2` | U-Net 总体结构图与通道/空间尺寸示意 | 直接作为基线架构依据 |
| `Fig.2` | `p.3` | overlap-tile strategy 示意图 | 推理策略参考 |
| `Fig.3` | `p.5` | HeLa 权重图与边界监督示意 | 边界监督动机 |
| `Fig.4` | `p.7` | ISBI cell tracking 结果可视化 | 经典成功案例引用 |
| `Table 1` | `p.7` | EM challenge 排名表 | 基线性能引用 |
| `Table 2` | `p.7` | ISBI cell tracking challenge IOU 结果 | 基线性能引用 |

---

## 17. 提取质量自检

- [x] 所有数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够复现（优化器+lr+bs+epoch+augmentation）
- [x] 预处理与数据细节已检查（stain normalization / patch overlap / label 生成）
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认（不是只记指标名字）
- [x] 消融实验的结论已量化（不只是"有效"）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/01_经典基线与对比方法/02_U-Net`
- `paper_type`: `planned_category:01_经典基线与对比方法`
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

- 记录字段：`paper_id=03_文献证据/01_经典基线与对比方法/02_U-Net`；`paper_type=planned_category:01_经典基线与对比方法`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/01_经典基线与对比方法/02_U-Net` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
