# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [x] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [x] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `gland segmentation for IHC biomarker quantification`
- `H&E to IHC transfer`
- `dual-output object + edge segmentation`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`04_腺体与病理近期相关工作`

- 本篇是连接经典腺体分割与病理下游 IHC 定量应用的关键过渡论文
- 本篇至少完成：`1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`Segmentation of glandular epithelium in colorectal tumours to automatically compartmentalise IHC biomarker quantification: a deep learning approach`
- 作者/团队：`Yves-Remi Van Eycke, Cedric Balsat, Laurine Verset, Olivier Debeir, Isabelle Salmon, Christine Decaestecker`
- 发表年份/会议/期刊：`2018, preprint submitted to Elsevier`
- DOI / arXiv ID：`[待确认]`
- BibTeX key：`vaneycke2018ihcgland`
- PDF 路径：`结直肠腺体分割_pdf库/04_腺体与病理近期相关工作/Segmentation_of_glandular_epithelium_in_colorectal_tumours_to_automatically_compartmentalise_IHC_biomarker_quantification_A_deep_learning_approach_2018.pdf`
- 当前定位：`一篇把结直肠腺体上皮分割直接服务于 IHC biomarker compartmentalised quantification 的方法论文，同时证明 H&E 训练模型可通过小样本 fine-tuning 迁移到 IHC`
- 与已提取论文的关系：
  - 继承自：`DCAN` 的 object + contour 双输出思路、`U-Net` 的像素级医学分割范式、`ResNet identity mapping` 的深层可训练性
  - 互补论文：`MAC-Net` 强调近期 attention/context fusion，而本篇强调跨染色泛化与病理下游量化
  - 对我们价值：`比单纯 GlaS 指标论文更贴近“分割服务病理定量分析”的真实应用链路`

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：病理学中常需把 IHC biomarker 的定量分析限制在特定组织 compartment，例如 colorectal glandular epithelium，以获得更有解释力的测量结果。
  - 用途：`引言中的临床意义`
  - 页码：`p.1-p.2`
- 句子/事实 2：作者的方法不仅适用于 H&E，也设计为适用于使用 haematoxylin counterstain 的 IHC 图像。
  - 用途：`任务动机与泛化性`
  - 页码：`Abstract, p.1`
- 句子/事实 3：方法只需在少量 IHC 数据上 fine-tuning，即可把 H&E 预训练模型迁移到新 IHC 数据集。
  - 用途：`迁移学习与小样本适配`
  - 页码：`Abstract, p.1; p.15-p.16`

#### 1.1.2 related work 可引用句

- 句子/事实 1：已有 histology gland segmentation 方法大多只面向 H&E，而本文的首要贡献是构建对 H&E 与 IHC 都适用的更通用方案。
  - 用途：`related work 中的方法差异`
  - 页码：`p.3`
- 句子/事实 2：作者将 `DCAN + U-Net + ResNet identity mapping` 的有效特性合并到一个更节省计算资源的统一网络中，而不是像多通道方法那样拆成多个独立网络再融合。
  - 用途：`架构脉络`
  - 页码：`p.3-p.5`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 输入尺寸 | `480 x 480` | 方法/实验设置 | `p.4` |
| 优化器 | `Adam` | 实验设置 | `p.5` |
| 学习率 | `0.0003` | 实验设置 | `p.5` |
| batch size | `2` | 实验设置 | `p.5` |
| GlaS train size | `85` | 数据集说明 | `p.10-p.11` |
| IHC fine-tuning iterations | `4000` | 迁移学习设置 | `p.17` |
| IHC scratch training iterations | `20000` | 训练设置 | `p.17` |
| GlaS inference time | `0.09s GPU + 0.43s CPU post-processing` | 效率 | `p.17` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 目标不是普通 gland 实例分割，而是分割 colorectal tissue 中的 `glandular epithelium`，以支持 `IHC biomarker quantification` 的 compartmentalised analysis。
- 现有方法主要针对 `H&E`，难以直接迁移到不同 `IHC marker`、不同 chromogen、不同扫描与制片条件。
- 真实病理分析需要同时具备：
  - 跨染色泛化能力
  - 腺体边界分离能力
  - 小数据条件下的可训练性
  - 对 whole slide / TMA 大批量图像的实用速度

对应原文依据（页码）：

- `Abstract, p.1`
- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出一个全卷积双输出网络。输入不是 RGB，而是经 colour deconvolution 得到的 `haematoxylin (HEM)` 单通道，从而尽量对 eosin 或 DAB 等额外染色成分保持不敏感。网络上半部分是更深的 residual encoder，用于提取多层语义；下半部分聚合不同层级特征后，输出 `object segmentation` 与 `edge segmentation` 两个分支。训练时配合针对 gland 与 edge 的加权交叉熵，以及面向真实病理染色/采集变化的 realistic data augmentation。推理时将 edge 输出从 gland 输出中扣除，并经形态学后处理得到最终实例化分割。随后用该分割自动完成 IHC biomarker 的 compartmental quantification，并与专家标注基础上的定量结果做 concordance 对比。

关键页码：

- `p.3-p.10`
- `p.15-p.20`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`fully convolutional encoder-style network with multi-scale fusion and dual outputs`
- Backbone：`VGG-like deep encoder + residual units`
- 输入尺寸：`480 x 480`
- 输入通道：`1-channel HEM after colour deconvolution`
- 输出头：
  - `gland object segmentation`
  - `gland edge segmentation`

### 3.2 关键模块详细描述

**模块 1：`HEM-only input representation`**

- 位置：`network input`
- 操作流程：
  1. 对 H&E 或 IHC RGB 图像做 colour deconvolution
  2. 只保留 blue `haematoxylin` 通道作为网络输入
  3. 丢弃 eosin 或 DAB 等非共享染色成分
- 目的：
  - 提高 H&E 到 IHC 的迁移能力
  - 降低对不同 marker/chromogen 的依赖
- 页码：`p.4-p.5`

**模块 2：`deep residual encoder`**

- 位置：`network upper part`
- 操作流程：
  1. 第一层使用 `7x7` 卷积
  2. 后续卷积和 residual units 使用 `3x3` 卷积，stride 为 `1`
  3. 通过多次 `2x2 max-pooling` 逐步下采样
- 特点：
  - 上半部分仅卷积层就达到 `25` 层
  - 借助 residual units 缓解 vanishing gradient
- 页码：`p.4-p.5`

**模块 3：`multi-level feature fusion from upper to lower part`**

- 位置：`network lower part`
- 操作流程：
  1. 从上半部分提取 4 个不同层级的特征通道
  2. 每个通道先经 transposed convolution 恢复到原图分辨率
  3. 将这 4 个通道拼接
  4. 用一系列 residual units 将特征数从 `128` 压缩到 `16`
- 页码：`p.5`

**模块 4：`dual-output object + edge heads`**

- 位置：`network output`
- 操作流程：
  1. 共享干路特征
  2. 最后分成两个 `1x1 conv + softmax` 头
  3. 一个预测 gland object，一个预测 gland edges
- 作用：
  - 用 edge 分支帮助分开黏连腺体
  - 训练时 edge 误差可反向改善 shared parameters，从而提升 object segmentation
- 页码：`p.5`

### 3.3 架构参数表

| 层/阶段 | 类型 | 通道/核设置 | 空间尺寸 | 备注 |
|---------|------|-------------|---------|------|
| input | HEM single-channel | `1` channel | `480 x 480` | colour deconvolution 后输入 |
| first conv | convolution | `7 x 7`, stride `1` | `480 x 480` | 唯一不是 `3 x 3` 的卷积 |
| encoder | conv + residual units + pooling | mostly `3 x 3` | down to `30 x 30` | 上半部分约 `25` 个卷积层 |
| lower fusion | transposed conv + concat + residual units | `4` paths fused | restore to full resolution | channels `128 -> 16` |
| output heads | `1 x 1 conv + softmax` | `2` heads | `480 x 480` | object / edge 双输出 |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：总损失

```text
c_tot = (c_a + c_b) / 2
```

符号说明：
- `c_a`：gland object segmentation 的加权交叉熵
- `c_b`：gland edge segmentation 的加权交叉熵
- 页码：`Eq.(1), p.8`

公式 2：gland object 分支损失

```text
c_a = - Σ_i w_a(Y_ai) log(Y_hat_ai)
```

符号说明：
- `Y_ai`：像素 `i` 的 gland 真值标签
- `Y_hat_ai`：网络对 gland 类别的预测概率
- `w_a`：object 分支的类别与接触区域加权
- 页码：`Eq.(2), p.8`

公式 3：edge 分支损失

```text
c_b = - Σ_i w_b(Y_bi) log(Y_hat_bi)
```

符号说明：
- `Y_bi`：像素 `i` 的 edge 真值标签
- `Y_hat_bi`：edge 预测概率
- `w_b`：edge 分支的类别不平衡加权
- 页码：`Eq.(3), p.8`

公式 4：object 分支权重分解

```text
w_a(Y_ai) = w_c(Y_ai) + w_d(Y_ai)
```

符号说明：
- `w_c`：按类别比例分配的权重
- `w_d`：对靠近 gland 接触区域像素的额外正则
- 页码：`Eq.(4), p.8-p.9`

公式 5：接触区域加权项

```text
w_d(Y_ai) =
  [ -k / (2(1-p)),  k / (2p) ]    if pixel i belongs to class 0
                                  and is within l pixels of class 1
  [ 0, 0 ]                        otherwise
