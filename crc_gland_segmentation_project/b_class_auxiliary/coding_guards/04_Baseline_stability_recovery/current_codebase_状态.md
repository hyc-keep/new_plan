# 04_Baseline 当前代码库状态

## 0. 本轮最小扫描范围

| 目录 | 是否存在 | 为什么必须扫描 | 最低检查动作 |
|---|---|---|---|
| `datasets/` | 是 | 确认 GlaS 数据入口未漂移。 | 已检查 `datasets/DATASETS_README.md`，计数 759 个文件。 |
| `splits/` | 是 | 确认 train/val/TestA/TestB 划分未漂移。 | 已检查 `splits/README.md`，计数 10 个文件。 |
| `configs/` | 是 | 确认六份稳定身份配置和协议引用存在。 | 已检查 `configs/experiment/A2_UNet_GlaS_seed3407.yaml`，计数 46 个文件。 |
| `src/` | 是 | 确认模型、训练循环、评估实现是当前源码。 | 已检查 `src/engine/trainer.py`，计数 117 个文件。 |
| `scripts/` | 是 | 确认正式训练入口和 run lock 实现位置。 | 已检查 `scripts/train.py`，计数 16 个文件。 |
| `tools/` | 是 | 确认辅助工具目录未缺失。 | 已检查 `tools/stage02_experiment_environment_check.py`，计数 13 个文件。 |
| `b_class_auxiliary/` | 是 | 确认当前 contract、gate 和 runtime 证据边界。 | 已检查 `b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/`，计数 285 个文件。 |
| `experiments/` | 是 | 确认正式输出 freshness 和历史归档边界。 | 已检查 `experiments/_historical_archive/`，计数 7901 个文件。 |
| `external/` | 是 | 确认外部参考实现仅作为只读依据。 | 已检查 `external/README.md`，计数 1 个文件。 |
| `reports/` | 是 | 确认实现依据和结果报告落点存在。 | 已检查 `reports/stage_reports/implementation_tracking/`，计数 349 个文件。 |

## 1. 当前阶段相关目录扫描

| 目录 | 已有文件/资产 | 状态 | 本次是否受影响 |
|---|---|---|---|
| `datasets/` | `datasets/DATASET_SOURCE_NOTES.md`、`datasets/DATASETS_README.md`；759 个文件 | 目录存在，数据入口未改 | 否，只读核对 |
| `splits/` | `splits/README.md`、`splits/glas/README.md`；10 个文件 | 目录存在，split 边界冻结 | 否，只读核对 |
| `configs/` | `configs/experiment/A2_UNet_GlaS_seed3407.yaml`、`configs/train/unet_flow_v2.yaml`；46 个文件 | 目录存在，稳定配置已更新 | 是，更新稳定 identity 字段 |
| `src/` | `src/engine/trainer.py`、`src/models/`；117 个文件 | 目录存在，日志保护已实现 | 是，训练循环保护属于当前实现依据 |
| `scripts/` | `scripts/train.py`；16 个文件 | 目录存在，run lock 已实现 | 是，训练入口保护属于当前实现依据 |
| `tools/` | `tools/stage02_experiment_environment_check.py`、`tools/README.md`；13 个文件 | 目录存在，辅助工具可读 | 否，只读核对 |
| `b_class_auxiliary/` | `b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/`；285 个文件 | 目录存在，当前 gate 已重建 | 是，当前轮次门禁文件更新 |
| `experiments/` | `experiments/_historical_archive/`；7901 个文件，六个稳定正式目录尚未生成 | 目录存在且 fresh | 是，当前轮次将新建正式输出 |
| `external/` | `external/README.md`；1 个文件 | 目录存在，外部资料只读 | 否，只读核对 |
| `reports/` | `reports/stage_reports/implementation_tracking/`；349 个文件 | 目录存在，实现依据可回链 | 是，当前轮次报告会新增 |

## 2. 已实现能力
- `scripts/train.py` 使用单写者 `.run.lock`，阻止同一 run 并发写入。
- `src/engine/trainer.py` 在 CSV append 前检查 epoch 严格大于物理最后一行，并在写入后 flush。
- 六份 experiment config 使用稳定 identity，协议版本写入机器字段。
- 当前 contract checker、阶段定义 gate、Pre-check gate 和 formal docs gate 均有当前输出路径。

## 3. 缺口与风险
- runtime、smoke、code quality、正式训练、TestA/TestB、raw metrics、mean/std 尚未生成。
- 任何历史目录中的 checkpoint、CSV、预测和 summary 都不能直接恢复为当前结果。
- 正式训练必须逐 run 启动并保留完整 summary/checkpoint。

## 4. 本次预计新增/修改
- 生成当前 runtime、smoke、code quality 和 Post-QC 证据。
- 在前置门禁通过后生成六个正式稳定身份输出。
- 生成 TestA/TestB raw metrics、mean/std aggregation 和阶段验收证据。

## 5. 预期工程落点汇总
| 对象 | 路径 | 状态 |
|---|---|---|
| 当前配置 | `configs/experiment/` | 已存在 |
| 正式输出 | `experiments/` | 待 fresh run |
| 历史输出 | `experiments/_historical_archive/` | 已归档 |
| 当前门禁 | `b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/` | 重新生成中 |
| 当前依据 | `reports/stage_reports/implementation_tracking/04_Baseline_stability_recovery/实现依据记录.md` | 已存在 |
