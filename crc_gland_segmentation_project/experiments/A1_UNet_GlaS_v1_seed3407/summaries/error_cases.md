# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `47`
- fragmented_complex_region: `11`
- boundary_over_smooth: `2`

### testB

- sample_count: `20`
- adhesion_merge: `10`
- fragmented_complex_region: `4`
- unclassified: `4`
- boundary_over_smooth: `1`
- small_gland_miss: `1`

## Worst Cases

- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.273686` / `dice=0.669900` / `boundary_f1=0.349407` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_21` / `failure_type=adhesion_merge` / `objdice=0.351755` / `dice=0.757998` / `boundary_f1=0.458454` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_21_overlay.png`
- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.352294` / `dice=0.792478` / `boundary_f1=0.372728` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testA` / `GlaS_official_testA_testA_45` / `failure_type=adhesion_merge` / `objdice=0.355631` / `dice=0.750064` / `boundary_f1=0.275240` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_45_overlay.png`
- `testA` / `GlaS_official_testA_testA_5` / `failure_type=adhesion_merge` / `objdice=0.380649` / `dice=0.467712` / `boundary_f1=0.366856` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_5_overlay.png`
- `testA` / `GlaS_official_testA_testA_43` / `failure_type=adhesion_merge` / `objdice=0.395831` / `dice=0.931240` / `boundary_f1=0.690995` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_43_overlay.png`
