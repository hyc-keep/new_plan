# Pre-check Guard

## 1. 本次任务归属
- 当前阶段: C1 / 05_LKMA
- 上一阶段: B1 current_standard / 04_Baseline
- 当前任务: 完成 C1 LKMA 的路径、协议、代码落点、lineage 和最小运行前核对。
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/05_LKMA/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- Stage Gate Result: `allow`

## 2. 来自规划的硬约束
- C1 必须消费 B1 current_standard 的真实资产，消费边界为 `frozen_baseline_with_warning`；`original_gate_b1=false`、`stability_warning=true` 和原始 B1 blocked 状态不可改写。
- LKMA 主变体固定为 bottleneck+k15，模块为 same-shape depth-wise spatial block，可选 1x1 channel mixing 和 direct residual；备选最多一个。
- C1 继承 B1 train/val/TestA/TestB、三 seed、训练、评估、selector、threshold、后处理和对象级指标协议。

## 3. 来自参考资料的实现依据
- RepLKNet segmentation 参考 depth-wise large-kernel same-shape 边界；C1 只采用 stride=1、same padding、groups=channels 的空间混合，不采用完整重参数化 backbone。
- VAN LKA/Attention 仅用于说明大核 attention 相邻路线；C1 不复制 attention gating、多分支或完整 VAN。
- 项目评估规范提供 float32 评估链和对象级主指标；C1 不新写指标语义。

## 4. 当前工程已有能力与缺口
- 已有能力: B1 当前配置、ResNet34-U-Net、model factory、train/test/summarize 入口、GlaS 数据/split、对象级评估和 B1 真实资产均可读。
- 当前缺口: `src/models/` 尚无 LKMA 实现；C1 配置、正式 run、manifest、cost、decision、handoff 和本轮 runtime 尚未生成；需要在本 Pre-check 通过后才允许编码。

## 5. 本次任务边界
- 明确要做: 完成 Pre-check 四件套和机器门禁，核对真实目录、已有代码、B1 conditional lineage、C1 主变体、配置/运行/报告落点和最小验证计划。
- 明确不做: 不修改 B1 metrics/checkpoint/Gate；不创建正式 LKMA 代码或配置；不运行 screening、smoke、runtime 或正式训练；不写 learning document。

## 6. 预期代码落点
- 新建文件: Pre-check 通过后，按真实 `src/models/` 接口新增 LKMA 模块和 C1 配置；当前不提前创建正式代码/配置。
- 修改文件: Pre-check 通过后，最小修改真实 R34-U-Net/factory/训练或汇总入口；当前不提前修改。
- 影响的 run / report / external: 后续仅新增 C1 run 和报告；B1 与历史资产只读消费；`external/README.md` 本轮不修改。
- 逐项落点: 代码=现有 src/models/；配置=现有 configs/；运行=现有 experiments/；报告=现有 reports/ 和 C1 guard 目录；本轮不新增未锁定目录。

## 6.1 预期最小运行验证
- py_compile 和 import 检查: Pre-check 通过后对真实新增/修改 Python 文件执行 `python -m py_compile` 和 import 检查。
- 最小运行验证命令: 运行项目 runtime check 工具并传入 Pre-check 后锁定的 C1 配置；正式 probe run_name 必须追加 `__runtime_probe`。
- smoke run: 使用独立 C1 smoke run_name 跑最小 train→val→checkpoint→test/eval 闭环。
- dataloader batch: 复用 B1 数据入口，记录一个 batch 的 shape、dtype、finite、标签范围和真实样本路径。
- loss、backward、optimizer.step: 记录 LKMA forward shape、BCE+Dice loss、finite、backward 和 optimizer.step 到 runtime 三件套。
- 计划生成的 runtime_check_report.md: C1 guard 目录中的 runtime_check_report.md，仅在真实 runtime 运行后生成。
- 计划生成的代码质量门禁报告: C1 guard 目录中的 code_quality_gate_report.md，仅在 runtime 三件套完成后生成。

## 6.1 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 计划动作 | 备注 |
|-------------|------|---------|-------------|-----------|---------|------|
| C1 Pre-check 四件套与 gate 报告 | B | 项目流程与机器门禁留痕，不是模型正式对象 | reports/stage_reports/implementation_tracking/项目问题与决策登记.md | reports/stage_reports/implementation_tracking/项目问题与决策登记.md | update | 该路径作为流程入口同步项；本轮不产生实验结果。 |
| 后续 LKMA 正式模块代码 | A | 05_LKMA 正式协议点名的模型实现对象 | not_applicable | not_applicable | not_applicable | 本轮尚未创建正式代码对象；进入编码后重新登记对象级说明文。 |
| 后续 C1 配置、run、manifest、结果表 | A | C1 正式实验资产 | not_applicable | not_applicable | not_applicable | 本轮尚未创建正式实验资产；正式运行后重新登记真实对象。 |
| B1 原始 Gate/metrics/checkpoint | A（历史正式对象） | 上游正式结果，只读消费 | not_applicable | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | not_applicable | 禁止改写，只记录 conditional consumption。 |

## 7. 上游 guard 文件回链
- 阶段卡正式输出名 00_阶段实现卡.md: 已完成；机器门禁为 pass，C1 边界为 allow_precheck。
- 阶段锁定门禁报告 stage_definition_gate_report.md: 已运行 `b_class_auxiliary/tools/check_stage_definition_gate.py`，状态为 pass。
- `pre_check_extraction.md`: 已完成；提取官方协议、路线、参考实现和工程冻结约束。
- `stage_gate_check.md`: 已完成；Stage Gate Result 为 allow，但明确这是 conditional baseline 下的 C1 Pre-check 入口，不是 B1 Gate 改写。
- `current_codebase_状态.md`: 已完成；扫描 datasets、splits、configs、src、scripts、tools、b_class_auxiliary、experiments、external、reports 并留下数量与样本路径。
- `precheck_doc_gate_report.md`: 由 `b_class_auxiliary/tools/check_precheck_docs.py` 真实生成；在该报告为 pass 前不允许进入编码。
