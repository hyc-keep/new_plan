# 当前阶段为什么能pass以及下一步怎么看

## 当前 lineage

- source_stage: `03_UNet稳定性`
- source_manifest: `reports/tables/unet_stage_manifest.csv`
- source_protocol_version: `eval_proto_v1`
- source_run_name: `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`
- consumer_stage: `04_Baseline`
- consumer_file: `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- consumption_boundary: `只消费冻结 A2 baseline，不重新评估或重开 A2 协议`

## 当前身份与精确结果

当前只聚合三个正式身份 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`，当前协议为 `eval_proto_v1`；`protocol_v3` 只作历史追溯。来源 `reports/tables/unet_mean_std_summary.csv` 的精确聚合值为：testA Object F1=`0.5290508133298323±0.06534870542228736`，testB Object F1=`0.5864995222306099±0.017711580461373767`；testA Object Dice=`0.7081049877960447±0.0528843478663972`，testB Object Dice=`0.7755628763239749±0.01214631192503348`；testA Pixel Dice=`0.8687005312137156±0.014245648618802897`，testB Pixel Dice=`0.8785019406751632±0.007950925190263055`；testA IoU=`0.7802676159056027±0.023159000977374777`，testB IoU=`0.7926352354780709±0.009535961930616718`。

## 结论

**`03_UNet稳定性`（A2）实验结果 gate 已通过；当前说明文与历史身份审计完成前，不允许进入 `04_Baseline`。**

这份文档只回答两个问题：一是"凭什么现在敢写严格通过"，二是"进 04 之前你还得盯住哪些前置条件"。它不重复解释每个脚本怎么写（那些在逐文件说明文里），只把判定标准、物理证据、回退条件和下游前置这四件事讲清楚。

## Gate_A2 判定标准骨架

A2 的放行不是靠"感觉跑完了"，而是靠 `summarize_stage.py` 里一个显式的布尔式：

```
Gate_A2 = complete_runs
          and proto_consistent
          and raw_results_ready
          and failure_summary_ready
          and blockers_resolved
```

五个子门只要有一个是 false，整个 Gate_A2 就是 blocked，脚本不会把 `stage_pass_a2` 写成 true。下面逐个说它检查什么、凭什么现在是 true：

| 子门 | 检查什么 | 判定标准 | 当前状态 | 物理证据锚点 |
|---|---|---|---|---|
| `complete_runs` | 三个 seed 是否都跑完正式训练 | 3 个 seed 目录都有 checkpoint + val_metrics + run_meta，且 `smoke_check=false`、`device=cuda` | ✓ | `experiments/A2_UNet_GlaS_seed{3407,1234,2025}/` |
| `proto_consistent` | 三次运行协议红线字段是否一致 | `_check_proto_consistency` 跨字段比对无 mismatch | ✓ | 三份 `run_meta.yaml` + 两张 CSV 的协议列 |
| `raw_results_ready` | 三个正式 seed 的 sample-only raw 是否齐全 | `unet_seed_results.csv` 有 42 行原始数据；`unet_mean_std_summary.csv` 是独立统计派生表，不表示 per-run CSV 存在 aggregate 行 | ✓ | `reports/tables/unet_seed_results.csv`、`reports/tables/unet_mean_std_summary.csv` |
| `failure_summary_ready` | 错误模式分析是否落盘 | `unet_stability_note.md` 存在且描述了 Object 级差距来源 | ✓ | `reports/stage_reports/unet_stability_note.md` |
| `blockers_resolved` | 是否还有未清的阻断项 | 无占位壳、无待修复缺陷、scipy 依赖已装回 | ✓ | `unet_stability_stage_summary.md` 验收结论 |

## A2 三 seed 的物理证据

以主 seed3407 的 `run_meta.yaml` 为例，关键字段如下（都是真实落盘值，不是预填）：

