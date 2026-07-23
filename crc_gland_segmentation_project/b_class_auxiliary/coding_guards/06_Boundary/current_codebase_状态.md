# Current Codebase 状态

## 0. 本轮最小扫描范围

| 目录 | 为什么必须扫描 | 最低检查动作 |
|------|---------------|-------------|
| `datasets/` | 确认 GlaS 原始图像、标注和官方来源资产可读 | 扫描 `datasets/01_GlaS_official_raw/Grade.csv`、BMP 样本；真实目录存在且文件数超过 200 条扫描上限 |
| `splits/` | 确认 train68/val17/TestA60/TestB20 split 文件完整 | 检查 `splits/glas/glas_train68.csv`、四个 CSV；真实目录识别到 10 个文件 |
| `configs/` | 确认 B1/eval 配置可复用，历史协议隔离 | 检查 `configs/eval/eval_proto_v1.yaml`、模型 YAML；真实目录识别到 30 个文件 |
| `src/` | 确认当前模型、数据、loss、评估和输出接口 | 扫描 `src/models/resnet34_unet.py`、`src/engine/trainer.py`；真实目录识别到 25 个 Python 文件 |
| `scripts/` | 确认 train/test/summarize/export 入口 | 检查 `scripts/train.py`、`scripts/test.py`；真实目录识别到 11 个文件 |
| `tools/` | 确认数据工具和辅助工具，不误改 C 类工具 | 检查 `tools/stage01_data_protocol/build_boundary_targets.py`、`tools/README.md`；真实目录识别到 13 个文件 |
| `b_class_auxiliary/` | 确认本阶段 guard、通用 checker 和历史证据隔离 | 检查 `b_class_auxiliary/tools/check_precheck_docs.py`、`b_class_auxiliary/tools/stage_contract_checker.py`；目录真实存在并有 06 guard 资产 |
| `experiments/` | 确认 B1/05 真实资产和当前目录是否会被覆盖 | 检查 `experiments/B1_ResNet34_UNet_GlaS_seed3407/val_metrics.csv`、C1 metric CSV；真实目录存在且有历史资产 |
| `external/` | 确认第三方适配层是否受影响 | 检查 `external/README.md`；真实目录识别到 1 个文件 |
| `reports/` | 确认 manifest、split/data checks、历史结果和 handoff | 检查 `reports/stage_reports/asset_manifest.json`、`reports/tables/baseline_stage_manifest.csv`；真实目录识别到 329 个文件 |

## 1. 当前阶段相关目录扫描

