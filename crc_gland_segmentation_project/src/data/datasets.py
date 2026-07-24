"""
对应阶段: 03_UNet稳定性
理论依据:
  - 论文: Sirinukunwattana et al., 2017, "Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest"
  章节: §2.1-2.2 (Dataset and Ground Truth)
  公式/定义: Ground truth provided as binary masks; official train/test split definition
  - DataConfig frozen dataclass 将 data protocol 字段固化，防止 train/test 端各自解引用不同值
  - CSV 驱动的 split 解析: build_dataset_from_csv 通过 split CSV manifest 决定样本归属，不依赖目录扫描
  - mask 二值化规则: mask_positive_rule > 0 -> binary mask，与冻结表 mask_rule_version 对齐
代码参考:
  - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
  - 文件: configs/data/glas.yaml, splits/glas/*.csv
  - commit: project_internal
  - 许可证: project_internal
  - 本项目调整: DataConfig 与 FormalSegmentationDataset 专为 GlaS 数据集三段式实验链设计，固化 CSV 驱动的 split 管理
冻结回链: 结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md
  - input_size=(512,512), mask_positive_rule=gt_zero, normalize_mean/std, stain_normalization=off
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

from .csv_loader import load_csv_rows, resolve_row_paths, validate_csv_schema, validate_unique_sample_ids
from .boundary_targets import build_boundary_target
from .distance_targets import build_distance_target
from .mask_ops import binarize_mask_gt_zero, load_mask_array


def _strip_inline_comment(value: str) -> str:
    """Strip trailing inline YAML comment from a scalar value string.

    YAML spec: a comment starts with ' #' (space + hash) outside of quoted strings.
    Quoted values ('...' or "...") are returned unchanged.
    """
    if value.startswith(("'", '"')):
        return value
    idx = value.find(" #")
    if idx != -1:
        return value[:idx].rstrip()
    return value


def parse_scalar(value: str) -> Any:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 本项目自建 src/data/datasets.py，无外部代码来源（数据加载为项目自建，详见模块级 docstring）
    本项目调整: 适配 03 阶段，固化协议
    """
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item.strip()) for item in inner.split(",")]
    if value.startswith(("'", '"')) and value.endswith(("'", '"')):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def simple_yaml_load(text: str) -> dict[str, Any]:
    """Load the minimal project-local YAML subset used by stage02 configs.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: reproducible config-to-runtime mapping
    - 章节: deterministic hierarchical configuration parsing
    - 公式/定义: indented key/value text -> nested dict
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/data/glas.yaml, configs/train/unet_flow_v1.yaml, src/data/datasets.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前只支持 stage02 真实用到的缩进映射和标量，不引入锚点、复杂 list block 或多文档语法。
    - 目标不是替代完整 YAML 库，而是让正式配置链在本项目本地环境里有可解释、可控的最小解析器。
    """
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    last_scalar: tuple[dict[str, Any], str, int] | None = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if ":" not in stripped:
            if last_scalar is None or indent <= last_scalar[2]:
                raise ValueError(f"unsupported YAML continuation line: {raw_line!r}")
            parent, key, _ = last_scalar
            previous = parent[key]
            if not isinstance(previous, str):
                raise ValueError(f"YAML continuation requires a scalar string: {raw_line!r}")
            parent[key] = f"{previous} {stripped}"
            continue
        key, raw_value = stripped.split(":", 1)
        value = _strip_inline_comment(raw_value.strip())
        while stack and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]
        if value:
            current[key] = parse_scalar(value)
            last_scalar = (current, key, indent)
        else:
            nested: dict[str, Any] = {}
            current[key] = nested
            stack.append((indent, nested))
            last_scalar = None
    return root


