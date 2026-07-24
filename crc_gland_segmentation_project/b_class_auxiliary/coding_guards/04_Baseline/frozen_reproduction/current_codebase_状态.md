# Current Codebase 状态

## 0. 本轮最小扫描范围

| 目录 | 为什么必须扫描 | 最低检查动作 |
|---|---|---|
| `datasets/` | 核对 GlaS 数据根仍是 future configs 的只读输入 | `datasets/01_GlaS_official_raw/train_1.bmp` 存在；扫描 759 个文件，不创建新数据。 |
| `splits/` | 核对固定 split 有真实资产 | `splits/glas/glas_train68.csv` 存在；扫描 10 个文件，未来配置继续消费。 |
| `configs/` | 核对 six future configs 与 train/eval refs | `configs/experiment/A2_UNet_GlaS_frozen_repro_seed3407.yaml` 存在；扫描 53 个文件。 |
| `src/` | 确认模型实现未在本轮编辑 | `src/models/unet.py` 存在；扫描 119 个文件，仅只读。 |
| `scripts/` | 确认未来训练/测试入口存在但不调用 | `scripts/train.py` 存在；扫描 18 个文件，不运行入口。 |
| `tools/` | 确认正式辅助工具目录存在 | `tools/stage02_experiment_environment_check.py` 存在；扫描 13 个文件。 |
| `b_class_auxiliary/` | 核对 checker、future guard 和契约路径 | `b_class_auxiliary/tools/check_precheck_docs.py` 与 future contract 文件 存在；扫描 328 个文件。 |
| `experiments/` | 防止 future output 与既有历史资产混用 | `experiments/README.md` 存在；扫描 14188 个文件；future six-run 输出目录保留给后续真实执行。 |
| `external/` | 核对本轮不消费第三方适配资产 | `external/README.md` 存在；扫描 1 个文件。 |
| `reports/` | 核对问题登记和历史边界可回链 | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` 存在；扫描 360 个文件。 |

## 1. 当前阶段相关目录扫描

| 目录 | 已有文件/资产 | 状态 | 本次是否受影响 |
|---|---|---|---|
| `datasets/` | `datasets/01_GlaS_official_raw/train_1.bmp`；759 个文件 | 数据目录存在；future round 只读使用，未运行数据加载 | 否 |
| `splits/` | `splits/glas/glas_train68.csv`；10 个文件 | 冻结 split 存在；未编辑、未执行采样 | 否 |
| `configs/` | `configs/experiment/A2_UNet_GlaS_frozen_repro_seed3407.yaml`、`configs/experiment/B1_ResNet34_UNet_GlaS_frozen_repro_seed3407.yaml`；53 个文件 | six future configs 存在；本轮仅核对，不编辑 | 否 |
| `src/` | `src/models/unet.py`、`src/models/resnet34_unet.py`；119 个文件 | 模型源码存在；本轮不修改且未运行 import/forward | 否 |
| `scripts/` | `scripts/train.py`、`scripts/test.py`；18 个文件 | 入口存在；本轮禁止调用正式训练或测试 | 否 |
| `tools/` | `tools/stage02_experiment_environment_check.py`；13 个文件 | 辅助工具存在；不作为 future runtime 证据 | 否 |
| `b_class_auxiliary/` | `b_class_auxiliary/tools/check_precheck_docs.py`、`b_class_auxiliary/tools/stage_contract_checker.py`；328 个文件 | 文档/契约检查工具存在；本轮只运行 checker 和 Python 语法编译 | 是 |
| `experiments/` | `experiments/README.md`；14188 个文件 | 历史资产存在；future six-run 输出目录保留给后续真实执行，未编辑任何结果、ckpt、run_meta 或 metrics | 否 |
| `external/` | `external/README.md`；1 个文件 | external 目录存在；future round 不消费外部实现 | 否 |
| `reports/` | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md`；360 个文件 | 报告与问题登记存在；只读使用其 historical/future 边界 | 否 |

## 2. 已实现能力
- 已有训练入口: `scripts/train.py` 存在，但本轮未运行。
- 已有评估入口: `scripts/test.py` 与 `configs/eval/eval_proto_v1.yaml` 存在，但本轮未运行。
- 已有配置体系: 六份 future experiment YAML 与 future stage contract 存在，且 contract checker 已用于前置核对。
- 已有结果资产: 仅有 historical/current 资产；future frozen reproduction 没有 run、checkpoint、metrics、prediction、runtime 或 smoke 资产。

## 3. 缺口与风险
- future six-run 尚未做 runtime、smoke、正式训练、测试和独立指标复核；所有模型性能未知。
- `experiments/` 含历史资产，future run 必须保持新 run_name/output_dir，禁止把现有 v1 指标作为 future 结果。
- checker pass 只证明 pre-run 契约与文档结构，不证明 dataloader、forward、loss、backward、optimizer.step 或模型质量。

## 4. 本次预计新增/修改

| 文件 | 动作 | 原因 | 是否已有相近实现 |
|---|---|---|---|
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/研究定标记录.md` | create | future-only 研究定标 | 有旧简版，改为导航/历史兼容。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/00_阶段实现卡.md` | create | future-only 阶段锁定 | 有旧简版，改为导航/历史兼容。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/pre_check_extraction.md` | create | checker 所需独立四件套 | 有旧汇总件，不替代独立文件。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/stage_gate_check.md` | create | 记录 allow 的 Pre-check 边界 | 有 04 共享范例。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/current_codebase_状态.md` | create | 留下 ten-directory 真实扫描 | 有 04 共享范例。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/Pre-check Guard.md` | create | 汇总前检与文档映射 | 有模板。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_*gate_report.md` | create | 专用 checker 输出，避免覆盖共享报告 | 有既有专用报告路径。 |

## 5. 预期工程落点汇总

| 对象层 | 目录/文件 | 当前状态 | 本轮动作 |
|---|---|---|---|
| 代码层 | `src/models/unet.py`、`src/models/resnet34_unet.py`、`scripts/train.py` | 已存在，未做本轮运行验证 | 只读，不修改。 |
| 配置层 | `configs/experiment/A2_UNet_GlaS_frozen_repro_seed3407.yaml`、`configs/experiment/B1_ResNet34_UNet_GlaS_frozen_repro_seed3407.yaml` | 已存在，future pending | 只读核对，不修改。 |
| 运行资产层 | future A2/B1 six-run 输出目录 | 当前未创建 | 不创建、不运行。 |
| 报告层 | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | 已存在，定义历史/未来边界 | 只读回链。 |
| 治理层 | `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/` | future 独立 B 类 guard 目录 | 创建文档、专用报告与实现依据记录。 |
