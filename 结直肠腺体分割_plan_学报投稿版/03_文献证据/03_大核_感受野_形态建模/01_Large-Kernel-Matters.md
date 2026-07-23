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

- `large kernel design`
- `global convolution`
- `boundary refinement`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`03_大核_感受野_形态建模`

- 本篇是这一组里最核心的“为什么大核对分割有效”的来源论文
- 本篇至少完成：`1, 2, 3, 4, 6, 8, 9, 10, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`Large Kernel Matters -- Improve Semantic Segmentation by Global Convolutional Network`
- 作者/团队：`Chao Peng, Xiangyu Zhang, Gang Yu, Guiming Luo, Jian Sun`
- 发表年份/会议/期刊：`2017, CVPR`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:1703.02719`
- BibTeX key：`peng2017large`
- PDF 路径：`结直肠腺体分割_pdf库/03_大核_感受野_形态建模/Large_Kernel_Matters_GCN_2017.pdf`
- 当前定位：`大核/大感受野模块的直接理论与工程来源；论文把语义分割中的 classification-localization 张力具体化，并提出 GCN + BR 作为兼顾两者的结构方案`
- 与已提取论文的关系：
  - 与 `DeepLabV3+_2018` 互补：后者强调 atrous multi-scale context，这篇强调 large kernel 对分类能力的直接补强
  - 与 `Gated-SCNN_2019`、`Boundary-Loss_2019` 互补：这篇不是专门改边界监督，而是让主干先获得更大的有效感受野，再由 BR 做边界修正
  - 可作为你后续 `LKMA` 或大核模块的最直接出处

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：语义分割需要同时处理 classification 与 localization，两者天然存在张力
  - 用途：`方法动机`
  - 页码：`p.1`
- 句子/事实 2：更大的 kernel size 与更大的有效感受野有助于缓解这种矛盾
  - 用途：`为何要做大核`
  - 页码：`p.1, p.3-p.4`
- 句子/事实 3：作者提出 `GCN + BR`，在 `PASCAL VOC 2012` 上达到 `82.2%`，在 `Cityscapes` 上达到 `76.9%`
  - 用途：`结果概括`
  - 页码：`Abstract, p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：传统分割网络虽然理论 receptive field 很大，但真正起作用的 valid receptive field 往往远小于理论值
  - 用途：`说明大核必要性`
  - 页码：`Sec.3.1, p.3-p.4`
- 句子/事实 2：作者并不直接使用代价高昂的 `k x k` 巨核，而是用对称分解的 `1 x k + k x 1` 路径近似大核
  - 用途：`工程实现出处`
  - 页码：`Sec.3.1, p.4`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| PASCAL base model | `ResNet-152 pretrained on ImageNet` | 主实验设置 | `p.4` |
| optimizer | `SGD` | 训练协议 | `p.4` |
| batch size | `1` | 训练协议 | `p.4` |
| momentum | `0.99` | 训练协议 | `p.4` |
| weight decay | `0.0005` | 训练协议 | `p.4` |
| PASCAL best val | `80.3` | `GCN + BR, Stage-3` | `p.6` |
| PASCAL test | `82.2` | SOTA 结果 | `p.6` |
| Cityscapes test | `76.9` | SOTA 结果 | `p.6-p.7` |
| best ablation kernel size | `k = 15` | GCN 消融 | `p.5` |
| Cityscapes final kernel size | `k = 25` | 因 feature map 为 `25 x 25` | `p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 语义分割同时需要类别判别能力和像素级定位能力
- 分类通常需要更大的感受野，而定位又需要更精细的空间对齐
- 现有分割网络虽然理论 receptive field 很大，但有效感受野不足，难以真正覆盖完整目标
- 需要一种既能引入大范围上下文、又不显著增加训练难度和参数量的结构

对应原文依据（页码）：

- `p.1`
- `Sec.3.1, p.3-p.4`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `Global Convolutional Network (GCN)` 与 `Boundary Refinement (BR)`。GCN 通过两条对称的大核分解路径 `1 x k -> k x 1` 与 `k x 1 -> 1 x k`，在较低计算量下实现接近大核 `k x k` 的密集连接，增强分类能力与有效感受野；BR 再以残差形式对粗分割图做局部边界修正，从而把“大核负责内部区域分类、边界模块负责边界对齐”的职责拆开。

关键页码：

- `Sec.3.1-Sec.3.2, p.3-p.4`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`ResNet backbone + FCN-style segmentation framework + GCN + BR`
- Backbone：
  - `ResNet-152` 用于主实验
  - 另做了 `ResNet50-GCN` 对照
- 输入尺寸：
  - `PASCAL VOC`：Stage-1 padding 到 `640 x 640`，Stage-2/3 为 `512 x 512`
  - `Cityscapes`：训练时随机裁成 `800 x 800`
