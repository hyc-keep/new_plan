# UNet Stability Note (A2)

## Mean+-Std Summary

### testA
- F1: 0.5847 +/- 0.0222
- Object Dice: 0.7399 +/- 0.0067
- Object Hausdorff: 116.1194 +/- 10.7763
- Dice: 0.8713 +/- 0.0122
- IoU: 0.7859 +/- 0.0159
- HD95: 55.5429 +/- 1.4929
- Boundary F1: 0.6532 +/- 0.0101

### testB
- F1: 0.6047 +/- 0.0215
- Object Dice: 0.7721 +/- 0.0144
- Object Hausdorff: 122.1415 +/- 7.1026
- Dice: 0.8746 +/- 0.0109
- IoU: 0.7896 +/- 0.0141
- HD95: 45.5977 +/- 8.9189
- Boundary F1: 0.6364 +/- 0.0109

## Cross-Seed Failure Pattern Analysis

- seeds_analyzed: [3407, 1234, 2025]

### testA
- adhesion_split_fail: not_consistent (seed3407=0, seed1234=0, seed2025=0)
- small_gland_miss: not_consistent (seed3407=0, seed1234=0, seed2025=0)
- boundary_blur: not_consistent (seed3407=0, seed1234=0, seed2025=0)

### testB
- adhesion_split_fail: not_consistent (seed3407=0, seed1234=0, seed2025=0)
- small_gland_miss: not_consistent (seed3407=0, seed1234=0, seed2025=0)
- boundary_blur: not_consistent (seed3407=0, seed1234=0, seed2025=0)

### testB_harder
- F1: testA_mean=0.5847, testB_mean=0.6047 -> testB_not_worse
- Object Dice: testA_mean=0.7399, testB_mean=0.7721 -> testB_not_worse
- Object Hausdorff: testA_mean=116.1194, testB_mean=122.1415 -> testB_worse

## Abnormal Run Adjudication

- seed3407: stop_reason=early_stopping, best_epoch=43, epoch_count=63
- seed1234: stop_reason=early_stopping, best_epoch=49, epoch_count=69
- seed2025: stop_reason=early_stopping, best_epoch=47, epoch_count=67

