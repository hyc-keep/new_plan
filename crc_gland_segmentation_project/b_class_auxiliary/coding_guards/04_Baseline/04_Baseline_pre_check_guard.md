# Pre-check Guard

## 1. 本次任务归属
- 当前阶段: `04_Baseline`
- 上一阶段: `03_UNet稳定性`
- 当前任务: `04_Baseline_Pre-check`
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/04_Baseline/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- Stage Gate Result: `blocked`

## 2. 来自规划的硬约束
- B1 只允许把 plain UNet encoder 替换为 ResNet34 residual encoder；来源为 04 阶段总协议。
- B1 必须继承 A2 的 GlaS split、train_proto_v1、eval_proto_v1、threshold_source=val17、best_selector=val_objdice_max、TestA/TestB 分开和七项指标；来源为 04 训练协议、比较协议和 A2 handoff。
- B1 未完成 complete_runs、baseline_assets_ready、freeze_ready、handoff_ready 和 comparison gate 前，不得宣称阶段完成；来源为 04 阶段验收协议。
- 当前 Pre-check 必须先形成四件套并运行检查器；真实检查文件位于 b_class_auxiliary/tools/ 目录；来源为项目内四份 Pre-check 模板文件。

## 3. 来自参考资料的实现依据
- ResNet34 residual/basic block 来源：ResNet 文献证据文件。
- U-Net decoder/skip 来源：U-Net 文献证据文件。
- GlaS split/object metrics 来源：GlaS Challenge 文献证据文件。
- 当前候选工程实现：`src/models/resnet34_unet.py`、`src/models/__init__.py`；它们只能作为候选输入，不能代替当前轮 formal implementation。

## 4. 当前工程已有能力与缺口
- 已有能力: A2 handoff manifest、A2 summary、A2 raw/meanstd、环境检查 pass、训练/测试/评估入口、ResNet34-U-Net 候选实现和 model config。
- 当前缺口: 04 当前轮 B1 experiment config、三 seed run mapping、权重缓存及 SHA256、离线权重策略、当前 eval/postprocess version、stage contract、正式 B1 runtime/smoke/独立复核和 gate 均不存在。
- Freshness boundary: implementation_status 和 RESET_STATUS 保留 fresh_reset/not_started 的阶段运行状态；当前模型代码、factory和标准model config已重写，旧候选仅在04 clean-restart source snapshot中保留，当前不消费历史快照。

## 5. 本次任务边界
- 明确要做: 只生成和核验本轮 B 类 Pre-check 四件套；记录真实目录扫描、A2 lineage、依赖、代码现状、权重和配置缺口；通过真实 gate 决定是否允许进入编码。
- 明确不做: 不修改 `src/`、`configs/` 正式代码或配置；不创建 B1 experiment config；不创建 B1 run；不运行 runtime、smoke、训练、测试或指标汇总；不消费历史 protocol_v3。

## 6. 预期代码落点
- 新建文件: `b_class_auxiliary/coding_guards/04_Baseline/pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md`、`04_Baseline_pre_check_guard.md`。
- 修改文件: 当前 Pre-check 不修改正式代码、配置、实验结果、A2 资产或 A 类计划协议。
- 影响的 run / report / external: 只更新 04 专属 B 类 Pre-check 记录和 stage gate report；A2 report 只读消费；experiments/、external/ 不修改。
- 正式代码落点状态: not_applicable；当前 Stage Gate 为 blocked，未获得正式编码许可。
- 正式配置落点状态: not_applicable；当前不创建 B1 experiment config。
- 运行资产落点状态: not_applicable；当前不创建 B1 run、checkpoint、metrics 或 predictions。
- 当前代码处理: src/models/resnet34_unet.py 和 src/models/__init__.py 已按标准文件名重写；尚未通过 runtime/code quality，不能宣称代码成立。旧候选仅在04 clean-restart source snapshot中保留。
- 当前model config处理: configs/model/resnet34_unet.yaml 是当前标准model config；三份B1 seed experiment config独立引用它。
- 当前进入编码条件: 必须先完成 B1 identity、权重缓存/离线策略、eval/postprocess 版本、stage contract 和 Pre-check gate；任一缺失都保持 blocked。

## 6.1 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 计划动作 | 备注 |
|-------------|------|---------|-------------|-----------|-----------|------|
| b_class_auxiliary/coding_guards/04_Baseline/pre_check_extraction.md | B | Pre-check 提取记录 | reports/stage_reports/implementation_tracking/04_Baseline/README.md | 04 implementation tracking | update | 当前只生成 B 类前置记录。 |
| b_class_auxiliary/coding_guards/04_Baseline/stage_gate_check.md | B | 阶段门控检查 | reports/stage_reports/implementation_tracking/04_Baseline/README.md | 04 implementation tracking | update | 记录真实 blocked 结论。 |
| b_class_auxiliary/coding_guards/04_Baseline/current_codebase_状态.md | B | 当前代码库状态 | reports/stage_reports/implementation_tracking/04_Baseline/README.md | 04 implementation tracking | update | 记录十目录扫描和 freshness 风险。 |
| b_class_auxiliary/coding_guards/04_Baseline/04_Baseline_pre_check_guard.md | B | Pre-check Guard | reports/stage_reports/implementation_tracking/04_Baseline/README.md | 04 implementation tracking | update | 汇总当前允许/禁止边界。 |

## 6.2 预期最小运行验证
- syntax/import check: 当前 Pre-check 不修改正式代码；Pre-check 通过且正式代码冻结后，必须对本轮修改文件执行 Python 编译和 import。
- 最小运行验证: 当前不执行；Pre-check 通过后使用当前 B1 experiment config 和隔离 probe run_name 运行。
- smoke run: 当前不执行，直到 contract pass 且正式 B1 experiment config 存在；历史 protocol_v3 smoke 不可代替当前证据。
- dataloader batch: 当前不执行；后续真实验证 input/target/output shape、dtype、finite 和标签范围。
- optimization step: 当前不执行；后续 runtime 必须记录 optimization step。
- runtime report: 当前不生成。
- code quality report: 当前不生成。

## 7. 上游 guard 文件回链
- 阶段卡正式输出名 `00_阶段实现卡.md`: 已完成；stage definition gate 为 pass，但阶段卡未决项仍需在 Pre-check/contract 中冻结。
- 阶段锁定门禁报告 `stage_definition_gate_report.md`: 已运行 `b_class_auxiliary/tools/check_stage_definition_gate.py`；当前为 pass。
- `pre_check_extraction.md`: 本轮已完成；提取 A2 继承、B1边界、工程落点和最小验证计划。
- `stage_gate_check.md`: 本轮已完成；真实结论为 blocked，原因是当前轮 B1 identity、权重和 freshness 未冻结。
- `current_codebase_状态.md`: 本轮已完成；十个目录均有真实扫描说明、样本路径/报告锚点和量化信号；明确 datasets/splits/experiments 当前不可直接消费。
- `precheck_doc_gate_report.md`: 本轮将运行 `b_class_auxiliary/tools/check_precheck_docs.py` 生成；当前尚未生成，因此不能宣称 Pre-check 通过。
