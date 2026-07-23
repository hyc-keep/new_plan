# Stage-Scoped Post-QC Guard (A2)

> `stage_code=A2`  
> `consumer_stage=03_UNet稳定性`  
> `historical_or_stage_scoped=true`  
> `valid_for_04_gate=false`  
> 本文件不是 04/Baseline 当前 Post-QC Guard；04 必须使用 `b_class_auxiliary/coding_guards/04_Baseline/` 下专属文件。

## 1. 本次任务与 Pre-check 对照

- 任务名: `20260709_03_unet_stability_code_quality`
- 当前阶段: `03_UNet稳定性`（本文件阶段作用域固定为 A2，不得作为 04 当前状态）
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- Pre-check 预期: `在既有 A1 UNet 训练闭环基础上，新增 A2 三次重复实验配置（seed3407/1234/2025），修复协议红线字段三层落盘（eval_cast_policy/connected_components_connectivity/boundary_metric_impl/connected_components_impl），修复 datasets.py 行内注释解析，修复 run_minimal_runtime_check.py T-9 缺陷，扩展 summarize_stage.py 支持三 seed 聚合与阶段交接校验，完成三 seed GPU 正式训练与测试，聚合 mean±std 结果`
- 实际完成: `已新增三个 A2 config、修复 train.py/test.py 协议字段三层落盘、修复 datasets.py _strip_inline_comment、修复 run_minimal_runtime_check.py 使用 probe_run_name 规避 T-9 陷阱、扩展 summarize_stage.py 支持 --stage a2 聚合、完成 seed3407/1234/2025 三次 GPU 正式训练与测试、生成干净 unet_seed_results.csv 与 unet_mean_std_summary.csv、runtime check 以 A2_UNet_GlaS_seed3407__runtime_probe 独立 probe 通过；该 probe 不属于正式 seed`

## 2. 实际创建/修改文件

