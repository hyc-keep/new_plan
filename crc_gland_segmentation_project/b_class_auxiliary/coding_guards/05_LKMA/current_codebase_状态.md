# Current Codebase 状态

## 0. 本轮最小扫描范围

| 目录 | 为什么必须扫描 | 最低检查动作 |
|------|---------------|-------------|
| `datasets/` | 确认 GlaS 数据入口和标签资产仍可被 B1/C1 复用 | 真实扫描识别 759 个文件，抽查 `datasets/DATASET_SOURCE_NOTES.md` 和数据样本路径 |
| `splits/` | 确认 train/val/TestA/TestB split 入口可复用 | 真实扫描识别 10 个文件，抽查 `splits/README.md` 并核对 split 文件字段/行数 |
| `configs/` | 确认 B1 当前标准配置和 C1 新配置的实际落点 | 真实扫描识别 30 个 yaml，抽查 `configs/experiment/B1_ResNet34_UNet_GlaS_seed3407.yaml` |
| `src/` | 确认现有模型、训练组件和 LKMA 注入点 | 真实扫描识别 111 个文件，抽查 `src/models/resnet34_unet.py`、`src/models/__init__.py` |
| `scripts/` | 确认 train/test/summarize 入口和输出覆盖行为 | 真实扫描识别 11 个文件，抽查 `scripts/train.py`、`scripts/test.py`、`scripts/summarize_stage.py` |
| `tools/` | 确认辅助检查与独立复核入口 | 真实扫描识别 13 个文件，抽查 `tools/stage02_experiment_environment_check.py` |
| `b_class_auxiliary/` | 确认 gate、runtime、coding guard 和治理产物分层 | 真实扫描识别 174 个文件，抽查 `b_class_auxiliary/tools/check_precheck_docs.py` 和 C1 guard 目录 |
| `experiments/` | 确认 B1 正式 run、历史归档和输出目录身份 | 真实扫描识别 4568 个文件，抽查 `experiments/README.md` 和 B1 run 目录 |
| `external/` | 确认第三方实现是否会被 C1 修改或消费 | 真实扫描识别 1 个文件，抽查 `external/README.md`；本轮不修改 external |
| `reports/` | 确认 B1 阶段报告、表格和 implementation tracking 可供 C1 lineage 回链 | 真实扫描识别 322 个文件，抽查 `reports/stage_reports/` 和问题登记 |

## 1. 当前阶段相关目录扫描

| 目录 | 已有文件/资产 | 状态 | 本次是否受影响 |
|------|--------------|------|---------------|
| `datasets/` | `datasets/DATASET_SOURCE_NOTES.md`；当前识别 759 个文件 | 已存在，数据资产可读；本轮沿用 | 否 |
| `splits/` | `splits/README.md`；当前识别 10 个文件 | 已存在，需在 Pre-check 继续核对字段/行数 | 否 |
| `configs/` | `configs/experiment/B1_ResNet34_UNet_GlaS_seed3407.yaml`、`configs/eval/eval_proto_v1.yaml`；当前识别 30 个 yaml | 已存在，已有 B1/UNet 配置体系；C1 LKMA 配置待 Pre-check 后新增 | 是，Pre-check 后新增 C1 配置 |
| `src/` | `src/models/resnet34_unet.py`、`src/models/__init__.py`；当前识别 111 个文件 | 已存在，已有 R34-U-Net 和 factory；未发现 LKMA 模块 | 是，Pre-check 后新增最小 LKMA 代码并修改真实注入入口 |
| `scripts/` | `scripts/train.py`、`scripts/test.py`、`scripts/summarize_stage.py`；当前识别 11 个文件 | 训练、测试、汇总入口已存在，需核对扩展点和 fresh-run 行为 | 是，可能新增/修改 C1 专属入口 |
| `tools/` | `tools/stage02_experiment_environment_check.py`；当前识别 13 个文件 | 辅助工具已存在，C1 主要复用 b_class_auxiliary gate 工具 | 否/待核对 |
| `b_class_auxiliary/` | `b_class_auxiliary/tools/check_precheck_docs.py`、C1 guard 目录；当前识别 174 个文件 | B 类门禁体系已存在，C1 四件套正在生成 | 是，新增 C1 Pre-check 报告 |
| `experiments/` | `experiments/README.md`、B1 及历史 run 资产；当前识别 4568 个文件 | 已存在，正式资产和历史归档并存；C1 必须使用新 run identity | 是，后续真实运行产生 C1 资产 |
| `external/` | `external/README.md`；当前识别 1 个文件 | 已存在，当前没有 C1 外部适配资产，本轮不影响 | 否 |
| `reports/` | `reports/environment/experiment_environment_check.md`、阶段报告和表格；当前识别 322 个文件 | 已存在，可提供 B1 lineage 和后续 C1 汇总落点 | 是，后续新增 C1 raw/aggregate/decision/handoff |

