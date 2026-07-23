# Current Codebase 状态

## 0. 本轮最小扫描范围

| 目录 | 为什么必须扫描 | 最低检查动作 |
|------|---------------|-------------|
| `datasets/` | 稳定性阶段三次 run 必须复用与 A1 完全一致的 GlaS 数据身份,需确认原始资产仍在工程区 | 检查 `datasets/01_GlaS_official_raw/Grade.csv`、`datasets/DATASETS_README.md`;GlaS 官方原始资产为 165 组原图与标注,已在工程区 |
| `splits/` | 三次 run 必须继承同一 val17 与 TestA/TestB split,需确认正式 split CSV 已冻结 | 检查 `splits/glas/glas_train68.csv`、`splits/glas/glas_val17.csv`;当前扫描到 10 个 split 文件 |
| `configs/` | 三个 A2 experiment 配置必须由 A1 配置派生,需确认 data/model/train/eval/experiment 五层配置已落地 | 检查 `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`、`configs/eval/eval_proto_v1.yaml`;当前扫描到 7 个配置文件 |
| `src/` | 三次 run 必须复用同一 UNet、loss、metrics、engine、eval 实现,需确认 stage02 主链已落地 | 检查 `src/models/unet.py`、`src/metrics/seg_metrics.py`、`src/engine/trainer.py`;当前扫描到 28 个 py 文件 |
| `scripts/` | 稳定性汇总必须扩展现有阶段汇总入口,需确认 train/test/summarize_stage 脚本现状 | 检查 `scripts/summarize_stage.py`、`scripts/train.py`;当前扫描到 5 个脚本文件 |
| `tools/` | 需确认 A 类正式工具是否已按阶段分区,避免把稳定性汇总误写进工具目录 | 检查 `tools/stage01_data_protocol/prepare_glas_split.py`、`tools/README.md`;当前扫描到 11 个文件、2 个子目录 |
| `b_class_auxiliary/` | 需确认研究、阶段锁定、Pre-check 门禁脚本与 coding guards 现状 | 检查 `b_class_auxiliary/tools/check_precheck_docs.py`、`b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md`;当前扫描到 9 个 gate 脚本 |
| `experiments/` | 需确认 A1 正式 run 已冻结并作为协议继承基准,避免把未来 A2 资产写成已存在 | 检查 `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`、`experiments/README.md`;当前已存在 A1 正式 run 与多个历史/备份目录 |
| `external/` | 需确认第三方实现适配层仍未进入接入阶段,避免误写成已接入 baseline | 检查 `external/README.md`;当前只有 1 个说明文,无外部实现接入 |
| `reports/` | 需确认 data stage 与 stage02 正式报告链已齐全,并为稳定性表预留落点 | 检查 `reports/stage_reports/unet_flow_stage_summary.md`、`reports/tables/unet_flow_stage_manifest.csv`;当前 stage_reports 已有 3 份正式报告 |

## 1. 当前阶段相关目录扫描

| 目录 | 已有文件/资产 | 状态 | 本次是否受影响 |
|------|--------------|------|---------------|
| `datasets/` | `datasets/01_GlaS_official_raw/Grade.csv`、`datasets/DATASETS_README.md`、`datasets/DATASET_SOURCE_NOTES.md` | 已存在;GlaS 官方原始资产为 165 组原图与标注,可被三次 run 直接沿用 | 否;本轮只核对数据身份,不改数据资产 |
| `splits/` | `splits/glas/glas_train68.csv`、`splits/glas/glas_val17.csv`、`splits/glas/glas_testA60.csv` | 已存在 10 个 split 文件、2 个子目录;GlaS 与 CRAG 正式 split 已冻结 | 否;三次 run 沿用同一 split,不改 |
| `configs/` | `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`、`configs/eval/eval_proto_v1.yaml`、`configs/train/unet_flow_v1.yaml` | 已存在 7 个配置文件、5 个子目录;data/model/train/eval/experiment 五层配置已落地 | 是;后续编码将由 A1 配置派生 A2 三配置 |
| `src/` | `src/models/unet.py`、`src/metrics/seg_metrics.py`、`src/engine/trainer.py`、`src/eval/run_eval.py` | 已存在 28 个 py 文件、7 个子目录;stage02 正式主链已落地并可复用 | 否;三次 run 复用同一实现,不改源码 |
| `scripts/` | `scripts/summarize_stage.py`、`scripts/train.py`、`scripts/test.py` | 已存在 5 个脚本文件;当前 summarize_stage 只服务 stage02 单 seed | 是;后续编码将扩展 summarize_stage 支持三 seed 聚合 |
| `tools/` | `tools/stage01_data_protocol/prepare_glas_split.py`、`tools/c_pending_review/build_manual_audit_notebook.py`、`tools/README.md` | 已存在 11 个文件、2 个子目录;A 类工具已按 stage01_data_protocol 分区 | 否;稳定性汇总不落 A 类工具目录 |
| `b_class_auxiliary/` | `b_class_auxiliary/tools/check_precheck_docs.py`、`b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md`、`b_class_auxiliary/coding_guards/20260708_03_unet_stability_research/研究定标记录.md` | 已存在 9 个 gate 脚本与多个 coding guards 任务目录;研究与阶段锁定留痕已就位 | 是;本轮在此新增当前阶段 Pre-check 文档链 |
| `experiments/` | `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`、`experiments/README.md` | 已存在 A1 正式 run 与多个历史/备份/smoke 目录(含 10 个含 run_meta 的目录);A1 已冻结为协议继承基准 | 否;本轮不产生 A2 run 资产,仅登记未来落点 |
| `external/` | `external/README.md` | 已存在 1 个说明文;第三方实现适配层仍未接入 baseline | 否;本轮不接外部实现 |
| `reports/` | `reports/stage_reports/unet_flow_stage_summary.md`、`reports/tables/unet_flow_stage_manifest.csv`、`reports/stage_reports/asset_manifest.json` | 已存在;stage_reports 有 3 份正式报告,implementation_tracking 已有 01 与 02 阶段目录 | 否;本轮不新增正式报告,仅登记稳定性表未来落点 |

