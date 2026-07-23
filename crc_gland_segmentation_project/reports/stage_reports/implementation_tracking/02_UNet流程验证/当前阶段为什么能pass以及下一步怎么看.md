# 当前阶段为什么能pass以及下一步怎么看

## 当前 lineage

- source_stage: `02_UNet流程验证`
- source_manifest: `reports/tables/unet_stage_manifest.csv`
- source_protocol_version: `eval_proto_v1`
- source_run_name: `A1_UNet_GlaS_v1_seed3407`
- consumer_stage: `03_UNet稳定性`
- consumer_file: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- consumption_boundary: `只消费 A1 冻结协议和基线；不把 A1 单 seed 结论扩写为 A2 多 seed 结果`

## 结论

**`02_UNet流程验证` 已严格通过，允许进入 `03_UNet稳定性`。**

## 为什么现在可以写成严格通过

严格规划要求的四个条件全部成立：

1. 正式 A1 为单 GPU 执行（`device: cuda`）✓
2. `AMP on`（`amp_active: true`）✓
3. 正式 run 前已完成不入表 GPU smoke check（`smoke_gpu_probe_20260707`）✓
4. 正式训练、验证、测试、评估、可视化与记录资产链全部在同一轮 GPU 语义下完整落盘 ✓

## 正式 A1 的物理证据

| 文件 | 关键字段 | 值 |
|---|---|---|
| `run_meta.yaml` | `device` | `cuda` |
| `run_meta.yaml` | `amp_active` | `true` |
| `run_meta.yaml` | `smoke_check` | `false` |
| `run_meta.yaml` | `stop_reason` | `early_stopping` |
| `run_meta.yaml` | `epoch_count` | `70` |
| `run_meta.yaml` | `best_epoch` | `50` |
| `run_meta.yaml` | `best_metric_value` | `0.7515` |
| `run_meta.yaml` | `testA_sample_count` | `60` |
| `run_meta.yaml` | `testB_sample_count` | `20` |
| `run_meta.yaml` | `metric_crosscheck_result` | `pass` |
| `testA_metrics.csv` sample-only 重聚合 | TestA split objdice | `0.6949` |
| `testB_metrics.csv` sample-only 重聚合 | TestB split objdice | `0.7510` |

## 历史证据的位置与身份

- `experiments/A1_UNet_GlaS_v1_seed3407_cpu_historical_20260707/`：历史 CPU 联通/前检证据，已存档，不承担正式 A1 身份。
- `experiments/A1_UNet_GlaS_v1_seed3407_smoke_gpu_probe_20260707/`：服务器 GPU smoke 通过证据，已存档。
- `experiments/A1_UNet_GlaS_v1_seed3407/`：严格规划意义下的正式主目录，所有正式资产已落盘。

## 下一步

进入 `03_UNet稳定性`。
