# Pre-check Guard

## 1. 本次任务归属
- 当前阶段: `03_UNet稳定性`
- 上一阶段: `02_UNet流程验证`
- 当前任务: `20260708_03_unet_stability_precheck`
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- Stage Gate Result: `allow`

## 2. 来自规划的硬约束
- `03_UNet稳定性` 只能在 `02_UNet流程验证`(A1 单次闭环)已严格放行后启动,且唯一变量只有 train_seed (`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`)。上一阶段放行锚点见 `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md` 和 `reports/stage_reports/implementation_tracking/02_UNet流程验证/implementation_status.md`。
- 三次 run 执行顺序为 seed3407、seed1234、seed2025,唯一合法差异是 train_seed 与派生字段 (`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`)
- raw per-seed 表必须先于 mean±std 聚合表,聚合表 n_runs 为 3 且 result_tag 记 reproduced,TestA 与 TestB 分开 (`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`)
- 数据口径、light_aug_v1、BCE 与 Dice、AdamW 与 scheduler、best_selector、threshold_source=val17、边界宽度、连通域实现全部冻结 (`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`)

## 3. 来自参考资料的实现依据
- `b_class_auxiliary/tools/check_precheck_docs.py` 已给出 Pre-check 四件套、阶段门禁一致性、十目录最小扫描与真实路径锚点的自动门禁规则
- `b_class_auxiliary/tools/check_stage_definition_gate.py` 已确认当前阶段锁定结论成立,可作为本轮 Pre-check 的直接上游依据
- `crc_gland_segmentation_project/experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 已冻结 train_proto_v1、eval_proto_v1、best_selector、threshold_source 与边界宽度,是 A2 协议继承基准
- `crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/02_UNet流程验证/scripts_test.py.md` 已记录 split-wise 指标导出链,A2 聚合必须建立在同一导出结果之上

## 4. 当前工程已有能力与缺口
- 已有能力:
  - 已有研究记录与研究门禁报告
  - 已有当前阶段实现卡与阶段锁定门禁报告
  - 已有五层正式配置 `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 与 stage02 完整源码主链 `src/models/unet.py`
  - 已有训练、测试与阶段汇总脚本 `scripts/summarize_stage.py`
  - 已有 A1 正式冻结 run `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`,metric_crosscheck_result 为 pass
  - 已有 stage02 正式报告链 `reports/stage_reports/unet_flow_stage_summary.md`
