# experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md

## 这份文件的定位

这份说明文对应 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`。

如果说 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 是 `TestA` 的正式分账单，那么这一份就是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 的正式分账单。

你可以把它理解成“TestB split 的原始成绩表”。

## 这个文件是干什么的

- 负责记录 `TestB20` 的 sample-only 评估行；当前正式 CSV 不写 aggregate 行，split 汇总由 sample 行重聚合
- 负责把 `pred_path` 与真实预测 png 连起来
- 负责给 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 提供上游数值

说白了，这张表是在回答:
`TestB` 到底测出了什么，而不是只给一个摘要结论。

## 当前这个文件说明了什么

当前文件最关键的现实信息有 4 组:

1. `TestB` 逐样本指标
2. `TestB` aggregate 指标
3. 对应原图、GT、预测路径
4. 后续错例总结所需的 `sample_id`

当前最硬的路径锚点包括:

- `datasets/01_GlaS_official_raw/testB_1.bmp`
- `datasets/01_GlaS_official_raw/testB_10.bmp`
- `experiments/A1_UNet_GlaS_v1_seed3407/predictions/testB/GlaS_official_testB_testB_1_pred.png`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 代码参考: `../../../../scripts/test.py`
- 上游实现: `../../../../src/eval/run_eval.py`
- 关联资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
- 论文依据: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`

## 这张表/这个文件长什么样

这张表和 `TestA` 版使用完全一致的 schema。

当前 schema 的关键列包括:

1. `row_type`
2. `run_name`
3. `seed`
4. `sample_id`
5. `split_role`
6. `source_image_path`
7. `source_mask_path`
8. `eval_image_path`
9. `eval_gt_path`
10. `pred_path`
11. `eval_proto_version`
12. `boundary_metric_*`
13. `objdice`
14. `dice`
15. `iou`
16. `f1`
17. `boundary_f1`
18. `hd95`
19. `object_hausdorff`

当前正式 TestB CSV 每行包含 `objdice`、`dice`、`iou`、`f1`、`boundary_f1`、`hd95`、`object_hausdorff`；共 20 条 sample 行。历史抽样值和 aggregate 值只保留 provenance，不得作为当前结论。

## 历史旧轮次记录

| 项目 | 当前真实结果 | 说明 |
|---|---|---|
| `sample_count` | `20` | 当前正式 A1 TestB 评估数量 |
| `row_type` | 全部为 `sample` | 当前 CSV 不写 aggregate 行 |
| `loss/loss_bce/loss_dice` | 全部为 `not_applicable` | 测试阶段不计算训练损失 |
| `eval_image/eval_gt/pred` | 同空间、同尺寸 | 支持独立 PNG+GT 重算 |
| `metric_crosscheck` | `pass` | 当前正式结果可进入阶段汇总 |

## 这些列/字段分别是什么意思

这里的列分成 5 组:

1. 身份列: `row_type`、`run_name`、`seed`、`sample_id`、`split_role`
2. 路径与 lineage 列: `source_image_path`、`source_mask_path`、`eval_image_path`、`eval_gt_path`、`pred_path`
3. 协议列: `checkpoint_*`、`eval_proto_version`、`boundary_metric_*`、`hd95_impl`、`empty_set_policy`
4. 损失列: `loss`、`loss_bce`、`loss_dice`，测试阶段为 `not_applicable`
5. 指标列: `objdice`、`dice`、`iou`、`f1`、`boundary_f1`、`hd95`、`object_hausdorff`

最值得记的一点是:
这张表不是只给人工看的，它同时也是后续 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 的结构化输入。

## 这个文件没说明什么

这张表没有单独解释:

1. 为什么 `boundary_f1` 会更低
2. 为什么当前 `TestB` 会出现 `boundary_over_smooth`
3. 阈值和 best checkpoint 是怎么来的

这些问题要去联读:

- `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `src_eval_run_eval.py.md`

## 和上下游怎么衔接

- 上游是 `../../../../scripts/test.py` 调 `../../../../src/eval/run_eval.py` 生成 `TestB` sample-only 行，并写入 source/eval lineage、同空间 GT/prediction 路径
- 下游是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 继续做口径对账，`../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 继续挑坏例子，`../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 继续汇总 split 级结论

## 当前最该注意的一点

不要因为 TestB 的某个指标高于 TestA，就直接写成“模型已经稳定”；A2 稳定性必须看三个 seed 的 mean±std。

当前只能引用正式 A1 的 20 条 TestB sample 行和 `run_meta.yaml`/阶段汇总；不能把历史 CPU 抽样结果当作当前正式 TestB 结论。

## 如何手工验证这个文件的正确性

最短验证步骤:

1. 检查表内全部行的 `row_type=sample`
2. 检查全部 sample 行的 `split_role` 都是 `testB`，正式数量为 20
3. 检查 `eval_image_path`、`eval_gt_path`、`pred_path` 是否真实存在且同尺寸
4. 用 sample 行重算指标均值，并与独立 PNG+GT 复核及阶段汇总一致

通过标准:

- 当前正式 A1 TestB 有 20 条 sample 行，无 aggregate 行
- `source_image_path`、`source_mask_path`、`eval_image_path`、`eval_gt_path`、`pred_path` 均可回溯
- 三类评估资产尺寸一致，GT 为二值
- 独立 PNG+GT 指标复核 `testB.status=pass`

## 常见问题

- 不要把 `TestB` 的较高 `dice` 误读成错误已经消失；边界问题仍在
- 当前正式 TestB 是 20 条 sample 行的全量评估；不要把历史 CPU 抽样数量误认为当前正式数量
- 不要跳过 `sample_id` 和 `pred_path`，后面 visual 回指都靠它们

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_metric_crosscheck_note.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`
- `scripts_test.py.md`
