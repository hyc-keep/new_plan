# experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md

> 历史资产说明：本文记录的是旧轮次 run_meta 说明（best_epoch=48、best_metric_value=0.7626771700880477、epoch_count=68），属于历史旧轮次，当前不可消费。当前 A1 唯一结果来源是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`：best_epoch=50、best_metric_value=0.7515312717616618、epoch_count=70、device=cuda、testA_objdice=0.6949207519755126、testB_objdice=0.750951634413634。本文旧数值仅供历史追溯。

## 这份文件的定位

这份文档解释的是主 run `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`。

它曾是旧 full run 的结果索引页；当前不可消费。当前 A1 的训练、验证、测试、crosscheck、visual 和阶段验收字段必须直接回查真实 run_meta.yaml。

## 一眼先抓住什么

- 定位: 当前文件对应主 run `A1_UNet_GlaS_v1_seed3407` 的正式 `run_meta.yaml`。
- 本文描述的是 `smoke_check=false` 的历史 full run，当前不可消费。
- 停止方式: 旧轮次以 `early_stopping` 结束；该运行记录当前不可消费。
- 历史旧轮次最优记录: `best_epoch=48`，`best_metric_value=0.7626771700880477`；这些值当前不可消费。当前真实值以 run_meta.yaml 的 `best_epoch=50`、`best_metric_value=0.7515312717616618` 为准。
- 训练长度: `epoch_count=68`，`epoch_max=120`，但按 `early_stop_patience=20` 提前正常收尾。
- 测试闭环: 已写入 `testA_sample_count=60`、`testB_sample_count=20`、`metric_crosscheck_result=pass`、visual 计数等正式测试字段。
- 历史阶段结论曾回填 `stage_pass=true`、`protocol_error=false`、`handoff_ready_for_a2=true`、`next_action=enter_03_unet_stability`；这些旧字段当前不可作为正式放行依据。

## 这个文件是干什么的

这份 `run_meta.yaml` 是主 run 的总索引卡。

它把下面几类信息压在一处:

1. run 身份和版本链
2. 训练冻结字段和评估冻结字段
3. 正式训练结果
4. 正式测试与可视化结果
5. 阶段验收门禁结果

如果没有这份文件，读者需要在 `train_log.csv`、`val_metrics.csv`、`testA_metrics.csv`、`testB_metrics.csv`、`metric_crosscheck_note.md`、`run_summary.md` 和阶段汇总之间来回拼接，才能知道当前主 run 是否已经达到 `02_UNet流程验证` 的正式收口状态。

## 历史旧轮次记录

本文旧轮次字段如下；它们仅供历史追溯，不得作为当前结果消费。当前 A1 唯一来源为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`，其关键值为 best_epoch=50、best_metric_value=0.7515312717616618、epoch_count=70、device=cuda、testA_objdice=0.6949207519755126、testB_objdice=0.750951634413634。旧轮次字段如下:

- `run_name=A1_UNet_GlaS_v1_seed3407`
- `smoke_check=false`
- `stop_reason=early_stopping`
- `best_epoch=48`
- `best_metric_value=0.7626771700880477`
- `epoch_count=68`
- `best_checkpoint_path=experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`
- `best_checkpoint_epoch=48`（历史旧轮次，当前不可消费）
- `metric_crosscheck_result=pass`
- `testA_sample_count=60`
- `testB_sample_count=20`
- `testA_objdice=0.6941893856375373`（历史旧轮次，当前不可消费）
- `testB_objdice=0.7619798771629787`（历史旧轮次，当前不可消费）
- `num_visual_samples_testA=5`
- `num_visual_samples_testB=5`
- `stage_pass=true`
- `protocol_error=false`
- `handoff_ready_for_a2=true`
- `next_action=enter_03_unet_stability`

这说明它现在记录的是主 run full run 已经收口到什么程度。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../scripts/train.py`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
4. `../../../../scripts/test.py`
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
6. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
7. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`

下游消费:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
2. `../../../../reports/stage_reports/unet_flow_stage_summary.md`
3. `../../../../reports/tables/unet_flow_stage_manifest.csv`
4. 主 run 的 checkpoint、曲线、可视化与后续阶段交接

## 对应代码里的真实协议痕迹

关键代码痕迹有三层:

1. `../../../../scripts/train.py` 负责写入 run 身份、版本链、训练结论字段。
2. `../../../../scripts/test.py` 负责回填测试样本数、crosscheck、visual 和 split 级 objdice。
3. `../../../../scripts/summarize_stage.py` 负责回填 `pass_train/pass_val/pass_test/pass_eval/pass_visual/pass_record/stage_pass/next_action`。

所以这份资产已经是 train、test、stage-summary 三段链路共同回填的正式总索引。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
4. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
5. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
6. 对照 `../../../../reports/stage_reports/unet_flow_stage_summary.md`

通过标准:

- `smoke_check=false`
- `stop_reason=early_stopping`
- `best_epoch=48`（历史旧轮次，当前不可消费）
- `epoch_count=68`（历史旧轮次，当前不可消费）
- `testA_sample_count=60`
- `testB_sample_count=20`
- `metric_crosscheck_result=pass`
- `stage_pass=true`
- `next_action=enter_03_unet_stability`

## 这个文件没说明什么

当前文件能证明的是:

1. 主 run full run 已经完成正式训练、正式测试和阶段汇总回填。
2. 当前阶段收口状态已经能从单一 YAML 索引卡回查。
3. 当前主目录已经具备独立、完整的正式结果索引入口。

当前文件不直接替代的是:

1. `train_log.csv` / `val_metrics.csv` 的逐轮原始记录
2. `best.ckpt` / `last.ckpt` 的实体 checkpoint
3. `testA_metrics.csv` / `testB_metrics.csv` 的逐样本指标
4. `error_cases.md` 与 `visuals/*` 的可视化观察面

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 当前主 run 为什么已经具备 full run 的正式结果索引特征。
2. 当前 `best_epoch=50`、`epoch_count=70` 和 `early_stopping` 分别说明什么；旧 `48/68` 只属于历史 provenance。
3. 为什么真实 `run_meta.yaml` 可以作为 `02_UNet流程验证` 正式收口的总索引卡。
