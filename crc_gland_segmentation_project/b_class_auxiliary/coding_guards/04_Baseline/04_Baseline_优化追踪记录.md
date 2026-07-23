# 04_Baseline 优化追踪记录

## 1. 文档角色

- 当前 active plan: `/home/featurize/work/Paper/结直肠腺体分割_plan_优化版`
- 当前 active project: `/home/featurize/work/Paper/crc_gland_segmentation_project`
- 当前阶段: `04_Baseline`
- 当前优化对象: `B1 ResNet34-U-Net`
- 对照对象: `A2 UNet`
- 本文件用途: 持续记录 04 阶段原计划、历史结果、失败原因、每轮优化变量、实际结果和最终裁决，防止重复尝试、遗忘失败证据或混用不同 protocol。
- 本文件不负责: 修改历史结果、替代阶段实现卡、替代 Gate 报告、提前宣称 04 通过或直接生成论文结论。

## 2. 原计划状态

原计划文件：

- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/01_R34UNet结构与来源.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/03_对比与判断规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`

### 2.1 原计划科学目标

在 A2 UNet 已冻结的 GlaS 数据、训练、评估和统计边界下，只把 plain encoder 升级为 ResNet34 residual encoder，同时保留 U-Net 风格 decoder、skip connection 和单通道 segmentation logit，建立后续模块统一使用的结构 baseline。

原计划不是理论上错误的方案。ResNet34-U-Net 作为结构升级具有明确的 ResNet residual learning 和 U-Net encoder-decoder 依据，且与 GlaS 对象级评估任务匹配。

### 2.2 原计划固定项

```text
GlaS train68 / val17 / TestA60 / TestB20
RGB, 512 x 512
ImageNet mean/std
light_aug_v1
BCE + Dice
AdamW, lr=1e-3, weight_decay=1e-4
ReduceLROnPlateau, monitor=val_objdice
max_epoch=120, early stopping=20
AMP on
best_selector=val_objdice_max
threshold_source=val17
threshold_value=0.5
TestA/TestB separate
mean/std = three-seed arithmetic mean and np.std(ddof=0)
seeds = 3407 / 1234 / 2025
```

B1 原计划默认继承 A2 的训练与评估协议；因此 v1 中 encoder 和 decoder 使用统一学习率 `1e-3`，physical batch 为 `2`，没有梯度累积。

### 2.3 原计划 Gate

原计划要求：

```text
Gate_B1_compare
= complete_runs
  AND proto_consistent
  AND fair_compare
  AND standard_identity_ok
  AND aggregate_ready
  AND main_metrics_not_worse
  AND stability_not_weaker
  AND qualitative_support_ready
```

稳定性子门要求六个主指标单元全部满足：

```text
{F1, Object Dice, Object Hausdorff}
× {TestA, TestB}