| 文件 | 关键字段 | 值 |
|---|---|---|
| `run_meta.yaml` | `device` | `cuda` |
| `run_meta.yaml` | `smoke_check` | `false` |
| `run_meta.yaml` | `stop_reason` | `early_stopping` |
| `run_meta.yaml` | `epoch_count` | `73` |
| `run_meta.yaml` | `best_epoch` | `53` |
| `run_meta.yaml` | `best_metric_value` | `0.7564017193729246` |
| `run_meta.yaml` | `best_selector` | `val_objdice_max` |
| `run_meta.yaml` | `eval_cast_policy` | `float32_before_threshold` |
| `run_meta.yaml` | `connected_components_connectivity` | `8` |
| `run_meta.yaml` | `connected_components_impl` | `scipy.ndimage.label` |
| `run_meta.yaml` | `boundary_metric_impl` | `binary_erosion_xor_plus_binary_dilation` |
| `run_meta.yaml` | `metric_crosscheck_result` | `pass` |

三 seed 聚合后的 mean±std 证据（来自 `reports/tables/unet_mean_std_summary.csv`，`n_runs=3`，`seeds="3407,1234,2025"`）：

| split | Object F1 mean±std | Object Dice mean±std | Object Hausdorff mean±std | IoU mean±std |
|---|---|---|---|---|
| testA | 0.5291 ± 0.0653 | 0.7081 ± 0.0529 | 128.84 ± 28.70 | 0.7803 ± 0.0232 |
| testB | 0.5865 ± 0.0177 | 0.7756 ± 0.0121 | 125.01 ± 10.77 | 0.7926 ± 0.0095 |

怎么读这张表：TestB 的 F1/Object Dice std 较小（分别为 0.0177、0.0121），但 TestA 的 F1/Object Dice std 明显更大（分别为 0.0653、0.0529）。因此 A2 gate 的“稳定性”应理解为三次正式 run 完整、协议一致、可聚合且边界已记录；不能把它表述成所有指标最多只抖动 1 个百分点。

## 历史证据的位置与身份

- `experiments/A2_UNet_GlaS_seed3407/`：主 seed 正式主目录，所有正式资产已落盘。
- `experiments/A2_UNet_GlaS_seed1234/`：第二 seed 正式主目录，同构完整产物。
- `experiments/A2_UNet_GlaS_seed2025/`：第三 seed 正式主目录，同构完整产物。
- `experiments/A2_UNet_GlaS_seed3407__runtime_probe/`：独立 runtime probe 目录，仅用于运行时探针，不承担正式训练身份，也不得作为当前汇总或 Gate_A2 的第 4 个 seed。
- 历史 `A2_UNet_GlaS_v1_seed*` 和 `protocol_v3` 目录只用于历史追溯，不能进入当前汇总或当前 gate。

## 什么情况下这个 pass 会被打回 blocked（回退条件）

严格通过不是终身有效。只要出现下面任意一条，这个阶段就要重新退回 blocked 并复跑：

1. 三个 seed 目录里任何一个的 checkpoint 或 `run_meta.yaml` 丢失、或 `smoke_check` 被改成 true —— `complete_runs` 立即变 false。
2. 有人改了评估协议（阈值、connectivity、cast policy 之一），导致三份 run_meta 的协议红线字段不再一致 —— `proto_consistent` 变 false，聚合失去可比性。
3. 两张结果 CSV 与 run_meta 的协议列对不上（比如手工改了聚合表却没重跑）—— 视为协议漂移，`raw_results_ready` 不可信；任何派生统计必须从 sample-only raw 重新生成。
4. scipy 环境再次缺失导致 `connected_components_impl` 无法运行 —— Object 级指标算不出来，`blockers_resolved` 变 false。

换句话说，这个 pass 的有效前提是"三 seed 产物 + 协议一致 + 依赖齐全"这三件事不被破坏。任何一件被动过，都要回到 `summarize_stage.py` 重新过一遍 Gate_A2。

## 进入 04_Baseline / B1 前的放行前置条件

下面这些是从 A2 交到下游时必须先确认为真的前置，不确认就别开工 04：

1. `stage_pass_a2 = true` 且 `handoff_ready_for_b1 = true`（已确认，见 `unet_stability_stage_summary.md`）。
2. 三个 seed 的 checkpoint 和 testA/testB 评估产物全部存在且可读（已确认）。
3. `_check_proto_consistency` 无 mismatch（已确认）。
4. 04_Baseline 若要复用 A2 的评估协议，必须沿用同一份 `configs/eval/eval_proto_v1.yaml`，否则 A2 的 mean±std 不能直接当对比基线。
5. 你理解 A2 的 mean±std 在下游扮演的角色：它是"参照系"。04 换了数据/模型/协议后指标变了，就靠 A2 这组 mean±std 来判断"这个变化是真的改进，还是落在三 seed 噪声区间里的抖动"。

