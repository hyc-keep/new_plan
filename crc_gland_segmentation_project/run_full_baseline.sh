#!/usr/bin/env bash
set -euo pipefail

cd /home/featurize/work/Paper/crc_gland_segmentation_project

export DEVICE=cuda
export PYTHON_BIN=python
export PYTHONUNBUFFERED=1

echo "===== JOB START $(date) ====="

echo "===== START A2 TRAINING ====="
bash scripts/run_baseline_sequential.sh a2 3407,1234,2025 fresh
echo "===== A2 TRAINING FINISHED $(date) ====="

echo "===== START B1 TRAINING ====="
bash scripts/run_baseline_sequential.sh b1 3407,1234,2025 fresh
echo "===== B1 TRAINING FINISHED $(date) ====="

echo "===== TEST A2 seed3407 ====="
python -u scripts/test.py --config configs/experiment/A2_UNet_GlaS_seed3407.yaml --run-name A2_UNet_GlaS_seed3407 --device "$DEVICE" --max-visual-samples 5

echo "===== TEST A2 seed1234 ====="
python -u scripts/test.py --config configs/experiment/A2_UNet_GlaS_seed1234.yaml --run-name A2_UNet_GlaS_seed1234 --device "$DEVICE" --max-visual-samples 5

echo "===== TEST A2 seed2025 ====="
python -u scripts/test.py --config configs/experiment/A2_UNet_GlaS_seed2025.yaml --run-name A2_UNet_GlaS_seed2025 --device "$DEVICE" --max-visual-samples 5

echo "===== TEST B1 seed3407 ====="
python -u scripts/test.py --config configs/experiment/B1_ResNet34_UNet_GlaS_seed3407.yaml --run-name B1_ResNet34_UNet_GlaS_seed3407 --device "$DEVICE" --max-visual-samples 5

echo "===== TEST B1 seed1234 ====="
python -u scripts/test.py --config configs/experiment/B1_ResNet34_UNet_GlaS_seed1234.yaml --run-name B1_ResNet34_UNet_GlaS_seed1234 --device "$DEVICE" --max-visual-samples 5

echo "===== TEST B1 seed2025 ====="
python -u scripts/test.py --config configs/experiment/B1_ResNet34_UNet_GlaS_seed2025.yaml --run-name B1_ResNet34_UNet_GlaS_seed2025 --device "$DEVICE" --max-visual-samples 5

echo "===== ALL TRAINING AND TESTING FINISHED $(date) ====="