sigma_B1 <= sigma_A2 + 1e-12 * max(1, sigma_A2)
```

该规则是项目内部保守验收门，不是 GlaS 论文或统计学规定的唯一科学标准；但历史 v1 必须按原规则如实记录，不能事后放宽。

## 3. 历史 v1 实验结果

### 3.1 v1 运行身份

```text
stage = B1
model = resnet34_unet
config_version = current_standard
train_proto_version = train_proto_v1
eval_proto_version = eval_proto_v1
seeds = 3407 / 1234 / 2025
result_tag = fresh_current_round
aggregation = single_seed
```

三组正式 run：

- `B1_ResNet34_UNet_GlaS_seed3407`
- `B1_ResNet34_UNet_GlaS_seed1234`
- `B1_ResNet34_UNet_GlaS_seed2025`

### 3.2 v1 TestA mean±std

| 指标 | B1 TestA mean±std | A2 对照 | v1 判断 |
|---|---:|---:|---|
| F1 | 0.7498 ± 0.0090 | 以当前 A2 表为准 | 主要均值方向通过 |
| Object Dice | 0.8359 ± 0.0057 | 以当前 A2 表为准 | 主要均值方向通过 |
| Object Hausdorff | 67.3310 ± 1.6289 | 以当前 A2 表为准 | 主要均值方向通过 |
| Dice | 0.9169 ± 0.0041 | 以当前 A2 表为准 | 通过 |
| IoU | 0.8535 ± 0.0047 | 以当前 A2 表为准 | 通过 |
| HD95 | 33.3530 ± 1.5259 | 以当前 A2 表为准 | 通过 |
| Boundary F1 | 0.7616 ± 0.0086 | 以当前 A2 表为准 | 通过 |

### 3.3 v1 TestB mean±std

| 指标 | B1 TestB mean±std | v1 判断 |
|---|---:|---|
| F1 | 0.6726 ± 0.0169 | 均值方向通过，波动需随主门核对 |
| Object Dice | 0.8225 ± 0.0143 | **std 超过 A2，明确失败项** |
| Object Hausdorff | 97.6961 ± 6.4103 | 均值方向通过，波动需随主门核对 |
| Dice | 0.9136 ± 0.0062 | 通过 |
| IoU | 0.8500 ± 0.0097 | 通过 |
| HD95 | 25.6997 ± 2.7903 | 通过 |
| Boundary F1 | 0.7090 ± 0.0083 | 通过 |

### 3.4 失败主指标的 raw 值

B1 TestB Object Dice：

```text
seed3407 = 0.8422597506
seed1234 = 0.8087669111
seed2025 = 0.8163788191
B1 std = 0.0143354032
A2 std = 0.0121463119
```

最大 seed 间差值约为 `0.0335`。TestB 只有 20 张图，现有错误案例主要集中于 `adhesion_merge` 等困难模式，说明少数黏连样本对 seed 轨迹较敏感。

### 3.5 v1 Gate 状态

```text
complete_runs = true
proto_consistent = true
fair_compare = true
standard_identity_ok = true
aggregate_ready = true
main_metrics_not_worse = true
qualitative_support_ready = true
baseline_assets_ready = true
freeze_ready = true
stability_not_weaker = false
gate_b1_compare = false
gate_b1 = false
stage_pass_b1 = false
handoff_ready_for_c1 = false
baseline_status = valid_with_stability_warning
stability_warning = true
conditional_research_execution = allowed_with_boundary; not_formal_handoff
```

**v1 裁决：不通过，但实验资产有效，可保留为带稳定性 warning 的历史 baseline。**

## 4. 已完成的代码与评估排查

当前工程已核对：

- `src/models/resnet34_unet.py` 的 ResNet34-U-Net 结构和单通道输出存在；
- LKMA、Boundary Head、Distance Head 默认关闭，未发现意外混入 B1；
- ImageNet ResNet34 预训练入口存在；
- seed 设置覆盖 Python、NumPy、Torch、CUDA，并启用 deterministic 设置；
- train loader 有显式 generator，验证/测试使用 `shuffle=False`；
- best checkpoint 按 `val_objdice` 选择；
- threshold 来源为 val17，值为 0.5；
- TestA/TestB 分开评估；
- 三组 checkpoint identity 已通过；
- 当前没有发现明确的指标公式错误、checkpoint 错载、测试集调阈值或评估 split 合并问题。

### 4.1 当前最可信的风险

```text
预训练 encoder 全量微调
+ encoder/decoder 统一 lr=1e-3
+ physical batch=2
+ encoder 与 decoder 使用 BatchNorm
+ 最后 batch 未明确 drop_last
+ TestB 样本量较小且困难样本敏感
```

这些是训练稳定性风险，不是已经确认的致命代码 bug。当前不能把失败简单归因于“模型不科学”或“指标代码错误”。

## 5. 已排除和禁止的伪修复

以下尝试不允许作为优化：

- 删除表现较差的 seed；
- 只保留最好 seed；
- 修改 `np.std(ddof=0)` 为其它统计口径；
- 调大 Gate 容差直到通过；
- 在 TestB 上重新搜索 threshold；
- 合并 TestA/TestB；
- 用历史 protocol_v3 数值替换 current_standard v1 数值；
- 手工修改 CSV、summary、manifest 或 Gate 字段；
- 只重跑 B1、却继续声称与 A2 完全公平；
- 同一轮同时修改 lr、BN、batch、scheduler 和 loss，导致无法归因。

## 6. 优化轮次总表

| 轮次 | 状态 | 唯一变量 | A2/B1 运行 | 结果 | Gate | 裁决 |
|---|---|---|---|---|---|---|
| v1 `current_standard` | 已完成 | B1 继承 A2 全部训练协议；统一 lr=1e-3 | A2 v1 / B1 v1 三 seed历史结果 | TestB Object Dice std=0.0143354，高于 A2=0.0121463 | `false` | 保留为 `valid_with_stability_warning` |
| v2 `baseline_stability_v2_lr` | 已完成 | encoder lr=1e-4；decoder lr=1e-3；两个 optimizer parameter groups | A2_v2 / B1_v2 各三 seed 已成对完成 | 六个稳定性单元 4 pass、2 fail；独立指标复核 pass | `false` | 保留为 `valid_with_stability_warning`；正式 current 汇总/Gate 链尚需按 v2 identity 重建 |
| v3 BN 独立候选 | 研究定标完成，待阶段锁定 | 仅冻结 B1 预训练 encoder BN running statistics；affine 可训练；decoder BN 不变 | v3 公平对照与成对边界须在阶段实现卡锁定 | 未运行 | 待运行 | 不得与 GroupNorm、batch 或 scheduler 同轮混合 |
| v4 effective batch 候选 | 未开始 | 仅修改 effective batch/grad accumulation | 只有前轮有明确依据后才决定 | 待运行 | 待运行 | 必须记录 physical/effective batch |
| v5 scheduler 候选 | 未开始 | 仅修改 scheduler/early stopping 联动 | 只有训练曲线证明需要时才决定 | 待运行 | 待运行 | 必须先有曲线证据 |

## 7. 当前确定的 v2 方案

### 7.1 v2 唯一训练变量

```text
protocol_version = train_proto_v2
config_version = baseline_stability_v2_lr
encoder_lr = 1e-4
decoder_lr = 1e-3
optimizer = AdamW
weight_decay = 1e-4
```

实现上必须使用两个明确 parameter groups：

```text
encoder parameters -> lr=1e-4
decoder/head parameters -> lr=1e-3
```

### 7.2 v2 不变项

```text
seeds = 3407 / 1234 / 2025
split = GlaS train68/val17/TestA60/TestB20
input = RGB, 512 x 512
normalization = ImageNet mean/std
augmentation = light_aug_v1
loss = BCE + Dice
physical batch = 2
no gradient accumulation in first v2 round
AMP = on
scheduler = ReduceLROnPlateau
scheduler monitor = val_objdice
epoch_max = 120
early_stop_patience = 20
best selector = val_objdice_max
threshold source = val17
threshold value = 0.5
TestA/TestB = separate
mean/std = np.std(ddof=0)
```

### 7.3 v2 公平比较要求

由于 v2 改变训练协议，不能只重新训练 B1。必须执行：

```text
A2_v2: seed3407 / seed1234 / seed2025
B1_v2: seed3407 / seed1234 / seed2025
```

A2_v2 与 B1_v2 使用同一 v2 训练控制协议，唯一结构差异仍为 plain encoder 与 ResNet34 residual encoder。

### 7.4 v2 验收输出

每个 run 必须保存：

- config.yaml；
- run_meta.yaml；
- train_log.csv；
- val_metrics.csv；
- best.ckpt 和 last.ckpt；
- learning-rate/训练曲线；
- TestA/TestB raw metrics；
- predictions、GT、overlay；
- error_cases；
- checkpoint identity；
- 权重来源和缓存信息。

汇总必须保存：

- A2_v2/B1_v2 per-seed raw 表；
- A2_v2/B1_v2 mean±std 表；
- v2 comparison 表；
- 六个主稳定性单元的逐项 Gate；
- v1 与 v2 分离的 lineage 和裁决记录。

## 8. v2 结果判定规则

### 8.1 通过条件

v2 只有在以下条件同时满足时，才允许把 B1 v2 记为正式通过：

- A2_v2、B1_v2 各三个 seed 完整；
- protocol、config、run_meta、manifest、checkpoint identity 一致且可追溯；
- TestA/TestB 独立；
- 主要指标均值方向不出现无解释退化；
- 六个主稳定性单元按原始 `ddof=0` 规则逐项通过；
- 预测、可视化、错误案例和独立指标复核完成；
- v1 warning 保留在 lineage 中，不被删除。

### 8.2 仍失败时的判定

如果 v2 仍有 std 失败：

- 不修改 v2 统计规则；
- 不把 v2 写成正式通过；
- 记录失败指标和 raw seed；
- 根据训练曲线判断是否进入 v3 BN 独立候选；
- 若 v2 均值和资产仍成立，可保留为 `valid_with_stability_warning`；
- 只有经过单变量、成对运行和完整记录，才允许调整下一训练变量。

## 9. 论文写作边界

v1、v2 都是真实、可复核的实验轮次，但都必须报告：

- 三 seed raw 或 mean±std；
- TestA/TestB 分开；
- v1 的 TestB Object Dice stability warning；
- v2 的 TestB Object Dice 与 Object Hausdorff stability warning；
- B1 主要均值优于 A2，但原项目 Gate 仍为 `false`；
- 不能写成“稳定性完全通过”“统计显著优于 A2”或“BN 已被证明是唯一根因”。

v2 逐病例诊断显示 TestB-9、14、15 等粘连病例对跨 seed 波动贡献较大；单独移除 TestB-9 后两个 Gate 仍失败。该 leave-out 结果只用于机制诊断，正式报告和 Gate 必须保留全部 20 张 TestB。

## 10. 当前下一步

1. 以更新后的 `研究定标记录.md` 运行 research alignment gate，确认 v3 只允许进入阶段锁定。
2. 在 v3 阶段实现卡中冻结：仅 B1 encoder BN running statistics 固定、BN affine 参数继续训练、decoder BN 不变；不得同时引入 GroupNorm、梯度累积或 scheduler 变化。
3. 把 `scripts/summarize_stage.py` 的旧 `current_standard` 硬编码、旧 A2 聚合表消费和 aggregate identity 缺失列为正式运行前 blocker；禁止再用 v1 summary 裁决 v2/v3。
4. 完成 stage definition gate、Pre-check、stage contract、最小 runtime 和 smoke 后，才允许修改并冻结正式代码/config。
5. 是否需要 A2/B1 全部成对运行及 A2 的 no-op BN policy 身份，必须由阶段锁定明确，不能在训练中临时决定。
6. v3 真实运行后重新生成 current-round raw、mean/std、comparison、manifest、Gate、error cases 和独立指标核验。
7. 若 v3 仍失败，不再重复相同 protocol；保留 `valid_with_stability_warning`，按治理边界决定条件性后续研究，而不是无限重训。

## 16. 记录规则

- 每一轮优化使用新 protocol/config/run lineage；
- 每一轮必须写明唯一变化、未变化项、A2/B1 是否成对运行、结果和 Gate；
- 失败轮次不得删除、覆盖或改写为通过；
- 新旧结果不得混入同一聚合表；
- 本文件是 04 优化历史的唯一追踪入口；
- 任何新增尝试必须先追加方案，再实施，不允许先训练后补写理由。

## 12. v2 正式运行结果与裁决

### 12.1 v2 运行身份

```text
stage = A2/B1 paired baseline stability recovery
model_pair = plain UNet vs ResNet34-UNet
config_version = baseline_stability_v2_lr
train_proto_version = train_proto_v2
eval_proto_version = eval_proto_v1
result_tag = fresh_v2_round
seeds = 3407 / 1234 / 2025
optimizer = AdamW
encoder_lr = 1e-4
decoder_head_lr = 1e-3
batch_size = 2
threshold_source = val17
threshold_value = 0.5
aggregation = three-seed arithmetic mean and np.std(ddof=0)
```

v2 成对正式 run 已全部完成训练、测试和独立 PNG+GT 指标复核：

- A2：`A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`
- B1：`B1_ResNet34_UNet_GlaS_seed3407`、`B1_ResNet34_UNet_GlaS_seed1234`、`B1_ResNet34_UNet_GlaS_seed2025`

每个 run 的 TestA/TestB 样本数分别为 60/20；六个 run 的独立指标复核均为 `pass`，`mismatch_count=0`，`missing_assets=[]`。

### 12.2 v2 三 seed mean±std

以下数值由当前 v2 raw metrics CSV 重新计算，统计为每个 seed 的 split 均值再进行三 seed arithmetic mean 和 `np.std(ddof=0)`；不消费旧 protocol_v1 汇总表。

| Split | 指标 | A2 mean±std | B1 mean±std | B1-A2 mean |
|---|---|---:|---:|---:|
| TestA | F1 | 0.595213 ± 0.055109 | 0.738286 ± 0.017031 | +0.143073 |
| TestA | Object Dice | 0.741033 ± 0.030601 | 0.835188 ± 0.007975 | +0.094155 |
| TestA | Object Hausdorff | 110.528880 ± 8.794409 | 70.328682 ± 1.549506 | -40.200198 |
| TestA | Dice | 0.871104 ± 0.019733 | 0.910468 ± 0.001200 | +0.039364 |
| TestA | IoU | 0.782724 ± 0.030022 | 0.841319 ± 0.002227 | +0.058595 |
| TestA | HD95 | 52.686882 ± 2.839209 | 39.590348 ± 4.467097 | -13.096534 |
| TestA | Boundary F1 | 0.643825 ± 0.039491 | 0.740226 ± 0.003303 | +0.096400 |
| TestB | F1 | 0.617727 ± 0.027102 | 0.687981 ± 0.013469 | +0.070254 |
| TestB | Object Dice | 0.786685 ± 0.005803 | 0.805857 ± 0.013450 | +0.019172 |
| TestB | Object Hausdorff | 110.406233 ± 2.896245 | 105.115628 ± 8.198661 | -5.290605 |
| TestB | Dice | 0.875933 ± 0.007439 | 0.897148 ± 0.009035 | +0.021215 |
| TestB | IoU | 0.790846 ± 0.012111 | 0.822502 ± 0.012679 | +0.031655 |
| TestB | HD95 | 41.609251 ± 3.016969 | 40.386122 ± 6.565570 | -1.223128 |
| TestB | Boundary F1 | 0.634658 ± 0.015361 | 0.684853 ± 0.007983 | +0.050195 |

### 12.3 v2 六项稳定性 Gate

原计划规则保持不变：主稳定性单元要求 `sigma_B1 <= sigma_A2`，统计使用 `np.std(ddof=0)`。不能因为 v2 仍有失败就修改统计口径或放宽阈值。

| 稳定性单元 | A2 std | B1 std | 裁决 |
|---|---:|---:|---|
| TestA F1 | 0.055109 | 0.017031 | pass |
| TestA Object Dice | 0.030601 | 0.007975 | pass |
| TestA Object Hausdorff | 8.794409 | 1.549506 | pass |
| TestB F1 | 0.027102 | 0.013469 | pass |
| TestB Object Dice | 0.005803 | 0.013450 | **fail** |
| TestB Object Hausdorff | 2.896245 | 8.198661 | **fail** |

v2 的真实裁决：

```text
complete_runs = true
proto_consistent = true
fair_compare = true
aggregate_ready = true
main_metrics_not_worse = true
independent_metric_recheck = pass
stability_not_weaker = false
gate_b1_compare = false
gate_b1 = false
stage_pass_b1 = false
baseline_status = valid_with_stability_warning
handoff_ready_for_c1 = false
```

### 12.4 v2 科学解释边界

- v2 不是训练链失败：六个 run 均完整，测试资产完整，PNG+GT 独立复核全部通过。
- B1 的 TestA/TestB 主要指标均值均优于 A2，说明 ResNet34-U-Net 作为结构 baseline 的性能改善得到当前三 seed 结果支持。
- v2 仍不能宣称稳定性完全通过；TestB 的 Object Dice 和 Object Hausdorff 跨 seed 波动高于 A2。
- 这两个失败项说明当前项目自定义的“B1 六个 std 必须不高于 A2”保守门仍未满足；不能把它直接等同于模型不科学、指标实现错误或论文统计显著性失败。
- TestB 只有 20 张困难样本，当前现象与困难样本对 seed 敏感的诊断一致，但该因果解释尚未由单变量实验完全证明。
- v1 warning 和 v2 warning 都必须保留在 lineage 中；不得用 v2 结果覆盖 v1，也不得把 v2 写成正式 Gate 通过。

## 13. v2 之后的处理决定

v2 已经回答了原优化问题的一部分：差分学习率使 B1 的均值和大部分稳定性单元出现明显改善，但没有解决 TestB 的两个稳定性单元；这不是统计显著性结论。因此不应无目的地重复同一套训练。

进一步核查表明：

- TestB Object Dice 中，B1 std 从 v1 的 `0.014335` 降至 v2 的 `0.013450`，失败差距扩大主要因为 A2 std 从 `0.012146` 收紧到 `0.005803`；
- TestB Object Hausdorff 中，B1 std 从约 `6.4103` 升至 `8.198661`，同时 A2 std 从 `10.774432` 收紧到 `2.896245`；新增失败由两者共同造成，但 A2 参照收紧贡献更大；
- TestB-9 是两个指标共同的最大单病例影响源，但单独移除后 Object Dice 与 Object Hausdorff Gate 仍均为 fail；波动不是一个坏文件造成，而是少数粘连困难病例对实例匹配的共同放大；
- 当前六个 v2 run 与旧 `baseline_stage_summary.md`、聚合表和 workflow Gate 的 protocol identity 不一致；现有正式 Gate 仍消费 v1，不得冒充 v2 Gate。

下一轮只能在完成新的阶段锁定、Pre-check、contract、runtime/smoke 后进行，并且必须继续 A2/B1 成对运行。候选方向按原记录顺序保留：

1. **v3 BN policy 独立候选**：只改变 BN policy，其他训练、数据、评估和统计项全部冻结；优先用于验证小 batch 下 BN 是否导致 TestB seed 敏感。
2. **v4 effective batch 候选**：只有 v3 结果和训练曲线支持时再考虑梯度累积，并明确 physical/effective batch。
3. **v5 scheduler/early stopping 候选**：只有训练曲线提供证据后再考虑，不能与 BN 或 batch 同轮混合。

禁止：删除 seed、重算 std 口径、放宽 Gate、在 TestB 调阈值、合并 TestA/TestB、只重跑 B1、或同时改变多个变量。若后续单变量轮次仍无法通过，应保留 `valid_with_stability_warning`，并将 B1 作为性能有效但稳定性有边界的 baseline，而不是无限训练直到“看起来通过”。

## 15. 当前总状态

```text
original_plan_scientific_basis = feasible
v1_experiment_assets = valid
v1_gate_b1 = false
v1_status = valid_with_stability_warning
v2_research_basis = documented
v2_research_alignment_gate = pass
v2_stage_lock = pass
v2_code_changes = completed
v2_training = completed
v2_testing = completed
v2_independent_metric_recheck = pass
v2_gate_b1 = false
v2_status = valid_with_stability_warning
next_action = stage_lock_v3_bn_policy_before_any_new_training
```
