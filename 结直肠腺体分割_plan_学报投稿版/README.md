# 结直肠腺体分割学报投稿版规划

## Active route
- `active_plan_root=/home/featurize/work/Paper/结直肠腺体分割_plan_学报投稿版`
- `active_project_root=/home/featurize/work/Paper/crc_gland_segmentation_project_journal`
- `historical_plan_root=/home/featurize/work/Paper/结直肠腺体分割_plan_优化版`
- `historical_project_root=/home/featurize/work/Paper/crc_gland_segmentation_project`
- `plan_status=planned`；`execution_status=not_run`；`result_eligibility=false`；`implementation_permission=false`

唯一编号路线：`05_方法协议 → 06_val筛查 → 07_正式GlaS → 08_CRAG验证 → 09_外部对比 → 10_结果汇总 → 11_总验收与止损`。N1/N2/N3 是 05 内方法身份，不是三个编号阶段。

## 历史边界
01–04 真实历史数值、run 名和 `original_gate_b1=false` 保持不变。B1=`historical_readonly + valid_with_stability_warning`。原规划/原工程与 `_historical*` 仅 `historical_provenance_only`，不得进入当前 Gate。

## 当前入口
1. `00_副本与历史资产保护声明.md`
2. `01_实验执行/00_总览与规范/00_执行导航.md`
3. `01_实验执行/05_方法协议/00_阶段总协议.md`

本轮仅治理，不启动研究之后的编码、训练、测试或新评估，不含任何新指标。
