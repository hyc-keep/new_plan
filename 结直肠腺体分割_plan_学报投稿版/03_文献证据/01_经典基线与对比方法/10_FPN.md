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

- `multiscale feature fusion 论文`
- `feature pyramid / top-down lateral 论文`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`01_经典基线与对比方法`

- 按模板要求，本篇至少完成：`1, 3, 6, 7, 9, 10, 13, 15, 16`
- 因为这篇对后续多尺度特征融合与小目标/细结构检测很有启发，所以额外完成：`2, 4, 8, 14`

---

## 1. 论文信息

- 论文名：`Feature Pyramid Networks for Object Detection`
- 作者/团队：`Tsung-Yi Lin, Piotr Dollar, Ross Girshick, Kaiming He, Bharath Hariharan, Serge Belongie`
- 发表年份/会议/期刊：`2017, CVPR 2017`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:1612.03144`
- BibTeX key：`lin2017fpn`
- PDF 路径：`结直肠腺体分割_pdf库/01_经典基线与对比方法/Feature_Pyramid_Networks_for_Object_Detection_FPN_2017.pdf`
- 当前定位：`多尺度特征融合的经典来源论文；虽然原任务是 detection/segmentation proposal，但其 top-down + lateral 设计对后续分割网络的多尺度语义增强很关键`
- 与已提取论文的关系：
  - 可与：`U-Net_2015`、`DeepLabV3+_2018`、`SegFormer_2021` 形成“多尺度表示”对照
  - 结构上启发：`top-down pathway + lateral connections`
  - 用途：`支撑后续任何 feature pyramid / multi-scale fusion 模块的合理性`

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：recent detectors 避免 image pyramid 的主要原因不是它无效，而是它在计算和显存上太昂贵
  - 用途：`背景 / 痛点`
  - 页码：`Abstract, p.1`
- 句子/事实 2：ConvNet 自身就有 pyramidal hierarchy，但高分辨率层语义弱、低分辨率层语义强，因此存在 semantic gap
  - 用途：`方法动机`
  - 页码：`p.1-p.3`
- 句子/事实 3：FPN 通过 top-down pathway 与 lateral connections，让所有尺度都具有更强语义，并且只带来 marginal extra cost
  - 用途：`方法概述`
  - 页码：`Abstract, p.2-p.4`

#### 1.1.2 related work 可引用句

- 句子/事实 1：FPN 与只输出单张高分辨率特征图的 top-down/skip 方法不同，它在每个 pyramid level 上都独立做预测
  - 用途：`related work / 结构差异`
  - 页码：`p.2-p.3`
- 句子/事实 2：仅有 top-down 没有 lateral 不够，因为多次下采样再上采样后的定位不精确，lateral features 对精确定位非常重要
  - 用途：`结构设计依据`
  - 页码：`p.4-p.6`
- 句子/事实 3：FPN 在不增加测试时间的情况下，相比 single-scale baseline 提升 detection AP 与 proposal AR
  - 用途：`实验结果概述`
  - 页码：`p.2, p.5-p.8`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 输入短边 | `800` | 训练/测试设置 | `p.5-p.7` |
| optimizer | `synchronized SGD` | 训练设置 | `p.5-p.7` |
| momentum | `0.9` | 训练设置 | `p.5-p.7` |
| weight decay | `0.0001` | 训练设置 | `p.5-p.7` |
| RPN 学习率 | `0.02 -> 0.002` | proposal 训练 | `p.5` |
| Fast R-CNN 学习率 | `0.02 -> 0.002` | detection 训练 | `p.6-p.7` |
| Anchor area | `{32^2, 64^2, 128^2, 256^2, 512^2}` | pyramid anchor design | `p.4` |
| Pyramid levels | `P2, P3, P4, P5, P6` | 多尺度表示 | `p.4-p.5` |
| FPS | `6 FPS` | 实用效率 | `Abstract, p.1` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 目标检测与分割面临强烈的尺度变化问题
- 传统 image pyramid 很有效，但太慢、太耗显存，而且训练时通常无法端到端使用
- ConvNet 自带 feature hierarchy，但不同层存在明显 semantic gap：
  - 高分辨率层定位准，但语义弱
  - 低分辨率层语义强，但定位粗
- 需要一种方式，在单尺度输入下也能构建“所有尺度都语义强”的 feature pyramid

对应原文依据（页码）：

- `Abstract, p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- FPN 以 backbone 的 pyramidal hierarchy 为基础，从高层语义强的低分辨率特征出发，沿 top-down pathway 逐级上采样，再通过 lateral connections 与底层高分辨率特征相加，从而构造 `P2-P5` 多个既具定位精度又具较强语义的 feature maps，并在各 level 独立进行预测。

关键页码：

