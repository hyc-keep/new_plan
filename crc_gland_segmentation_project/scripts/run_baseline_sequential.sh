#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

MODEL="${1:-a2}"
SEED_LIST="${2:-3407,1234,2025}"
MODE="${3:-safe}"
DEVICE="${DEVICE:-cuda}"
PYTHON_BIN="${PYTHON_BIN:-python}"
export CUBLAS_WORKSPACE_CONFIG="${CUBLAS_WORKSPACE_CONFIG:-:4096:8}"

case "$MODEL" in
  a2)
    PREFIX="A2_UNet_GlaS"
    ;;
  b1)
    PREFIX="B1_ResNet34_UNet_GlaS"
    ;;
  *)
    echo "用法: $0 [a2|b1] [seed列表，例如 1234,2025] [safe|fresh]" >&2
    exit 2
    ;;
esac

case "$MODE" in
  safe|fresh)
    ;;
  *)
    echo "模式必须是 safe 或 fresh: $MODE" >&2
    exit 2
    ;;
esac

if pgrep -af '[p]ython .*scripts/train.py' >/dev/null; then
  echo "检测到已有训练进程，拒绝启动串行队列。" >&2
  exit 1
fi

is_train_complete() {
  local run_dir="$1"
  local expected_config_version="original_protocol_reproduction"
  local expected_train_proto="train_proto_v1"
  [[ -f "$run_dir/summaries/run_summary.md" ]] || return 1
  [[ -f "$run_dir/checkpoints/best.ckpt" ]] || return 1
  [[ -f "$run_dir/checkpoints/last.ckpt" ]] || return 1
  [[ -f "$run_dir/run_meta.yaml" ]] || return 1
  grep -q '^- stop_reason: `\(early_stopping\|epoch_max_reached\)`' "$run_dir/summaries/run_summary.md" || return 1
  grep -q "^config_version: ${expected_config_version}$" "$run_dir/run_meta.yaml" || return 1
  grep -q "^train_proto_version: ${expected_train_proto}$" "$run_dir/run_meta.yaml" || return 1
  "$PYTHON_BIN" - "$run_dir" <<'PY'
import csv
import hashlib
import math
import sys
from pathlib import Path
import torch
import yaml
run_dir = Path(sys.argv[1])
for filename in ("train_log.csv", "val_metrics.csv"):
    path = run_dir / filename
    if not path.exists():
        raise SystemExit(1)
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    if not rows:
        raise SystemExit(1)
    for row in rows:
        for key, value in row.items():
            if key == "amp" or value in ("", None):
                continue
            try:
                if not math.isfinite(float(value)):
                    raise SystemExit(1)
            except ValueError:
                continue
for filename in ("best.ckpt", "last.ckpt"):
    checkpoint = torch.load(run_dir / "checkpoints" / filename, map_location="cpu")
    for value in checkpoint.get("model_state_dict", {}).values():
        if torch.is_tensor(value) and not torch.isfinite(value).all():
            raise SystemExit(1)
meta = yaml.safe_load((run_dir / "run_meta.yaml").read_text(encoding="utf-8"))
required_meta = ("run_name", "train_seed", "config_version", "model_name", "stage_code", "dataset_code", "best_checkpoint_path", "best_checkpoint_sha256")
if any(not meta.get(key) for key in required_meta):
    raise SystemExit(1)
checkpoint_path = run_dir / meta["best_checkpoint_path"]
if checkpoint_path.resolve() != (run_dir / "checkpoints" / "best.ckpt").resolve():
    raise SystemExit(1)
if hashlib.sha256(checkpoint_path.read_bytes()).hexdigest() != meta["best_checkpoint_sha256"]:
    raise SystemExit(1)
if meta.get("smoke_check") is True:
    raise SystemExit(1)
PY
}

