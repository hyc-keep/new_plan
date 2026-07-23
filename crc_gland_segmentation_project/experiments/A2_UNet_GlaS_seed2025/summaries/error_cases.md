# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `48`
- unclassified: `5`
- fragmented_complex_region: `5`
- small_gland_miss: `1`
- boundary_over_smooth: `1`

### testB

- sample_count: `20`
- adhesion_merge: `10`
- unclassified: `6`
- fragmented_complex_region: `2`
- boundary_over_smooth: `1`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.312967` / `dice=0.776015` / `boundary_f1=0.381019` / `overlay=experiments/A2_UNet_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testA` / `GlaS_official_testA_testA_45` / `failure_type=adhesion_merge` / `objdice=0.383786` / `dice=0.790961` / `boundary_f1=0.329832` / `overlay=experiments/A2_UNet_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_45_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.386004` / `dice=0.730795` / `boundary_f1=0.338299` / `overlay=experiments/A2_UNet_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_9` / `failure_type=adhesion_merge` / `objdice=0.499417` / `dice=0.955031` / `boundary_f1=0.660121` / `overlay=experiments/A2_UNet_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_28` / `failure_type=adhesion_merge` / `objdice=0.505122` / `dice=0.888045` / `boundary_f1=0.616011` / `overlay=experiments/A2_UNet_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_28_overlay.png`
- `testA` / `GlaS_official_testA_testA_41` / `failure_type=adhesion_merge` / `objdice=0.536171` / `dice=0.669416` / `boundary_f1=0.392930` / `overlay=experiments/A2_UNet_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_41_overlay.png`
