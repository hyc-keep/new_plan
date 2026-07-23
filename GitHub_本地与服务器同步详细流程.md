# GitHub 本地与服务器同步流程

## 一、仓库边界

本仓库根目录为 `Paper`，上传以下可版本化内容：

- 实验计划、阶段路线和验收规则
- 论文研究说明、参数依据和阶段总结
- `crc_gland_segmentation_project/src/`
- `crc_gland_segmentation_project/scripts/`
- `crc_gland_segmentation_project/configs/`
- `crc_gland_segmentation_project/b_class_auxiliary/`
- `crc_gland_segmentation_project/reproducibility_audit/`
- `crc_gland_segmentation_project/reports/stage_reports/` 下的轻量文本和 YAML/CSV 元数据
- `experiments/` 下的 `run_meta.yaml`、CSV、Markdown 摘要和复现报告
- 项目内 ResNet34 预训练权重 `crc_gland_segmentation_project/weights/resnet34-b627a593.pth`

预训练权重 SHA256：

```text
b627a593bcbe140c234610266fe4f8ae95ea42fc881d091c9b6052e6b1d0590f
```

不上传以下内容：

- 原始数据集和本地数据副本
- `结直肠腺体分割_正式参考资料/` 中的完整 PDF、外部代码库和大型参考资料
- checkpoint、预测结果、可视化图片、TensorBoard 文件
- `.npy/.npz` 中间缓存
- Conda/venv 环境、日志、临时归档和 IDE 配置

这些规则由根目录 `.gitignore` 执行。GitHub 保存的是可复现的代码和实验协议基线，不是服务器磁盘镜像。

## 二、首次创建仓库

在 Paper 根目录执行：

```bash
git init
git branch -M main
git status --short --ignored
```

确认没有数据集、checkpoint、大量图片和本地环境后，再加入并检查文件：

```bash
git add .
git status --short
```

确认清单无误后提交：

```bash
git commit -m "init: add reproducible colorectal gland segmentation project"
```

新建 GitHub 私有仓库后绑定远端：

```bash
git remote add origin <你的新仓库地址>
git push -u origin main
```

不要在没有检查 `git status` 前使用 `git add .`、commit 或 push。

## 三、服务器接入

服务器从 GitHub 基线 clone：

```bash
git clone <你的新仓库地址>
cd Paper
```

服务器需要另外准备：

- 与冻结记录一致的 Python/PyTorch/CUDA/cuDNN 环境
- 原始数据集
- 训练输出目录和 checkpoint 存储空间

数据集和大结果不通过 GitHub 同步；只将代码、配置、协议、轻量元数据和正式结论 commit/push。

## 四、后续同步原则

```text
本地修改 -> commit -> push -> 服务器 pull
服务器修改 -> commit -> push -> 本地 pull
```

正式 GPU 训练期间以服务器为主线。不要让本地和服务器同时修改同一个核心脚本或状态文档，也不要手动复制覆盖 Git 管理的文件。

服务器完成一个可记录的阶段后，只提交代码、配置、文档和轻量结果元数据：

```bash
git status --short
git add <明确的文件或目录>
git commit -m "docs: record reproducibility audit status"
git push
```

本地查看服务器更新：

```bash
git pull --ff-only
```

如果本地和服务器都产生了未提交修改，先停止训练相关文件的继续编辑，再检查差异并解决冲突。不要使用破坏性 reset 或手动覆盖。

## 五、当前实验顺序

GitHub 基线建立后，服务器先完成：

1. A2/B1 在冻结代码下的两次完整 train→test 复现；
2. 用 `reproducibility_audit/compare_runs.py` 比较两次结果；
3. 只有复现审计通过后，才关闭 04_Baseline 并进入 05_LKMA。
