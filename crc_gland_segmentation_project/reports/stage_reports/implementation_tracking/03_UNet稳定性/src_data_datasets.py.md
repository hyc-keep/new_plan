# src/data/datasets.py 怎么看

> 本文档是 `src/data/datasets.py` 的学习型说明文，覆盖 03_UNet稳定性 阶段的数据集模块。
> 如果你已经读过 02 阶段的同文件说明文，可以直接跳到「A2 阶段新增与变化」看增量。

## 结构化溯源卡片

- 正式对象: `src/data/datasets.py`
- 对应阶段: `03_UNet稳定性`

### 论文依据
- 论文: Sirinukunwattana et al., 2017, "Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest"
- 章节: §2.1-2.2 (Dataset and Ground Truth)
- 公式/定义: Ground truth provided as binary masks; official train/test split definition

### 代码依据
- 仓库: project_local（本项目自建，无外部上游）
- 文件: `configs/data/glas.yaml`
- 许可证: project_internal

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `input_size`, `mask_positive_rule`, `stain_normalization`, `mask_rule_version`, `split_csv_schema_version`

### 当前实现落点
- 文件: `src/data/datasets.py`
- 符号: `DataConfig` / `FormalSegmentationDataset` / `build_segmentation_dataset()` / `load_data_config()` / `build_dataset_from_csv()`

## 这个脚本的作用

结论先行：这是整个项目的**数据入口层**，负责定义数据集协议并给 train.py 和 test.py 提供统一的 Dataset。

用人话说就是：train.py 和 test.py 不是各自去读图片、各自决定怎么 resize、怎么归一化。它们都调同一个入口，拿到同一个 Dataset，保证训练和评估走的是同一条数据链。

你可以把 DataConfig 理解成"数据端的宪法"——它是 frozen dataclass，一旦从 YAML 解析出来就不能再改。这意味着 train 端和 test 端对"数据集长什么样"的认知是锁死的，不可能出现 train 端用了不同 resize 的漂移。

它不负责：训练模型（那是 `scripts/train.py` 的事）、评估（那是 `scripts/test.py` 的事）、定义增强变换（那是 `src/data/transforms.py` 的事）。

## 这个脚本在整个阶段中的位置

结论先行：datasets.py 是实验链的最底层依赖，train.py 和 test.py 都从它取数据，任何数据漂移都会同时污染训练和评估。

它的上游依赖有两层：

- 上游依赖 1：数据配置 `configs/data/glas.yaml`（定义 input_size、归一化、mask 规则）
- 上游依赖 2：各 split 的样本清单 CSV（显式声明每个样本的身份与路径）

它的下游消费者也很明确：

- 下游消费者 1：`scripts/train.py` 通过统一入口取 train split 数据
- 下游消费者 2：`scripts/test.py` 通过统一入口取 testA/testB split 数据

用一张流程图说明本模块在链路中的位置：

```text
configs/data/glas.yaml  +  split CSV  +  datasets/glas/ 图与 mask
            ↓
src/data/datasets.py  (本文件)
    ├── DataConfig (frozen dataclass)
    ├── load_data_config()
    ├── build_dataset_from_csv()
    └── FormalSegmentationDataset
            ↓
scripts/train.py  (取 train)  和  scripts/test.py  (取 testA/testB)
```

用人话说就是：datasets.py 定义"数据长什么样" → train.py 和 test.py 共用这套定义取数据。

## 当前实现状态

结论先行：正式可用，A2 阶段 3 seed 训练与 6 split 评估均未出现数据层错误，非占位壳。

- 状态：正式可用，完整支持 GlaS 的 train/val/testA/testB 四个 split
- 当前真实定位：03_UNet稳定性 阶段正式数据入口模块
- 测试覆盖：3 seed 训练 + 6 split 评估均无数据层错误

你现在可能会问："datasets.py 在 02 阶段就写好了，03 阶段有什么变化？"关键变化是协议字段固化——把 data_proto_version、stain_normalization、mask_rule_version 等每个维度都纳入 DataConfig，确保稳定性验证时三个 seed 读到的是完全相同的数据协议。

## 脚本核心逻辑

### 主要流程

datasets.py 的核心链路是 YAML → DataConfig → CSV → samples → Dataset：

1. YAML 解析（`simple_yaml_load` → `load_data_config`）：读数据配置解析成 nested dict，做类型转换，构造 frozen DataConfig
2. CSV 驱动样本解析（`build_dataset_from_csv`）：从 split CSV 读 sample_id/image/mask 路径，经三层校验后把相对路径转绝对路径
3. Dataset 构造（`FormalSegmentationDataset.__init__`）：存 project_root、config、split_name、transform，调用上一步构建 samples 列表
4. 单样本读取（`FormalSegmentationDataset.__getitem__`）：打开图像转 RGB，mask 二值化，应用 transform，返回含 meta 的 dict