- 输出头：
  - 多尺度 semantic score maps
  - BR refinement 后的最终 segmentation map

### 3.2 关键模块详细描述

**模块 1：`Global Convolutional Network (GCN)`**

- 位置：`多尺度 feature maps 到 score maps 的分类头`
- 操作流程：
  1. 对 backbone 各 stage 的 feature maps 接入 GCN
  2. 每个 GCN 用两条对称分支近似大核卷积
  3. 输出多尺度 semantic score maps
  4. 再经 FCN 风格上采样与逐级融合得到预测
- 核心意义：
  - 在大 `k x k` 区域内建立更密集连接
  - 提升分类能力和有效感受野
- 页码：`Sec.3.1-Sec.3.2, p.3-p.4`

**模块 2：`Boundary Refinement (BR)`**

- 位置：`score map refinement`
- 操作流程：
  1. 输入 coarse score map `S`
  2. 经过 residual branch 预测修正项 `R(S)`
  3. 输出 refined map `S_tilde = S + R(S)`
- 核心意义：
  - 主要修复边界区域的定位误差
  - 与 GCN 形成“内部分类 vs 边界修正”的互补
- 页码：`Sec.3.2, p.4; p.5`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| GCN kernel size | `3-15` 消融，最佳 `15` | 扩大有效感受野 | `p.5` |
| Cityscapes GCN k | `25` | 对应最终 `25 x 25` feature map | `p.6` |
| GCN branch design | `1 x k -> k x 1` 和 `k x 1 -> 1 x k` | 低成本近似大核 | `p.4` |
| nonlinearity inside GCN | `无` | 保持与大核线性变换一致 | `p.4` |
| BR | `residual refinement block` | 边界细化 | `p.4-p.5` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
GCN(X) = (1 x k -> k x 1)(X) + (k x 1 -> 1 x k)(X)
```

符号说明：

- `X`：输入 feature map
- 两条分支共同近似一个大范围 `k x k` 的线性变换
- 目的：在较少参数与计算量下获得更大有效感受野
- 页码：`Sec.3.1, p.4`

公式 2：

```text
S_tilde = S + R(S)
```

符号说明：

- `S`：coarse score map
- `R(S)`：boundary refinement residual branch
- `S_tilde`：refined score map
- 含义：用残差方式做局部边界对齐修正
- 页码：`Sec.3.2, p.4`

### 4.2 推导过程或梯度行为

- 直觉推导：
  - 分割中的内部区域更接近分类问题，因此更依赖大范围上下文
  - 边界区域更接近定位问题，因此需要额外局部修正
- GCN 的工程推导：
  - 不直接上 `k x k` 大核，避免参数和优化难度暴涨
  - 用两条可分解路径近似大核，同时不加非线性，保持线性大核的表达性质
- BR 的职责划分：
  - GCN 主要提升内部区域准确率
  - BR 主要提升 boundary accuracy
- 页码：
  - `p.3-p.5`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `segmentation loss` | `[标准像素级分类损失，文中未单列公式]` | 监督语义分割预测 | final score map |

### 5.2 总损失公式

```text
L_total = L_seg
```

说明：

- 本文创新点不在 loss，而在 GCN 与 BR 的结构设计
- 原文重点讨论的是结构消融、kernel size 与区域贡献差异

### 5.3 权重配置与调度策略

- 未引入特殊多项 loss 权重
- BR 作为结构分支接入，而不是单独的边界监督项
- 页码：`通篇未突出特殊 loss 设计`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `PASCAL VOC 2012` | `1464 train + SBD => 10582` | `1456 test` | `1449 val` | 20 类 + background |
| `Cityscapes` | `2975 fine train + 19998 coarse` | `1525 test` | `500 val` | 19 类 leaderboard |

### 6.2 数据增强

- 增强列表：
  - `mean subtraction`
  - `horizontal flip`
- Patch / crop 策略：
  - `PASCAL VOC`：Stage-1 输入 pad 到 `640 x 640`，Stage-2/3 pad 到 `512 x 512`
  - `Cityscapes`：训练时随机 crop 为 `800 x 800`
- 测试策略：
  - `Cityscapes`：切成四个 `1024 x 1024` crop 并融合 score maps
- 页码：`p.4, p.6`

### 6.3 优化器与超参数

- 框架：`Caffe`
- 优化器：`SGD`
- batch size：`1`
- momentum：`0.99`
- weight decay：`0.0005`
- 预训练：
  - `PASCAL/Cityscapes` 主实验用 `ImageNet-pretrained ResNet-152`
  - 另有 `COCO` 预训练后再做 PASCAL 三阶段训练
- 多阶段训练：
  - `PASCAL VOC`: `COCO+SBD+VOC -> SBD+VOC -> VOC`
  - `Cityscapes`: `coarse+train -> fine train`
- 学习率：`[待确认原文附录/代码具体值]`
- 设备：`[待确认]`
- 页码：`p.4, p.6`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；自然图像`
- resize / crop / pad 策略：见上
- 标签处理：
  - 直接用标准 segmentation labels
  - 额外 boundary region 分析时，以距边界 `<= 7` 像素定义 boundary 区域
