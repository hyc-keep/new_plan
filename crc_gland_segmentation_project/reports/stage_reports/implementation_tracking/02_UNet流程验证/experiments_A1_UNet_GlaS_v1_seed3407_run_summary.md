# experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md

> 历史资产说明：本文记录的是旧轮次 run_summary 说明（best_epoch=48、best_metric_value=0.7626771700880477），属于历史旧轮次，当前不可消费。当前 A1 唯一结果来源是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`：best_epoch=50、best_metric_value=0.7515312717616618、epoch_count=70、device=cuda、testA_objdice=0.6949207519755126、testB_objdice=0.750951634413634。本文旧数值仅供历史追溯。

## 这份文件的定位

这份文档解释的是主 run 旧轮次摘要页 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`。

它只保留历史旧轮次的人工回查信息，当前不可消费。当前 A1 是否完成训练、测试、可视化和阶段收口，必须直接读取 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`。

## 一眼先抓住什么

- 本文对应 `smoke_check=false` 的历史 full run，当前不可消费。
- 历史旧轮次以 `early_stopping` 正常结束；当前正式训练状态只读真实 run_meta.yaml。
- 历史旧轮次最优验证结果来自 `best_epoch=48`，`best_metric_value=0.7626771700880477`；当前不可消费。
- 历史旧轮次曾覆盖 `TestA60/TestB20`；该旧结果当前不可消费。
- 历史旧轮次曾记录 `stage_pass=true`、`protocol_error=false`、`next_action=enter_03_unet_stability`；这些旧字段当前不可作为正式放行依据。
- 当前 `truthful_interpretation` 必须回链真实 run_meta.yaml 和当前阶段汇总；本文旧 summary 不单独承担当前 formal closure。

## 这个文件是干什么的

这份 `run_summary.md` 曾是历史旧 full run 的最短人工结论页，当前不可消费。

它曾把以下内容压缩给人工审阅者:

1. 训练如何结束
2. 最优轮次是谁
3. 当前 split-wise 测试是否已经补齐
4. crosscheck 是否通过
5. 视觉错误模式有哪些
6. 当前阶段是否已经可以从 `02` 转入 `03`

如果没有这份文件，读者只能在 `run_meta.yaml`、`testA_metrics.csv`、`testB_metrics.csv`、`metric_crosscheck_note.md` 和阶段汇总里来回拼接结论。

## 当前真实结果

本文只保留旧轮次摘要字段，不能表达当前正式结论。当前 A1 真实结果唯一以 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 为准：best_epoch=50、best_metric_value=0.7515312717616618、epoch_count=70、device=cuda、testA_objdice=0.6949207519755126、testB_objdice=0.750951634413634。本文旧轮次字段如下:

- `stop_reason=early_stopping`
- `best_epoch=48`
- `best_metric_name=val_objdice`
- `best_metric_value=0.7626771700880477`
- `smoke_check=false`
- `amp_active=false`
- `pass_train=true`
- `pass_val=true`
- `pass_test=true`
- `pass_eval=true`
- `pass_visual=true`
- `pass_record=true`
- `stage_pass=true`
- `protocol_error=false`
- `freeze_status=true`
- `handoff_ready_for_a2=true`
- `next_action=enter_03_unet_stability`
- `testA_expected_count=60`
- `testA_actual_count=60`
- `testA_objdice=0.6941893856375373`（历史旧轮次，当前不可消费）
- `testB_expected_count=20`
- `testB_actual_count=20`
- `testB_objdice=0.7619798771629787`（历史旧轮次，当前不可消费）
- `metric_crosscheck_result=pass`

因此，这份摘要页现在已经是正式验收结论页。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`
6. `../../../../reports/stage_reports/unet_flow_stage_summary.md`

下游用途:

1. 人工复审快速阅读
2. 阶段交接快速结论页
3. 与 `run_meta.yaml` / `stage_summary` 做一致性核对

## 对应代码里的真实协议痕迹

历史摘要页的生成逻辑曾从单纯 trainer 输出升级成两段式；当前正式结论不消费本文旧资产:

1. `../../../../src/engine/trainer.py` 先写训练结论字段。
2. `../../../../scripts/summarize_stage.py` 再把阶段门禁、split 计数、formal closure 解释写回这份摘要页。

因此，当前摘要页的最终语义应以“正式 full run + 正式阶段汇总回填”理解。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
3. 对照 `../../../../reports/stage_reports/unet_flow_stage_summary.md`

通过标准:

- `stage_pass=true`
- `protocol_error=false`
- `next_action=enter_03_unet_stability`
- `testA_actual_count=60`
- `testB_actual_count=20`
- `truthful_interpretation` 明确写出 formal A1 acceptance 已经成立

## 这个文件没说明什么

当前文件能证明的是:

1. 历史主 run full run 曾达到旧正式摘要级收口；该历史结论当前不可消费。
2. 训练、测试、crosscheck 和阶段门禁可以被一页快速概括。
3. 当前主目录的训练、测试和阶段结论已经可以被一页稳定概括。

当前文件不替代的是:

1. `train_log.csv` / `val_metrics.csv` 的逐轮详情
2. `testA_metrics.csv` / `testB_metrics.csv` 的逐样本详情
3. `best.ckpt` / `last.ckpt` 的 checkpoint 实体
4. `visuals/*` 和 `error_cases.md` 的观察面

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么当前 `run_summary.md` 必须和 `run_meta.yaml`、`stage_pass=true` 保持完全同步。
2. 为什么它现在是正式 full run 摘要页。
3. 为什么 `truthful_interpretation` 必须直接表达当前正式验收已经成立。
