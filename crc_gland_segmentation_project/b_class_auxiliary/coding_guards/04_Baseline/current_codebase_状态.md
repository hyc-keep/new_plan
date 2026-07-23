# Current Codebase 状态

## 0. 本轮最小扫描范围

| 目录 | 为什么必须扫描 | 最低检查动作 |
|------|---------------|-------------|
| `datasets/` | 确认正式 GlaS 数据根和 B1 可复用性 | 读取 `datasets/01_GlaS_official_raw` 与 `reports/data_checks/glas_split_report.md`；目录存在，真实扫描文件数为 759，核对 train68/val17/TestA60/TestB20。 |
| `splits/` | 确认冻结 split 不被 B1 改写 | 读取 `splits/README.md`、`splits/glas/README.md`、`splits/glas/glas_train68.csv`；目录存在，真实扫描文件数为 10，核对 CSV 表头和样本字段。 |
| `configs/` | 区分 model/data/eval 候选配置和正式 experiment config | 读取 `configs/model/resnet34_unet.yaml`、`configs/data/glas.yaml`、`configs/eval/eval_proto_v1.yaml`；目录存在，真实扫描文件数为 27，当前无 B1 正式 experiment config。 |
| `src/` | 确认模型、factory、训练和评估接口 | 读取 `src/models/resnet34_unet.py`、`src/models/__init__.py`、`src/eval/run_eval.py`、`src/metrics/seg_metrics.py`；目录存在，真实扫描文件数为 111。 |
| `scripts/` | 确认训练、测试、汇总入口 | 读取 `scripts/train.py`、`scripts/test.py`、`scripts/summarize_stage.py`；目录存在，真实扫描文件数为 11。 |
| `tools/` | 确认环境和数据辅助入口 | 读取 `tools/stage02_experiment_environment_check.py`；目录存在，真实扫描文件数为 13。 |
| `b_class_auxiliary/` | 确认研究、阶段锁定、Pre-check、runtime、质量和总放行工具 | 读取 `b_class_auxiliary/tools/check_precheck_docs.py` 与 `b_class_auxiliary/coding_guards/04_Baseline/04_Baseline_pre_check_guard.md`；目录存在，当前轮证据在此；这两个文件作为真实扫描样本锚点。 |
| `experiments/` | 确认正式 run、checkpoint 和日志是否存在 | 读取 `experiments/README.md`、`experiments/A2_UNet_GlaS_seed1234/testA_metrics.csv`；目录存在，真实扫描文件数为 3680，有 A2 资产但无当前 B1 formal run。 |
| `external/` | 确认第三方适配层是否影响 B1 | 读取 `external/README.md`；目录存在，真实扫描文件数为 1，仅有 README。 |
| `reports/` | 确认 A2 handoff、数据质检和当前/历史边界 | 读取 `reports/tables/unet_stage_manifest.csv`、`reports/stage_reports/unet_stability_stage_summary.md`、`reports/data_checks/glas_split_report.md`；目录存在，真实扫描文件数为 316。 |

## 1. 当前阶段相关目录扫描

| 目录 | 已有文件/资产 | 状态 | 本次是否受影响 |
|------|--------------|------|---------------|
| `datasets/` | `datasets/01_GlaS_official_raw`、`reports/data_checks/glas_split_report.md`；759 个文件 | 正式数据目录存在；数据报告记录 68/17/60/20；B1 只能复用，不改写 | 是 |
| `splits/` | `splits/README.md`、`splits/glas/README.md`、`splits/glas/glas_train68.csv`；10 个文件 | 冻结 split 目录存在；已读取 train68 CSV 表头和样本字段；完整 split contract 尚未生成 | 是 |
| `configs/` | `configs/model/resnet34_unet.yaml`、`configs/data/glas.yaml`、`configs/eval/eval_proto_v1.yaml`；27 个文件 | 配置目录存在；候选 model/data/eval 配置存在；当前没有 B1 正式 experiment config | 是 |
| `src/` | `src/models/resnet34_unet.py`、`src/models/__init__.py`、`src/eval/run_eval.py`、`src/metrics/seg_metrics.py`；111 个文件 | 共享源码目录存在；ResNet34-U-Net 是候选输入，来源和 freshness 尚未裁决 | 是 |
| `scripts/` | `scripts/train.py`、`scripts/test.py`、`scripts/summarize_stage.py`；11 个文件 | 训练、测试、汇总入口存在；当前无 B1 正式调用证据 | 是 |
| `tools/` | `tools/stage02_experiment_environment_check.py`；13 个文件 | 辅助工具存在；环境报告可用不等于 B1 代码已通过 | 否 |
| `b_class_auxiliary/` | `b_class_auxiliary/tools/check_precheck_docs.py`、`b_class_auxiliary/coding_guards/04_Baseline/04_Baseline_pre_check_guard.md`；当前轮 04 门禁目录存在 | B 类工具和当前轮研究、阶段锁定、Pre-check 目录存在；Pre-check 当前仍未通过 | 是 |
| `experiments/` | `experiments/README.md`、`experiments/A2_UNet_GlaS_seed1234/testA_metrics.csv`；3680 个文件 | A2 正式资产存在；当前没有 B1 formal run；历史 B1 不消费 | 是 |
| `external/` | `external/README.md`；1 个文件 | 外部目录存在但无 B1 外部实现消费 | 否 |
| `reports/` | `reports/tables/unet_stage_manifest.csv`、`reports/stage_reports/unet_stability_stage_summary.md`、`reports/data_checks/glas_split_report.md`；316 个文件 | reports/ 目录存在且 A2 handoff 可消费；当前 B1 正式报告尚未生成；历史 B1 报告不消费 | 是 |