```

符号说明：
- `p`：网络预测为前景的像素比例，截断在 `[0.01, 0.99]`
- `k = 4`
- `l = 16`
- 该项增强 touching glands 附近像素的重要性
- 页码：`Eq.(7), p.9`

### 4.2 推导过程或梯度行为

- 论文没有做复杂闭式推导，但明确给出设计直觉：
  - `object + edge` 双输出能改善相邻腺体分离
  - edge 分支的误差信号通过共享参数反向作用于 object 分支
  - `w_d` 针对 touching objects 的邻近区域增大权重，专门缓解腺体黏连
- 页码：`p.5; p.8-p.10`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `c_a` | `Eq.(2)` | gland epithelium vs background | object output |
| `c_b` | `Eq.(3)` | gland edges vs non-edge | edge output |
| `w_c` | `Eq.(5)-(6)` | 类别不平衡重加权 | both branches |
| `w_d` | `Eq.(7)` | 强化 touching glands 附近区域 | object branch |

### 5.2 总损失公式

```text
c_tot = (c_a + c_b) / 2
```

### 5.3 权重配置与调度策略

- edge 分支采用与 object 分支类似的类别比例权重
- object 分支额外加入 `touching objects regularisation`
- 论文实验设定：
  - `k = 4`
  - `l = 16`
- 未报告动态权重调度，视为固定配置
- 页码：`p.8-p.9`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `GlaS WQUD` | `85` | `Part A: 60`, `Part B: 20` | `[待确认]` | H&E，官方 challenge 设置 |
| `IHC BAX fine-tuning set` | `43 cores` | `used for fine-tuning/train-from-scratch` | second BAX set used as validation | 10x magnification |
| `IHC test sets` | `[训练外独立]` | `BAX 34`, `IGFBP2 37`, `alpha-SMA 32` cores | independent test sets | 无 gland 交叉 |

### 6.2 数据增强

- 增强列表：
  - random crops of `480 x 480`
  - elastic deformations
  - random rotations
  - staining augmentation on HEM colour vector
  - OD distribution perturbation with B-spline remapping
  - exposure perturbation
  - white balance / temperature perturbation
  - Gaussian blur
- Patch 提取策略：`每个 epoch 从每个训练 core 随机裁一张 480x480，再做全增强`
- 页码：`p.5-p.8; p.15`

### 6.3 优化器与超参数

- 框架：`TensorFlow on GPU 1.2.1`
- 语言/环境：`Python 3.5.3`
- 优化器：`Adam`
- 初始学习率：`0.0003`
- 学习率调度：`[待确认]`
- Batch size：`2`
- Epoch / Steps：
  - GlaS training converged at about `200000` iterations
  - IHC fine-tuning needed `4000` iterations
  - IHC training from scratch used `20000` iterations
- 权重初始化：
  - `H&E pretraining + IHC fine-tuning` 是最佳条件
  - 也评估了 `IHC from scratch`
- 是否冻结部分层：`未说明`
- 设备：
  - `Nvidia Titan X Pascal 12GB`
  - `Core i7-3930K`, `16GB RAM`
- 页码：`p.5; p.17; Appendix E`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`无传统 stain normalization；改为基于 colour deconvolution 的 HEM-only 输入 + realistic augmentation`
- 颜色空间转换：`RGB -> colour deconvolution -> HEM channel`
- resize / crop / pad 策略：
  - 输入固定 `480 x 480`
  - 小于该尺寸时用 border reflection padding
- patch overlap：
  - 对大图切成 overlapping `480 x 480` tiles
  - 重叠区域取离 tile center 更近的像素值
- 背景过滤策略：`IHC quantification 时通过 OD distance 阈值剔除无 tissue 区域`
- 标签生成方式：
  - 主标签为 glandular epithelium mask
  - edge labels 由 gland 标签经形态学操作生成，edge width 为 `16` pixels
- 类别不平衡处理：`weighted cross-entropy`
- 随机种子/重复次数：`未报告`
- 数据泄漏风险点：
  - IHC 四个 core sets 之间无 gland 交叉，作者已明确避免交叉污染
- 页码：`p.4-p.10; p.15-p.16`

---

## 7. 推理与后处理

- 推理时输入尺寸：`480 x 480`
- 概率阈值：`0.5`
- 后处理步骤：
  1. 对 object 与 edge 两个输出做阈值化
  2. 用 edge mask 从 object mask 中相减，增强相邻腺体分离
  3. 填洞
  4. 连通域编号
  5. 对整张 mask 反射 padding `32` 像素
  6. 形态学膨胀补偿 edge subtraction
  7. 删除过小对象，阈值 `< 2048 pixels`
  8. 去掉 padding，得到最终 mask
- TTA / Test-time refinement：`无`
- 页码：`p.9-p.10`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | 去掉 edge output，仅用 object 输出 | 各项指标明显下降 | edge 分支确实改善分割 |
| `A2` | 去掉 acquisition augmentation | Part B 性能下降 | 采集条件增强有贡献 |
| `A3` | 去掉 colour augmentation | 性能下降 | realistic stain augmentation 有贡献 |
| `A4` | 去掉 morphology augmentation | 性能大幅下降 | elastic deformation 最关键 |
| `A5` | simpler colour augmentation | 低于完整方案 | 简单 hue/saturation 扰动不足 |
| `A6` | simpler morphology augmentation | 低于完整方案 | 真实弹性形变优于简单刚体变化 |
| `A7` | 用 `1x1 conv` 学习融合双输出 | 结果劣于逻辑相减方案 | 简单逻辑组合反而更有效 |

### 8.2 各模块贡献量化

- 去掉 `edge output` 后，主结果从 `F1 0.895 / 0.788, Object Dice 0.902 / 0.841` 降至 `0.869 / 0.775, 0.883 / 0.814`，Hausdorff 也明显变差。
- 去掉 `morphology augmentation` 影响最大，Part A/B 的 F1 与 Object Dice 基本跌到 `0.759/0.728` 与 `0.763/0.769`。
- `1x1 fusion` 没有优于原始的 `threshold + subtraction + morphology` 组合。
- 页码：`Table 2, p.12-p.14`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS Part A/B` | `F1 0.895 / 0.788` | `Object Dice 0.902 / 0.841` | `Object Hausdorff 42.941 / 105.931` | H&E 主结果 |
| `IHC pretrained + fine-tuning` | `F1 0.825 / 0.830 / 0.863` | `Pixel Dice 0.895 / 0.895 / 0.914` | `STD 0.021 / 0.011` | BAX / IGFBP2 / alpha-SMA |
| `IHC trained from scratch` | `F1 0.803 / 0.827 / 0.858` | `Pixel Dice 0.882 / 0.891 / 0.909` | `STD 0.027 / 0.014` | 小样本从头训练 |
| `IHC pretrained without fine-tuning` | `F1 0.684 / 0.684 / 0.716` | `Pixel Dice 0.804 / 0.793 / 0.817` | `STD 0.018 / 0.012` | 直接迁移效果明显较差 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `Proposed` | `GlaS` | `best rank-sum` | `best weighted rank-sum` | `HEM-only input` |
| `Xu et al. 2017b` | `GlaS` | object Dice 略优某项 | Hausdorff 弱于本文 | 更复杂网络 |
| `DCAN (CUMedVision2)` | `GlaS` | 弱于本文，尤其 Part B | object Dice 更低 | 经典 contour-aware baseline |
| `U-Net / Freiburg` | `GlaS` | 整体弱于本文 | boundary 指标更差 | 经典医学基线 |

