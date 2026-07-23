# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `36`
- unclassified: `22`
- small_gland_miss: `1`
- fragmented_complex_region: `1`

### testB

- sample_count: `20`
- unclassified: `9`
- adhesion_merge: `7`
- small_gland_miss: `2`
- fragmented_complex_region: `1`
- boundary_over_smooth: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.260044` / `dice=0.735818` / `boundary_f1=0.352518` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.363748` / `dice=0.723268` / `boundary_f1=0.361831` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.469770` / `dice=0.710499` / `boundary_f1=0.542524` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testB` / `GlaS_official_testB_testB_14` / `failure_type=boundary_over_smooth` / `objdice=0.555277` / `dice=0.644189` / `boundary_f1=0.321576` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_14_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=adhesion_merge` / `objdice=0.660851` / `dice=0.824115` / `boundary_f1=0.572096` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
- `testA` / `GlaS_official_testA_testA_15` / `failure_type=unclassified` / `objdice=0.660973` / `dice=0.659339` / `boundary_f1=0.537477` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_15_overlay.png`