## 2. 已实现能力
- 已有训练入口: `scripts/train.py`；B1 当前 experiment config 可解析并运行，C1 需要复用其训练协议和 fresh-run 保护。
- 已有评估入口: `scripts/test.py`、`scripts/summarize_stage.py`；对象级指标和阶段汇总入口已存在，C1 需保持字段一致。
- 已有配置体系: `configs/data/glas.yaml`、`configs/model/resnet34_unet.yaml`、`configs/train/unet_flow_v1.yaml`、`configs/eval/eval_proto_v1.yaml` 和 B1 三 seed experiment config。
- 已有结果资产: `experiments/` 下已有 B1/历史资产，`reports/stage_reports/` 下已有阶段报告；C1 尚无正式 run。

## 3. 缺口与风险
- 缺口1: 当前 `src/models/` 未发现 LKMA 模块，且当前 factory 只路由 UNet/ResNet34UNet；Pre-check 后才可确定最小修改接口。
- 缺口2: C1 model/experiment config、stage manifest、cost table、decision note 和 handoff 尚未生成，不能提前把它们写成已完成。
- 风险1: B1 原始 workflow gate blocked，C1 必须携带 stability warning 和 frozen_baseline_with_warning，不能伪造上游 pass。
- 风险2: 历史 v1/v2/v3 配置和正式 B1 当前配置共存，C1 必须显式使用 current_standard lineage，不能误消费历史归档。

## 4. 本次预计新增/修改

| 文件 | 动作 | 原因 | 是否已有相近实现 |
|------|------|------|----------------|
| 项目现有 `src/models/` 下 LKMA 模块文件 | create | 实现 C1 最小 depth-wise large-kernel block | 无直接同类 LKMA 实现；有 R34-U-Net 基础 |
| 项目现有 `src/models/` 下真实 R34-U-Net/factory 入口 | update | 在 bottleneck 注入主版本并保留 shape/identity | 有 `src/models/resnet34_unet.py` 和 `src/models/__init__.py` |
| 项目现有 configs 目录下 C1 model/experiment 配置 | create | 固定主变体、seed、lineage 和评估字段 | 有 B1 experiment config 可作为协议模板，但不复制其 run identity |
| C1 汇总/比较/manifest 入口 | create/update after Pre-check | 生成 raw、aggregate、cost、decision 和 handoff | 有 `scripts/summarize_stage.py`，需先核对可复用性 |

## 5. 预期工程落点汇总

| 对象层 | 目录/文件 | 本轮为什么会受影响 |
|------|----------|------------------|
| 代码层 | 项目现有 `src/models/` 和 `scripts/` 入口 | 新增 LKMA 并将其接入真实 R34-U-Net/汇总链；Pre-check 前不修改。 |
| 配置层 | 项目现有 `configs/` 目录 | 新增 C1 model/experiment 配置并贯通 run identity/eval fields。 |
| 运行资产层 | 项目现有 `experiments/` 目录 | 后续产生 screening、三 seed 正式 run、probe 和 smoke；probe 与正式 run 隔离。 |
| 报告层 | 项目现有 `reports/`、C1 guard 目录 | 后续生成 C1 raw/aggregate/cost/decision/handoff 和运行/质量 gate。 |
| 治理层 | C1 `b_class_auxiliary/coding_guards/` | 当前生成四件套和 Pre-check gate；不修改 B1 结果。 |