### 9.3 公平对比条件确认

- 是否统一 backbone：`否，属于文献横向对比`
- 是否统一数据增强：`否`
- 是否统一后处理：`否`
- 是否统一输入尺寸：`否`
- 结果来源：`原文 Table 1/2/3`
- 补充说明：
  - GlaS 对比使用官方 challenge 协议
  - IHC 结果是作者自建数据与作者协议
- 页码：`p.10-p.16`

### 9.4 评价协议与指标定义

- 数据划分来源：
  - `GlaS`：官方 `train / Part A / Part B`
  - `IHC`：作者自建独立 core sets
- 结果汇报层级：
  - GlaS：`testA`, `testB`
  - IHC：marker-specific test sets
- 实例匹配规则：`segmented object overlap > 50%` 计为 TP
- Dice 类型：
  - `GlaS`: `Object Dice`
  - `IHC`: `pixel Dice`
- Hausdorff 类型：`object Hausdorff`
- F1 类型：
  - `GlaS`: object detection F1
  - `IHC`: pixel F1
- 是否含后处理后再报结果：`是`
- 是否多 seed 平均：`未报告`
- 是否报告标准差 / 置信区间：
  - `IHC` 报告了跨 marker 的 `STD`
- 是否和官方 challenge protocol 一致：`GlaS 是`
- 页码：`p.10-p.11; p.15-p.16`

