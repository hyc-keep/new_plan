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

- `domain-specific pretraining`
- `transfer learning case study`
- `gland vs cell segmentation`
- `OOD generalization`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`06_半监督_拓扑_扩展工作`

- 本篇不是提出新分割结构，而是系统评估“病理专用预训练到底是否值得”，对 encoder 初始化选择非常重要
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`To Pretrain or not to Pretrain? A Case Study of Domain-Specific Pretraining for Semantic Segmentation in Histopathology`
- 作者/团队：`Tushar Kataria, Beatrice Knudsen, Shireen Elhabian`
- 发表年份/会议/期刊：`2023, arXiv`
- DOI / arXiv ID：`arXiv:2307.03275`
- BibTeX key：`kataria2023pretrain`
- PDF 路径：`结直肠腺体分割_pdf库/06_半监督_拓扑_扩展工作/To_Pretrain_or_Not_to_Pretrain_A_Case_Study_of_Domain-Specific_Pretraining_for_Histopathology_Segmentation_2023.pdf`
- 当前定位：`06` 目录中的初始化策略决策论文，直接回答“病理专用 SSL 预训练是否优于 ImageNet 或随机初始化”
- 与已提取论文的关系：
  - 与 [03_Cerberus.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/06_半监督_拓扑_扩展工作/03_Cerberus.md) 相辅相成：`Cerberus` 证明多任务共享表示有效，本篇进一步追问 encoder 初始权重如何选
  - 与 [01_PRS2.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/06_半监督_拓扑_扩展工作/01_PRS2.md) 互补：`PRS2` 解决标签不足，本篇解决初始化不足
  - 与 [12_DEA-Net.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/12_DEA-Net.md) 形成对照：`DEA-Net` 关注结构设计，本篇证明很多时候初始化本身就会影响 gland segmentation 上限

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者明确指出，histopathology-specific pretrained models 是否优于非病理领域预训练，并不是一个已经被系统验证的问题，尤其在 `gland` 与 `cell segmentation` 上仍缺乏直接证据。
  - 用途：`研究动机`
  - 页码：`p.1-p.3`
- 句子/事实 2：本文最终结论不是“病理预训练一定更好”，而是其收益同时依赖 `task` 和 `training dataset size`。
  - 用途：`谨慎结论`
  - 页码：`p.1, p.9`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者统一比较四类初始化：`random initialization`、`ImageNet supervised`、`ImageNet SSL` 和 `SSLPathology`。
  - 用途：`实验框架`
  - 页码：`p.3-p.4`
- 句子/事实 2：domain-specific pretraining 对 gland segmentation 尤其在小数据时有显著优势，但对 cell segmentation 并不稳定，甚至常常不如 ImageNet 初始化。
  - 用途：`核心结论`
  - 页码：`p.5-p.6`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| arXiv | `2307.03275` | 文献信息 | `p.1` |
| backbone | `ResNet50` | 模型设置 | `p.4-p.5` |
| decoder | `U-Net decoder` | 模型设置 | `p.4-p.5` |
| GlaS reported split | `88 train / 80 test` | 数据集说明 | `p.4` |
| CRAG split | `160 train / 40 test` | 数据集说明 | `p.4` |
| KUMAR | `16 train / 14 test` | 数据集说明 | `p.4` |
| CPM17 | `31 train / 31 test` | 数据集说明 | `p.4` |
| TNBC | `34 train / 16 test` | 数据集说明 | `p.4` |
| patch size | `256x256` | 训练设置 | `p.5` |
| inference overlap | `window size 128` | 推理设置 | `p.5` |
| lr | `1e-4` | 训练设置 | `p.5` |
| epochs (gland) | `4000` | 训练设置 | `p.5` |
| epochs (cell) | `2000` | 训练设置 | `p.5` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 在病理分割里，标注代价高，fine-tuning pretrained model 通常是默认选择。
- 但从自然图像学到的表示可能存在 `texture bias`，未必适合 histopathology。
- 另一方面，病理专用预训练是否真的稳定优于：
  - `ImageNet supervised`
  - `ImageNet SSL`
  - `random initialization`
  尚缺乏系统评估。
- 此外，这种收益是否能在 OOD 测试下保留，也并不清楚。

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 作者不提出新的 segmentation architecture，而是搭建一个严格受控的比较框架：对 `gland segmentation` 和 `cell segmentation` 两类任务，统一使用 `U-Net + ResNet50 backbone`，只改变 encoder 初始化方式，分别比较 `random`, `ImageNet supervised`, `ImageNet SSL (SSLImage)`, `histopathology SSL (SSLPathology)` 四类权重；同时系统改变训练数据量、训练 epoch，并做跨数据集 `OOD` 测试，从而判断病理专用预训练到底在什么条件下真正有帮助。

