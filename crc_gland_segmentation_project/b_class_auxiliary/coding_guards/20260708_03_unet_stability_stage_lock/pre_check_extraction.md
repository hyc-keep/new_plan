# Pre-check 约束提取

## 1. 本轮任务与上游依据
- 当前阶段: `03_UNet稳定性`,当前任务: 为三个当前正式 run（`A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`）锁定 Pre-check 边界；配置文件名的 `v1` 只是版本路径标识
- 阶段实现卡: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md`,阶段锁定门禁结论已在同目录 stage_definition_gate_report.md 记为 pass
- 研究依据: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_research/研究定标记录.md` 研究结论状态已为 allow_stage_lock
- 上游冻结基准: `crc_gland_segmentation_project/experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 已记录 metric_crosscheck_result 为 pass

## 2. 规划约束提取

| 约束类型 | 来源 | 提取出的硬约束 | 本轮如何遵守 |
|---------|------|---------------|-------------|
| 官方协议固定项 | `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md` | TestA 与 TestB 分开评估,阈值只来自 val17,测试集不得重搜阈值,对象级三指标为主表,阈值前保持 float32 | 三次 run 评估链必须逐字段继承 A1,不新增测试集调参 |
| 路线层已锁定 | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md` | 当前阶段唯一变量只有 train_seed,其余数据、训练、评估协议全部继承 A1 冻结项 | 只新增三个 experiment 配置改 train_seed 与 run_name,不动其它协议 |
| 论文支持的候选范围 | `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md` | GlaS 的 TestA 与 TestB 是分开的官方测试角色,对象级评价是任务传统 | 稳定性统计按 TestA 与 TestB 分别产出 mean±std,不合并两个测试集 |
| 工程冻结规则 | `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md` | 数据口径、light_aug_v1、BCE 与 Dice、AdamW 与学习率与 scheduler、epoch_max、early_stop、batch_size、best_selector、threshold_source、边界宽度、连通域实现全部冻结,三组 seed 固定为 3407、1234、2025 | 本轮把这些写成禁止改动项,三次 run 仅 train_seed 派生字段不同 |

## 2.1 预期工程落点
- 正式代码: `crc_gland_segmentation_project/scripts/summarize_stage.py` 扩展三 seed sample-only raw per-seed 表与可选 mean±std 派生表能力
- 配置模板: `/home/featurize/work/Paper/crc_gland_segmentation_project/configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`；真实配置文件分别为 `/home/featurize/work/Paper/crc_gland_segmentation_project/configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml`、`/home/featurize/work/Paper/crc_gland_segmentation_project/configs/experiment/A2_UNet_GlaS_v1_seed1234.yaml`、`/home/featurize/work/Paper/crc_gland_segmentation_project/configs/experiment/A2_UNet_GlaS_v1_seed2025.yaml`。三个正式 `run_name` 分别固定为 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`，均不带 `v1` 后缀，并由对应配置文件中的 `run_name` 字段提供。
- 运行资产: `crc_gland_segmentation_project/experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 作为协议继承基准,后续新增三个 A2 run 目录
- 当前评估资产：每个 run 的 TestA60/TestB20 sample-only CSV，无 aggregate 行；同空间 eval image/GT/prediction PNG；独立 PNG+GT 复核 pass。
- 报告文件位于 `/home/featurize/work/Paper/crc_gland_segmentation_project/reports/tables/`；阶段报告新增稳定性说明，per-run CSV 不写 aggregate 行

## 3. 路线层约束提取
- 唯一变量: 依据 `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`,三次 run 执行顺序为 seed3407、seed1234、seed2025,唯一合法差异是 train_seed 与其派生的 run_name 及时间字段
- 聚合规则: 依据 `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`,当前 per-run TestA/TestB CSV 为 sample-only、无 aggregate 行；先由 sample 行生成 raw per-seed=42 行，再按需生成 mean±std summary=14 行，统计派生表 n_runs 为 3 且 result_tag 记 reproduced
- 验收边界: 依据 `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`,Gate_A2 要求三次 run 完整、协议一致、sample-only raw=42、七项指标和失败汇总就绪；mean±std 是独立派生统计，才允许交接 04_Baseline

## 4. 文献/参考实现提取
- 结构身份: `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/02_U-Net.md` 明确标准 UNet 结构身份在 A1 已冻结,稳定性阶段不得改动结构
- 对象级评估: `crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/02_UNet流程验证/src_metrics_seg_metrics.py.md` 已记录 pixel/object/boundary 三层指标口径,三次 run 必须复用同一实现
- 汇总入口现状: `crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/02_UNet流程验证/scripts_test.py.md` 已记录 split-wise 指标导出链,A2 聚合必须建立在同一导出结果之上

## 5. 当前阶段唯一允许改动的变量
- 允许改: 只允许新增三个真实配置文件，且其正式身份由配置中的 `run_name` 字段固定；唯一变量为 train_seed；扩展 summarize_stage.py 支持三 seed sample-only raw、七项指标和统计派生
- 不允许改: 不允许改动 GlaS split、数据口径、mask 前景规则、input_size、归一化、light_aug_v1、BCE 与 Dice 组合、AdamW 与学习率与 scheduler、epoch_max、early_stop、batch_size、best_selector=val_objdice_max、threshold_source=val17、eval_cast_policy、boundary_metric_width=3、连通域实现与 UNet 结构;不允许提前进入 04_Baseline;不允许删除或替换难看 seed 后再汇总
