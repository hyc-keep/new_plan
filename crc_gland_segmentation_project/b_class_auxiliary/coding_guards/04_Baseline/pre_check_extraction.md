# Pre-check Extraction

## 1. 本次任务
- 任务名: `04_Baseline_Pre-check`
- 当前阶段: `04_Baseline`
- 上一阶段: `03_UNet稳定性`
- 日期: `2026-07-15`
- 本轮目的: 在阶段锁定已通过后，核对 B1 的真实工程现状、上游 handoff、评估/训练依赖、权重来源和 contract 输入；本轮不开始编码或实验。

## 2. 规划约束提取

| 来源文件 | 章节 | 约束内容 | 约束类型 | 对本次实现的影响 |
|---------|------|---------|---------|----------------|
| `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md` | B1 阶段边界 | B1 唯一新增变量是 plain UNet encoder 到 ResNet34 residual encoder；不得提前混入后续模块 | 路线层已锁定 | 只允许建立结构 baseline，不能修改 A2 训练/评估科学协议。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/01_R34UNet结构与来源.md` | ResNet34/U-Net结构 | 必须使用 ResNet34 encoder、U-Net style decoder、多尺度 skip 和单通道 logit | 论文支持的候选范围 | Pre-check 必须核对当前候选实现的 feature taps、decoder、输出 shape。 |
| 04训练协议文件 | train_proto_v1继承 | split、loss、optimizer、scheduler、epoch、early stopping、AMP、seed 和 threshold 继承 A2 | 官方协议固定项 | 没有正式 B1 experiment config 前不能开始训练。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/03_对比与判断规则.md` | Gate_B1_compare | 只能按 TestA/TestB 分开、三 seed mean+-std 和对象级主指标比较 | 工程冻结规则 | B1 contract 必须锁定 raw/aggregate schema 和比较边界。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md` | Gate_B1 | complete_runs、baseline_assets_ready、freeze_ready、handoff_ready 和 comparison gate 均必须真实通过 | 工程冻结规则 | 当前只能做前置核对，不能把阶段卡或候选代码写成 B1 已通过。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md` | A2 handoff | B1 只能消费当前 eval_proto_v1 的三正式 run、raw=42、mean+-std=14 | 官方协议固定项 | 必须回链 `reports/tables/unet_stage_manifest.csv`，历史 protocol_v3 不可消费。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md` | 评估主链 | checkpoint 由 val_objdice_max 选择，threshold 来自 val17，TestA/TestB 分开，七项指标不漂移 | 官方协议固定项 | contract 必须包含 eval_proto、postprocess、threshold、connectivity 和 metric set。 |
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md` | 工程映射 | model code、model config、experiment config、run、report、guard 分层保存 | 工程冻结规则 | 候选 model config 不得冒充正式 B1 experiment config；每个正式文件需回链实现依据。 |

## 2.1 预期工程落点

| 对象层 | 预期落点 | 为什么现在就要写 |
|------|---------|----------------|
| Pre-check留痕 | `b_class_auxiliary/coding_guards/04_Baseline/pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md`、`04_Baseline_pre_check_guard.md` | 形成当前轮可审计的前置证据，不借用历史 B1。 |
| 正式代码 | `src/models/resnet34_unet.py`、`src/models/__init__.py` | 当前轮已按标准文件名重写；后续需通过静态检查、runtime和code quality。 |
| 配置 | `configs/model/resnet34_unet.yaml`、后续 `configs/experiment/B1_*.yaml` | model config 已存在，正式 experiment config 当前不存在；后续必须分开创建并锁定身份。 |
| 运行资产 | `experiments/B1_ResNet34_UNet_GlaS_seed*/` | 当前目录扫描未发现正式 B1 run；只有历史归档资产，不能消费。 |
| 评估/报告 | `reports/tables/`、`reports/stage_reports/` | A2 handoff 已存在，B1 当前结果、独立复核和 handoff 尚不存在。 |
| 门禁 | `b_class_auxiliary/coding_guards/04_Baseline/` | 当前轮研究和阶段锁定已存在，Pre-check 四件套和 contract 输入需要在此落盘。 |

