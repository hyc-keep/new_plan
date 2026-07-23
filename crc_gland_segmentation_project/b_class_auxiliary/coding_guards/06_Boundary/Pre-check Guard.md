# Pre-check Guard

## 1. 本次任务归属
- 当前阶段: `06_Boundary`
- 上一阶段: `05_LKMA C1`，正式科学决策为 `drop`
- 当前任务: 核对 BoundaryHead 正式编码前的规划约束、代码库现状、工程落点、评估口径和运行契约前提。
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/06_Boundary/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- Stage Gate Result: `blocked`

## 2. 来自规划的硬约束
- 06 只研究 decoder final shared feature 上的最小显式 BoundaryHead；主版本为 boundary_width=3、boundary_loss=BCE、lambda_boundary=0.3，不引入完整 GSCNN/DCAN、距离图、拓扑损失或多变量搜索。依据文件为 `/home/featurize/work/Paper/结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/00_阶段总协议.md` 与 `/home/featurize/work/Paper/结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/01_设计依据.md`。
- 输入必须是 B1 baseline，并继承 `valid_with_stability_warning`、`stability_warning=true`、`original_gate_b1=false`；05 LKMA `drop`，不能作为 06 输入（见 `crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/项目问题与决策登记.md`）。
- 训练仍沿用 train68/val17/TestA60/TestB20、三 seed、BCE+Dice、AdamW、ReduceLROnPlateau、val_objdice_max、val17 threshold=0.5、float32 threshold 前评估链和 8-connectivity（见 `/home/featurize/work/Paper/结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`、`/home/featurize/work/Paper/结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`、`/home/featurize/work/Paper/crc_gland_segmentation_project/configs/eval/eval_proto_v1.yaml`）。
- Boundary target 必须由冻结 binary mask 派生，训练和分析共用实现；当前 Pre-check 冻结为 erosion-xor contour 后按 width=3 进行 dilation，和现有 Boundary F1 的 contour/tolerance 语义保持一致；计划文字中的 find_boundaries 作为历史文字差异保留，不能静默修改历史结果。

## 3. 来自参考资料的实现依据
- GlaS/DCAN 参考要求保留对象级指标、TestA/TestB split 语义和样本配对（见 `/home/featurize/work/Paper/结直肠腺体分割_正式参考资料/04_task_specific_benchmarks/GlandSegBenchmarks-master/DCAN/metrics.py` 与 `/home/featurize/work/Paper/结直肠腺体分割_正式参考资料/04_task_specific_benchmarks/GlandSegBenchmarks-master/DCAN/test_GlaS.py`）；Boundary 评估不能只报告 pixel Dice，还必须保留对象级指标并遵循 TestA/TestB 的样本配对语义。
- GSCNN 仅提供显式边界监督的研究启发；本项目不复制完整 GSCNN gated architecture（见 `/home/featurize/work/Paper/结直肠腺体分割_正式参考资料/02_boundary_shape_losses/GSCNN/README.md`）。
- 当前工程 Boundary F1 已实现 erosion-xor contour 后 dilation、width=3、8-connectivity（见 `crc_gland_segmentation_project/src/metrics/seg_metrics.py`）；训练 target 不能直接复用现有内向 band，必须在编码时实现和验证冻结 target 语义。

## 4. 当前工程已有能力与缺口
- 已有能力:
  - `crc_gland_segmentation_project/datasets/01_GlaS_official_raw/Grade.csv` 以及该目录下的 GlaS 原始图像和标注可读。
  - `crc_gland_segmentation_project/splits/glas/glas_train68.csv`、`crc_gland_segmentation_project/splits/glas/glas_val17.csv`、`crc_gland_segmentation_project/splits/glas/glas_testA60.csv`、`crc_gland_segmentation_project/splits/glas/glas_testB20.csv` 均存在。
  - `crc_gland_segmentation_project/src/models/resnet34_unet.py` 有 ResNet34-U-Net baseline，decoder 的最终共享 feature 是 `up5` 输出，当前 `forward` 只返回 `self.head(x)` 的单一 segmentation logits。
  - `crc_gland_segmentation_project/src/data/boundary_targets.py` 有 `build_boundary_band`，但其当前实现是 PIL MaxFilter/MinFilter 后取 mask 内部 band，不等于已经完成的 06 target 契约。
  - `crc_gland_segmentation_project/src/metrics/seg_metrics.py` 有 Boundary F1、Object Dice、Object F1、HD95 和 Object Hausdorff；`crc_gland_segmentation_project/scripts/test.py` 有 TestA/TestB、prediction、eval asset 和 metric crosscheck 入口。
  - `crc_gland_segmentation_project/b_class_auxiliary/tools/check_precheck_docs.py`、`crc_gland_segmentation_project/b_class_auxiliary/tools/stage_contract_checker.py` 和 06 前置研究/阶段锁定 gate 已存在。
- 当前缺口:
  - 没有正式 BoundaryHead 类或双输出 model forward 契约。
  - `src/engine/trainer.py` 当前 loss 接收单一 logits 和 mask；没有 boundary target、boundary BCE 和总损失组合入口。
  - `scripts/train.py`、`scripts/test.py` 和 model builder 尚未注册 Boundary 模型身份和双输出 checkpoint 兼容性。
  - 没有 06 专属 experiment config、stage contract、formal run identity、runtime、smoke、manifest、visual boundary output 或 metric crosscheck schema。
  - 现有 target 与计划/metric 的关系已记录，但正式代码和测试证据尚未存在。

## 5. 本次任务边界
- 明确要做:
  - 完成 Pre-check 四件套和机器门禁。
  - 核对当前单输出模型、target、metric、trainer、train/test、配置、manifest、实验资产和报告落点。
  - 在不修改正式代码和实验结果的前提下，冻结 Boundary target 与历史 metric 的协议关系，并把未实现接口列为编码前置项。