关键页码：

- `p.3-p.8`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`controlled comparison on identical segmentation architecture`
- 主要模块：
  - `U-Net decoder`
  - `ResNet50 encoder`
  - `four initialization schemes`
  - `in-distribution data-size experiments`
  - `OOD transfer experiments`
- Backbone：
  - `U-Net + ResNet50`
- 关键机制：
  - 固定网络结构，只更换初始化
  - gland 与 cell 分开评估
  - 数据量与训练时间双重分析

### 3.2 关键模块详细描述

**模块 1：`Common Segmentation Backbone`**

- 位置：`全部实验共享`
- 操作流程：
  1. 使用同一 `U-Net` 分割框架
  2. encoder 统一为 `ResNet50`
  3. decoder 在所有实验中保持不变
  4. 仅通过初始化差异分析 pretraining 影响
- 页码：`p.4-p.5`

**模块 2：`Initialization Families`**

- 位置：`实验变量`
- 包含：
  - `random initialization`
  - `ImageNet supervised`
  - `ImageNet SSL (SSLImage)`
  - `SSLPathology` domain-specific SSL
- 设计理由：排除结构差异，只比较预训练来源
- 页码：`p.3-p.4`

**模块 3：`Data-Size Study`**

- 位置：`主实验`
- 操作流程：
  1. 用不同百分比训练数据 fine-tune
  2. 比较各初始化在小样本与全量数据下的表现
  3. 同时观察性能方差如何随数据量变化
- 页码：`p.5-p.6`

**模块 4：`Epoch / Compute Study`**

- 位置：`训练过程分析`
- 操作流程：
  1. 比较不同训练 epoch 下各初始化的 Dice 变化
  2. 分析 domain-specific pretraining 优势是否只是“更快收敛”
  3. 结论是其收益更多与 dataset diversity / size 相关，而不单是算力
- 页码：`p.5-p.6`

**模块 5：`OOD Testing`**

- 位置：`泛化分析`
- 操作流程：
  1. 在 source dataset 上 fine-tune
  2. 直接在同任务的另一个 dataset 上测试
  3. 不对目标数据做微调
  4. 比较不同初始化下性能下降幅度
- 页码：`p.7-p.8`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| encoder | `ResNet50` | `未逐层展开` | `256x256` patch 输入 | 所有实验共用 |
| decoder | `U-Net decoder` | `未逐层展开` | 输出同输入 | 所有实验共用 |
| init 1 | random | `N/A` | `N/A` | baseline |
| init 2 | `ImageNet supervised` | `N/A` | `N/A` | Pytorch default |
| init 3 | `SSLImage` | `N/A` | `N/A` | ImageNet self-supervised |
| init 4 | `SSLPathology` | `N/A` | `N/A` | histopathology SSL |

---

## 4. 公式与推导

### 4.1 核心公式

- 本文核心贡献不在新公式，而在受控实验设计。
- 文中主要使用常规 segmentation 指标：

公式 1：

```text
Dice
```

符号说明：
- 用于衡量 segmentation overlap
- 页码：`p.5`

公式 2：

```text
Jaccard / IoU
```

符号说明：
- 用于补充 Dice
- 页码：`p.5`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本文没有设计新损失或新梯度机制。
- 实验思想是：保持 architecture 与 decoder 固定，仅改变权重初始化来源，以判断 encoder 初始表示对不同任务和数据规模的真实影响。

---

## 5. 损失函数

### 5.1 各监督项

- 正文当前抽取片段未强调特定 task loss
- 主要讨论的是：
  - 初始化方式
  - 数据量
  - epoch
  - OOD 性能变化

### 5.2 总损失公式

- `正文当前抽取片段未单独展开`
- 本篇重点不在 loss，而在相同分割模型下对不同 pretraining 的 controlled comparison

### 5.3 权重配置与调度策略

- 所有模型共享相同训练设置：
  - `lr = 1e-4`
  - gland `4000 epochs`
  - cell `2000 epochs`
- 这样可以更公平地比较初始化影响

---

## 6. 训练协议

### 6.1 数据集与划分

- gland segmentation：
  - `GlaS`
  - `CRAG`
- cell segmentation：
  - `KUMAR`
  - `CPM17`
  - `TNBC`
- 数据集细节：
  - `GlaS`: `88 train / 80 test`, 图像小于 `700x600`
  - `CRAG`: `160 train / 40 test`, 图像约 `1512x1512`
  - `KUMAR`: `16 train / 14 test`, `1000x1000`, `21623` nuclei
  - `CPM17`: `31 train / 31 test`, `500x500`, `7570` nuclei
  - `TNBC`: `34 train / 16 test`, `512x512`, `4022` nuclei
- 统一训练/验证划分：
  - `80/20` train/validation split
  - 用 validation loss 最低的模型做 test inference
