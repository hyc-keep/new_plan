# Pre-check Extraction

## 1. 本次任务
- 任务名: 06_Boundary BoundaryHead formal pre-check
- 当前阶段: 06_Boundary
- 上一阶段: 05_LKMA C1，正式决策为 drop；输入回到 B1 baseline
- 日期: 2026-07-17

## 2. 规划约束提取

| 来源文件 | 章节 | 约束内容 | 约束类型 | 对本次实现的影响 |
|---------|------|---------|---------|----------------|
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md` | 阶段顺序和门禁 | 必须按 research→stage lock→Pre-check→stage contract→编码→runtime→smoke→正式运行执行 | 工程冻结规则 | 当前只能完成 Pre-check 文档和门禁，不能创建 Boundary 正式代码。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/00_阶段总协议.md` | Boundary 身份、Gate_D1 | 06 只验证最小 Boundary Head，正式结论需有三 seed、分 split、资产、独立复核和 handoff | 路线层已锁定 | 后续代码和结果必须围绕单一 Boundary 变量闭环。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/02_边界标签生成规则.md` | target 流程 | binary mask→contour→fixed-width dilation→boundary band；主 width=3 | 官方协议固定项 | 现有 target 必须逐项核验，不能直接复用未确认的内向 band 语义。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/03_实验步骤.md` | screening 和正式运行 | 先 seed=3407 screening，再补 1234/2025；screening 不构成最终结论 | 路线层已锁定 | 所有 config/run_name 必须区分 screening、正式 run 和 runtime probe。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/04_保留或删除标准.md` | keep/backup/drop | 重点证据为 Boundary F1、HD95/Object Hausdorff、可视化、Object Dice/F1、成本和三 seed 稳定性 | 论文支持的候选范围 | 不能只添加 pixel Dice 或单 seed 结果。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md` | 全局参数 | train68/val17/TestA60/TestB20、BCE+Dice、AdamW、120 epoch、val_objdice_max、threshold=0.5、三 seed | 官方协议固定项 | 06 只增加 Boundary 分支监督，不改训练、数据和 checkpoint 选择协议。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md` | 评估链 | threshold 前 float32；TestA/TestB 分开；8-connectivity；记录 boundary_metric_impl | 官方协议固定项 | 必须继续消费 eval_proto_v1，口径冲突不能静默处理。 |
| `crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | B1、05 状态 | B1 为 valid_with_stability_warning；05 LKMA=drop；下游消费 baseline | 工程冻结规则 | 06 的 lineage 必须保留 warning 和 original_gate_b1=false。 |

## 2.1 预期工程落点

| 对象层 | 预期落点 | 为什么现在就要写 |
|------|---------|----------------|
| guard 提取留痕 | `b_class_auxiliary/coding_guards/06_Boundary/pre_check_extraction.md` | 记录本轮 Pre-check 来源和约束。 |
| 阶段门控与代码库扫描 | `b_class_auxiliary/coding_guards/06_Boundary/stage_gate_check.md`、`current_codebase_状态.md`、`Pre-check Guard.md` | 为机器门禁提供真实路径、能力和缺口。 |
| 模型代码 | `src/models/resnet34_unet.py`、`src/models/` 下 BoundaryHead 落点 | 当前 forward 只返回单一 segmentation logits，需在编码前固定最小修改边界。 |
| 数据和指标 | `src/data/boundary_targets.py`、`src/metrics/seg_metrics.py` 或对应新增模块 | 当前已有相关文件，但语义和接口仍需在编码前按本卡片修正/核验。 |
| 训练与配置 | `src/engine/trainer.py`、`scripts/train.py`、`scripts/test.py`、`configs/experiment/` | 当前训练/测试链按单输出模型工作，双输出损失和模型构建需要最小适配。 |
| 运行与报告 | `experiments/`、`reports/`、本阶段 guard 目录 | 后续真实运行才产生正式资产；本轮不创建实验结果。 |

## 3. 路线层约束提取

