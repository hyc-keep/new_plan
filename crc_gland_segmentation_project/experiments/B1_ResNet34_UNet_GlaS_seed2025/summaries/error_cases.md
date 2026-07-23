# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `39`
- unclassified: `17`
- fragmented_complex_region: `3`
- small_gland_miss: `1`

### testB

- sample_count: `20`
- unclassified: `9`
- adhesion_merge: `8`
- fragmented_complex_region: `1`
- boundary_over_smooth: `1`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.280266` / `dice=0.751445` / `boundary_f1=0.341553` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.377788` / `dice=0.728027` / `boundary_f1=0.359699` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.471837` / `dice=0.464344` / `boundary_f1=0.429480` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testB` / `GlaS_official_testB_testB_14` / `failure_type=boundary_over_smooth` / `objdice=0.507222` / `dice=0.581168` / `boundary_f1=0.332846` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_14_overlay.png`
- `testA` / `GlaS_official_testA_testA_21` / `failure_type=adhesion_merge` / `objdice=0.560684` / `dice=0.738573` / `boundary_f1=0.587403` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_21_overlay.png`
- `testB` / `GlaS_official_testB_testB_4` / `failure_type=adhesion_merge` / `objdice=0.568721` / `dice=0.568755` / `boundary_f1=0.555637` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_4_overlay.png`