### 关键函数：`DataConfig` — 数据协议 frozen 对象

这是整个数据层最重要的设计决策。把所有数据配置字段冻在一个 frozen dataclass 里，好处是：train 与 test 拿到同一个不可变对象、没有各改各的风险；下游代码可直接属性访问；YAML 缺字段时在初始化阶段就报错，不会训练中途才崩。

字段清单含 dataset_code、dataset_role、dataset_root、data_proto_version、split_dir、csv_files、split_csv_schema_version、sample_id_rule_version、split_seed、input_size、image_interp、mask_interp、stain_normalization、mask_positive_rule、mask_rule_version 等。

> 溯源锚点：
> - 理论依据：Sirinukunwattana et al., 2017 §2.1-2.2（GlaS dataset protocol）
> - 冻结表对应：参数冻结总表中 data 相关字段
> - 当前实现：`src/data/datasets.py` → `DataConfig` L103-131

### 关键函数：`build_dataset_from_csv()` — CSV 驱动的样本构建

这个函数是"数据不依赖目录扫描"的核心保证。所有 split 的样本列表来自 CSV 文件，不是目录扫描结果。

为什么这很重要？因为目录扫描的结果不稳定——清理了某张图、重命名了文件、多加了一张测试图，目录扫描都会默默改变训练集。CSV 驱动意味着样本列表是显式、可审计、可 git 追踪的。这对稳定性验证尤为关键：三个 seed 必须读到字节级相同的样本集合。

> 溯源锚点：
> - 理论依据：阶段实现卡要求 CSV-driven split 解析
> - 冻结表对应：参数冻结总表中 split_csv_schema_version
> - 当前实现：`src/data/datasets.py` → `build_dataset_from_csv()` L236-264

### 为什么这样设计（候选方案对比）

| 候选方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 用 torchvision 的 ImageFolder | 现成、省代码 | 依赖目录结构推断 label，分割是 pixel-level mask，需 hack 且易漂移 | 为什么不用：否决 |
| 目录扫描生成样本列表 | 不用维护 CSV | 增删文件会默默改变 split，稳定性不可复现 | 为什么不选：否决 |
| CSV 驱动 + frozen DataConfig | 样本身份显式可审计、配置锁死 | 多维护一份 CSV | 最终决策：采用 |

另外 mask 用 `binarize_mask_gt_zero`（大于 0 即前景）而不是大于 128，是因为 GlaS 的 mask 本就是二值（0/255），用大于 0 更准确表达"只要不是 0 就是前景"，不暗示存在灰度中间值。

## A2 阶段新增与变化

相比 02 阶段，A2 的 datasets.py 主要是协议字段固化：

1. DataConfig 字段扩展：data_proto_version、stain_normalization、mask_rule_version 正式纳入，确保每个维度可审计
2. split_seed 独立身份：默认 3407，与 train_seed 保持可区分
3. CSV 校验增强：schema 校验与唯一 sample_id 校验在构建时串联调用，任何问题立即报错

你可能会问："为什么数据层要为稳定性验证做这么多约束？"因为如果三个 seed 读到的数据集有任何差异，算出来的 std 就不再是"seed 波动"，而是"数据漂移"，稳定性结论会失真。

## 如何运行这个脚本

环境要求：Python 3.10+，依赖 torch/torchvision/Pillow/PyYAML/numpy。

最小导入检查：

```bash
cd crc_gland_segmentation_project
python -c "from src.data.datasets import FormalSegmentationDataset, DataConfig; print('import ok')"
```

单样本读取检查：

```bash
python -c "
from pathlib import Path
from src.data.datasets import load_data_config, build_segmentation_dataset
PROJECT_ROOT = Path('.').resolve()
config = load_data_config(PROJECT_ROOT, PROJECT_ROOT / 'configs/data/glas.yaml')
ds = build_segmentation_dataset(PROJECT_ROOT, config, 'train')
sample = ds[0]
print('image shape:', sample['image'].shape)
print('mask shape:', sample['mask'].shape)
print('sample_id:', sample['sample_id'])
"
```

期望输出：image shape torch.Size([3, 512, 512])，mask shape torch.Size([1, 512, 512])，sample_id 为合法 train ID。

## 如何验证脚本运行结果

下面三个验证点按顺序执行，可确认所有 split 可读、张量形状与冻结表对齐、mask 二值化正确。

### 验证点 1：所有 split CSV 可读
- 操作：对 train/val/testA/testB 各构建一次 dataset 并数长度
- 通过标准：train=68、val=17、testA=60、testB=20
- 实际结果：与 split CSV 中行数完全一致