---

## 10. 计算量与效率

- 参数量（Params）：`[未给出]`
- 计算量（FLOPs / MACs）：`[未给出]`
- 推理时间（ms/image）：
  - `0.09 second` on GPU for an image of about `250000 pixels`
  - `0.43 second` CPU post-processing
- 训练时间（总 GPU-hours）：
  - GlaS training: `a bit more than a day`
- 输入尺寸（计算量对应的）：`around 250000 pixels input`；模型训练 patch 为 `480 x 480`
- 对比方法的效率数据：
  - 论文称其速度略快于 `DCAN`，后者约 `1.5s` for `755 x 522` image

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `Proposed` | `[未给出]` | `[未给出]` | `0.52s/image incl. post-processing` |
| `DCAN` | `[未给出]` | `[未给出]` | `~1.5s/image` |

- 页码：`p.17; p.19-p.20`

---

## 13. 开源与复现

- 代码是否开源：`未见公开说明`
- 代码仓库地址：`[待确认]`
- 框架/语言：`Python 3.5.3 + TensorFlow GPU 1.2.1 + scikit-image`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中-高`
- 复现障碍：
  - 老版本 TensorFlow 环境较旧
  - realistic stain augmentation 细节较多，实现成本高
  - IHC 自建数据无法公开获得

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `复现时需多次运行取稳健结果` | `中` |
| 验证集划分 | `部分明确` | `IHC 用 second BAX as validation；GlaS 验证细节待确认` | `中` |
| 推理阈值 | `是` | `使用 0.5` | `低` |
| 后处理细节 | `是` | `按文中逐步复现` | `低` |
| 训练轮数停止准则 | `否` | `按迭代数近似重建` | `中` |
| 数据预处理 | `是` | `colour deconvolution + HEM-only` | `低` |

- 不确定但影响较大的点：
  - `IHC 训练集具体采样与增强实现代码`
  - `GlaS 训练时的验证/early stopping 细节`

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 方法依赖 `HEM` 通道中细胞核有足够可见性；若 counterstain 太弱，分割会受影响。
- 复杂肿瘤区域中 gland 边界本身不清楚，自动分割与专家边界都可能存在不确定性。
- 当前工作主要聚焦结肠腺体，其他组织如前列腺虽然初步可行，但仍需进一步 fine-tuning。
- 页码：`p.18-p.20`

### 14.2 我们观察到的潜在问题

- 本文方法虽然在 GlaS 上很强，但核心设计前提是 `HEM-only`，这在某些强 DAB 或低 counterstain 场景下可能丢失有用信息。
- IHC 结果来自作者自建数据，跨机构泛化证据仍有限。
- 后处理步骤较多，说明网络原始输出本身还依赖显式 morphology pipeline 才能稳定实例分离。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是，文中提到复杂且局部不可见的 gland objects 容易被错误合并`
- 典型失败场景：
  - touching glands 分离不充分
  - tumour glands lumen / secretion 标注与算法理解不一致
  - 复杂肿瘤组织中 gland exact delimitation 不清晰
