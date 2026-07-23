# Pre-check Extraction

## 1. 本次任务
- 任务名: C1_LKMA_precheck
- 当前阶段: C1 / 05_LKMA
- 上一阶段: B1 current_standard / 04_Baseline
- 日期: 2026-07-17

## 2. 规划约束提取

| 来源文件 | 章节 | 约束内容 | 约束类型 | 对本次实现的影响 |
|---------|------|---------|---------|----------------|
| `结直肠腺体分割_plan_优化版/01_实验执行/05_LKMA/00_阶段总协议.md` | C1 身份、Gate_C1、交付物 | 当前消费对象是 B1 current_standard 的 frozen conditional baseline；主变体为 bottleneck+k15；必须完成三 seed、比较、资产、决策和 handoff | 官方协议固定项 | Pre-check 必须逐项核对 C1 identity、run、manifest、结果和 handoff 字段，但不能制造结果。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/05_LKMA/01_设计依据.md` | LKMA 角色与职责 | LKMA 只承担 morphology/context/large receptive field，不承担 boundary/distance 或完整 backbone | 路线层已锁定 | 代码只能实现单职责模块，禁止引入下游模块变量。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/05_LKMA/02_插入位置与参数范围.md` | 位置、kernel、forward 边界 | 位置集合仅 bottleneck/decoder_stage1，kernel 仅 15/21；主版本 bottleneck+k15；模块保持 same-shape | 论文支持的候选范围 | 代码落点只能支持主变量和最多一个互斥备选，不得扩展成组合搜索。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/05_LKMA/03_实验步骤.md` | screening 和正式顺序 | seed3407 screening 仅做结构和运行健康检查；通过后主版本必须跑 3407/1234/2025 | 官方协议固定项 | 配置和 run_name 必须区分 screening、smoke、runtime probe 和正式 run。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md` | 全局冻结项 | train/val/TestA/TestB、三 seed、best_selector、threshold_source 和训练协议继承 B1 | 工程冻结规则 | 不得借 LKMA 改动数据、训练、选择器或阈值。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md` | 评估链和字段 | float32 logits→sigmoid→threshold→binary mask→connected components→metrics；对象级指标优先；评估实现字段必须贯通 | 官方协议固定项 | C1 config、run_meta、per-seed、aggregate、manifest 和 handoff 使用同一口径。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md` | 命名和结果记录 | stage/model/dataset/seed/config/run_name 必须一一对应，正式结果不得复用历史身份 | 工程冻结规则 | 所有 C1 运行目录和配置必须单独命名，历史 B1/v3 只能归档引用。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md` | 质检和回退 | 代码先冻结再正式运行；结果只能由真实脚本产生；指标和 Gate 不得手工改写 | 工程冻结规则 | Pre-check 通过前只能扫描和锁定；运行后只能依据真实产物更新报告。 |

## 2.1 预期工程落点

| 对象层 | 预期落点 | 为什么现在就要写 |
|------|---------|----------------|
| guard 提取留痕 | `b_class_auxiliary/coding_guards/05_LKMA/pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md`、Pre-check Guard | 让四件套可被机器检查并回链到阶段锁定门禁。 |
| 正式代码 | `src/models/` 下新增 LKMA 模块并修改真实的 R34-U-Net/model factory 入口 | 当前代码扫描确认只有 ResNet34-U-Net 和 UNet，无 LKMA 实现；具体文件在 Pre-check 后按真实接口落定。 |
| 配置与资产 | `configs/` 下新增 C1 model/experiment 配置；正式 run 写入 `experiments/`；汇总和 handoff 写入 `reports/` | 先锁定身份/schema/lineage，避免配置和运行资产混用。 |

## 3. 路线层约束提取

| 来源文件 | 章节 | 当前结论 | 不允许做什么 |
|---------|------|---------|-------------|
| `05_LKMA/01_设计依据.md` | LKMA 职责 | LKMA 只验证 morphology/context/large receptive field 价值 | 不得承担 Boundary、Distance 或完整 backbone 替换。 |
| `05_LKMA/02_插入位置与参数范围.md` | 主变量 | 首轮唯一主变体为 bottleneck+k15 | 不得同时打开位置、kernel、模块家族和训练协议。 |
| `05_LKMA/03_实验步骤.md` | 执行链 | screening→three_seed_main→optional_one_backup→decision | 不得把 screening 单次结果当 keep。 |
| 治理记录与问题登记 | B1 conditional handoff | warning 真实存在但允许在边界内消费 | 不得把 original_gate_b1=false 改为 true，或删除 stability_warning。 |

## 4. 文献/参考实现提取

| 类型 | 来源 | 章节/文件/行号 | 可直接采用内容 | 本项目调整 |
|------|------|---------------|---------------|-----------|
| 参考代码 | `结直肠腺体分割_正式参考资料/03_large_kernel_backbones/VAN-Classification/models/van.py` | `LKA`、`Attention` | depth-wise spatial large-kernel 和 projection 的相邻实现启发 | 不采用 attention gating 和完整 VAN block。 |
| 参考代码 | `结直肠腺体分割_正式参考资料/03_large_kernel_backbones/RepLKNet-pytorch/segmentation/replknet.py` | `ReparamLargeKernelConv`、`RepLKBlock` | stride=1、same padding、groups=channels 的大核空间卷积边界 | 不采用重参数化、小核分支或完整 RepLK backbone。 |
| 官方评估依据 | `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md` | 评估链、对象级指标 | 继承项目固定评估链和字段 | 不在 C1 新写评估语义。 |

## 5. 当前阶段唯一允许改动的变量
- 允许改: 仅 LKMA 模块本身及其单一插入位置/主 kernel 的实现变量；主版本固定 bottleneck+k15，最多一个互斥备选；允许新增 C1 专属配置、运行和汇总落点。
- 不允许改: 数据、split、seed、训练协议、loss、optimizer、scheduler、AMP、best selector、threshold、后处理、评估实现、Boundary/Distance 变量、B1 原始结果和 Gate 数字。
- 如果越界会影响: 会破坏 C1 单变量归因、B1 conditional handoff、跨阶段 lineage 和正式论文证据链。

## 5.1 本轮最小验证计划

| 验证项 | 计划动作 | 预期证据 |
|------|---------|---------|
| py_compile 和 import 检查 | Pre-check 后对实际新增/修改的 LKMA、model factory、训练/汇总入口执行语法和导入检查。 | 真实命令退出码 0、源码路径和导入日志。 |
| `smoke run` | 使用独立 C1 smoke run_name 跑最小 train→val→checkpoint→test/eval 闭环。 | 独立 smoke 目录、日志、checkpoint、run_meta 和成功退出码；不当正式结果。 |
| dataloader batch | 复用 B1 数据入口抽查一个 train batch。 | input/target shape、dtype、finite、标签 unique/范围和样本路径。 |
| loss、backward | 使用带 `__runtime_probe` 后缀的独立 probe 运行 LKMA forward、BCE+Dice、backward 和 optimizer.step。 | runtime_evidence.json、runtime_check.log、runtime_check_report.md 中的 shape/dtype/loss/finite/backward/optimizer.step。 |