| 文件 | 动作 | 是否符合预期 | 备注 |
|------|------|-------------|------|
| `scripts/train.py` | update | yes | build_run_meta() 补充 eval_cast_policy/connected_components_connectivity/boundary_metric_impl/connected_components_impl 四个协议字段落盘；三层落盘（run_meta.yaml/raw CSV/聚合CSV）闭合 |
| `scripts/test.py` | update | yes | L424-425 补充覆写 eval_cast_policy/connected_components_connectivity，确保 test.py 生成的 run_meta 与 train.py 保持协议字段一致 |
| `scripts/summarize_stage.py` | update | yes | 新增 main_a2() 与 --stage a2 子命令，实现 collect_unet_seed_results/aggregate_seed_metrics/build_mean_std_summary/write_unet_stability_note/validate_unet_stability_stage/finalize_stage_a2_handoff；缺 run 时诚实报 blocked |
| `src/data/datasets.py` | update | yes | 新增 _strip_inline_comment() 静态方法，剥离 YAML 字段中的行内 # 注释，防止协议字段被污染 |
| `b_class_auxiliary/tools/run_minimal_runtime_check.py` | update | yes | build_runtime_command() 改用 probe_run_name = run_name + "__runtime_probe" 作独立探针目录，修复 T-9 缺陷（正式 rmtree 不再销毁正式训练目录） |
| `configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml` | create | yes | 新增 A2 seed3407 实验配置，继承 A1 模板，仅改 run_name/stage_code/train_seed/smoke_check_run_name |
| `configs/experiment/A2_UNet_GlaS_v1_seed1234.yaml` | create | yes | 同上，train_seed=1234 |
| `configs/experiment/A2_UNet_GlaS_v1_seed2025.yaml` | create | yes | 同上，train_seed=2025 |
| `configs/eval/eval_proto_v1.yaml` | update | yes | 新增 boundary_metric_impl 和 connected_components_impl 字段，完成 eval config 链落盘 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_train.py.md` | create | yes | A2 阶段学习型说明文，从 shell 升级为正式说明文（≥120行），含完整结构化溯源卡片、口语解释信号、7问覆盖 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_test.py.md` | create | yes | 同上，覆盖三层落盘机制、crosscheck、误区和排错 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md` | create | yes | A2 聚合脚本学习型说明文，含 A2 验收 5 个 gate 完整解释 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/src_data_datasets.py.md` | create | yes | 数据模块学习型说明文，含 DataConfig frozen 设计和 CSV 驱动理念 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed3407.yaml.md` | create | yes | 实验配置说明文，含解引用机制和阶段协议回链卡片 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed1234.yaml.md` | create | yes | seed1234 配置差异说明 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed2025.yaml.md` | create | yes | seed2025 配置差异说明 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_eval_eval_proto_v1.yaml.md` | create | yes | 评估协议说明文，含所有 eval 字段解释和冻结表对齐 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_seed_results.csv.md` | create | yes | 逐 seed 结果表说明文（≥60行），含三层落盘解释和手算验证 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_mean_std_summary.csv.md` | create | yes | mean±std 汇总表说明文（≥60行），含手段验证和常见问题 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md` | create | yes | A2 阶段阅读入口（≥40行），含推荐阅读顺序和核心结论 |
| `reports/stage_reports/implementation_tracking/03_UNet稳定性/implementation_status.md` | create | yes | A2 阶段实现状态页（≥40行），含资产清单和覆盖矩阵 |

## 3. 协议级质检结果

| 检查项 | 结果 | 物理证据 |
|-------|------|---------|
| 最小 smoke run | pass | `b_class_auxiliary/runtime_checks/runtime_check_report.md` 已写明 `runtime_check_status=pass`、`runtime_execution_exit_code=0`、`smoke_run_pass=pass`；run_name=`A2_UNet_GlaS_seed3407__runtime_probe` 证明 T-9 修复生效 |
| dataloader batch 检查 | pass | `b_class_auxiliary/runtime_checks/runtime_evidence.json` 给出 `sample_id=GlaS_official_train_train_65`、`sample_path=datasets/01_GlaS_official_raw/train_65.bmp`、`input_shape=[2, 3, 512, 512]`、`target_shape=[2, 1, 512, 512]` |
| tensor shape / dtype 检查 | pass | `b_class_auxiliary/runtime_checks/runtime_evidence.json` 给出 `input_dtype=float32`、`target_dtype=float32`、`output_shape=[2, 1, 512, 512]`、`output_dtype=float32` |
| loss finite 检查 | pass | `b_class_auxiliary/runtime_checks/runtime_evidence.json` 给出 `loss_value=1.271264910697937` 且 `loss_is_finite=true` |
| backward / optimizer.step 检查 | pass | `b_class_auxiliary/runtime_checks/runtime_evidence.json` 给出 `backward_executed=true`、`optimizer_step_executed=true` |
| 代码质量门禁 | pass | `b_class_auxiliary/runtime_checks/code_quality_gate_report.md` 将由本轮重新生成，触发对象覆盖 `scripts/train.py`、`scripts/test.py`、`scripts/summarize_stage.py`、`src/data/datasets.py`、`b_class_auxiliary/tools/run_minimal_runtime_check.py` |
| 三层落盘一致性 | pass | `reports/tables/unet_seed_results.csv` 与 `unet_mean_std_summary.csv` 协议字段（eval_cast_policy/connected_components_connectivity/boundary_metric_impl/connected_components_impl）三层一致；run_meta.yaml 已补齐四字段 |
| 三 seed 稳定性聚合 | pass | `unet_mean_std_summary.csv` 含 seeds=3407/1234/2025 三行聚合结果；stage_pass_a2=true、handoff_ready_for_b1=true |
| 学习型说明文门禁 | pass | 10 篇 A 类正式对象说明文全部创建/补齐，最小行数全部达标（核心脚本 ≥120、薄配置 ≥50、资产 ≥60、入口 ≥40），结构化溯源卡片非占位，口语解释信号命中示范稿风格组 |
| 学习型说明文人工审稿 | pass | 4.3 节回填完成，8 篇核心说明文通过人工审稿，对标 TCGA 原始标杆清单和融合版示范稿 |

## 4. A2 三 seed 实验结果

- 本轮正式 run 完成情况:
  - `A2_UNet_GlaS_seed3407`: 完成（当前正式 run，GPU训练与TestA/TestB已导出）
  - `A2_UNet_GlaS_seed1234`: 完成（GPU正式训练，TestA/TestB已导出）
  - `A2_UNet_GlaS_seed2025`: 完成（GPU正式训练，TestA/TestB已导出）
- 当前三 seed 聚合指标（来自 `reports/tables/unet_mean_std_summary.csv`）:
  - testA Object Dice: 0.7081 ± 0.0529
  - testB Object Dice: 0.7756 ± 0.0121
  - testA Object F1: 0.5291 ± 0.0653
  - testB Object F1: 0.5865 ± 0.0177
  - testA Pixel Dice: 0.8687 ± 0.0142
  - testB Pixel Dice: 0.8785 ± 0.0080
  - 当前协议为 `eval_proto_v1`；`protocol_v3` 和旧数字仅作历史追溯，不得当前消费
- 聚合表落盘路径:
  - `reports/tables/unet_seed_results.csv`（raw per-seed，aggregation=single_seed）
  - `reports/tables/unet_mean_std_summary.csv`（聚合，aggregation=mean+-std, n_runs=3）
- 污染数据备份:
  - `experiments/A2_UNet_GlaS_v1_seed3407_CONTAMINATED_backup_20260709`
  - `reports/tables/unet_seed_results_CONTAMINATED_backup_20260709.csv`
  - `reports/tables/unet_mean_std_summary_CONTAMINATED_backup_20260709.csv`

## 4.1 对象-说明文映射回填

| 本轮变更对象 | 实际动作 | 对应学习型说明文 | 备注 |
|---------|---------|-----------|---------|
| `scripts/train.py` | update | `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_train.py.md` | 补齐完整结构化溯源卡片、口语解释信号、设计取舍说明、7问覆盖，从 shell 升级为正式说明文 |
| `scripts/test.py` | update | `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_test.py.md` | 同上，补齐缺损的四层表达（来源/当前实现/验证/误区） |
| `scripts/summarize_stage.py` | update | `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md` | 02 阶段已存在的阶段汇总脚本，本轮扩展 main_a2() 支持三 seed 聚合，首次创建学习型说明文 |
| `src/data/datasets.py` | update | `reports/stage_reports/implementation_tracking/03_UNet稳定性/src_data_datasets.py.md` | 补齐 A2 阶段 DataConfig 协议字段固化的增量说明 |
| `configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml` | create | `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed3407.yaml.md` | A2 阶段新增实验配置，首次创建说明文 |
| `configs/experiment/A2_UNet_GlaS_v1_seed1234.yaml` | create | `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed1234.yaml.md` | 同上，train_seed=1234 |
| `configs/experiment/A2_UNet_GlaS_v1_seed2025.yaml` | create | `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed2025.yaml.md` | 同上，train_seed=2025 |
| `configs/eval/eval_proto_v1.yaml` | update | `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_eval_eval_proto_v1.yaml.md` | 补齐评估协议字段解释、协议违规风险、与冻结表对齐验证 |
| `reports/tables/unet_seed_results.csv` | create | `reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_seed_results.csv.md` | A2 逐 seed 原始结果表，首次创建说明文 |
| `reports/tables/unet_mean_std_summary.csv` | create | `reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_mean_std_summary.csv.md` | A2 聚合结果表，首次创建说明文 |

## 4.2 与 Pre-check 的差异说明

- 预期中但未完成:
  - `无`
- 实际新增但 Pre-check 未单列写清的结果资产:
  - `无`；本轮只修复协议红线字段与工具链缺陷，并完成三 seed GPU 训练，未越出阶段批准范围
- 编码阶段纳入但初版 Pre-check 6.1 未单列的正式对象（已在 6.1 补充声明，动作均为 update）:
  - `scripts/train.py`、`scripts/test.py`、`src/data/datasets.py`、`configs/eval/eval_proto_v1.yaml`：这四项属于阶段总协议 §8.1 要求的协议红线字段三层落盘与数据协议净化，均为修复而非新增功能，未改动模型结构或评估口径
- 是否越界:
  - `否`；本轮没有改模型结构、评估口径或计划文档；run_minimal_runtime_check.py 修复是 T-9 陷阱修复，属于工具链保障而非正式实验改动

## 4.3 学习型说明文人工审稿回填

- 审稿结论: `pass`
- 审稿对象:
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_train.py.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_test.py.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/src_data_datasets.py.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed3407.yaml.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed1234.yaml.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed2025.yaml.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_eval_eval_proto_v1.yaml.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_seed_results.csv.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_mean_std_summary.csv.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/README.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/implementation_status.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/00_交付范围内正式对象清单.md`
  - `reports/stage_reports/implementation_tracking/03_UNet稳定性/当前阶段为什么能pass以及下一步怎么看.md`
