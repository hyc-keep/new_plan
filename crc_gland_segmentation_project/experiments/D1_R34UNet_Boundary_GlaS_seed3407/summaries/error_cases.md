# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `40`
- unclassified: `17`
- fragmented_complex_region: `2`
- small_gland_miss: `1`

### testB

- sample_count: `20`
- adhesion_merge: `9`
- unclassified: `8`
- fragmented_complex_region: `1`
- boundary_over_smooth: `1`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.344806` / `dice=0.793498` / `boundary_f1=0.380350` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.415450` / `dice=0.775117` / `boundary_f1=0.381168` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.450194` / `dice=0.712252` / `boundary_f1=0.546989` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=adhesion_merge` / `objdice=0.503774` / `dice=0.839656` / `boundary_f1=0.605677` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
- `testA` / `GlaS_official_testA_testA_54` / `failure_type=adhesion_merge` / `objdice=0.590628` / `dice=0.918798` / `boundary_f1=0.746915` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_54_overlay.png`
- `testA` / `GlaS_official_testA_testA_7` / `failure_type=adhesion_merge` / `objdice=0.594621` / `dice=0.737577` / `boundary_f1=0.686827` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_7_overlay.png`
