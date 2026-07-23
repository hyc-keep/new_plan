# Metric Crosscheck Note

- crosscheck_scope: `python_reaggregation_from_split_csv`
- official_reference_type: `project_internal_reaggregation_sanity_check`
- threshold_source: `val17`
- threshold_value: `0.5`
- metric_crosscheck_result: `pass`
- boundary_metric_width: `3`
- boundary_metric_impl: `binary_erosion_xor_plus_binary_dilation`
- connected_components_connectivity: `8`

## Split Checks

### testA

- sample_count: `60`
- sampled_ids: `GlaS_official_testA_testA_1, GlaS_official_testA_testA_10, GlaS_official_testA_testA_11, GlaS_official_testA_testA_12, GlaS_official_testA_testA_13`
- `objdice`: sample_mean=`0.850540284503769` / aggregate=`0.850540284503769` / status=`pass`
- `dice`: sample_mean=`0.9159254308796231` / aggregate=`0.9159254308796232` / status=`pass`
- `iou`: sample_mean=`0.851011436141276` / aggregate=`0.8510114361412757` / status=`pass`
- `f1`: sample_mean=`0.7582346505105299` / aggregate=`0.7582346505105302` / status=`pass`
- `boundary_f1`: sample_mean=`0.7645653782493038` / aggregate=`0.7645653782493039` / status=`pass`
- `hd95`: sample_mean=`33.94424016793566` / aggregate=`33.94424016793566` / status=`pass`
- `object_hausdorff`: sample_mean=`61.271981435855444` / aggregate=`61.27198143585543` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.8376465149077352` / aggregate=`0.8376465149077352` / status=`pass`
- `dice`: sample_mean=`0.9126559940506557` / aggregate=`0.9126559940506557` / status=`pass`
- `iou`: sample_mean=`0.8491225636636871` / aggregate=`0.8491225636636871` / status=`pass`
- `f1`: sample_mean=`0.6789693420614474` / aggregate=`0.6789693420614473` / status=`pass`
- `boundary_f1`: sample_mean=`0.7088303026263325` / aggregate=`0.7088303026263324` / status=`pass`
- `hd95`: sample_mean=`27.444045867919925` / aggregate=`27.444045867919925` / status=`pass`
- `object_hausdorff`: sample_mean=`90.9174377867993` / aggregate=`90.9174377867993` / status=`pass`

