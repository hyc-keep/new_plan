# Stage Gate Check

## 1. 检查对象
- 当前阶段: `03_UNet稳定性`
- 上一阶段: `02_UNet流程验证`
- 当前任务: 三个当前正式 run `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025` 的稳定性验证；配置路径的 `v1` 仅表示配置版本
- 阶段实现卡: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md`

## 2. 上游放行依据
- 上一阶段严格通过: `crc_gland_segmentation_project/reports/stage_reports/unet_flow_stage_summary.md` 已记 stage_pass 为 true 且 handoff_ready_for_a2 为 true
- 研究定标已通过: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_research/研究定标记录.md` 研究结论状态为 allow_stage_lock
- 阶段锁定已通过: 同目录 stage_definition_gate_report.md 记 stage_definition_gate_status 为 pass

## 3. 当前阶段进入条件

| 进入条件 | 是否满足 | 证据 |
|---------|---------|------|
| A1 单次闭环已严格完成并冻结 | 满足 | `crc_gland_segmentation_project/experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 记 metric_crosscheck_result 为 pass |
| 三次重复的唯一变量与执行顺序已锁定 | 满足 | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md` 已固定 seed3407、seed1234、seed2025 顺序 |
| sample-only raw 与 mean±std 统计派生 schema 已锁定 | 满足 | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md` 已定义七项指标、raw=42、mean±std=14 和无 per-run aggregate 行 |
| Gate_A2 与交接边界已明确 | 满足 | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md` 已定义完整性、一致性与交接门槛 |
| 阶段边界已正式锁定 | 满足 | `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md` 已锁定唯一目标与禁止改动项 |

## 4. 阻断项

| 阻断项 | 当前状态 | 说明 |
|-------|---------|------|
| 三次 run 是否在一致 GPU 与 cudnn/AMP 语义下连续执行 | 当前已由三份正式 run_meta 和训练资产核验 | 三个正式 run 均为 cuda、smoke_check=false；后续代码/运行变更需重核 |
| 某 seed 极端偏离判为真实波动还是回退的量化边界 | 当前已记录 | TestA 对象级 F1/Object Dice 波动较大，但不自动阻断；按阶段验收记录异常和回退边界 |
| 异常 run 重跑的新目录命名与作废标签 | 当前规则已锁定 | 需沿用 `experiments/README.md` 和当前 run_name/config path 分层约定，不得覆盖正式目录 |
| 是否存在未继承 A1 冻结项的隐性改动 | 无 | `pre_check_extraction.md` 已把冻结项写死为禁止改动,唯一变量仅 train_seed；当前正式 run_name 与配置路径版本已分开 |

## 5.1 本轮允许进入的工程落点

| 对象层 | 允许动作 | 落点 |
|-------|---------|------|
| 正式代码 | update | `crc_gland_segmentation_project/scripts/summarize_stage.py` |
| 配置 | create | `crc_gland_segmentation_project/configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 派生的 A2 三配置 |
| 运行资产 | create | `crc_gland_segmentation_project/experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 同级新增三个 A2 run 目录 |
| 报告 | create | `crc_gland_segmentation_project/reports/tables/unet_flow_stage_manifest.csv` 同级新增稳定性 raw 与聚合表 |

## 5. 结论
- 上一阶段已严格放行,研究定标与阶段锁定均已通过,进入条件全部满足,阻断项无一构成 Pre-check 进入阻断
- Stage Gate Result: `allow`
