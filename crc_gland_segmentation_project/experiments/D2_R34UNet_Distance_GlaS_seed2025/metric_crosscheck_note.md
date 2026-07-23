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
- `objdice`: sample_mean=`0.8180253640686926` / aggregate=`0.8180253640686928` / status=`pass`
- `dice`: sample_mean=`0.909458128317003` / aggregate=`0.9094581283170029` / status=`pass`
- `iou`: sample_mean=`0.8411606275435805` / aggregate=`0.8411606275435805` / status=`pass`
- `f1`: sample_mean=`0.744299086778737` / aggregate=`0.744299086778737` / status=`pass`
- `boundary_f1`: sample_mean=`0.7569685093658918` / aggregate=`0.7569685093658918` / status=`pass`
- `hd95`: sample_mean=`39.502018922964716` / aggregate=`39.502018922964716` / status=`pass`
- `object_hausdorff`: sample_mean=`83.21937875849287` / aggregate=`83.2193787584929` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.8295660218362964` / aggregate=`0.8295660218362965` / status=`pass`
- `dice`: sample_mean=`0.9227721379016527` / aggregate=`0.9227721379016527` / status=`pass`
- `iou`: sample_mean=`0.8644049202066675` / aggregate=`0.8644049202066675` / status=`pass`
- `f1`: sample_mean=`0.7214786602286601` / aggregate=`0.7214786602286601` / status=`pass`
- `boundary_f1`: sample_mean=`0.7196367803585112` / aggregate=`0.7196367803585112` / status=`pass`
- `hd95`: sample_mean=`25.65455338001251` / aggregate=`25.654553380012505` / status=`pass`
- `object_hausdorff`: sample_mean=`90.40675429510087` / aggregate=`90.40675429510088` / status=`pass`

