# UNet Stability Note (A2)

## Mean+-Std Summary

### testA
- F1: 0.5291 +/- 0.0653
- Object Dice: 0.7081 +/- 0.0529
- Object Hausdorff: 128.8409 +/- 28.7017
- Dice: 0.8687 +/- 0.0142
- IoU: 0.7803 +/- 0.0232
- HD95: 57.4652 +/- 3.8713
- Boundary F1: 0.6283 +/- 0.0388

### testB
- F1: 0.5865 +/- 0.0177
- Object Dice: 0.7756 +/- 0.0121
- Object Hausdorff: 125.0122 +/- 10.7744
- Dice: 0.8785 +/- 0.0080
- IoU: 0.7926 +/- 0.0095
- HD95: 47.2812 +/- 10.7473
- Boundary F1: 0.6155 +/- 0.0026

## Cross-Seed Failure Pattern Analysis

- seeds_analyzed: [3407, 1234, 2025]

### testA
- adhesion_split_fail: cross_seed_consistent (seed3407=47, seed1234=45, seed2025=51)
- small_gland_miss: not_consistent (seed3407=0, seed1234=2, seed2025=0)
- boundary_blur: cross_seed_consistent (seed3407=1, seed1234=1, seed2025=2)

### testB
- adhesion_split_fail: cross_seed_consistent (seed3407=9, seed1234=10, seed2025=11)
- small_gland_miss: cross_seed_consistent (seed3407=1, seed1234=1, seed2025=1)
- boundary_blur: cross_seed_consistent (seed3407=1, seed1234=2, seed2025=1)

### testB_harder
- F1: testA_mean=0.5291, testB_mean=0.5865 -> testB_not_worse
- Object Dice: testA_mean=0.7081, testB_mean=0.7756 -> testB_not_worse
- Object Hausdorff: testA_mean=128.8409, testB_mean=125.0122 -> testB_not_worse

## Abnormal Run Adjudication

- seed3407: stop_reason=early_stopping, best_epoch=53, epoch_count=73
- seed1234: stop_reason=early_stopping, best_epoch=95, epoch_count=115
- seed2025: stop_reason=early_stopping, best_epoch=47, epoch_count=67