| 来源文件 | 当前结论 | 不允许做什么 |
|---------|---------|-------------|
| `b_class_auxiliary/coding_guards/06_Boundary/研究定标记录.md` | 研究 gate 已通过，06 研究问题和主版本已锁定 | 不允许重新打开多模块、多 loss 或多接入位置搜索。 |
| `b_class_auxiliary/coding_guards/06_Boundary/00_阶段实现卡.md` | 阶段定义 gate 已通过，当前允许进入 Pre-check | 不允许把 allow_precheck 写成允许编码或正式训练。 |
| `b_class_auxiliary/coding_guards/05_LKMA/workflow_gate_report.md` | 05 已闭环但 LKMA 科学决策为 drop | 不允许消费 LKMA 作为 06 输入或改写 05 结果。 |
| `crc_gland_segmentation_project/configs/eval/eval_proto_v1.yaml` | 当前评估协议为 eval_proto_v1，boundary metric 为 erosion-xor+dilation | 不允许直接把计划文字 find_boundaries 口径替换历史结果。 |

## 4. 文献/参考实现提取

| 类型 | 来源 | 章节/文件/行号 | 可直接采用内容 | 本项目调整 |
|------|------|---------------|---------------|-----------|
| 任务指标 | `结直肠腺体分割_正式参考资料/04_task_specific_benchmarks/GlandSegBenchmarks-master/DCAN/metrics.py` | object metrics | 保留 GlaS 对象级评价语义 | 继续使用项目已冻结实现和独立 crosscheck，不复制外部训练工程。 |
| 任务测试 | `结直肠腺体分割_正式参考资料/04_task_specific_benchmarks/GlandSegBenchmarks-master/DCAN/test_GlaS.py` | split/test flow | TestA/TestB 分开统计和样本配对 | 与项目 run_meta、CSV、predictions 资产对齐。 |
| 边界模块 | `结直肠腺体分割_正式参考资料/02_boundary_shape_losses/GSCNN/README.md` | Gated-SCNN entry | 采用显式边界监督作为设计启发 | 不复制 gated architecture，不引入多分支反馈。 |
| 当前工程 | `crc_gland_segmentation_project/src/models/resnet34_unet.py` | `ResNet34UNet.forward` | decoder final 位于 `up5` 输出后、现有 `head` 前 | 需要在编码阶段以最小改动暴露共享 feature 并保持 seg_logits 推理语义。 |
| 当前工程 | `crc_gland_segmentation_project/src/data/boundary_targets.py` | `build_boundary_band` | 已有 width=3/5 的 target 相关函数 | 现实现使用 PIL MaxFilter/MinFilter 且只保留 mask 内部 band；不能未经核验当作 06 唯一 target。 |
| 当前工程 | `crc_gland_segmentation_project/src/metrics/seg_metrics.py` | `boundary_f1_score` | 已有 erosion-xor、dilation、8-connectivity、width=3 实现 | 作为历史可比 metric 继续核对；与训练 target 分开记录。 |

## 5. 当前阶段唯一允许改动的变量
- 允许改: 仅允许在后续编码阶段实现 decoder final 单分支 BoundaryHead；主版本固定 width=3、BCE、lambda=0.3；允许为双输出 loss、边界可视化和边界误差分析做必要的最小接口适配。
- 不允许改: 数据 split、输入/归一化、三 seed、主分割 loss、优化器、学习率、scheduler、epoch/patience、AMP、best selector、threshold、connected components、历史 B1/C1 结果和既有 eval_proto_v1 语义。
- 如果越界会影响: 06 单变量归因、B1/C1 可比性、Gate_D1、后续 07 Distance 的输入绑定和论文中的失败/保留解释。

## 5.1 本轮最小验证计划

| 验证项 | 计划动作 | 预期证据 |
|------|---------|---------|
| Python 编译和 import | 编码完成后对实际修改的 model、target、loss、trainer、train/test 入口执行 Python 编译和 import | 真实退出码和源码路径日志；本轮 Pre-check 不执行该项。 |
| smoke run | 编码和 stage contract checker 通过后，用独立 06 smoke identity 跑 train→val→checkpoint→test/eval | 独立 smoke 目录、日志、checkpoint、metrics；不作为正式科学结果。 |
| dataloader batch | 复用 `crc_gland_segmentation_project/src/data/datasets.py` 与 `crc_gland_segmentation_project/splits/glas/glas_train68.csv`，抽查 image、mask、boundary target | shape、dtype、finite、unique 值、空间对齐和真实 sample path。 |
| loss / backward | 用带 __runtime_probe 的独立 probe run_name 检查 seg/boundary logits、BCE+Dice+0.3*BCE、finite、backward、optimizer.step | runtime 三件套中的真实 shape/dtype/loss/backward/step 证据。 |