## 3. 路线层约束提取

| 来源文件 | 当前结论 | 不允许做什么 |
|---------|---------|-------------|
| `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` | research alignment 和 stage definition 已通过，当前只进入 Pre-check | 不得跳过 Pre-check 进入编码、runtime、smoke 或正式训练。 |
| `crc_gland_segmentation_project/.trae/skills/模板5_Pre-check提取.md` | 必须把规划约束、工程落点、参考依据和唯一变量结构化记录 | 不得只列文件名或凭聊天历史写结论。 |
| `crc_gland_segmentation_project/.trae/skills/模板7_当前代码库状态.md` | 十个工程目录必须逐目录留下真实样本、量化信号和影响判断 | 不得把目录存在写成正式资产已成立。 |
| `crc_gland_segmentation_project/.trae/skills/模板8_Pre-check Guard.md` | Guard 必须回链阶段卡、stage definition、Pre-check 四件套和 gate 报告 | 不得在四件套缺失时写 allow。 |

## 4. 文献/参考实现提取

| 类型 | 来源 | 章节/文件/行号 | 可直接采用内容 | 本项目调整 |
|------|------|---------------|---------------|-----------|
| 论文 | `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/05_ResNet.md` | ResNet residual/basic block | ResNet34 的 residual encoder 是结构升级依据 | 只将 encoder 作为 B1 变量，禁止提前添加后续模块。 |
| 论文 | `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/02_U-Net.md` | U-Net contracting/expanding path | 保留 U-Net decoder 和对应尺度 skip | 必须在 runtime 验证尺度和输出 shape。 |
| 任务 benchmark | `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md` | GlaS split/object metrics | 继承 train68/val17/TestA60/TestB20 和对象级指标 | B1 不得重新定义 split、阈值或指标。 |
| 本地参考实现 | `结直肠腺体分割_正式参考资料/04_task_specific_benchmarks/GlandSegBenchmarks-master/DCAN/metrics.py` | 对象级指标实现 | F1、Object Dice、Object Hausdorff 的对象级语义 | 正式结果仍使用项目自有 eval_proto_v1 实现并独立复核。 |
| 当前工程候选 | `src/models/resnet34_unet.py` | ResNet34UNet/DecoderBlock/build_resnet34_unet | 可作为候选代码起点 | 不能在 Pre-check 前自动视为本轮正式实现。 |

## 5. 当前阶段唯一允许改动的变量
- 允许改: Pre-check B类记录、路径/依赖/权重/身份/lineage/schema/freshness 的机器核对输入；在 Pre-check 通过后才允许按阶段卡实现或修正 B1 正式模型和配置。
- 不允许改: A2 数据、split、标签、train_proto_v1、loss、optimizer、scheduler、seed、best_selector、threshold、评估指标、TestA/TestB边界、历史归档边界；不得在本轮 Pre-check 中改正式模型代码、创建正式 B1 experiment config 或运行实验。
- 如果越界会影响: 将破坏 04_Baseline 正式协议、02 训练协议、A2 handoff lineage 和后续 Gate_B1_compare 的单变量解释。

## 5.1 本轮最小验证计划

| 验证项 | 计划动作 | 预期证据 |
|------|---------|---------|
| `syntax and import check` | 当前 Pre-check 只读取现存候选代码；正式代码变更后才执行 Python 编译和 import | 本轮不产生正式代码验证；后续需生成当前轮日志。 |
| `smoke run` | 当前阶段禁止运行；Pre-check 通过、代码冻结和 contract pass 后，使用正式 B1 experiment config 跑最小 train-val-checkpoint-test/eval | 当前不应有 B1 smoke 证据；不得用历史 protocol_v3 smoke 代替。 |
| `dataloader batch` | 后续 runtime 真实读取 train68 一个 batch，核对 tensor shape、dtype、finite 和标签范围 | runtime_evidence.json、runtime_check.log、runtime_check_report.md。 |
| `optimization step` | 后续 runtime 真实执行 BCE+Dice、finite、backward、optimizer.step，且 probe run_name 与正式 run 隔离 | runtime 三件套；当前不执行。 |