@dataclass(frozen=True)
class DataConfig:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 本项目自建 src/data/datasets.py，无外部代码来源（数据加载为项目自建，详见模块级 docstring）
    本项目调整: 适配 03 阶段，固化协议
    """
    dataset_code: str
    dataset_role: str
    dataset_root: str
    dataset_source_note: str
    dataset_version: str
    dataset_layout_version: str
    data_proto_version: str
    split_dir: str
    csv_files: dict[str, str]
    split_csv_schema_version: str
    sample_id_rule_version: str
    asset_status: str
    split_seed: int
    input_size: tuple[int, int]
    image_interp: str
    mask_interp: str
    normalize_mean: tuple[float, float, float]
    normalize_std: tuple[float, float, float]
    stain_normalization: str
    mask_positive_rule: str
    mask_rule_version: str


def _as_tuple_of_floats(value: Any, length: int, field_name: str) -> tuple[float, ...]:
    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f"{field_name} must be a list of length {length}: {value!r}")
    return tuple(float(item) for item in value)


def _as_hw_tuple(value: Any, field_name: str) -> tuple[int, int]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{field_name} must be a list of length 2: {value!r}")
    return int(value[0]), int(value[1])


def load_data_config(project_root: Path, config_path: Path) -> DataConfig:
    """Load the formal data config and cast it into a frozen `DataConfig`.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: benchmark configuration freeze before training
    - 章节: config fields as the single source of truth for dataset protocol
    - 公式/定义: config path -> parsed YAML dict -> typed `DataConfig`
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/data/glas.yaml, scripts/train.py, src/data/datasets.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 解析入口统一接受 project-root 相对路径和绝对路径，保持和 experiment config 解引用逻辑一致。
    - `csv_files`、`input_size`、`normalize_mean/std` 会在装载阶段立刻做结构检查，尽量把坏配置挡在 dataset 构造之前。
    """
    resolved = config_path if config_path.is_absolute() else (project_root / config_path)
    data = simple_yaml_load(resolved.read_text(encoding="utf-8"))
    csv_files = data.get("csv_files", {})
    if not isinstance(csv_files, dict):
        raise ValueError(f"csv_files must be a mapping: {resolved}")
    return DataConfig(
        dataset_code=str(data["dataset_code"]),
        dataset_role=str(data["dataset_role"]),
        dataset_root=str(data["dataset_root"]),
        dataset_source_note=str(data["dataset_source_note"]),
        dataset_version=str(data["dataset_version"]),
        dataset_layout_version=str(data["dataset_layout_version"]),
        data_proto_version=str(data["data_proto_version"]),
        split_dir=str(data["split_dir"]),
        csv_files={str(key): str(value) for key, value in csv_files.items()},
        split_csv_schema_version=str(data["split_csv_schema_version"]),
        sample_id_rule_version=str(data["sample_id_rule_version"]),
        asset_status=str(data["asset_status"]),
        split_seed=int(data.get("split_seed", 3407)),
        input_size=_as_hw_tuple(data["input_size"], "input_size"),
        image_interp=str(data["image_interp"]),
        mask_interp=str(data["mask_interp"]),
        normalize_mean=_as_tuple_of_floats(data["normalize_mean"], 3, "normalize_mean"),
        normalize_std=_as_tuple_of_floats(data["normalize_std"], 3, "normalize_std"),
        stain_normalization=str(data.get("stain_normalization", "off")),
        mask_positive_rule=str(data["mask_positive_rule"]),
        mask_rule_version=str(data["mask_rule_version"]),
    )


def resolve_dataset_root(project_root: Path, config: DataConfig) -> Path:
    """Resolve the frozen raw-dataset root for the current stage02 dataset.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: benchmark asset root consistency
    - 章节: raw asset directory as the physical source of train/val/test splits
    - 公式/定义: project_root + dataset_root -> absolute raw dataset path
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/data/glas.yaml, src/data/datasets.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前明确以 data config 中的 `dataset_root` 为唯一物理资产根，不允许 trainer/runtime 各自拼接不同目录。
    - 返回绝对路径，方便后续 CSV row 解析和 learning-doc 锚点统一对账。
    """
    return (project_root / config.dataset_root).resolve()


def resolve_split_csv(project_root: Path, config: DataConfig, split_name: str) -> Path:
    """Resolve the formal split CSV path for one dataset split.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: train/val/test role separation in benchmark protocols
    - 章节: split manifest as the canonical sample list
    - 公式/定义: split_name + split_dir + csv_files -> absolute split CSV path
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/data/glas.yaml, splits/glas/*.csv, src/data/datasets.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - split 名称只认 data config 显式登记的键，避免 runtime/train 自己发明新的别名。
    - 一旦 split 名称缺失立即报错，防止训练链默默退回错误 CSV。
    """
    csv_name = config.csv_files.get(split_name)
    if not csv_name:
        raise KeyError(f"Unknown split_name for {config.dataset_code}: {split_name}")
    return (project_root / config.split_dir / csv_name).resolve()


def build_dataset_from_csv(project_root: Path, config: DataConfig, split_name: str) -> list[dict[str, Any]]:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 本项目自建 src/data/datasets.py，无外部代码来源（数据加载为项目自建，详见模块级 docstring）
    本项目调整: 适配 03 阶段，固化协议
    """
    csv_path = resolve_split_csv(project_root, config, split_name)
    rows = load_csv_rows(csv_path)
    schema_issues = validate_csv_schema(rows, config.dataset_code)
    unique_issues = validate_unique_sample_ids(rows)
    issues = schema_issues + unique_issues
    if issues:
        raise ValueError(f"Split CSV is invalid: {csv_path} -> {issues}")

    samples: list[dict[str, Any]] = []
    for row in rows:
        image_path, mask_path = resolve_row_paths(project_root, row)
        samples.append(
            {
                "sample_id": row["sample_id"],
                "dataset": row["dataset"],
                "split": row["split"],
                "image_path": image_path,
                "mask_path": mask_path,
                "meta": row,
            }
        )
    return samples


def _load_rgb_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        return image.convert("RGB")


class FormalSegmentationDataset(Dataset[dict[str, Any]]):
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 本项目自建 src/data/datasets.py，无外部代码来源（数据加载为项目自建，详见模块级 docstring）
    本项目调整: 适配 03 阶段，固化协议
    """
    def __init__(
        self,
        project_root: Path,
        config: DataConfig,
        split_name: str,
        transform: Callable[[Image.Image, torch.Tensor], tuple[torch.Tensor, torch.Tensor]] | None = None,
    ) -> None:
        self.project_root = project_root
        self.config = config
        self.split_name = split_name
        self.transform = transform
        self.samples = build_dataset_from_csv(project_root, config, split_name)

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> dict[str, Any]:
        sample = self.samples[index]
        image = _load_rgb_image(Path(sample["image_path"]))
        mask = torch.from_numpy(binarize_mask_gt_zero(load_mask_array(Path(sample["mask_path"])))).unsqueeze(0).float()

        if self.transform is not None:
            image_tensor, mask_tensor = self.transform(image, mask)
        else:
            image_tensor = torch.from_numpy(np.array(image, dtype=np.float32)).permute(2, 0, 1) / 255.0
            mask_tensor = mask

        result = {
            "image": image_tensor,
            "mask": mask_tensor.float(),
            "sample_id": sample["sample_id"],
            "split": sample["split"],
            "image_path": str(sample["image_path"]),
            "mask_path": str(sample["mask_path"]),
        }
        result["boundary_target"] = torch.from_numpy(
            build_boundary_target(mask_tensor.squeeze(0).cpu().numpy(), width=3)
        ).unsqueeze(0).float()
        result["distance_target"] = torch.from_numpy(
            build_distance_target(mask_tensor.squeeze(0).cpu().numpy())
        ).unsqueeze(0).float()
        return result


def build_segmentation_dataset(
    project_root: Path,
    config: DataConfig,
    split_name: str,
    transform: Callable[[Image.Image, torch.Tensor], tuple[torch.Tensor, torch.Tensor]] | None = None,
) -> FormalSegmentationDataset:
    """Construct the formal dataset object for one stage02 split.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: dataset factory pattern for train/val split consumption
    - 章节: split-specific dataset instantiation under one frozen protocol
    - 公式/定义: project_root + data config + split_name + transform -> `FormalSegmentationDataset`
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: scripts/train.py, src/data/datasets.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 builder 只做正式对象装配，不在这里混入 dataloader、sampler 或 debug side effects。
    - 把 split 和 transform 的进入点集中在一个 builder，方便训练入口和学习说明文共同回链。
    """
    return FormalSegmentationDataset(project_root=project_root, config=config, split_name=split_name, transform=transform)