is_complete() {
  local run_dir="$1"
  is_train_complete "$run_dir" || return 1
  "$PYTHON_BIN" - "$run_dir" <<'PY'
import csv
import math
import sys
from pathlib import Path
run_dir = Path(sys.argv[1])
for filename, expected_rows in (("testA_metrics.csv", 60), ("testB_metrics.csv", 20)):
    path = run_dir / filename
    if not path.exists():
        raise SystemExit(1)
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    if len(rows) != expected_rows:
        raise SystemExit(1)
    for row in rows:
        for key, value in row.items():
            if value in ("", None):
                continue
            try:
                if not math.isfinite(float(value)):
                    raise SystemExit(1)
            except ValueError:
                continue
for path in (run_dir / "metric_crosscheck_note.md", run_dir / "predictions" / "testA", run_dir / "predictions" / "testB", run_dir / "visuals"):
    if not path.exists():
        raise SystemExit(1)
meta_text = (run_dir / "run_meta.yaml").read_text(encoding="utf-8")
if "metric_crosscheck_result: pass" not in meta_text:
    raise SystemExit(1)
PY
}

IFS=',' read -r -a SEEDS <<< "$SEED_LIST"
[[ "${#SEEDS[@]}" -gt 0 ]] || { echo "seed列表不能为空" >&2; exit 2; }

for seed in "${SEEDS[@]}"; do
  [[ "$seed" =~ ^[0-9]+$ ]] || { echo "非法 seed: $seed" >&2; exit 2; }
  run_name="${PREFIX}_seed${seed}"
  config="configs/experiment/${run_name}.yaml"
  run_dir="experiments/${run_name}"
  log="experiments/${run_name}.console.log"

  [[ -f "$config" ]] || { echo "缺少配置: $config" >&2; exit 1; }

  if is_complete "$run_dir"; then
    echo "===== SKIP COMPLETE ${run_name} ====="
    continue
  fi

  if is_train_complete "$run_dir"; then
    echo "===== TRAIN ASSET COMPLETE ${run_name}; TEST WILL RUN ====="
    echo "===== TEST ${run_name} ====="
    PYTHONHASHSEED="$seed" "$PYTHON_BIN" -u scripts/test.py --config "$config" --run-name "$run_name" --device "$DEVICE" 2>&1 | tee -a "$log"
    if ! is_complete "$run_dir"; then
      echo "测试完成但正式资产完整性检查失败，队列停止: $run_name" >&2
      exit 1
    fi
    echo "===== FINISHED ${run_name} ====="
    continue
  fi

  if [[ -e "$run_dir" ]]; then
    if [[ "$MODE" == "fresh" ]]; then
      archive_root="experiments/_historical_archive"
      timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
      reason_code="interrupted_fresh"
      archive_dir="${archive_root}/${run_name}__historical_${reason_code}_${timestamp}"
      mkdir -p "$archive_root"
      config_snapshot="$(mktemp)"
      cp "$config" "$config_snapshot"
      mv "$run_dir" "$archive_dir"
      metric_summary="$("$PYTHON_BIN" - "$archive_dir" <<'PY'
import csv
import math
import sys
from pathlib import Path

root = Path(sys.argv[1])
metrics = ("objdice", "dice", "iou", "f1", "boundary_f1", "hd95", "object_hausdorff")
for filename, split_name in (("testA_metrics.csv", "TestA"), ("testB_metrics.csv", "TestB")):
    path = root / filename
    print(f"### {split_name}")
    if not path.exists():
        print("- 指标文件：缺失")
        continue
    rows = list(csv.DictReader(path.open(newline="")))
    print(f"- 样本行数：{len(rows)}")
    for metric in metrics:
        values = [float(row[metric]) for row in rows if row.get(metric) not in (None, "")]
        if not values:
            print(f"- {metric}：未知")
            continue
        mean = sum(values) / len(values)
        std = math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))
        print(f"- {metric}: mean={mean:.6f}, std={std:.6f}")