| 目录 | 已有文件/资产 | 状态 | 本次是否受影响 |
|------|--------------|------|---------------|
| `datasets/` | `datasets/01_GlaS_official_raw/Grade.csv`、`datasets/01_GlaS_official_raw/train_1.bmp`、`datasets/01_GlaS_official_raw/testA_1.bmp`、`datasets/01_GlaS_official_raw/testB_1.bmp` | 原始 GlaS 图像/标注文件存在；本次扫描结果达到 200 条上限，因此不据此推断总文件数；另有 `crc_gland_segmentation_project/datasets/DATASETS_README.md` 和 `crc_gland_segmentation_project/datasets/DATASET_SOURCE_NOTES.md` | 只读消费，不修改 |
| `splits/` | `crc_gland_segmentation_project/splits/glas/glas_train68.csv`、`crc_gland_segmentation_project/splits/glas/glas_val17.csv`、`crc_gland_segmentation_project/splits/glas/glas_testA60.csv`、`crc_gland_segmentation_project/splits/glas/glas_testB20.csv` | `splits/` 当前识别到 10 个文件；四个冻结 GlaS split CSV 均存在，字段/样本数在文件名和既有协议中分别固定为 68/17/60/20 | 只读消费，不修改 |
| `configs/` | `crc_gland_segmentation_project/configs/model/resnet34_unet.yaml`、`crc_gland_segmentation_project/configs/eval/eval_proto_v1.yaml`、3 个 B1 config、3 个 C1 LKMA config | 当前识别到 30 个配置文件；当前 config 体系存在，但没有 06 Boundary config | 后续 Pre-check 通过后新增 06 config |
| `src/` | `crc_gland_segmentation_project/src/models/resnet34_unet.py`、`crc_gland_segmentation_project/src/data/boundary_targets.py`、`crc_gland_segmentation_project/src/metrics/seg_metrics.py`、`crc_gland_segmentation_project/src/engine/trainer.py` | 当前有 25 个 Python 文件；模型 forward 是单输出，Boundary target/metric 已有但语义不完全闭合 | 后续最小修改，当前不改 |
| `scripts/` | `crc_gland_segmentation_project/scripts/train.py`、`crc_gland_segmentation_project/scripts/test.py`、`crc_gland_segmentation_project/scripts/summarize_stage.py`、`crc_gland_segmentation_project/scripts/export_visuals.py` | 正式入口存在；当前识别到 11 个脚本/相关文件，import/build 路径按单输出模型 | 后续可能最小适配，当前不改 |
| `tools/` | `crc_gland_segmentation_project/tools/stage01_data_protocol/build_boundary_targets.py`、`crc_gland_segmentation_project/tools/stage01_data_protocol/build_distance_targets.py`、`crc_gland_segmentation_project/tools/stage01_data_protocol/validate_data_assets.py` | 当前识别到 13 个工具文件；数据辅助工具存在，Boundary target 工具不是当前正式训练入口 | 不受影响；只读核对，不复制为正式实现 |
| `b_class_auxiliary/` | `crc_gland_segmentation_project/b_class_auxiliary/tools/check_precheck_docs.py`、`crc_gland_segmentation_project/b_class_auxiliary/tools/stage_contract_checker.py`、`crc_gland_segmentation_project/b_class_auxiliary/coding_guards/06_Boundary/00_阶段实现卡.md` | 当前 guard/tool 体系识别到 06 阶段卡、研究 gate、stage definition gate 和 05 历史 runtime/code-quality 资产；06 尚无 runtime/code quality | 本轮新增 06 Pre-check guard 资产 |
| `experiments/` | `crc_gland_segmentation_project/experiments/C1_R34UNet_LKMA_GlaS_v1_seed3407/metric_crosscheck_note.md`、`crc_gland_segmentation_project/experiments/C1_R34UNet_LKMA_GlaS_v1_seed1234/testB_metrics.csv`、`crc_gland_segmentation_project/experiments/A2_UNet_GlaS_seed2025/testA_metrics.csv` | 当前识别到多阶段实验目录和历史预测/visual/metrics 资产；没有正式 06 Boundary run | 不受影响；只读消费，禁止覆盖 B1/C1 |
| `external/` | `crc_gland_segmentation_project/external/README.md` | 当前识别到 1 个文件；第三方适配层只有说明入口，没有本轮 Boundary 正式实现 | 不受影响 |
| `reports/` | `crc_gland_segmentation_project/reports/stage_reports/asset_manifest.json`、`crc_gland_segmentation_project/reports/data_checks/boundary_target_report.md`、`crc_gland_segmentation_project/reports/tables/baseline_stage_manifest.csv`、`crc_gland_segmentation_project/reports/tables/lkma_stage_manifest.csv` | 当前识别到 329 个报告/辅助文件；manifest、数据检查、baseline/LKMA 表和 handoff 资产存在 | 后续 06 summary/manifest 需新增，不改历史表 |

## 2. 已实现能力
- 已有训练入口: `scripts/train.py`，默认 device 为 cuda；配置、数据入口和单输出 trainer 链存在；当前 `src/engine/trainer.py` 的 forward/loss 接收单一 logits。
- 已有评估入口: `scripts/test.py`、`src/eval/run_eval.py`、`src/metrics/seg_metrics.py`；可输出 TestA/TestB 指标、predictions、eval assets 和 metric crosscheck；当前正式 Boundary F1 使用 erosion-xor+dilation。
- 已有配置体系: B1 当前标准模型/训练/eval config 存在；C1 LKMA config 仅作为历史已完成阶段，06 config 尚未建立。
- 已有结果资产: B1 baseline manifest、summary、predictions、CSV、checkpoint 和 warning lineage 可读；05 LKMA 三 seed 资产和 drop 决策可读；本轮不改结果。

