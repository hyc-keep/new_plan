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
- `objdice`: sample_mean=`0.6949207519755126` / aggregate=`0.6949207519755126` / status=`pass`
- `dice`: sample_mean=`0.85828785593138` / aggregate=`0.8582878559313802` / status=`pass`
- `iou`: sample_mean=`0.7652133719067941` / aggregate=`0.7652133719067942` / status=`pass`
- `f1`: sample_mean=`0.43558855195420654` / aggregate=`0.4355885519542065` / status=`pass`
- `boundary_f1`: sample_mean=`0.6012487784110163` / aggregate=`0.6012487784110164` / status=`pass`
- `hd95`: sample_mean=`61.64207582155861` / aggregate=`61.64207582155862` / status=`pass`
- `object_hausdorff`: sample_mean=`129.07928694846166` / aggregate=`129.07928694846163` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.7509516344136339` / aggregate=`0.750951634413634` / status=`pass`
- `dice`: sample_mean=`0.8715500123086111` / aggregate=`0.8715500123086113` / status=`pass`
- `iou`: sample_mean=`0.781431892367164` / aggregate=`0.781431892367164` / status=`pass`
- `f1`: sample_mean=`0.44974882067051264` / aggregate=`0.4497488206705126` / status=`pass`
- `boundary_f1`: sample_mean=`0.5908166123238467` / aggregate=`0.5908166123238467` / status=`pass`
- `hd95`: sample_mean=`42.18943420410153` / aggregate=`42.18943420410153` / status=`pass`
- `object_hausdorff`: sample_mean=`132.73784589526073` / aggregate=`132.7378458952607` / status=`pass`

