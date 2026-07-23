#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if pgrep -af "scripts/train.py.*D2_R34UNet_Distance_GlaS_seed" >/dev/null; then
  echo "已有 D2 Distance 训练进程，先停止或等待它结束。" >&2
  exit 1
fi

BASE_CONFIG="configs/experiment/D2_R34UNet_Distance_GlaS_seed3407.yaml"

for SEED in 3407 1234 2025; do
  RUN_NAME="D2_R34UNet_Distance_GlaS_seed${SEED}"
  CONFIG="configs/experiment/${RUN_NAME}.yaml"

  python - "$SEED" "$CONFIG" "$RUN_NAME" <<'PY'
import sys
from pathlib import Path

seed = sys.argv[1]
config_path = Path(sys.argv[2])
run_name = sys.argv[3]
base_path = Path("configs/experiment/D2_R34UNet_Distance_GlaS_seed3407.yaml")
text = base_path.read_text(encoding="utf-8")
text = text.replace(
    "run_name: D2_R34UNet_Distance_GlaS_seed3407",
    f"run_name: {run_name}",
)
text = text.replace(
    "consumer_file: configs/experiment/D2_R34UNet_Distance_GlaS_seed3407.yaml",
    f"consumer_file: configs/experiment/{run_name}.yaml",
)
text = text.replace("train_seed: 3407", f"train_seed: {seed}")
text = text.replace(
    "D2_R34UNet_Distance_GlaS_seed3407__smoke",
    f"{run_name}__smoke",
)
config_path.write_text(text, encoding="utf-8")
print(f"created_config={config_path}")
PY

done

for SEED in 3407 1234 2025; do
  RUN_NAME="D2_R34UNet_Distance_GlaS_seed${SEED}"
  CONFIG="configs/experiment/${RUN_NAME}.yaml"
  LOG="experiments/${RUN_NAME}.console.log"

  echo "===== TRAIN ${RUN_NAME} ====="
  mkdir -p experiments
  python -u scripts/train.py \
    --config "$CONFIG" \
    --run-name "$RUN_NAME" \
    --device cuda \
    2>&1 | tee "$LOG"

  echo "===== TEST ${RUN_NAME} ====="
  python -u scripts/test.py \
    --config "$CONFIG" \
    --run-name "$RUN_NAME" \
    --device cuda \
    2>&1 | tee -a "$LOG"

  echo "===== FINISHED ${RUN_NAME} ====="
done

echo "===== ALL THREE DISTANCE SEEDS FINISHED ====="