- 备注：
  - `GlaS 88 train` 与常见 `85 train` 说法不一致，需保留为原文报告值，可能存在版本差异或 OCR 差异

### 6.2 数据增强

- horizontal flip
- vertical flip
- random rotation
- translation

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| architecture | `U-Net + ResNet50` |
| patch size | `256x256` |
| inference averaging window | `128` |
| learning rate | `1e-4` |
| epochs (gland) | `4000` |
| epochs (cell) | `2000` |
| repeats | `5` runs average |
| framework | `PyTorch` |
| hardware | `NVIDIA V100` |

### 6.4 预处理与数据细节

- 训练时从 whole image 中随机采样 `256x256` patch
- 推理时使用重叠窗口并对预测平均
- 所有模型在完全相同训练协议下比较，以减少实验偏差

---

## 7. 推理与后处理

- 推理时对重叠窗口预测做 averaging
- `window size = 128`
- OOD 测试时：
  - 不在 target dataset 上再 fine-tune
  - 直接评估 source-trained model 的迁移性能

---

## 8. 消融实验

### 8.1 消融设计

- 初始化方式对比：
  - `random`
  - `ImageNet supervised`
  - `SSLImage`
  - `SSLPathology`
- 数据量对比：
  - 小比例训练集 vs 全量训练集
- 训练时间对比：
  - 不同 epochs 下性能曲线
- 泛化对比：
  - OOD gland
  - OOD cell

### 8.2 各模块贡献量化

- gland segmentation：
  - 小数据时，`SSLPathology` 显著优于其他初始化
  - 数据量增加后，这种优势逐渐减弱
  - 在很小数据比例和较少 epoch 下，domain-specific pretraining 全程领先
- cell segmentation：
  - `SSLPathology` 通常与 `ImageNet` 持平或更差
  - 在 `KUMAR` 上，random initialization 甚至可竞争或更优
- OOD：
  - domain-specific pretraining 往往能减小性能下降
  - 但并不能真正消除 site bias / distribution shift

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

- 本文主要用曲线图而非主表数字展示结论，当前抽取片段没有稳定的逐点数值表。
- 可以可靠确认的核心结果是：
  - `gland segmentation` 上，小数据时 `SSLPathology` 最强
  - `cell segmentation` 上，domain-specific pretraining 不具备普适优势
  - `OOD` 下，domain-specific 初始化通常跌幅更小，但仍遭受明显分布偏移影响

### 9.2 与其他方法的对比

- 不是不同 segmentation model 的横向 SOTA 比赛
- 而是在同一 `U-Net + ResNet50` 框架里比较不同初始化
- 这使得“初始化效应”能被更清楚地单独观察

### 9.3 公平对比条件确认

- 所有模型使用同一 backbone / decoder
- 同一任务内使用相同数据划分与训练协议
- 多次重复训练并报告平均结果
- 这是本文可信度最高的部分之一

### 9.4 评价协议与指标定义

- `Dice`
- `Jaccard / IoU`
- OOD 分析看的是不同初始化在跨数据集测试时的相对性能下降

---

## 10. 计算量与效率

- 参数量：`未报告`
- FLOPs：`未报告`
- 硬件：`NVIDIA V100`
- 训练长度：
  - gland `4000 epochs`
  - cell `2000 epochs`
- 论文指出：
  - domain-specific pretraining 的收益不只是“更长训练就能替代”，因为小数据时即使随 epoch 变化它仍保持优势

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 实际比较的是四类初始化路线：
  - `train from scratch`
  - `ImageNet supervised pretraining`
  - `ImageNet SSL pretraining`
  - `histopathology-specific SSL pretraining`

### 11.2 论文指出的研究空白 / Open Problems

- 先前没有系统评估 domain-specific pretraining 在：
  - `gland segmentation`
  - `cell segmentation`
  - `OOD testing`
  三方面的真实收益边界
- 也没有明确说明“病理预训练是否对所有任务都有效”

### 11.3 对我们选题的启示

- 如果你做的是 gland segmentation，尤其数据不大，病理专用预训练值得优先考虑
- 但写论文时不能把这个结论泛化成“病理预训练对所有病理分割都更好”
- 本篇非常适合支撑更谨慎、更可信的 related work 与 discussion

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本文不讨论正式 grading system
- 但强调 gland segmentation 与 cell segmentation 都服务于自动诊断、癌症分级和患者结局预测等上层任务

### 12.2 涉及的生物标志物

- 无单一 biomarker 分析
- 更关注 representation quality 与跨站点泛化

### 12.3 临床意义

- 这篇文章的临床价值不在直接提出新病理指标，而在帮助选择更合适的初始化策略，降低小样本病理任务建模成本

---

## 13. 开源与复现

