# 03_UNet稳定性 实现说明

## 当前状态

这份文档是 03 阶段的实现状态总账，用来回答一个问题：这个阶段到底做完了没有、能不能放行。

结论先说：A2 编号阶段实验 gate 与当前 workflow gate 均已通过，当前文档身份审计已完成收口；该结论只允许进入 04 的 research/stage-lock，不代表 04 自身通过。04 仍保持 not_started，不得跳过其前置门禁。下面的列表把结论拆成“实验结果”和“文档放行边界”两块。

- 阶段结论: **pass**
- 当前最真实的说法:
  - A2 阶段的三 seed 训练、评估、聚合、验收全部完成，没有残留的占位壳或待修复项。
  - 已创建 10 篇 A 类对象级学习型说明文，覆盖训练/评估/聚合脚本、数据模块、实验配置、评估协议和结果资产；本轮已完成当前身份/历史结果审计，辅助说明文中的检查项已按真实产物回写。
  - 当前 A2 编号阶段与 workflow gate 可以放行；04 仍是独立 not_started 阶段。n=3 的 std 只描述三 seed 间的一致度，不做统计推断。

- 当前已经闭环的正式资产:

| 资产 | 路径 | 作用 |
|------|------|------|
| 训练产物 (×3) | `experiments/A2_UNet_GlaS_seed{3407,1234,2025}/` | 3 seed 完整训练结果 |
| 逐 seed 结果表 | `reports/tables/unet_seed_results.csv` | 42 行原始逐 seed 指标 |
| mean±std 汇总 | `reports/tables/unet_mean_std_summary.csv` | 14 行聚合指标 |
| 稳定性分析 | `reports/stage_reports/unet_stability_note.md` | 错误模式分析 |
| A2 验收总结 | `reports/stage_reports/unet_stability_stage_summary.md` | 阶段验收判定 |
| 阶段 manifest | `reports/tables/unet_stage_manifest.csv` | 交付资产清单 |

## 为什么要重建这一组文档

03_UNet稳定性 是 02_UNet流程验证 之后的关键一步：从"单 seed 能跑"推进到"多 seed 稳定"。这意味着需要新文档来解释：

1. **三段式实验链的完整闭环**（train → test → summarize）
2. **协议一致性校验机制**（`_check_proto_consistency`）
3. **A2 验收的 5 个 gate 分别检查什么**
4. **为什么 pixel-level Dice 和 object-level Dice 差了 ~10%**

如果不写清楚这些，后面的人会困惑于"为什么 02 阶段跑 1 个 seed，03 跑 3 个，04 又变"。

## 当前阅读入口

请直接按编号从 README 开始，或按最短路径快速获取核心结论：

如果你只想最快理解当前阶段为什么能放行，最短路径是:
1. `README.md` — 先看结论和"你最该搞明白的四件事"
2. `scripts_summarize_stage.py.md` — 理解 5 个 gate 如何判定 pass
3. `reports_tables_unet_mean_std_summary.csv.md` — 确认 mean±std 数值合理

## 当前已经实现的脚本

| 脚本 | A 类 | 状态 | 说明 |
|------|------|------|------|
| `scripts/train.py` | A | 正式可用 | 训练入口，3 seed 均跑完 |
| `scripts/test.py` | A | 正式可用 | 评估入口，3 seed × 2 split 评估完成 |
| `scripts/summarize_stage.py` | A | 正式可用 | A2 聚合验收，gate_a2=pass |
| `src/data/datasets.py` | A | 正式可用 | 数据协议模块，DataConfig frozen |

## 当前仍然是占位的脚本

- 无。A2 阶段所有需要的脚本均已正式可用。

## 当前学习型说明文覆盖矩阵