- `p.2-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`bottom-up backbone + top-down pathway + lateral connections`
- Backbone：`ResNet`
- Bottom-up 特征：`C2, C3, C4, C5`
- 输出 pyramid：`P2, P3, P4, P5`，并额外构造 `P6`
- 关键目标：`high-level semantics at all scales`

### 3.2 关键模块详细描述

**模块 1：`Bottom-up Pathway`**

- 位置：`backbone 主干`
- 操作流程：
  1. 正常执行 ResNet 前向传播
  2. 取各 stage 最深层输出作为 `C2-C5`
  3. 它们相对输入图像的 stride 分别为 `{4, 8, 16, 32}`
- 页码：`p.4`

**模块 2：`Top-down Pathway`**

- 位置：`由高层向低层传播语义`
- 操作流程：
  1. 从高层 coarse but semantic-rich feature 开始
  2. 逐级做 `2×` 上采样
  3. 将高层语义传播到更高分辨率层
- 页码：`p.4-p.5`

**模块 3：`Lateral Connections`**

- 位置：`top-down 与 bottom-up 同尺度融合处`
- 操作流程：
  1. 用 `1×1 conv` 先把 bottom-up 特征通道统一
  2. 与上采样后的 top-down 特征逐元素相加
  3. 再用 `3×3 conv` 减少上采样带来的 aliasing
- 页码：`p.4-p.5`

**模块 4：`Prediction on Each Pyramid Level`**

- 位置：`P2-P6`
- 操作流程：
  1. 在每个 pyramid level 上独立做 RPN / detection prediction
  2. 把不同尺度对象分配到不同 level
  3. 用 pyramid 而不是单层大特征图处理尺度变化
- 页码：`p.3-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| bottom-up levels | `C2, C3, C4, C5` | backbone multi-stage features | `p.4` |
| output pyramid | `P2, P3, P4, P5` | 多尺度语义特征 | `p.4-p.5` |
| extra level | `P6 = stride-2 subsampling of P5` | 更大尺度对象 | `p.4-p.5` |
| upsampling | `2× nearest neighbor` | top-down pathway | `p.4-p.5` |
| lateral conv | `1×1` | 通道对齐与语义融合 | `p.4-p.5` |
| smoothing conv | `3×3` | 抑制 aliasing | `p.4-p.5` |
| anchor areas | `{32^2,64^2,128^2,256^2,512^2}` on `P2-P6` | 多尺度 RPN | `p.4` |

说明：

- 论文最关键的结构点不是单纯“用多层特征”，而是：
  - 自顶向下传播强语义
  - 再通过 lateral 纠正定位
  - 最终让每层都可独立承担预测任务

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
k = k0 + log2( sqrt(w*h) / 224 )
```

符号说明：

- `w, h`：RoI 的宽和高
- `224`：canonical ImageNet pre-training size
- `k0`：参考 level，论文设为 `4`
- 含义：根据 RoI 尺度将其映射到合适的 pyramid level
- 页码：`p.4`

### 4.2 推导过程或梯度行为

- FPN 的逻辑不是复杂数学推导，而是多尺度表达的结构性修复
- 没有 lateral 时：
  - top-down 特征语义强
  - 但定位不准，因为已多次下采样再上采样
- 仅用最细层 `P2` 也不够：
  - 虽然高分辨率，但 scale robustness 不如跨层 pyramid
- 因此 FPN 的实质是把 `semantic strength` 与 `localization precision` 在每个层级重新配平

对应页码：

- `p.5-p.7`

---

## 5. 损失函数

### 5.1 各监督项

- 论文本体不在新 loss，而在 feature pyramid 结构
- 使用的是对应 detection / RPN / proposal 任务的标准监督
- 这里更适合把它当结构论文，而不是 loss 论文

### 5.2 总损失公式

- 主文未把创新点放在总损失形式上
- 如果后续要严格复现，应回到 Faster R-CNN / RPN 原始监督项

### 5.3 权重配置与调度策略

- 无特别强调新的 loss reweighting
- 训练重点是：
  - pyramid level 分配
  - anchor 设计
  - end-to-end 多层联合训练

---

## 6. 训练协议

### 6.1 数据集与划分

- 主要 benchmark：`COCO`
- 任务包括：
  - bounding box proposals
  - object detection
  - mask proposals / instance segmentation proposals

### 6.2 数据增强

- 主文没有复杂增强列表
- 关键 preprocessing 是将输入图像短边 resize 到 `800`

### 6.3 优化器与超参数

| 项目 | 数值/策略 | 页码 |
|------|-----------|------|
| 输入短边 | `800` | `p.5-p.7` |
| optimizer | `synchronized SGD` | `p.5-p.7` |
| momentum | `0.9` | `p.5-p.7` |
| weight decay | `1e-4` | `p.5-p.7` |
| RPN batch | `2 images / GPU, 256 anchors / image` | `p.5` |
| RPN lr | `0.02 for 30k, 0.002 for 10k` | `p.5` |
| Fast R-CNN batch | `2 images / GPU, 512 RoIs / image` | `p.6-p.7` |
| Fast R-CNN lr | `0.02 for 60k, 0.002 for 20k` | `p.6-p.7` |
| RPN training time | `~8 hours on COCO` | `p.5` |
| Fast R-CNN training time | `~10 hours on COCO` | `p.6-p.7` |

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；本文是自然图像检测`
- 颜色空间转换：`未强调`
- resize / crop / pad 策略：`shorter side = 800`
- patch overlap：`不适用`
- 背景过滤策略：`RPN/anchor sampling based`
- 标签生成方式：`bounding boxes / mask proposals`
- 类别不平衡处理：`沿用检测框架默认采样策略`
- 随机种子/重复次数：`未见强调`
- 数据泄漏风险点：`主要是 detection benchmark 协议，不直接对应病理 patient-level 问题`