- 代码是否开源：`摘要与正文提到有 GitHub repository`
- 代码仓库地址：`当前抽取片段未给出具体 URL`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`SSLPathology 来自文献 [13] 已发布模型`
- 复现难度评估：`低-中`
- 复现障碍：
  - 具体 GitHub URL 在当前抽取片段中缺失
  - 主要数值结果以曲线图呈现，逐点数值不方便精确复写
  - OOD 结果的具体数值更多体现在图中而非表格

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| GitHub URL | 否（当前抽取片段未显示） | 只记录“有代码仓库” | 低 |
| batch size | 否 | 不脑补 | 中 |
| 具体 loss 实现 | 否 | 不写死 | 中 |
| 各数据比例实验的精确数值表 | 否，主要在曲线图中 | 记录趋势结论 | 中 |
| OOD 图中精确坐标值 | 否 | 记录相对结论 | 中 |

- 不确定但影响较大的点：
  - `GlaS 88 train` 是否为版本差异或 OCR 问题
  - 具体 patch sampling 数量
  - fine-tuning 的 early stopping 与 checkpoint 细节

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文明确承认：
  - domain-specific pretraining 的收益不是 universal
  - 它也无法真正学到 site-independent features
  - 仍会遭受与 ImageNet 权重类似的分布偏移问题

### 14.2 我们观察到的潜在问题

- 本文只覆盖：
  - semantic segmentation
  - gland / cell 两类任务
- 未覆盖：
  - multi-class semantic segmentation
  - cell detection
  - vision-language pretraining
- 因此其结论虽重要，但适用范围仍有限

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`主要通过曲线和质性图说明`
- 可从结果推断的典型难点：
  - site bias
  - 低多样性小数据
  - cell segmentation 对初始化不敏感甚至反向受益

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- encoder 初始化决策依据
- “病理预训练有条件成立”这一更严谨的写作结论
- OOD 讨论里的谨慎表述：预训练能缓解，但不能根治跨站点偏移

### 15.2 可以作为候选参数来源的

- `U-Net + ResNet50`
- `patch 256x256`
- `lr 1e-4`
- `gland 4000 epochs`
- `80/20` train/val

### 15.3 不应照搬的（及原因）

- 不应直接把“病理专用预训练更好”写成无条件结论
  - 原因：本文已明确指出 benefits are not universal
- 不应把 cell segmentation 的结论直接移植到 gland segmentation
  - 原因：任务间响应不同

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| encoder 预训练选择 | 小数据 gland 上优先考虑 domain-specific SSL | 强 |
| discussion 写作 | 预训练收益依赖 task 与 data size | 强 |
| OOD 结果解释 | 预训练可减轻但不能消除分布偏移 | 强 |
| cell/gland 区分论证 | 不能把不同病理任务混为一谈 | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`预训练策略与初始化选择`
- [ ] 需要和哪篇论文交叉验证：`03_Cerberus.md`, `12_DEA-Net.md`
- [ ] 待确认的问题：`我们是否已有可用的 pathology-specific encoder 权重`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 标注昂贵与初始化重要性 | 研究背景 |
| related work | domain-specific vs non-domain pretraining | 预训练小节 |
| 方法 | 选择某类 encoder 初始化的理由 | 实验设计依据 |
| 讨论 | 预训练收益并非 universal | 谨慎结论 |
| 局限性 | OOD 下 site bias 仍存在 | 讨论提升空间 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.2` | 研究问题与初始化选择框架 | 总体设计 |
| `Fig. 2` | `p.6` | GlaS 上不同初始化与数据量/epoch 关系 | gland 主结论 |
| `Fig. 3` | `p.6` | cell segmentation 初始化比较 | 任务差异 |
| `Fig. 4` | `p.7` | UMAP 表征分析 | latent 表征差异 |
| `Fig. 5` | `p.8` | gland OOD 测试 | 跨数据集泛化 |
| `Table 1` | `p.4` | cell datasets 统计 | 数据集说明 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 关键实验变量与结论边界已明确
- [ ] 训练参数足够完全复现（`batch size`、loss 细节未完全给出）
- [x] 预处理与数据细节已检查
- [x] 评价协议已确认
- [x] OOD 与数据量实验的结论已记录
- [x] 与我们项目的关联已具体到初始化策略
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注而未脑补

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/06_半监督_拓扑_扩展工作/04_PretrainingCaseStudy`
- `paper_type`: `planned_category:06_半监督_拓扑_扩展工作`
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

- 记录字段：`paper_id=03_文献证据/06_半监督_拓扑_扩展工作/04_PretrainingCaseStudy`；`paper_type=planned_category:06_半监督_拓扑_扩展工作`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/06_半监督_拓扑_扩展工作/04_PretrainingCaseStudy` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