| 正式对象 | 说明文 | 状态 |
|---------|--------|------|
| `scripts/train.py` | `scripts_train.py.md` | 已创建 (≥120行) |
| `scripts/test.py` | `scripts_test.py.md` | 已创建 (≥120行) |
| `scripts/summarize_stage.py` | `scripts_summarize_stage.py.md` | 已创建 (≥120行) |
| `src/data/datasets.py` | `src_data_datasets.py.md` | 已创建 (≥120行) |
| `configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml` | `configs_experiment_A2_UNet_GlaS_v1_seed3407.yaml.md` | 已创建 (≥50行) |
| `configs/experiment/A2_UNet_GlaS_v1_seed1234.yaml` | `configs_experiment_A2_UNet_GlaS_v1_seed1234.yaml.md` | 已创建 (≥50行) |
| `configs/experiment/A2_UNet_GlaS_v1_seed2025.yaml` | `configs_experiment_A2_UNet_GlaS_v1_seed2025.yaml.md` | 已创建 (≥50行) |
| `configs/eval/eval_proto_v1.yaml` | `configs_eval_eval_proto_v1.yaml.md` | 已创建 (≥50行) |
| `reports/tables/unet_seed_results.csv` | `reports_tables_unet_seed_results.csv.md` | 已创建 (≥60行) |
| `reports/tables/unet_mean_std_summary.csv` | `reports_tables_unet_mean_std_summary.csv.md` | 已创建 (≥60行) |

## 当前 A2 正式结果（唯一当前消费口径；manifest 角色见 `reports/tables/unet_stage_manifest.csv`，该文件是 04 handoff 总 manifest；`a2_stage_manifest.csv` 仅是单 run/局部汇总，不替代总 manifest）

来源固定为 `reports/tables/unet_mean_std_summary.csv`，身份为 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`，协议为 `eval_proto_v1`。精确值：testA Object F1=`0.5290508133298323±0.06534870542228736`，testB Object F1=`0.5864995222306099±0.017711580461373767`；testA Object Dice=`0.7081049877960447±0.0528843478663972`，testB Object Dice=`0.7755628763239749±0.01214631192503348`；testA Pixel Dice=`0.8687005312137156±0.014245648618802897`，testB Pixel Dice=`0.8785019406751632±0.007950925190263055`；testA IoU=`0.7802676159056027±0.023159000977374777`，testB IoU=`0.7926352354780709±0.009535961930616718`。A2 numbered stage gate=true、workflow_gate_status=pass、handoff_ready_for_b1=true，但不等于 04 自身通过。

## 本轮重写直接依赖的前置文件

`00_总览与规范` 全部规范文件、`02_路线与投稿` 相关路线文件、`03_文献证据` GlaS 指标依据，以及本阶段 README、聚合脚本说明和结果表说明；用于核对状态、路线、指标、接口和数字。

## 代码落地接口

`scripts/train.py`、`scripts/test.py`、`scripts/summarize_stage.py`；`run_stage02_training()` 若出现，仅是源码历史函数名，当前消费阶段是 A2。

## 冲突裁决记录

旧高 F1/旧 Pixel Dice 冒名数字是历史错误口径，不得当前消费；`A2_UNet_GlaS_v1_seed*` 仅为配置路径版本；`protocol_v3` 仅历史追溯。

## 回退条件

若三 seed、eval_proto_v1、聚合 CSV、stage gate、workflow gate 或 handoff 任一不一致，状态回退 blocked，禁止把结果交给下游。

## 文件质量自检

- [x] 状态、资产、精确主结果、身份与协议一致。
- [x] 旧数字/旧协议/旧身份均有合法语境。
- [x] 下游边界明确为“03 gate/handoff 已通过，不代表 04 自身通过”。

## Diagnostics 闭环

已扫描本阶段全部当前可见 Markdown 的身份、协议、旧数字、gate 与历史函数名；未发现未标注的当前消费残留。

## 审计对表

前置规范/路线/文献 → 当前 A2 正式结果与阅读入口；脚本说明 → 代码落地接口；历史更正 → 冲突裁决；全目录扫描 → Diagnostics；缺口：无。

## 当前最重要的诚实结论

- **阶段维度的结论**: A2 三个 seed（来源 `reports/tables/unet_mean_std_summary.csv`，`n_runs=3`）的当前对象级 F1 为 testA `0.5291 ± 0.0653` / testB `0.5865 ± 0.0177`，Object Dice 为 testA `0.7081 ± 0.0529` / testB `0.7756 ± 0.0121`；协议一致性、汇总和 A2 编号阶段 gate 已通过。当前文档身份审计已收口；该结论只允许进入 04 的 research/stage-lock，不代表 04 自身通过。
- **工具维度的结论**: 三段式实验链（train → test → summarize）已经验证可工作，summarize_stage.py 的协议一致性校验机制可以有效阻止协议漂移。
- **这两句话不冲突**: 结论说"链路稳定"不是说"指标已经最优"——Object Dice 仍然比 Dice 低 10%+，这是 UNet 架构自身的限制，不是训练不稳定的问题。
