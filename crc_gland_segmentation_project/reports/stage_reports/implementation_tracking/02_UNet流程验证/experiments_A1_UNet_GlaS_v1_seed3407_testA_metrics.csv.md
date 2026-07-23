# experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md

## 这份文件的定位

你现在可能会问:

“既然 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 已经写了 `testA_objdice`，为什么还要单独解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`？”

因为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 只给摘要。
当前这份文件才是 `TestA` split 的正式原始结果表。

## 这个文件是干什么的

- 这份资产对应 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`。
- 它负责记录 `TestA60` 的 sample-only 评估行；当前正式 CSV 不写 aggregate 行，split 汇总由 `summarize_stage.py` 从 sample 行重聚合。
- 它回答的问题不是“这次 run 大概怎么样”，而是“TestA 每个样本和整体现实结果分别是多少”。

你可以先把它想成 `TestA` 的正式分账单。

## 当前这个文件说明了什么

当前这张表最关键的现实信息有 4 层:

1. `row_type=sample` 的逐样本结果
2. 当前正式 CSV 不包含 `row_type=aggregate`；split 汇总由 sample-only 行派生计算
3. `source_image_path`、`source_mask_path`、`eval_image_path`、`eval_gt_path`、`pred_path` 的物理回指
4. `objdice`、`dice`、`iou`、`f1`、`boundary_f1`、`hd95`、`object_hausdorff` 这一组正式指标列

说白了，没有这张表，后面的 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 都会缺少最硬的上游依据。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 代码参考: `../../../../scripts/test.py`
- 上游实现: `../../../../src/eval/run_eval.py`
- 关联资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
- 论文依据: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`

## 这张表/这个文件长什么样

当前表头固定包含:

1. `row_type`
2. `sample_id`
3. `split_role`
4. `sample_count`
5. `source_image_path`
6. `source_mask_path`
7. `eval_image_path`
8. `eval_gt_path`
9. `pred_path`
10. `loss`
11. `loss_bce`
12. `loss_dice`
13. `objdice`
14. `dice`
15. `iou`
16. `f1`
17. `boundary_f1`
18. `hd95`
19. `object_hausdorff`

当前真实样例里:

- 当前正式 CSV 每行包含 `objdice`、`dice`、`iou`、`f1`、`boundary_f1`、`hd95`、`object_hausdorff`
- 当前正式 TestA 共 60 条 sample 行；split 级结果应回看 `run_meta.yaml` 与当前阶段汇总
- 历史抽样值和历史 aggregate 值只保留 provenance，不得作为当前结论

## 当前真实结果

最值得直接记住的结果有 5 条:

| 项目 | 当前真实结果 | 为什么重要 |
|---|---|---|
| `sample_count` | `60` | 当前正式 A1 TestA 评估数量 |
| `row_type` | 全部为 `sample` | 当前 CSV 不写 aggregate 行 |
| `loss/loss_bce/loss_dice` | 全部为 `not_applicable` | 测试阶段不计算训练损失 |
| `eval_image/eval_gt/pred` | 同空间、同尺寸 | 支持独立 PNG+GT 重算 |
| `metric_crosscheck` | `pass` | 当前正式结果可进入阶段汇总 |

## 这些列/字段分别是什么意思

这里的列分成 5 组职责:

1. 身份列: `row_type`、`run_name`、`seed`、`sample_id`、`split_role`
2. 路径与 lineage 列: `source_image_path`、`source_mask_path`、`eval_image_path`、`eval_gt_path`、`pred_path`
3. 协议列: `checkpoint_*`、`eval_proto_version`、`boundary_metric_*`、`hd95_impl`、`empty_set_policy`
4. 损失列: `loss`、`loss_bce`、`loss_dice`，测试阶段为 `not_applicable`
5. 指标列: `objdice`、`dice`、`iou`、`f1`、`boundary_f1`、`hd95`、`object_hausdorff`

换句话说:

- 这不是只给人看的表
- 它也是后续 crosscheck 和 visual 导出的结构化输入

## 这个文件没说明什么

这张表没有单独解释:

1. `best.ckpt` 是怎么来的
2. `threshold_value` 是怎么冻结的
3. 为什么出现 `adhesion_merge`

这些问题要分别去看:

- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `src_eval_run_eval.py.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`

## 和上下游怎么衔接

- 上游是 `../../../../scripts/test.py` 调 `../../../../src/eval/run_eval.py` 生成 sample-only 行，并写入 source/eval lineage、同空间 GT/prediction 路径
- 下游是 `../../../../scripts/summarize_stage.py` 做 split 重聚合，`../../../../b_class_auxiliary/tools/check_independent_metrics.py` 读取 PNG+GT 独立重算，crosscheck、error_cases 与阶段 summary 消费这些结果

## 当前最该注意的一点

最容易读偏的地方只有一个:

不要把 split 级汇总当成整张表的全部价值。

真正支撑后续错例定位和人工审稿的，是 sample 行保留下来的路径与指标。

## 如何手工验证这个文件的正确性

最短验证步骤可以按 4 步走:

1. 检查表内全部行的 `row_type=sample`
2. 检查全部 sample 行的 `split_role` 都是 `testA`，正式数量为 60
3. 检查 `eval_image_path`、`eval_gt_path`、`pred_path` 是否真实存在且同尺寸
4. 用 sample 行重算指标均值，并与独立 PNG+GT 复核及阶段汇总一致

通过标准:

- 当前正式 A1 TestA 有 60 条 sample 行，无 aggregate 行
- `source_image_path`、`source_mask_path`、`eval_image_path`、`eval_gt_path`、`pred_path` 均可回溯
- 三类评估资产尺寸一致，GT 为二值
- 独立 PNG+GT 指标复核 `testA.status=pass`，且与阶段汇总一致

## 常见问题

- 测试阶段 `loss`、`loss_bce`、`loss_dice` 明确为 `not_applicable`，不能以 aggregate 行解释当前正式 CSV
- 当前正式 A1 TestA 是 60 条 sample 行；历史本地抽样数量不属于当前结果
- 不要跳过 `sample_id`，后面 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 都靠它回指

## 建议联读

- `scripts_test.py.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_metric_crosscheck_note.md`