## 3. 缺口与风险
- 缺口1: `crc_gland_segmentation_project/src/models/resnet34_unet.py` 中的 `ResNet34UNet.forward` 当前只返回 `self.head(x)` 的单一 segmentation logits；没有 BoundaryHead 或共享 decoder final feature 输出协议。
- 缺口2: `crc_gland_segmentation_project/src/data/boundary_targets.py` 中的 `build_boundary_band` 使用 PIL MaxFilter/MinFilter，并返回 mask 内部 band；与 06 规定的 contour→dilation boundary band 以及训练/metric 关系尚未完成正式裁决。
- 缺口3: `crc_gland_segmentation_project/scripts/train.py`、`crc_gland_segmentation_project/src/engine/trainer.py`、`crc_gland_segmentation_project/scripts/test.py` 当前按单输出模型组织，双输出 loss、model factory 适配和边界可视化消费接口尚未实现。
- 风险1: 若直接复用现有 target，可能将“内向边界带”误当作计划要求的 contour dilation band，导致训练监督与 Boundary F1 不可解释。
- 风险2: 若直接修改 `eval_proto_v1` 或历史结果字段，会破坏 B1/C1 可比性和 lineage；必须先决定是否沿用 erosion-xor 口径，必要时新建协议并重跑受影响结果。
- 风险3: 06 正式 run、manifest、stage contract、runtime 和 code quality 尚未生成；当前不能由目录存在推断阶段实现成立。

## 4. 本次预计新增/修改

| 文件 | 动作 | 原因 | 是否已有相近实现 |
|------|------|------|----------------|
| `b_class_auxiliary/coding_guards/06_Boundary/pre_check_extraction.md` | create | 留痕规划/路线/参考依据 | 05 有同类 Pre-check 提取 |
| `b_class_auxiliary/coding_guards/06_Boundary/stage_gate_check.md` | create | 留痕进入条件与阻断项 | 05 有同类 Stage Gate |
| `b_class_auxiliary/coding_guards/06_Boundary/current_codebase_状态.md` | create | 留痕真实扫描和工程缺口 | 05 有同类 codebase 状态 |
| `b_class_auxiliary/coding_guards/06_Boundary/Pre-check Guard.md` | create | 汇总本轮 Pre-check 结论 | 05 有同类 guard |
| `b_class_auxiliary/coding_guards/06_Boundary/precheck_doc_gate_report.md` | generate | 机器检查 guard bundle | 05 有同类报告 |
| `src/models/` BoundaryHead 相关文件 | not_applicable in current turn | Pre-check 未通过，不能提前编码 | 当前无正式 BoundaryHead |
| `configs/experiment/` 06 configs | not_applicable in current turn | 正式身份和 schema 尚未由编码后契约生成 | 当前无 06 config |

## 5. 预期工程落点汇总

| 对象层 | 目录/文件 | 本轮为什么会受影响 |
|------|----------|------------------|
| 代码层 | `src/models/resnet34_unet.py`、`src/data/boundary_targets.py`、`src/engine/trainer.py`、`scripts/train.py`、`scripts/test.py` | 只做代码现状核对；实际修改必须等 Pre-check gate 通过并登记实现依据 |
| 配置层 | `configs/model/`、`configs/experiment/`、`configs/eval/eval_proto_v1.yaml` | 只核对当前版本和历史可比性；本轮不修改配置 |
| 运行资产层 | `experiments/` | 只核对 B1/05 资产，不产生 06 run |
| 报告层 | `reports/stage_reports/asset_manifest.json`、`reports/tables/`、`b_class_auxiliary/coding_guards/06_Boundary/` | 只新增本轮 Pre-check guard 文档，不改历史结果表 |
| 治理层 | 当前阶段协议和 `.trae/skills` | 本轮不修改治理规则和计划正文 |