## 下一步

进入 `04_Baseline`。开工时记住两条边界：

- n=3 的 std 只描述三 seed 之间的一致度，**不做统计推断**。别拿它当置信区间用，也别声称"显著优于"。
- 对象级检测 F1（testA 0.5291 ± 0.0653 / testB 0.5865 ± 0.0177）低于像素 Dice（testA 0.8687 / testB 0.8785），也低于 Object Dice（testA 0.7081 ± 0.0529 / testB 0.7756 ± 0.0121）。这不是训练不稳定，而是 vanilla UNet baseline 在腺体实例分离上的架构限制——像素分得准，但相邻腺体粘连导致对象检测大量失配。04 阶段引入更强 baseline（如 DCAN 式 contour 分支/后处理）时，抬升对象级 F1 就是重点验证目标。
  - 历史更正记录（20260711）：旧版本曾误把主指标 F1 写成像素 Dice（0.8908/0.8854）；这些旧数字不可作为当前结果。当前对象级 F1 以 `reports/tables/unet_mean_std_summary.csv` 的 `0.5291 ± 0.0653`（testA）和 `0.5865 ± 0.0177`（testB）为准。

## 复现命令清单（03 阶段，二次重做照抄即可）

> 所有命令均在 `crc_gland_segmentation_project/` 目录下执行；命令与参数取自已跑通的真实记录（gate 报告 `command:` 字段）。按顺序执行。

前置：
```bash
cd /home/featurize/work/Paper/crc_gland_segmentation_project
```

### 步骤 1：三 seed 测试评估（用现有 checkpoint，不训练）

```bash
python scripts/test.py --config configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml --run-name A2_UNet_GlaS_seed3407 --device cuda
python scripts/test.py --config configs/experiment/A2_UNet_GlaS_v1_seed1234.yaml --run-name A2_UNet_GlaS_seed1234 --device cuda
python scripts/test.py --config configs/experiment/A2_UNet_GlaS_v1_seed2025.yaml --run-name A2_UNet_GlaS_seed2025 --device cuda
```
产物：每个 `experiments/A2_UNet_GlaS_seed*/` 下的 `testA_metrics.csv`、`testB_metrics.csv`（"w" 覆盖写）。每条输出应含 `metric_crosscheck_result=pass`。配置文件名中的 `v1` 是配置版本路径，不是当前 run_name。

### 步骤 2：聚合三 seed，生成论文表与稳定性说明

```bash
python scripts/summarize_stage.py --stage a2
```
产物：`reports/tables/unet_seed_results.csv`（42 行）、`reports/tables/unet_mean_std_summary.csv`（14 行）、`reports/stage_reports/unet_stability_note.md`、`reports/tables/unet_stage_manifest.csv`。输出末尾应为 `stage_pass_a2=true`。

### 步骤 3：总放行门禁（六步串行，一次给全 6 个参数）

```bash
python b_class_auxiliary/tools/enforce_workflow_gate.py \
  --stage-card b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md \
  --research-record b_class_auxiliary/coding_guards/20260708_03_unet_stability_research/研究定标记录.md \
  --precheck-guard b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/20260708_03_unet_stability_pre_check_guard.md \
  --post-qc-guard b_class_auxiliary/runtime_checks/post_qc_guard.md \
  --experiment-config configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml \
  --runtime-split testA
```
产物：`b_class_auxiliary/runtime_checks/workflow_gate_report.md`，末尾应为 `workflow_gate_status=pass`。该命令内部自动串联 research → stage_definition → precheck → runtime_check → code_quality → workflow 六步，无需单独跑。

> 参数说明：`enforce_workflow_gate.py` 只有 `--stage-card` 是必填，其余四个（research-record / precheck-guard / post-qc-guard / experiment-config）默认值为空会导致对应步骤 `blocked`，所以必须显式给全。若报 `missing_xxx`，即缺对应参数；若报 `blocked_by_xxx`，是被上一步阻断，修好上一步即可。
