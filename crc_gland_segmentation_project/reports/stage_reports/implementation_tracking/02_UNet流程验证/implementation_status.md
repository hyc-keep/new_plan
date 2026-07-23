# 02_UNet流程验证 implementation_status

## 当前状态

- source_stage: `02_UNet流程验证`
- source_manifest: `reports/tables/unet_stage_manifest.csv`
- source_protocol_version: `eval_proto_v1`
- source_run_name: `A1_UNet_GlaS_v1_seed3407`
- consumer_stage: `03_UNet稳定性`
- consumer_file: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- consumption_boundary: `仅继承 A1 冻结协议和真实单 seed 基线；不得将 A1 结果扩写为 A2 多 seed 结果`
- 工程闭环状态: `pass`
- GPU smoke 状态: `pass`
- 严格规划放行状态: `pass`
- 当前阅读入口状态: `pass`
- 当前说明文覆盖状态: `audited_current_consumer_docs`; 历史调试与历史 CPU 记录已显式隔离
- 当前阶段级入口文档: `4` 份
- 当前对象级说明文: `50` 份

## 当前最重要的诚实结论

当前最重要的结论有三句:

1. `02_UNet流程验证` 的正式单 GPU + AMP `A1_UNet_GlaS_v1_seed3407` 已按规划完成，训练、验证、测试、评估、可视化与记录资产链全部在同一轮 GPU 语义下落盘完毕。
2. `metric_crosscheck_result: pass`，TestA60 / TestB20 两个 split 的 sample-only 行重聚合与独立 PNG+GT 复核一致；这里的 split 汇总是派生结果，不是正式 CSV 内的 aggregate 行。
3. 本次正式 GPU run 为从头 fresh run（seed=3407，cuda，AMP on），best_epoch=50，epoch_count=70（early stopping，patience=20），testA objdice=0.6949，testB objdice=0.7510。

这三句可以同时成立，不冲突。

## 历史 CPU 主 run 当前状态

> 以下仅是历史 CPU 证据，不是当前 A1 入口。

历史 CPU 主 run `../../../../experiments/A1_UNet_GlaS_v1_seed3407_cpu_historical_20260707/` 的历史状态是（当前不可消费）:

- `smoke_check=false`
- `stop_reason=early_stopping`
- `best_epoch=48`
- `epoch_count=68`
- `testA_sample_count=60`
- `testB_sample_count=20`
- `metric_crosscheck_result=pass`
- `stage_pass=true`
- `protocol_error=false`
- `next_action=enter_03_unet_stability`
- `device=cpu`
- `amp_active=false`

因此，这个目录仍然保留为重要历史证据，但不能继续承担严格规划意义下的最终正式 A1 身份。

## 规范 smoke run 当前状态

当前规范 smoke run `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/` 仍然保留，并继续纳入说明文。

它的作用是:

1. 作为规范 smoke 对照目录
2. 解释 smoke 资产链如何单独落盘
3. 避免读者把 smoke 与主 run full run 混在一起

它不是主目录当前现实的替身。

## 当前服务器 GPU smoke 当前状态

当前服务器 GPU smoke probe `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke_gpu_probe_20260707/` 的真实状态是:

- `device=cuda`
- `amp_active=true`
- `smoke_check=true`
- `stop_reason=smoke_check_complete`
- `epoch_count=1`

这说明当前服务器环境已经满足:

1. 单 GPU 可用
2. AMP 可启用
3. dataloader / forward / loss / backward / optimizer.step 已真实跑通

但这仍然不是正式 A1 最终结果。

## 正式 A1 关键结果

正式 A1 运行参数（冻结协议已严格遵守）：

- `device: cuda`、`amp_active: true`、`smoke_check: false`
- `stop_reason: early_stopping`，`epoch_count: 70`，`best_epoch: 50`
- `best_metric_value: 0.7515`（`val_objdice`）
- `threshold_source: val17`，`threshold_value: 0.5`

测试结果：

| split | sample_count | objdice | dice | iou | boundary_f1 | hd95 |
|---|---|---|---|---|---|---|
| testA | 60 | 0.6949 | 0.8583 | 0.7652 | 0.6012 | 61.64 |
| testB | 20 | 0.7510 | 0.8716 | 0.7814 | 0.5908 | 42.19 |

当前可以直接回查的硬证据：

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
6. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`
7. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`

## 当前入口文档

当前阶段级入口仍然是:

1. `00_交付范围内正式对象清单.md`
2. `README.md`
3. `implementation_status.md`
4. `当前阶段为什么能pass以及下一步怎么看.md`

建议先看:

1. `README.md`
2. `当前阶段为什么能pass以及下一步怎么看.md`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_cpu_historical_20260707/run_meta.yaml`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke_gpu_probe_20260707/run_meta.yaml`
5. `00_交付范围内正式对象清单.md`

## 容易误解的地方

最容易误解的地方有四个:

1. 把历史 CPU 主 run 继续理解成严格规划下的最终正式 A1。
2. 把 GPU smoke probe 目录理解成正式主目录。
3. 把“正式 A1 已启动”误写成“正式 A1 已完成”。
4. 把工程闭环 `pass` 误写成严格规划放行 `pass`。

## 阶段最终结论

**`02_UNet流程验证` 已严格符合规划，允许进入 `03_UNet稳定性`。**

- 正式 A1 已在单 GPU + AMP 语义下完成
- 正式 smoke check 已提前通过（`smoke_gpu_probe_20260707`）
- 所有正式资产链在同一轮 GPU 语义下互相一致
- 入口文档、run_meta、run_summary 世界观已统一

## 下一步

进入 `03_UNet稳定性`。