- 当前缺口:
  - `scripts/summarize_stage.py` 只做 stage02 单 seed,缺三 seed raw 与 mean±std 聚合能力
  - `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 尚未派生 seed1234 与 seed2025 两个 A2 配置
  - `experiments/` 尚无 A2 三次重复 run 资产,稳定性物理证据链未建立

## 5. 本次任务边界
- 明确要做:
  - 新建 `pre_check_extraction.md`
  - 新建 `stage_gate_check.md`
  - 新建 `current_codebase_状态.md`
  - 新建当前 Pre-check Guard
  - 运行 `b_class_auxiliary/tools/check_precheck_docs.py`
- 明确不做:
  - 不进入正式编码
  - 不创建 A2 experiment 配置或三次 run 资产
  - 不改动 `scripts/summarize_stage.py` 或任何 A1 已冻结结果

## 6. 预期代码落点
- 新建文件:
  - `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/stage_gate_check.md`
  - `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/current_codebase_状态.md`
  - `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/pre_check_extraction.md`
  - `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/20260708_03_unet_stability_pre_check_guard.md`
- 修改文件:
  - 本轮无正式代码修改;`scripts/summarize_stage.py` 的扩展留到编码阶段
- 影响的 run / report / external:
  - 只影响 `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/` 下的 Pre-check 文档与 gate 报告;不影响 `experiments/`、`external/` 与 A 类正式报告链

## 6.0 预期最小运行验证
- py_compile / import: 本轮无正式代码改动,运行级 import 与 py_compile 记为 not_applicable;当前最小验证只针对 Pre-check 文档门禁
- `最小运行验证命令`: 当前只运行 `b_class_auxiliary/tools/check_precheck_docs.py` 对本轮 Pre-check Guard 做正式检查
- smoke run: 当前只检查四件套、阶段卡与阶段锁定门禁一致性,不进入训练链
- dataloader batch: not_applicable;本轮只声明后续编码阶段必须基于 `configs/data/glas.yaml` 与 `splits/glas/glas_val17.csv` 留下 batch 级物理证据
- loss / backward / optimizer.step: not_applicable;本轮不进入训练与反向链
- 计划生成的 runtime_check_report.md: `not_applicable`
- 计划生成的代码质量门禁报告: `not_applicable`

## 6.1 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对应学习型说明文 | 入口同步项 | 计划动作 | 备注 |
|-------------|------|---------|-------------|-----------|---------|------|
| scripts/train.py | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md` §8.1 要求协议红线字段三层落盘,编码阶段需在 build_run_meta() 补写 eval_cast_policy/connected_components_connectivity/boundary_metric_impl/connected_components_impl | reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_train.py.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | update | 编码阶段为修复协议红线字段三层落盘纳入,详见 Post-QC 4.2 差异说明 |
| scripts/test.py | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md` §8.1 要求 test.py 生成的 run_meta 与 train.py 协议字段一致 | reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_test.py.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | update | 编码阶段为对齐 run_meta 协议字段纳入,详见 Post-QC 4.2 差异说明 |
| scripts/summarize_stage.py | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md` 点名三 seed 聚合入口,后续编码将扩展 raw 与 mean±std 能力 | reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | update | 编码阶段落地后由 learning-doc 回填 |
| src/data/datasets.py | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md` 要求数据协议字段不被行内注释污染,编码阶段需修复 _strip_inline_comment | reports/stage_reports/implementation_tracking/03_UNet稳定性/src_data_datasets.py.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | update | 编码阶段为修复 YAML 行内注释解析纳入,详见 Post-QC 4.2 差异说明 |
| configs/eval/eval_proto_v1.yaml | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md` §8.1 要求 eval config 链落盘 boundary_metric_impl 与 connected_components_impl | reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_eval_eval_proto_v1.yaml.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | update | 编码阶段为补齐评估协议字段落盘纳入,详见 Post-QC 4.2 差异说明 |
| configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md` 要求 seed3407 独立 experiment 配置 | reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed3407.yaml.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | create | 由 A1 配置仅改 train_seed 与 run_name 派生 |
| configs/experiment/A2_UNet_GlaS_v1_seed1234.yaml | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md` 要求 seed1234 独立 experiment 配置 | reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed1234.yaml.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | create | 由 A1 配置仅改 train_seed 与 run_name 派生 |
| configs/experiment/A2_UNet_GlaS_v1_seed2025.yaml | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md` 要求 seed2025 独立 experiment 配置 | reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed2025.yaml.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | create | 由 A1 配置仅改 train_seed 与 run_name 派生 |
| reports/tables/unet_seed_results.csv | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md` 要求 raw per-seed 表先落盘 | reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_seed_results.csv.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | create | aggregation 记 single_seed |
| reports/tables/unet_mean_std_summary.csv | A | `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md` 要求 mean±std 聚合表 | reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_mean_std_summary.csv.md | reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md | create | n_runs 为 3,result_tag 记 reproduced |
| b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/pre_check_extraction.md | B | Pre-check 提取文件,只服务当前流程留痕 | not_applicable | not_applicable | not_applicable | 不属于 implementation_tracking |
| b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/stage_gate_check.md | B | Pre-check 阶段门控检查文件,只服务当前流程留痕 | not_applicable | not_applicable | not_applicable | 不属于 implementation_tracking |
| b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/current_codebase_状态.md | B | 代码库现实扫描文件,只服务当前流程留痕 | not_applicable | not_applicable | not_applicable | 不属于 implementation_tracking |
| b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/20260708_03_unet_stability_pre_check_guard.md | B | 当前 Pre-check 汇总件,只服务当前流程留痕 | not_applicable | not_applicable | not_applicable | 不属于 implementation_tracking |

## 7. 上游 guard 文件回链
- 阶段卡正式输出名 `00_阶段实现卡.md`: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md`
- 阶段锁定门禁报告 `stage_definition_gate_report.md`: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/stage_definition_gate_report.md`
- `pre_check_extraction.md`: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/pre_check_extraction.md`
- `stage_gate_check.md`: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/stage_gate_check.md`
- `current_codebase_状态.md`: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/current_codebase_状态.md`
- 门禁报告 precheck_doc_gate_report.md: 生成于同目录 precheck_doc_gate_report.md
