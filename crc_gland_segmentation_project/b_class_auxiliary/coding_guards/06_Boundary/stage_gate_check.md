# Stage Gate Check

## 1. 阶段信息
- 当前阶段: `06_Boundary`
- 上一阶段: `05_LKMA C1`，正式决策为 `drop`
- 当前任务: 完成 BoundaryHead formal Pre-check，确认当前工程是否具备进入最小编码实现的真实条件。

## 2. 上一阶段通过证据
- 通过文件: `crc_gland_segmentation_project/b_class_auxiliary/coding_guards/05_LKMA/workflow_gate_report.md`
- 通过状态: 05 流程证据闭环已完成；科学决策为 `drop`，不消费 LKMA。
- 关键交付物: 三 seed 正式 run、TestA/TestB 资产、独立指标复核、summary、manifest、runtime、code quality 和 workflow gate；B1 作为下游 baseline，并保留 stability warning。

## 3. 当前阶段进入条件

| 条件 | 证据文件 | 检查方法 | 结果 |
|------|---------|---------|------|
| 研究定标已通过 | `b_class_auxiliary/coding_guards/06_Boundary/research_alignment_gate_report.md` | 确认 `research_alignment_gate_status=pass` | pass |
| 阶段实现卡已锁定 | `b_class_auxiliary/coding_guards/06_Boundary/00_阶段实现卡.md` | 检查唯一目标、允许/禁止改动和 `allow_precheck` | pass |
| 阶段定义 gate 已通过 | `b_class_auxiliary/coding_guards/06_Boundary/stage_definition_gate_report.md` | 确认 `stage_definition_gate_status=pass` | pass |
| B1 输入资产可读 | `reports/stage_reports/asset_manifest.json`、`reports/tables/baseline_stage_manifest.csv`、`reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | 检查 manifest、baseline summary 和 warning lineage 路径存在且字段可回链 | pass（可读；warning 保留） |
| 当前 Boundary 代码接口已完成 | `src/models/resnet34_unet.py`、`src/engine/trainer.py`、`scripts/train.py` | 检查是否已有双输出模型、Boundary loss 和训练入口注册 | not_applicable（Pre-check 的职责是核对待实现缺口；正式接口应在本阶段编码中实现） |
| 当前 target/metric 口径已闭合 | `src/data/boundary_targets.py`、`src/metrics/seg_metrics.py`、`configs/eval/eval_proto_v1.yaml` | 对照 target 语义、Boundary F1 和历史 eval_proto 字段；冻结 Boundary target 采用 erosion-xor contour 后 dilation，和现有 Boundary F1 实现保持同一 contour/tolerance 语义，计划中的 find_boundaries 仅作为历史文字记录 | pass（口径裁决已落入本 Pre-check 文档，后续代码必须按此实现并真实验证） |
| 当前任务没有越界到正式编码 | b_class_auxiliary/coding_guards/06_Boundary/00_阶段实现卡.md 和本目录 Pre-check 文件 | 检查本轮只生成 guard 文档，不修改正式代码/配置/结果 | pass |

## 4. 阻断项

| 阻断项 | 是否触发 | 说明 |
|-------|---------|------|
| `00_阶段实现卡.md` 缺失或空壳 | 否 | 阶段卡已存在，研究和阶段定义 gate 均已通过。 |
| 阶段定义门禁报告状态不是 pass | 否 | 06 专属 stage definition gate 已真实通过。 |
| 上一阶段未正式 pass | 否 | 05 流程已收口，但其科学决策是 drop，06 输入按 baseline 处理。 |
| 当前任务越界到后续阶段 | 否 | 本轮未写正式代码、配置、runtime 或训练结果。 |
| 数据/评估/命名协议仍未冻结 | 是 | eval_proto_v1 可继承，但 Boundary target 与 metric 的实现关系、双输出 schema 和新 run identity 尚未形成可执行契约。 |
| 本轮拟修改文件不属于当前阶段允许范围 | 否 | 本轮只创建 06 guard 文档。 |
| decoder final / model factory / loss registry 未完成核对 | 是 | 当前 `ResNet34UNet.forward` 只返回单一 logits；正式接口适配尚未实现。 |

## 5. 结论
- Stage Gate Result: `blocked`
- 结论说明: 上游研究和阶段锁定均已通过，B1 输入资产可读；但当前工程仍是单输出 segmentation 训练链，BoundaryHead、双输出 loss、模型构建适配和 target/metric 可比口径尚未形成可执行契约。因此本 Pre-check 当前阻断正式编码；先完成工程接口核对和协议裁决，再重新运行 Pre-check 文档 gate。

## 5.1 本轮允许进入的工程落点

| 对象 | 允许动作 | 预期落点 |
|------|---------|---------|
| 正式代码 | `not_applicable` | Pre-check 未通过前不得修改 `src/`、`scripts/`、`tools/` 正式实现。 |
| 配置与正式资产 | `not_applicable` | Pre-check 未通过前不得创建 06 experiment config、run、checkpoint、metrics 或 predictions。 |
| 模板与协议文档 | create | 仅允许创建或更新本阶段 b_class_auxiliary/coding_guards/06_Boundary/ 下的 Pre-check guard 文件和真实门禁报告。 |
