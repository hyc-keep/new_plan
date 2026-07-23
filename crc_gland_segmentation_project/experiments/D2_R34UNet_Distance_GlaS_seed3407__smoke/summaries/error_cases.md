# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `59`
- unclassified: `1`

### testB

- sample_count: `20`
- adhesion_merge: `20`

## Worst Cases

- `testA` / `GlaS_official_testA_testA_19` / `failure_type=adhesion_merge` / `objdice=0.047718` / `dice=0.686900` / `boundary_f1=0.203889` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407__smoke/visuals/testA/GlaS_official_testA_testA_19_overlay.png`
- `testA` / `GlaS_official_testA_testA_27` / `failure_type=adhesion_merge` / `objdice=0.058196` / `dice=0.709410` / `boundary_f1=0.164176` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407__smoke/visuals/testA/GlaS_official_testA_testA_27_overlay.png`
- `testA` / `GlaS_official_testA_testA_40` / `failure_type=adhesion_merge` / `objdice=0.064435` / `dice=0.666382` / `boundary_f1=0.182361` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407__smoke/visuals/testA/GlaS_official_testA_testA_40_overlay.png`
- `testA` / `GlaS_official_testA_testA_18` / `failure_type=adhesion_merge` / `objdice=0.076434` / `dice=0.570297` / `boundary_f1=0.205328` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407__smoke/visuals/testA/GlaS_official_testA_testA_18_overlay.png`
- `testA` / `GlaS_official_testA_testA_5` / `failure_type=adhesion_merge` / `objdice=0.083392` / `dice=0.737081` / `boundary_f1=0.225655` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407__smoke/visuals/testA/GlaS_official_testA_testA_5_overlay.png`
- `testA` / `GlaS_official_testA_testA_60` / `failure_type=adhesion_merge` / `objdice=0.087318` / `dice=0.554219` / `boundary_f1=0.234044` / `overlay=not_exported`