- 明确不做:
  - 不修改 B1/C1 的 metrics、checkpoint、run_meta、manifest、Gate 或历史结果。
  - 不创建 BoundaryHead、Boundary loss、06 config 或正式实验资产。
  - 不运行 runtime、smoke、screening、正式训练、测试或独立指标复核。
  - 不把当前已有 target/metric 文件冒充成 06 已完成实现。
  - 不把 `Stage Gate Result=blocked` 改写为 allow。

## 6. 预期代码落点
- 新建文件: Pre-check 通过后，按真实接口决定是否新增 BoundaryHead/loss 文件；当前不创建正式代码。
- 修改文件: Pre-check 通过后，最小修改 `src/models/resnet34_unet.py`、真实 model builder、`src/engine/trainer.py`、`scripts/train.py`、`scripts/test.py` 和必要的 target/metric 入口；当前不修改。
- 影响的 run / report / external:
  - 后续只新增 `06_Boundary` 专属 experiment configs、runs、manifest、summary、visuals、crosscheck 和 gates。
  - B1/C1 资产只读消费。
  - `external/README.md` 本轮不修改。

## 6.1 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 计划动作 | 备注 |
|-------------|------|---------|-------------|-----------|---------|------|
| `06_Boundary` Pre-check 四件套和 gate 报告 | B | 流程审计和机器门禁留痕，不是正式模型结果 | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | `create` | 只记录真实扫描、阻断项和 gate 状态。 |
| BoundaryHead 正式代码 | A | 06 Boundary 正式协议点名的模型实现对象 | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | `not_applicable` | 当前未创建；Pre-check 通过后重新登记逐文件实现依据。 |
| 06 experiment config、run、manifest、结果表 | A | 06 正式实验资产 | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | `not_applicable` | 当前未创建；正式运行后根据真实路径登记。 |
| B1 baseline/C1 LKMA 历史结果 | A（历史正式对象） | 上游正式结果，只读消费 | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | `not_applicable` | 保留 B1 warning，禁止改写历史 Gate。 |

## 6.2 预期最小运行验证
- py_compile / import：编码完成后，对每个实际改动的 Python 文件执行 Python 编译和 import；本轮不执行，因为正式代码尚未创建。
- 最小运行验证命令：Pre-check 通过并生成 06 config 后，使用 b_class_auxiliary/tools/run_minimal_runtime_check.py；probe run_name 必须独立追加 __runtime_probe。
- smoke run：使用独立 06 smoke identity 跑最小 train→val→checkpoint→test/eval，证明双输出、loss、checkpoint 和评估入口连通；不作为正式科学结论。
- dataloader batch：抽查 splits/glas/glas_train68.csv 的真实 image/mask，记录 image、seg target、boundary target 的 shape、dtype、finite、unique 和空间对齐。
- loss / backward / optimizer.step：记录 seg_logits、boundary_logits、L_seg、L_boundary、L_total、finite、backward 和 optimizer.step；runtime probe 不得覆盖正式 run。
- 计划生成的 runtime check report：只有真实 runtime 后才生成，落点为 b_class_auxiliary/coding_guards/06_Boundary/runtime_check_report.md。
- 计划生成的代码质量门禁报告：只有 runtime 三件套完成后才生成，落点为 b_class_auxiliary/coding_guards/06_Boundary/code_quality_gate_report.md。

## 6.3 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 计划动作 | 备注 |
|-------------|------|---------|-------------|-----------|---------|------|
| `06_Boundary` Pre-check 四件套和 gate 报告 | B | 流程审计和机器门禁留痕，不是正式模型结果 | `not_applicable` | `not_applicable` | `create` | 只记录真实扫描、阻断项和 gate 状态。 |
| BoundaryHead 正式代码 | A | 06 Boundary 正式协议点名的模型实现对象 | `not_applicable` | `not_applicable` | `not_applicable` | 当前未创建；Pre-check 通过后重新登记逐文件实现依据。 |
| 06 experiment config、run、manifest、结果表 | A | 06 正式实验资产 | `not_applicable` | `not_applicable` | `not_applicable` | 当前未创建；正式运行后根据真实路径登记。 |
| B1 baseline/C1 LKMA 历史结果 | A（历史正式对象） | 上游正式结果，只读消费 | `not_applicable` | `crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | `not_applicable` | 保留 B1 warning，禁止改写历史 Gate。 |

## 7. 上游 guard 文件回链
- 阶段卡正式输出名 `00_阶段实现卡.md`: 已完成；阶段定义 gate 为 pass，锁定结论为 allow_precheck。
- 阶段锁定门禁报告 `stage_definition_gate_report.md`: 已真实运行，状态为 pass。
- `b_class_auxiliary/coding_guards/06_Boundary/pre_check_extraction.md`: 已完成；记录本轮规划、路线、参考资料和最小验证约束。
- `b_class_auxiliary/coding_guards/06_Boundary/stage_gate_check.md`: 已完成；当前结论为 blocked，原因是正式 Boundary 双输出接口和可执行运行契约仍未实现/闭合。
- `b_class_auxiliary/coding_guards/06_Boundary/current_codebase_状态.md`: 已完成；已扫描 datasets、splits、configs、src、scripts、tools、b_class_auxiliary、experiments、external、reports，并留下真实样本路径和量化信号。
- `b_class_auxiliary/coding_guards/06_Boundary/precheck_doc_gate_report.md`: 将由 `b_class_auxiliary/tools/check_precheck_docs.py` 真实生成；在该报告为 pass 前不允许进入编码。
