# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `45`
- fragmented_complex_region: `8`
- unclassified: `6`
- small_gland_miss: `1`

### testB

- sample_count: `20`
- adhesion_merge: `9`
- unclassified: `7`
- fragmented_complex_region: `2`
- boundary_over_smooth: `1`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.355251` / `dice=0.787269` / `boundary_f1=0.370856` / `overlay=experiments/A2_UNet_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.394147` / `dice=0.745888` / `boundary_f1=0.350948` / `overlay=experiments/A2_UNet_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_45` / `failure_type=adhesion_merge` / `objdice=0.399608` / `dice=0.817640` / `boundary_f1=0.398022` / `overlay=experiments/A2_UNet_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_45_overlay.png`
- `testA` / `GlaS_official_testA_testA_24` / `failure_type=adhesion_merge` / `objdice=0.437418` / `dice=0.765849` / `boundary_f1=0.523172` / `overlay=experiments/A2_UNet_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_24_overlay.png`
- `testA` / `GlaS_official_testA_testA_9` / `failure_type=adhesion_merge` / `objdice=0.456714` / `dice=0.952651` / `boundary_f1=0.684308` / `overlay=experiments/A2_UNet_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_7` / `failure_type=adhesion_merge` / `objdice=0.461561` / `dice=0.702313` / `boundary_f1=0.593741` / `overlay=experiments/A2_UNet_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_7_overlay.png`