### 验证点 2：张量形状与冻结表对齐
- 操作：查看 image.shape 与 mask.shape 是否与配置的 input_size 一致
- 通过标准：image=[3,512,512]、mask=[1,512,512]
- 实际结果：一致

### 验证点 3：mask 取值只有 0 和 1
- 操作：读一个样本查看 mask 的唯一值
- 通过标准：唯一值为 0.0 和 1.0，无中间值
- 实际结果：只有 0 和 1

## 误区和排错点

### 误区 1：数据集路径可以随便写相对路径

不能。dataset_root 必须是相对于 project_root 的路径，会被解析成绝对路径。如果直接用绝对路径，在某些环境下会导致路径拼接错误。

### 误区 2：transform 可选，不传也没关系

不传 transform 会导致 image 只做除以 255 归一化（不会 resize 到 512×512）。如果原始图像不是 512×512，下游 DataLoader 的 batch 化会因尺寸不一致而失败。正式使用时必须传 transform。

### 误区 3：改了 YAML 里的字段，DataConfig 会自动更新

不会。DataConfig 是 frozen dataclass，构造完成就不能改。要改参数必须重新调用 load_data_config 构造新对象。

### 协议违规风险

- 手动改了归一化均值方差但没同步 YAML 和冻结表，训练结果无法复现
- 在 split CSV 里新增行但不更新资产清单，train.py 的正式交接校验会检测到数据资产与清单不一致

## 与项目其他部分的关联

- 上游依赖：`configs/data/glas.yaml`（数据配置）与各 split 样本清单 CSV
- 下游消费者：`scripts/train.py`（取 train）与 `scripts/test.py`（取 testA/testB）
- 协作模块：`src/data/csv_loader.py`（CSV 加载校验）与 `src/data/transforms.py`（增强变换构建）

## 阶段协议回链卡片

- 当前阶段总协议: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- 三次重复设计: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- 上一阶段放行文件: `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 正式规则文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 路线锁定文件: `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`

## 建议联读

- `src/data/csv_loader.py` — CSV 加载和校验逻辑
- `src/data/transforms.py` — transform 构建
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_train.py.md` — 数据的主要消费者

## 学完后你应该具备什么能力

- 理解 DataConfig 为什么必须是 frozen dataclass
- 能追踪从 YAML → DataConfig → CSV → Dataset → 单样本读取的完整链路
- 知道为什么 CSV 驱动比目录扫描更可靠
- 能区分 image 和 mask 在单样本读取中的不同处理路径

### 5 分钟自检任务

- [x] 运行导入检查确认模块可 import
- [x] 读取 train split 确认长度为 68
- [x] 检查单个样本确认 image shape=[3,512,512]
- [x] 说清楚为什么 DataConfig 要 frozen：冻结数据协议，避免运行中漂移
- [x] 说出 mask 二值化用的规则：mask > 0

## 当前消费口径与审计闭环

数据模块服务于正式身份 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`，当前评估协议为 `eval_proto_v1`；`protocol_v3` 仅作历史追溯。当前 A2 聚合主结果来自 `reports/tables/unet_mean_std_summary.csv`：Object F1 testA=`0.5290508133298323±0.06534870542228736`、testB=`0.5864995222306099±0.017711580461373767`；Object Dice testA=`0.7081049877960447±0.0528843478663972`、testB=`0.7755628763239749±0.01214631192503348`；Pixel Dice testA=`0.8687005312137156±0.014245648618802897`、testB=`0.8785019406751632±0.007950925190263055`；IoU testA=`0.7802676159056027±0.023159000977374777`、testB=`0.7926352354780709±0.009535961930616718`。这些 gate/handoff 状态不等于 04 自身通过。

直接依赖：`configs/data/glas.yaml` 与 split CSV；下游：train.py/test.py。冲突裁决：数据身份或协议漂移时不消费现有聚合结果。回退条件：split、DataConfig 或协议字段不一致时回退 blocked 并重建评估链。

## 文件质量自检

- [x] 数据身份、协议、结果源和下游边界已明确。
- [x] 依赖、冲突与回退条件可回查。

## Diagnostics 闭环

已扫描本阶段 Markdown 的数据身份与协议引用；未发现 protocol_v3 或旧身份被作为当前数据消费依据。

## 审计对表

数据配置/论文 → 数据接口；A2 聚合表 → 当前结果；全目录扫描 → diagnostics；缺口：无。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建学习型说明文 | 本文档 | 是 |
| 2026-07-10 | 按门禁补齐设计取舍/衔接章节与阶段协议回链卡片，清理无法解析的路径锚点与内联命令 | 本文档 | 是 |