- 随机种子/重复次数：`未明确`
- 页码：`p.5-p.6`

---

## 7. 推理与后处理

- 推理流程：
  1. backbone 提取多尺度特征
  2. 各尺度经 GCN 生成 score maps
  3. FCN 风格逐级上采样与融合
  4. BR 对边界做残差细化
- 后处理：
  - `PASCAL` 与 `Cityscapes` 都报告了 `MS` 和 `CRF` 进一步增益
- 页码：`p.4-p.6`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | 改变 `k=3...15` | `69.0 -> 74.5` | kernel 越大总体越好，`k=15` 最优 |
| `A2` | GCN vs trivial `k x k` conv | GCN 更优且参数更少 | 提升不是单纯靠参数量 |
| `A3` | GCN vs stack of small convs | GCN 在大核下更稳、更强 | 大核分解优于简单堆叠 |
| `A4` | 仅 GCN vs `GCN + BR` | `74.5 -> 74.7` overall，但边界更明显提升 | BR 主要改善边界 |
| `A5` | boundary vs internal analysis | GCN 对 internal 提升更大 | 支持“GCN 管分类、BR 管边界” |

### 8.2 各模块贡献量化

- Table 1：
  - baseline `69.0`
  - `k=3: 70.1`
  - `k=5: 71.1`
  - `k=7: 72.8`
  - `k=9: 73.4`
  - `k=11: 73.7`
  - `k=13: 74.0`
  - `k=15: 74.5`
- Table 5：
  - `Baseline`: boundary `71.3`, internal `93.9`, overall `69.0`
  - `GCN`: boundary `71.5`, internal `95.0`, overall `74.5`
  - `GCN + BR`: boundary `73.4`, internal `95.1`, overall `74.7`
- 页码：`p.5-p.6`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `PASCAL VOC 2012 val` | `80.3` | `80.4 (MS)` | `81.0 (MS+CRF)` | `GCN + BR` |
| `PASCAL VOC 2012 test` | `82.2` | `SOTA` | `vs 80.2 previous best` | official server |
| `Cityscapes val` | `76.9` | `77.2 (MS)` | `77.4 (MS+CRF)` | `GCN + BR` |
| `Cityscapes test` | `76.9` | `SOTA` | `vs 71.8 previous best` | official server |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `CentraleSupelec Deep G-CRF` | `PASCAL test` | `80.2` | previous best | 对照 |
| `Our approach` | `PASCAL test` | `82.2` | `+2.0` | 新 SOTA |
| `previous best` | `Cityscapes test` | `71.8` | previous best | 对照 |
| `Our approach` | `Cityscapes test` | `76.9` | `+5.1` | 新 SOTA |

### 9.3 公平对比条件确认

- 是否统一 backbone：`主对比在相同框架内替换 GCN/BR 设计`
- 是否统一数据增强：`基本统一，额外报告 MS/CRF 后处理版本`
- 是否统一输入尺寸：`按数据集固定训练/测试设置`
- 结果来源：`官方 server + validation tables`
- 页码：`p.5-p.7`

### 9.4 评价协议与指标定义

- 主要指标：`mean IoU`
- 附加分析：
  - `boundary region accuracy`
  - `internal region accuracy`
- boundary region 定义：`距离 object boundary <= 7`
- 页码：`p.5-p.6`

---

## 10. 计算量与效率

- GCN 不直接用巨大的 `k x k` 卷积，而是用分解结构把参数量与计算量降到更可行的水平
- 相比 trivial large conv：
  - `k=9` 时 GCN 约 `782K` 参数
  - 对应 trivial conv 约 `3484K` 参数
- 相比 stack of small convs：
  - 大等效核下 stack 参数更多且性能反而下降
- 论文核心结论：
  - 大核很重要，但必须采用可训练、低成本的结构实现
- 对我们项目的意义：
  - 后续做大核模块时，优先考虑结构化分解，而不是直接暴力增大卷积核
- 页码：`p.4-p.5`

---

## 13. 开源与复现