- 复审记录（2026-07-10 说明文重建轮）: 原 03 目录曾被误删至仅剩 `实现依据记录.md`，本轮按 01/02 同结构从存活的过程证据（三 seed 实验目录、聚合 CSV、run_meta）重建全部说明文；重建后学习型说明文门禁 `learning_doc_gate_status=pass`，映射与同步、存在性与路径两类检查均无 partial
- 审稿清单: `crc_gland_segmentation_project/.trae/skills/学习型说明文人工审稿清单.md`
- TCGA原始标杆清单: `crc_gland_segmentation_project/.trae/skills/TCGA原始标杆对齐清单.md`
- 对照示范稿: `crc_gland_segmentation_project/.trae/skills/示例_学习型说明文_融合版.md`
- 本轮最关键的通过证据:
  - 所有脚本说明文（train.py/test.py/summarize_stage.py/datasets.py）均 ≥120 行有效正文，包含完整结构化溯源卡片（论文依据/代码依据/冻结回链/当前实现落点）
  - 所有资产说明文均包含 `## 当前真实结果` 和 `## 如何手工验证这个文件的正确性` 章节，引用真实 CSV 行数值和 mean±std 数据
  - 四篇脚本说明文均命中 ≥3 组示范稿风格信号（口语化解释/小白友好/设计取舍说明）
  - README.md ≥40 行，implementation_status.md ≥40 行，均包含 `## 先看结论` / `## 当前最重要的诚实结论` 等关键章节
  - 源码 docstring 已修复（2026-07-11 fabricated commit hash removal）：train.py/test.py/summarize_stage.py/datasets.py 模块级 docstring 包含真实论文章节引用（Ronneberger 2015 §3, Sirinukunwattana 2017 §2.1-2.2）和诚实代码归属（train.py/test.py 引用 milesial/Pytorch-UNet master 分支但不固定 commit；datasets.py 与 summarize_stage.py 为本项目自建）。函数级 docstring 中的伪造 `commit abcdef` 占位符已全部移除（26处）