---

## 7. 推理与后处理

- 使用单尺度输入，而不是显式 image pyramid
- 在各 pyramid levels 上独立做预测
- `P6` 用于更大 anchor 范围
- 论文强调：
  - 训练/测试时都可一致使用 feature pyramid
  - 不像 image pyramid 那样只在 test-time 上额外加多尺度

---

## 8. 消融实验

### 8.1 消融设计

- `single-scale baseline` vs `FPN`
- `top-down without lateral`
- `only P2`
- `bottom-up pyramid only`
- 在 RPN 与 Fast R-CNN 两个层面都做 ablation

### 8.2 各模块贡献量化

- bounding box proposals：
  - FPN 相对 single-scale RPN baseline，`AR1k +8.0`
- object detection：
  - COCO-style `AP +2.3`
  - PASCAL-style `AP +3.8`
- 去掉 lateral：
  - 性能明显下降，说明仅靠 top-down 不够
- 只用最细层 `P2`：
  - 好于 baseline，但仍不如完整 pyramid

关键表中可直接引用：

- `Table 1(c)`：完整 FPN proposal 效果最好
- `Table 1(e)`：去掉 lateral 后显著变差
- `Table 2(c)`：all pyramid levels 优于单层
- `Table 2(f)`：only P2 marginally worse than full pyramid

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 场景 | 结果 | 页码 |
|------|------|------|
| COCO detection benchmark | `state-of-the-art single-model result` | `Abstract, p.1-p.2, p.7-p.8` |
| bounding box proposals | `AR1k +8.0 over single-scale baseline` | `p.2, p.5-p.6` |
| object detection | `COCO AP +2.3`, `PASCAL AP +3.8` | `p.2` |
| runtime | `6 FPS on a GPU` | `Abstract, p.1` |

### 9.2 与其他方法的对比

- 与显式 image pyramid 相比：
  - 训练/测试更一致
  - 显存和时间开销更低
- 与 single-scale Faster R-CNN baseline 相比：
  - proposal AR 与 detection AP 都更高
- 与 SSD 风格多层预测相比：
  - FPN 更充分复用了高分辨率 backbone features
  - 不是从高层往下新堆额外层，而是把已有 hierarchy 语义增强后再使用

### 9.3 公平对比条件确认

- 优势：
  - 基于标准 Faster R-CNN / RPN 框架
  - 与强 baseline 同 backbone 对比
  - 把速度和精度一起报告
- 需要注意：
  - 原始任务是 detection，不是语义分割
  - 但其结构思想对多尺度分割模块仍然非常有借鉴价值

### 9.4 评价协议与指标定义

- `AR`：Average Recall，用于 proposal 评价
- `AP`：Average Precision，用于 detection 评价
- 同时关注：
  - `APs / APm / APl`
  - `ARs / ARm / ARl`
- 说明：FPN 特别强调对小目标的提升，小尺度指标很关键

---

## 10. 计算量与效率

- 核心卖点之一是：
  - 相比 image pyramid，额外计算代价很小
  - 相比 single-scale baseline，精度提升但测试时间几乎不增加
- 运行速度：
  - `6 FPS on GPU`
- 对我们项目的意义：
  - 多尺度特征融合并不一定意味着显著更重
  - 合理的 top-down + lateral 设计可以用较低成本增强小结构与细边界表示

---

## 13. 开源与复现

- 开源情况：`是`
- 复现难度：`中`
- 关键难点：
  - level assignment
  - anchor design
  - 与 RPN / detector head 的接口
