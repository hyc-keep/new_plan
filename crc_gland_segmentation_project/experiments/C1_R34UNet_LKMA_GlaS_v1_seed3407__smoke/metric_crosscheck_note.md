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

- sample_count: `2`
- sampled_ids: `GlaS_official_testA_testA_1, GlaS_official_testA_testA_10`
- `objdice`: sample_mean=`0.0` / aggregate=`0.0` / status=`pass`
- `dice`: sample_mean=`5.9476608529959446e-12` / aggregate=`5.9476608529959446e-12` / status=`pass`
- `iou`: sample_mean=`5.9476608529959446e-12` / aggregate=`5.9476608529959446e-12` / status=`pass`
- `f1`: sample_mean=`0.0` / aggregate=`0.0` / status=`pass`
- `boundary_f1`: sample_mean=`0.0` / aggregate=`0.0` / status=`pass`
- `hd95`: sample_mean=`nan` / aggregate=`nan` / status=`pass`
- `object_hausdorff`: sample_mean=`nan` / aggregate=`nan` / status=`pass`

### testB

- sample_count: `2`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10`
- `objdice`: sample_mean=`0.0` / aggregate=`0.0` / status=`pass`
- `dice`: sample_mean=`8.254672982240481e-12` / aggregate=`8.254672982240481e-12` / status=`pass`
- `iou`: sample_mean=`8.254672982240481e-12` / aggregate=`8.254672982240481e-12` / status=`pass`
- `f1`: sample_mean=`0.0` / aggregate=`0.0` / status=`pass`
- `boundary_f1`: sample_mean=`0.0` / aggregate=`0.0` / status=`pass`
- `hd95`: sample_mean=`nan` / aggregate=`nan` / status=`pass`
- `object_hausdorff`: sample_mean=`nan` / aggregate=`nan` / status=`pass`

