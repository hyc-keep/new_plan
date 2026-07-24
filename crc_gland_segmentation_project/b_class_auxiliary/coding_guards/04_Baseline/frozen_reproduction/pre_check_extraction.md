# Pre-check Extraction

## 1. 本次任务
- 任务名: `04_Baseline_frozen_reproduction_Pre-check`
- 当前阶段: `04_Baseline`
- 上一阶段: `04_Baseline historic v1 recovery（仅审计边界，不作为 future 指标来源）`
- 日期: `2026-07-24`
- 本轮目的: 为 future six-run frozen reproduction 核对文档、契约、配置、路径和工程落点；不运行训练、测试、runtime、smoke、独立复核或正式 Gate。

## 2. 规划约束提取

| 来源文件 | 章节 | 约束内容 | 约束类型 | 对本次实现的影响 |
|---|---|---|---|---|
| `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md` | 冻结训练协议 | 固定 GlaS、train_proto_v1、三 seed 和 A2/B1 对照 | 官方协议固定项 | 只核对 six future configs；不得改训练参数或启动训练。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/03_对比与判断规则.md` | 统计与比较 | TestA/TestB 分离、7 项指标、逐 seed 与 ddof=0 派生统计 | 官方协议固定项 | contract 锁定 schema；本轮不得写出或复用任何 future 指标。 |
| `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | P04-010、3.1 节 | historic v1 recovery 是审计边界；future round pending_not_run | 路线层已锁定 | 必须使用新 run_name/output_dir，historic 指标不进入本轮。 |
| `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/02_U-Net.md` | A2 结构依据 | A2 plain U-Net 是冻结对照 | 论文支持的候选范围 | 不引入 LKMA、Boundary、Distance 或其他变量。 |
| `b_class_auxiliary/tools/stage_contract_checker.py` | identity/schema/lineage/freshness | pre-run 机器检查必须读取真实 config 与 required paths | 工程冻结规则 | 运行 checker 和 py_compile；不以 checker pass 冒充 runtime 或实验成功。 |

## 2.1 预期工程落点

| 对象层 | 预期落点 | 为什么现在就要写 |
|---|---|---|
| Pre-check 留痕 | `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md`、`Pre-check Guard.md` | checker 只接受同目录的四个独立前检件。 |
| B 类 gate 报告 | `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_*gate_report.md` | 避免覆盖 04/07 共享报告，并保留 future-only 裁决。 |
| 配置 | `configs/experiment/A2_UNet_GlaS_frozen_repro_seed3407.yaml`、`configs/experiment/B1_ResNet34_UNet_GlaS_frozen_repro_seed3407.yaml` | 六份 config 已存在，只做真实路径与身份核对。 |
| 契约 | `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_stage_contract.yaml` | 锁定六个 run/output、schema、lineage 与 freshness。 |
| 实验资产 | future A2/B1 输出目录 | 预期当前不存在；不得创建或编辑，未来正式执行才产生。 |

## 3. 路线层约束提取

| 来源文件 | 当前结论 | 不允许做什么 |
|---|---|---|
| `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` | Pre-check pass 仅允许进入编码；后续仍需 runtime、smoke、正式训练、独立复核和 Gate | 不得把文档/contract pass 写成模型实验通过。 |
| `b_class_auxiliary/tools/check_precheck_docs.py` | 四件套、阶段锁定 pass 和十目录真实扫描均是强制输入 | 不得用旧汇总件替代独立文件。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_stage_contract.yaml` | current_round=frozen_reproduction_pending、future_only | 不得消费 historic v1 的指标、checkpoint、run_meta、metrics 或 Gate。 |

## 4. 文献/参考实现提取

| 类型 | 来源 | 章节/文件/行号 | 可直接采用内容 | 本项目调整 |
|---|---|---|---|---|
| 论文 | `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/02_U-Net.md` | plain U-Net 对照 | A2 保持基线身份 | 仅核对已有 future config，不运行。 |
| 论文 | `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/05_ResNet.md` | residual encoder | B1 保持 ResNet34-U-Net 身份 | 不把文献依据扩写为 future 性能结论。 |
| 官方配置 | `configs/eval/eval_proto_v1.yaml` | eval_proto_v1 | 使用固定评估版本 | 本轮不调用评估入口。 |
| 本地工具 | `b_class_auxiliary/tools/stage_contract_checker.py` | main | 检查契约路径与字段 | checker 不产生训练或指标证据。 |

## 5. 当前阶段唯一允许改动的变量
- 允许改: future round 的 B 类研究、阶段锁定、Pre-check、报告与实现依据文档；对现有 YAML 的只读检查。
- 不允许改: 正式代码、six configs、historic v1 资产、`experiments/**` 的结果/checkpoint/run_meta/metrics；不得运行训练、测试、runtime、smoke、独立复核或正式 Gate。
- 如果越界会影响: 会破坏 future-only 证据边界和正式证据必须由真实运行产生的协议。

## 5.1 本轮最小验证计划

| 验证项 | 计划动作 | 预期证据 |
|---|---|---|
| Python 语法编译 | 编译四个 document/contract checker | 当前命令退出码 0；只验证脚本语法。 |
| `smoke run` | not_applicable：用户明确禁止本轮运行 | 无 smoke 证据；未来隔离 `__smoke` run 执行。 |
| `dataloader batch` | not_applicable：用户明确禁止本轮运行 | 无 batch/shape/dtype 证据；未来 runtime probe 生成。 |
| 优化单步 | not_applicable：用户明确禁止本轮运行 | 无 loss/backward/step 证据；未来 runtime probe 生成。 |
