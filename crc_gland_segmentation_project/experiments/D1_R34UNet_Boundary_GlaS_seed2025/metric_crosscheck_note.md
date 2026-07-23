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
- `objdice`: sample_mean=`0.8331047307998272` / aggregate=`0.8331047307998273` / status=`pass`
- `dice`: sample_mean=`0.9234309603442309` / aggregate=`0.9234309603442308` / status=`pass`
- `iou`: sample_mean=`0.8624261064772897` / aggregate=`0.8624261064772897` / status=`pass`
- `f1`: sample_mean=`0.7476770996937656` / aggregate=`0.747677099693766` / status=`pass`
- `boundary_f1`: sample_mean=`0.7646210208677673` / aggregate=`0.7646210208677673` / status=`pass`
- `hd95`: sample_mean=`32.39851258039473` / aggregate=`32.39851258039473` / status=`pass`
- `object_hausdorff`: sample_mean=`72.40085241515898` / aggregate=`72.400852415159` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.8205782955832891` / aggregate=`0.8205782955832891` / status=`pass`
- `dice`: sample_mean=`0.9183217235130112` / aggregate=`0.918321723513011` / status=`pass`
- `iou`: sample_mean=`0.8565048172123696` / aggregate=`0.8565048172123696` / status=`pass`
- `f1`: sample_mean=`0.6795354645354645` / aggregate=`0.6795354645354645` / status=`pass`
- `boundary_f1`: sample_mean=`0.7111817915337907` / aggregate=`0.7111817915337907` / status=`pass`
- `hd95`: sample_mean=`27.07495685100555` / aggregate=`27.07495685100555` / status=`pass`
- `object_hausdorff`: sample_mean=`100.26717933541968` / aggregate=`100.26717933541966` / status=`pass`