## 2. 已实现能力
- 已有正式数据身份与 split: `datasets/01_GlaS_official_raw/Grade.csv`、`splits/glas/glas_val17.csv`
- 已有五层正式配置: `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`、`configs/eval/eval_proto_v1.yaml`
- 已有 stage02 完整源码主链: `src/models/unet.py`、`src/losses/seg_losses.py`、`src/engine/trainer.py`、`src/eval/run_eval.py`、`src/metrics/seg_metrics.py`
- 已有训练与测试与汇总脚本入口: `scripts/train.py`、`scripts/test.py`、`scripts/summarize_stage.py`
- 已有 A1 正式冻结 run: `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`,metric_crosscheck_result 为 pass
- 已有 stage02 正式报告链: `reports/stage_reports/unet_flow_stage_summary.md`、`reports/tables/unet_flow_stage_manifest.csv`

## 3. 缺口与风险
- 缺口1: `scripts/summarize_stage.py` 当前只做 stage02 单 seed,缺三 seed raw per-seed 表与 mean±std 聚合能力
- 缺口2: `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 只有一个 seed 配置,尚未派生 seed1234 与 seed2025 两个 A2 配置
- 缺口3: `experiments/` 目录尚无 A2 三次重复 run 资产,稳定性统计的物理证据链未建立
- 风险1: 若在扩展 `scripts/summarize_stage.py` 时顺手改动 A1 已有结果或聚合口径,会破坏 A1 与 A2 的协议一致性
- 风险2: 若三个 A2 配置在复制时误改 train_seed 以外字段,会让 mean±std 失去"同协议随机波动"的语义

## 4. 本次预计新增/修改

| 文件 | 动作 | 原因 | 是否已有相近实现 |
|------|------|------|----------------|
| `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/pre_check_extraction.md` | create | 需把上游约束、路线约束与未来落点收紧到当前阶段真实边界 | 是;02 阶段同名文件可作参照 |
| `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/stage_gate_check.md` | create | 需把"为何允许进入 Pre-check"写成正式门控检查 | 是;02 阶段同名文件可作参照 |
| `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/current_codebase_状态.md` | create | 需把当前工程现实、已有能力、缺口与风险写成可审计结果 | 是;02 阶段同名文件可作参照 |
| `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/20260708_03_unet_stability_pre_check_guard.md` | create | 需把 Pre-check 汇总件正式落盘并为 gate 提供输入 | 是;02 阶段 Pre-check Guard 可作参照 |
| stage03 正式代码与配置对象 | not_applicable | 本轮只做 Pre-check,不进入正式编码,仅预登记后续将涉及对象 | 是;`scripts/summarize_stage.py` 与 `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 可作扩展参照 |

## 5. 预期工程落点汇总

| 对象层 | 目录/文件 | 本轮为什么会受影响 |
|------|----------|------------------|
| 代码层 | `crc_gland_segmentation_project/scripts/summarize_stage.py` | 本轮不改,但登记为后续唯一允许扩展三 seed 聚合的正式代码落点 |
| 配置层 | `crc_gland_segmentation_project/configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` | 本轮不改,但登记为 A2 三配置唯一派生模板 |
| 运行资产层 | `crc_gland_segmentation_project/experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` | 本轮不产生 run 资产,但登记为协议继承基准与未来 A2 run 落点参照 |
| 报告层 | `crc_gland_segmentation_project/reports/tables/unet_flow_stage_manifest.csv` | 本轮不新增报告,但登记为后续稳定性 raw 与聚合表的同级落点 |
| guard 层 | `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/20260708_03_unet_stability_pre_check_guard.md` | 本轮所有实际新增只允许落在当前阶段 Pre-check guard 目录 |