## 2. 已实现能力
- 训练入口存在：`scripts/train.py`；当前没有 B1 正式 experiment config 和运行证据。
- 评估入口存在：`src/eval/run_eval.py`；B1 只能继承冻结评估链。
- 模型候选存在：`src/models/resnet34_unet.py`；当前仅作为候选工程输入，不得视为 B1 正式模型，正式身份尚未冻结。
- A2 handoff 存在：`reports/tables/unet_stage_manifest.csv`；是当前 B1 唯一允许消费的上游来源。

## 3. 缺口与风险
- B1 正式 experiment config、三个 seed 的 config/run mapping 和 stage contract 尚不存在。
- ImageNet 预训练权重来源、torchvision 版本、缓存文件、SHA256 和离线加载策略尚未形成当前轮机器证据。
- `src/models/resnet34_unet.py`、factory 和标准 model config 已按当前轮重写并登记；旧候选已进入 historical source snapshot。
- 可能误把历史 protocol_v3 资产或候选代码当作当前 B1，造成 freshness/lineage 污染。

## 4. 本次预计新增/修改

本轮只更新 04 专属 B 类 Pre-check 留痕，不修改 A 类协议、共享源码、正式配置或实验结果。
本轮动作范围仅限四件套文档和对应 gate 报告，所有正式代码与实验资产保持只读。
本轮影响判断以真实目录扫描、A2 handoff 和当前 freshness 状态为依据，不把候选文件写成正式 B1 成果。
Pre-check 通过前不创建 B1 experiment config、run、checkpoint、metrics、predictions 或 runtime 证据。

| 文件 | 动作 | 原因 | 是否已有相近实现 |
|------|------|------|----------------|
| b_class_auxiliary/coding_guards/04_Baseline/pre_check_extraction.md | update | 当前轮前置约束留痕 | 有模板，无当前轮旧件 |
| b_class_auxiliary/coding_guards/04_Baseline/stage_gate_check.md | update | 当前轮进入条件和阻断项 | 有模板，无当前轮旧件 |
| b_class_auxiliary/coding_guards/04_Baseline/current_codebase_状态.md | update | 根据真实扫描同步状态 | 有旧版，当前更新 |
| b_class_auxiliary/coding_guards/04_Baseline/04_Baseline_pre_check_guard.md | update | 当前轮 Pre-check 总结 | 有旧版，当前更新 |
| src/models/resnet34_unet.py | not_applicable | Pre-check 不修改正式代码 | 现有候选输入 |
| configs/experiment/ | not_applicable | Pre-check 不创建正式实验配置 | 当前无 B1 配置 |

本轮此前已创建 B1 experiment config；当前仍不创建 formal run、checkpoint、metrics、predictions 或 runtime 证据。

## 5. 预期工程落点汇总

| 对象层 | 目录/文件 | 当前状态 | 本轮动作 |
|------|----------|----------|----------|
| 当前正式协议 | 04_Baseline 计划目录五份协议 | A 类正式协议，原路径保留 | 只读消费，不修改 |
| 当前模型代码 | src/models/resnet34_unet.py | 当前轮标准实现，尚未通过 runtime/code quality | 原路径保留，等待运行证据 |
| 当前模型 factory | src/models/__init__.py | 当前轮标准实现，尚未通过 runtime/code quality | 原路径保留，等待运行证据 |
| 当前 model config | configs/model/resnet34_unet.yaml | 当前轮标准 model config，不是 seed experiment config | 原路径保留，不启动训练 |
| B1 experiment config | configs/experiment/B1_ResNet34_UNet_GlaS_seed3407.yaml、seed1234.yaml、seed2025.yaml | 当前轮正式配置已建立 | 本轮只更新标准model引用，不创建run |
| B1 formal run | experiments/ | 当前无 B1 formal run | 本轮不创建 |
| A2 handoff | reports/tables/unet_stage_manifest.csv | 当前可消费的上游来源 | 只读消费 |
| 当前 Pre-check 证据 | b_class_auxiliary/coding_guards/04_Baseline/ | 当前轮 B 类证据目录 | 只更新四件套和 gate 报告 |
