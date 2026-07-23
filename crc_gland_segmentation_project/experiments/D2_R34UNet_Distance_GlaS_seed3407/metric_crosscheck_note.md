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
- `objdice`: sample_mean=`0.8529445991431764` / aggregate=`0.8529445991431763` / status=`pass`
- `dice`: sample_mean=`0.9156158431928941` / aggregate=`0.9156158431928941` / status=`pass`
- `iou`: sample_mean=`0.8518542876826681` / aggregate=`0.8518542876826681` / status=`pass`
- `f1`: sample_mean=`0.7701528514456248` / aggregate=`0.7701528514456252` / status=`pass`
- `boundary_f1`: sample_mean=`0.7671826543069213` / aggregate=`0.7671826543069213` / status=`pass`
- `hd95`: sample_mean=`31.988658347129807` / aggregate=`31.988658347129807` / status=`pass`
- `object_hausdorff`: sample_mean=`59.972286172371696` / aggregate=`59.972286172371696` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.8509274203377448` / aggregate=`0.8509274203377449` / status=`pass`
- `dice`: sample_mean=`0.921399646318546` / aggregate=`0.921399646318546` / status=`pass`
- `iou`: sample_mean=`0.8625357930339794` / aggregate=`0.8625357930339794` / status=`pass`
- `f1`: sample_mean=`0.7309094818150546` / aggregate=`0.7309094818150546` / status=`pass`
- `boundary_f1`: sample_mean=`0.7219223670607018` / aggregate=`0.7219223670607018` / status=`pass`
- `hd95`: sample_mean=`25.906810870170585` / aggregate=`25.906810870170585` / status=`pass`
- `object_hausdorff`: sample_mean=`82.9933188195697` / aggregate=`82.9933188195697` / status=`pass`