- 对分割项目来说，真正可迁移的是结构思想，而不是原始 detection pipeline 全套实现

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `后续复现需固定` | `中` |
| 验证集划分 | `按 COCO 协议` | `病理任务不可直接照搬` | `高` |
| 推理阈值 | `检测框架相关，未在主文展开` | `不作为当前提取重点` | `中` |
| 后处理细节 | `检测 pipeline 默认` | `结构迁移时不必强行保留` | `中` |
| 训练停止准则 | `是（给出迭代与 lr schedule）` | `作为结构论文参考足够` | `低` |
| 数据预处理 | `是（short side 800）` | `病理任务需自己定义 resize/patch 策略` | `高` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文主场景是 detection / proposal，不直接针对分割边界质量展开
- 需要与具体 task head 联合使用，FPN 本身不是完整任务网络

### 14.2 我们观察到的潜在问题

- 腺体分割中目标不是 box-level small objects，而是细胞/腺体形态、边界与粘连分离
- 直接照搬 FPN 检测式 multi-level assignment 不一定适合病理语义/实例分割
- 但 `semantic strengthening of high-resolution features` 这一思想仍然很强

### 14.3 失败案例 / 定性分析

- 没有 lateral 时性能明显掉，说明单纯上采样语义不够
- 只用最细层也不如完整 pyramid，说明 scale robustness 不能只靠高分辨率
- 对我们任务的映射：
  - 细边界任务既需要高分辨率，又需要高层语义
  - 这正是 FPN 结构启发最适合回填的地方

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `top-down pathway + lateral connections`
- 对高分辨率低语义特征做语义增强
- 用多尺度预测/融合代替单层硬扛全部尺度

### 15.2 可以作为候选参数来源的

- 多尺度 level 设计思路：`P2-P5 / P6`
- `1×1 lateral + 3×3 smoothing`
- 单尺度输入下构建 in-network pyramid 的思想

### 15.3 不应照搬的（及原因）

- 原始 anchor、RoI、proposal 机制：
  - 这些属于 detection 特有设置
- 直接按 box size 做 level assignment：
  - 病理分割里更可能按 feature scale 或 object morphology 做适配

### 15.4 对我们具体模块的支撑

- 对 `多尺度特征融合`：
  - 是最经典直接的结构来源
- 对 `小腺体/细边界`：
  - 能支持“高分辨率层需要更强语义”的论点
- 对 `相关工作写作`：
  - 可以把它写成 CNN 时代多尺度表示的经典里程碑，再过渡到后续 `DeepLab / SegFormer / U-Net family`

### 15.5 后续行动项

- 当前 `01_经典基线与对比方法` 已可作为一个相对完整的经典/外部对比证据包
- 下一步可切换到：
  - `02_边界_形状_损失支撑`
  - 或把当前 10 篇提取内容回填进 `01_实验执行`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 多尺度识别与 image pyramid 代价问题 | 解释多尺度模块动机 |
| related work | CNN 多尺度 feature pyramid 经典路线 | 放在多尺度特征融合小节 |
| 方法 | top-down + lateral 模块设计依据 | 作为结构启发，不写成直接复现 |
| 实验设置 | 小目标与多尺度指标的评价意识 | 用于结果分析框架 |
| 讨论 | 高分辨率层语义弱、低分辨率层定位差的矛盾 | 用来解释边界和小结构问题 |

---

## 16. 关键图表索引

| 图/表 | 内容 | 用途 |
|------|------|------|
| `Figure 1` | image pyramid / single-scale / hierarchy / FPN 对比 | 写动机时最关键 |
| `Figure 2` | 与普通 top-down skip 架构的区别 | 写结构定位 |
| `Figure 3` | top-down + lateral building block | 回填模块设计 |
| `Table 1` | proposal 消融 | 说明 lateral / pyramid 必要性 |
| `Table 2` | detection 消融 | 说明完整 FPN 优于单层 |
| `Table 4` | COCO 单模型主结果 | 写 benchmark 结论 |

---

## 17. 提取质量自检

- [x] 所有数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现（optimizer+lr schedule+输入尺度）
- [x] 预处理与数据细节已检查（short side / anchors / levels）
- [x] 结果数字与原文 table 一致（已核对关键项）
- [x] 指标定义和评价协议已确认（AR / AP）
- [x] 消融实验的结论已量化（不只是“有效”）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`

---

## 证据状态与当前消费边界

- `paper_id`: `03_文献证据/01_经典基线与对比方法/10_FPN`
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

- 记录字段：`paper_id=03_文献证据/01_经典基线与对比方法/10_FPN`；`paper_type=planned_category:01_经典基线与对比方法`；`evidence_status=unverified`；`formal_result=not_run`；`result_eligibility=false`；`quoted_or_reproduced=quoted_from_original_paper/reference_only`。
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
| `03_文献证据/01_经典基线与对比方法/10_FPN` 原单篇文献稿 | 原正文全部既有章节；本区追加状态边界 | 文件质量自检 | `partial_pending_manual_source_review` | 逐篇 PDF、空白字段、指标/split、代码状态尚待人工核验 | 已完成结构化补齐，保持 `unverified/blocked` |
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