PY
)"
      {
        printf '%s\n' '# 历史归档说明' ''
        printf '%s\n' '## 一、归档身份' '' "- 原正式目录：\`${run_dir}\`" "- 当前归档目录：\`${archive_dir}\`" "- 归档时间（UTC）：${timestamp}" "- 归档原因代码：\`${reason_code}\`" '- 归档原因：本次训练未形成完整正式 run，现有目录被 fresh 重跑替代；原目录仅作为历史追溯证据保留。' '- 实验资产类别：A 类正式实验资产' '- 当前 Gate 是否允许消费：否' '- 是否可以直接复用而不重训：否，必须先完成 checkpoint、协议身份、预测资产和独立指标复核。' ''
        printf '%s\n' '## 二、当时的实验身份' '' "- 正式 run_name：\`${run_name}\`" '- 阶段、模型、数据集和 seed：见下方配置快照及 run_meta.yaml；未知字段不得凭记忆补写。' "- 当前配置文件：\`${config}\`" '- 历史归档标记：historical_archive_only = true' '- 当前 Gate 标记：valid_for_current_gate = false' ''
        printf '%s\n' '## 三、归档前配置快照' '' '以下内容是归档前实际使用的配置，不是当前配置的推测。' '' '```yaml'
        cat "$config_snapshot"
        printf '%s\n' '```' ''
        printf '%s\n' '## 四、当时运行记录' ''
        if [[ -f "$archive_dir/run_meta.yaml" ]]; then
          printf '%s\n' '归档目录中的 run_meta.yaml 是当时程序实际写入的运行记录：' '' '```yaml'
          cat "$archive_dir/run_meta.yaml"
          printf '%s\n' '```'
        else
          printf '%s\n' '- run_meta.yaml：缺失，无法确认当时的完整运行参数。'
        fi
        printf '%s\n' '' '## 五、结果和资产状态' ''
        for path in config.yaml run_meta.yaml train_log.csv val_metrics.csv testA_metrics.csv testB_metrics.csv metric_crosscheck_note.md; do
          if [[ -f "$archive_dir/$path" ]]; then printf '%s\n' "- ${path}：存在"; else printf '%s\n' "- ${path}：缺失"; fi
        done
        printf '%s\n' "- best.ckpt：$([[ -f \"$archive_dir/checkpoints/best.ckpt\" ]] && echo 存在 || echo 缺失)" "- last.ckpt：$([[ -f \"$archive_dir/checkpoints/last.ckpt\" ]] && echo 存在 || echo 缺失)"
        printf '%s\n' '' '说明：本文件只记录归档时能从真实资产读取的状态；指标数值由 testA_metrics.csv、testB_metrics.csv 或独立汇总脚本提供，不在归档脚本中猜测或改写。' ''
        printf '%s\n' '' '## 六、真实指标摘要' '' "$metric_summary" '' '以上指标由归档目录中的 TestA/TestB CSV 自动计算，使用 population std（ddof=0）；CSV 缺失或字段缺失时明确标记为未知。' ''
        printf '%s\n' '## 七、与当前计划的差异和失败原因' '' '- 归档直接原因：未完成的 run 被 fresh 模式替代。' '- 是否代表模型性能失败：未知；本次归档原因是运行状态，不等同于模型指标失败。' '- 与当前计划的参数差异：以配置快照和 run_meta.yaml 为准；如果协议字段不同，必须单独列出，不得把不同协议结果合并。' ''
        printf '%s\n' '## 八、复用和重训条件' '' '- 不能仅凭目录存在就作为当前正式结果。' '- 复用前必须核对配置快照、run_meta.yaml、checkpoint hash、预测资产、TestA/TestB 原始指标和独立复核。' '- 任一关键证据缺失时，只能作为历史参考，不能进入当前 Gate。'
      } > "$archive_dir/archive_manifest.md"
      rm -f "$config_snapshot"
      echo "===== ARCHIVED INCOMPLETE ${run_name} -> ${archive_dir} ====="
    else
      echo "输出目录已存在但未完成，拒绝覆盖: $run_dir" >&2
      echo "如确认需要全新重跑，请使用第三个参数 fresh。" >&2
      exit 1
    fi
  fi

  echo "===== TRAIN ${run_name} ====="
  PYTHONHASHSEED="$seed" "$PYTHON_BIN" -u scripts/train.py \
    --config "$config" \
    --run-name "$run_name" \
    --device "$DEVICE" \
    2>&1 | tee "$log"

  if ! is_complete "$run_dir"; then
    echo "训练进程虽已退出，但完整性检查失败，队列停止: $run_name" >&2
    exit 1
  fi

  echo "===== TEST ${run_name} ====="
  PYTHONHASHSEED="$seed" "$PYTHON_BIN" -u scripts/test.py --config "$config" --run-name "$run_name" --device "$DEVICE" 2>&1 | tee -a "$log"

  if ! is_complete "$run_dir"; then
    echo "测试完成但正式资产完整性检查失败，队列停止: $run_name" >&2
    exit 1
  fi

  echo "===== FINISHED ${run_name} ====="
done

echo "===== BASELINE ${MODEL} SEQUENTIAL QUEUE FINISHED ====="