- 代码是否开源：`[待确认]`
- 代码仓库地址：`[待确认]`
- 框架/语言：`Caffe`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：
  - 原始实现较老，基于 `Caffe`
  - 多阶段训练与大核分解实现细节需要核对
  - `PASCAL/Cityscapes` 数据准备链较长

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 学习率具体数值 | `未在正文突出` | `后续查附录/实现` | `中` |
| 随机种子 | `否` | `复现时固定` | `低` |
| 代码链接 | `未在当前文本确认` | `后续补查` | `低` |
| 各 stage 训练轮数 | `正文未细写` | `后续以实现补全` | `中` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文主要针对自然图像语义分割，不是病理场景
- 大核虽有效，但若直接用 trivial 大卷积会难收敛、代价高

### 14.2 我们观察到的潜在问题

- 对腺体分割来说，单纯放大感受野不一定自动改善实例分离
- GCN 主要提升内部区域分类，而腺体任务常常更受边界黏连、实例断裂影响
- 因此若迁移到病理图像，最好把大核和边界/拓扑模块组合使用，而不是单独依赖大核

### 14.3 失败案例 / 定性分析

- 论文主要通过区域拆分分析说明问题：
  - GCN 对 internal region 提升显著
  - boundary region 单靠 GCN 提升有限
- 这意味着：
  - 大核可以先解决“看全目标”的问题
  - 边界精细对齐仍需专门 refinement 或边界分支
- 页码：`p.5-p.6`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `大核能缓解 classification-localization 张力` 这一理论表述
- `1 x k + k x 1` 的可训练大核分解方式
- “内部区域靠大感受野、边界区域靠 refinement” 的职责分工

### 15.2 可以作为候选参数来源的

- 主消融可优先从较大 kernel 开始尝试，如 `k=7/9/11`
- 若特征图尺寸允许，可用“接近 feature map 尺寸”的大核思路
- 边界区域分析可参考 `distance <= 7` 的定义方式

### 15.3 不应照搬的（及原因）

- 直接照搬 `Caffe + ResNet152 + VOC/Cityscapes` 训练流程：
  - 原因：任务域和工程栈都不同
- 直接把 `GCN` 当成腺体分割的唯一关键改进：
  - 原因：腺体分割还需要考虑 boundary separation、instance split、morphology consistency

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| `LKMA` / 大核模块 | 直接给出大核必要性与结构化实现方式 | `强` |
| 编码器感受野增强 | 证明更大有效感受野能提升分割分类能力 | `强` |
| 边界细化分支 | BR 提供“主干 + refinement”组合逻辑 | `中-强` |
| 单纯 loss 改进路线 | 不是本文重点 | `弱` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`大核模块设计动机`、`编码器改造依据`
- [ ] 需要和哪篇论文交叉验证：`Scaling_Up_Your_Kernels_to_31x31_2022`、`Wavelet_Convolutions_2024`、`Boundary-Loss_2019`
- [ ] 待确认的问题：`你的 LKMA 更适合放 encoder 还是 decoder，是否需要并联 boundary refinement`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 分割里 classification 和 localization 的矛盾 | 作为大核设计动机 |
| related work | 大核/全局卷积路线的代表方法 | 放在 receptive field 模块综述 |
| 方法 | `1 x k + k x 1` 分解大核结构 | 作为 LKMA 设计来源 |
| 实验分析 | internal vs boundary 的差异收益 | 用来解释为什么还需要边界模块 |
| 讨论 | 大核不是边界问题的全部答案 | 连接到边界/拓扑支撑文献 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 2` | `p.3-p.4` | 整体框架、GCN、BR 结构 | 回填方法结构 |
| `Figure 3` | `p.4` | VRF 可视化 | 写大核动机 |
| `Table 1` | `p.5` | 不同 kernel size 消融 | 回填参数与趋势 |
| `Table 2` | `p.5` | GCN vs trivial large conv | 写效率与可训练性 |
| `Table 3-4` | `p.5` | GCN vs stack of small convs | 写结构优越性 |
| `Table 5` | `p.5-p.6` | boundary/internal 分析 | 解释 GCN 与 BR 分工 |
| `Table 7-10` | `p.6-p.7` | PASCAL / Cityscapes 主结果 | 数字引用 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] 公式符号都有解释
- [x] 训练参数已覆盖 optimizer、batch、momentum、weight decay、crop
- [x] GCN 与 BR 的职责分工已写清
- [x] 大核消融和主结果已核对
- [x] 效率与参数对比已记录
- [x] 与我们项目的关联已具体到模块级别
- [x] 不确定内容已标注 `[待确认]`

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/03_大核_感受野_形态建模/01_Large-Kernel-Matters`
- `paper_type`: `planned_category:03_大核_感受野_形态建模`
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

- 记录字段：`paper_id=03_文献证据/03_大核_感受野_形态建模/01_Large-Kernel-Matters`；`paper_type=planned_category:03_大核_感受野_形态建模`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/03_大核_感受野_形态建模/01_Large-Kernel-Matters` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