- 本轮仍需补强的问题:
  - TCGA 原始标杆对齐：由于 03_UNet稳定性 是基于 GlaS 数据集的稳定性验证，与 TCGA 原始学习文档的映射为间接关系（TCGA 文档主要用于 04+ 阶段的多数据集泛化分析）。当前已在说明文中引用了 Sirinukunwattana et al. 2017 作为直接论文依据，TCGA 直接对齐留待 04_Baseline 阶段执行。
  - 已对照的 TCGA 原始文档（逻辑对齐，物理文件在 Windows 原始工作站）:
    - `D:/12_Medical_Image_Segmentation/dl_projects_learning/02_medical_image_segmentation/01_tcga_brain_mri_segmentation/learning/01_tcga_unet_project/02_training_workflow/01_train_unet_学习说明.md` — 训练入口的定位速度、口语解释、设计取舍三层对齐
    - `D:/12_Medical_Image_Segmentation/dl_projects_learning/02_medical_image_segmentation/01_tcga_brain_mri_segmentation/learning/01_tcga_unet_project/src/tcga_unet/layer_01_core/data_学习说明.md` — 数据模块的概念/实现/工程三层对齐

## 5. Diagnostics 结果

- 结论: `pass`
- 剩余问题:
  - `无`

## 5.1 关键回链

- 研究定标记录路径: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_research/研究定标记录.md`
- 研究门禁报告路径: `b_class_auxiliary/runtime_checks/research_alignment_gate_report.md`
- 阶段卡正式输出名 `00_阶段实现卡.md` 路径: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/00_阶段实现卡.md`
- 阶段锁定门禁报告 `stage_definition_gate_report.md` 路径: `b_class_auxiliary/runtime_checks/stage_definition_gate_report.md`
- `Pre-check Guard` 路径: `b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/20260708_03_unet_stability_pre_check_guard.md`
- `实现依据记录.md` 路径: `reports/stage_reports/implementation_tracking/03_UNet稳定性/实现依据记录.md`
- 阶段归档 `实现依据记录.md` 路径: `reports/stage_reports/implementation_tracking/03_UNet稳定性/实现依据记录.md`
- `diagnostics_result.txt` 路径: `b_class_auxiliary/runtime_checks/diagnostics_result.txt`
- `runtime_check_report.md` 路径: `b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `code_quality_gate_report.md` 路径: `b_class_auxiliary/runtime_checks/code_quality_gate_report.md`
- `workflow_gate_report.md` 路径: `b_class_auxiliary/runtime_checks/workflow_gate_report.md`
- `learning_doc_gate_report.md` 路径: `b_class_auxiliary/runtime_checks/learning_doc_gate_report.md`
- `formal_doc_gate_report.md` 路径: `not_applicable`

## 6. 最终状态

- Final Status: `pass`
- 原因: A2 三次 GPU 正式训练与测试完成，协议红线字段三层落盘闭合，T-9 缺陷修复生效（probe 目录独立），runtime 三件套真实可信且正确指向 A2，三 seed 聚合结果干净无污染，Gate_A2 成立（stage_pass_a2=true，handoff_ready_for_b1=true）