- 页码：`p.11-p.12; p.15-p.18`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `gland segmentation -> biomarker quantification` 这一叙事链条，可直接支撑我们为什么不是为了分割而分割。
- `HEM-only + colour deconvolution` 提供了一条跨染色泛化思路，可作为 IHC/特殊染色扩展任务的备选输入设计。
- `object + edge dual supervision` 仍然是腺体黏连分离的高价值经典路线。
- realistic stain augmentation 思路比简单 RGB jitter 更贴近病理成像实际。

### 15.2 可以作为候选参数来源的

- `input size = 480 x 480`
- `Adam, lr = 3e-4`
- `batch size = 2`
- `edge width = 16`
- `remove small objects < 2048 pixels`

### 15.3 不应照搬的（及原因）

- 不应直接照搬整套 `HEM-only` 输入作为当前主线默认设置
  - 原因：你的主任务不一定是跨 IHC marker 泛化，且部分场景 RGB/HED 多通道可能保留更多上下文。
- 不应无条件照搬复杂 morphology 后处理
  - 原因：后处理强依赖分辨率、对象尺度和数据域，迁移到新数据容易失稳。

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界分支/轮廓监督 | `object + edge` 双输出在腺体任务中有效 | `强` |
| 病理下游价值表述 | 分割用于 IHC compartmental quantification | `强` |
| stain-aware preprocessing | `HEM-only` 跨 H&E/IHC 泛化 | `中` |
| realistic augmentation | 病理染色与采集变化建模 | `强` |
| 轻量快速部署 | 推理速度可用于大批量 TMA/WSI | `中` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`引言中的病理下游价值`、`边界分支设计依据`、`IHC 扩展应用储备`
- [ ] 需要和哪篇论文交叉验证：`DCAN`、`U-Net`、`MAC-Net`
- [ ] 待确认的问题：`我们是否需要做 H&E -> IHC 的小样本迁移实验作为扩展结果`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 分割服务 IHC biomarker quantification 的直接动机 | 作为临床/病理意义论据 |
| related work | DCAN/U-Net/ResNet 融合式腺体分割基线 | 放在经典与过渡路线段落 |
| 方法 | edge supervision、HEM-only 输入、realistic augmentation | 作为设计来源或对照依据 |
| 实验设置 | input/lr/bs/后处理阈值 | 仅在场景相近时借鉴 |
| 讨论 | 跨染色泛化、边界不确定性、人工标注偏差 | 用于解释模型边界条件 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.4` | 整体网络结构图 | 参考架构设计 |
| `Figure 2` | `p.7` | HEM colour augmentation 示意 | 参考 realistic stain augmentation |
| `Figure 4` | `p.9-p.10` | object/edge 输出与后处理流程 | 参考后处理链路 |
| `Table 1` | `p.11` | GlaS 与 SOTA 对比 | 引用主结果 |
| `Table 2` | `p.13-p.14` | 消融实验 | 引用模块贡献 |
| `Table 3` | `p.15-p.16` | IHC 三种训练条件结果 | 引用迁移学习价值 |
| `Figure 7` | `p.16-p.17` | IHC quantification concordance scatterplots | 支撑下游病理价值 |
| `Figure 8` | `p.17` | convergence 分析 | 参考训练稳定性 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写
- [x] 公式符号都有解释
- [x] 训练参数足够复现（优化器+lr+bs+iteration+augmentation）
- [x] 预处理与数据细节已检查（colour deconvolution / HEM-only / overlap / label 生成）
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认（object-level 与 pixel-level 已区分）
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/04_腺体与病理近期相关工作/02_IHC-Glandular-Epithelium`
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

- 记录字段：`paper_id=03_文献证据/04_腺体与病理近期相关工作/02_IHC-Glandular-Epithelium`；`paper_type=planned_category:04_腺体与病理近期相关工作`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/04_腺体与病理近期相关工作/02_IHC-Glandular-Epithelium` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
