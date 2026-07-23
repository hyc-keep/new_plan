# 02_UNet流程验证 阅读入口

## 先看结论

- source_stage: `02_UNet流程验证`
- source_manifest: `reports/tables/unet_stage_manifest.csv`
- source_protocol_version: `eval_proto_v1`
- source_run_name: `A1_UNet_GlaS_v1_seed3407`
- consumer_stage: `03_UNet稳定性`
- consumer_file: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- consumption_boundary: `只传递 A1 协议和冻结基线；不传递 A2 结果或 04 结果`

- `02_UNet流程验证` **已严格通过，允许进入 `03_UNet稳定性`**。
- 正式单 GPU + AMP `A1_UNet_GlaS_v1_seed3407` 已按冻结协议完成，TestA60 / TestB20 / crosscheck / visuals / error_cases / run_summary 全部落盘，`metric_crosscheck_result: pass`。
- 历史 CPU 主 run 保留在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_cpu_historical_20260707/`，作为历史联通/前检证据存档，不承担正式 A1 身份。
- 服务器 GPU smoke probe 保留在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke_gpu_probe_20260707/`，作为 smoke 通过证据存档。
- 正式主目录为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/`，所有正式资产在同一轮 GPU 语义下一致。

## 如果你只先读 3 份

请先读:

1. `00_交付范围内正式对象清单.md`
2. `implementation_status.md`
3. `当前阶段为什么能pass以及下一步怎么看.md`

如果你要快速确认“正式 GPU A1 已完成、02 为什么严格通过”，再接着读:

4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`
6. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`

## 最推荐阅读顺序

建议按下面顺序读:

1. `00_交付范围内正式对象清单.md`
2. `implementation_status.md`
3. `scripts_train.py.md`
4. `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`
5. `configs_data_glas.yaml.md`
6. `configs_model_unet_v1.yaml.md`
7. `configs_train_unet_flow_v1.yaml.md`
8. `configs_eval_eval_proto_v1.yaml.md`
9. `src_data___init__.py.md`
10. `src_models___init__.py.md`
11. `src_losses___init__.py.md`
12. `src_engine___init__.py.md`
13. `src_utils___init__.py.md`
14. `src_data_datasets.py.md`
15. `src_data_csv_loader.py.md`
16. `src_data_mask_ops.py.md`
17. `src_data_transforms.py.md`
18. `src_models_unet.py.md`
19. `src_losses_seg_losses.py.md`
20. `src_engine_lr_scheduler.py.md`
21. `src_engine_early_stop.py.md`
22. `src_engine_trainer.py.md`
23. `src_metrics_seg_metrics.py.md`
24. `src_eval_threshold.py.md`
25. `src_eval_run_eval.py.md`
26. `src_eval_checkpoint_selector.py.md`
27. `src_utils_seed.py.md`
28. `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
29. `experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md`
30. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md`
31. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_summary.md`
32. `当前阶段为什么能pass以及下一步怎么看.md`

## 这一版和旧版最重要的区别

这次最关键的更新不是“又补了一批说明文”，而是把 `历史 CPU 主 run`、`规范 smoke run` 和 `服务器 GPU smoke probe` 三者的身份重新拆开了。

当前必须明确区分:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_cpu_historical_20260707/` 是历史 CPU 联通/前检证据。
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/` 是历史 smoke 对照目录。
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke_gpu_probe_20260707/` 是当前服务器侧 GPU smoke 通过证据。
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/` 现为正式 GPU A1 主目录，正式训练已按冻结协议完成，所有资产链已落盘。

## 当前这组文档覆盖什么

当前这组文档当前主要覆盖:

1. `3` 份脚本入口与结果脚本: `scripts/train.py`、`scripts/test.py`、`scripts/export_visuals.py`
2. `20` 份源码对象: data/model/loss/engine/utils 门面与训练、验证、指标、可视化主链源码
3. `5` 份核心配置: experiment/data/model/train/eval
4. 正式 GPU A1 主目录资产链及其说明文
5. 规范 smoke run 资产及其说明文

正式规划口径下的 GPU A1 已完成，02 阶段严格通过。

## 正式 A1 关键结果

| split | sample_count | objdice | dice |
|---|---|---|---|
| testA | 60 | 0.6949 | 0.8583 |
| testB | 20 | 0.7510 | 0.8716 |

- `device: cuda`，`amp_active: true`，`smoke_check: false`
- `stop_reason: early_stopping`，`epoch_count: 70`，`best_epoch: 50`
- `best_val_objdice: 0.7515`，`metric_crosscheck_result: pass`

## 阶段最终结论

**`02_UNet流程验证` 已严格符合规划，可进入 `03_UNet稳定性`。**

## 这一页的职责边界

这份 README 负责：

1. 告诉读者先看什么
2. 告诉读者历史 CPU、历史 smoke、正式 GPU A1 三类目录应怎样区分
3. 说明阶段已正式放行

它不替代：

1. `实现依据记录.md`
2. 对象级说明文本体
3. `runtime_check_report.md`、`runtime_evidence.json`、`workflow_gate_report.md`
