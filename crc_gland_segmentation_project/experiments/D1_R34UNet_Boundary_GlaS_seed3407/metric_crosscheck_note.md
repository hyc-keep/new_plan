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
- `objdice`: sample_mean=`0.8329379735907058` / aggregate=`0.832937973590706` / status=`pass`
- `dice`: sample_mean=`0.9161331631227635` / aggregate=`0.9161331631227633` / status=`pass`
- `iou`: sample_mean=`0.8517868628562385` / aggregate=`0.8517868628562388` / status=`pass`
- `f1`: sample_mean=`0.7779276335830583` / aggregate=`0.7779276335830586` / status=`pass`
- `boundary_f1`: sample_mean=`0.7629326910921761` / aggregate=`0.762932691092176` / status=`pass`
- `hd95`: sample_mean=`33.57921883900959` / aggregate=`33.5792188390096` / status=`pass`
- `object_hausdorff`: sample_mean=`71.18705662453529` / aggregate=`71.18705662453527` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.8346237987143634` / aggregate=`0.8346237987143634` / status=`pass`
- `dice`: sample_mean=`0.9201043980255541` / aggregate=`0.9201043980255539` / status=`pass`
- `iou`: sample_mean=`0.8591669699060474` / aggregate=`0.8591669699060474` / status=`pass`
- `f1`: sample_mean=`0.7261451611683809` / aggregate=`0.7261451611683809` / status=`pass`
- `boundary_f1`: sample_mean=`0.7074398140363588` / aggregate=`0.7074398140363586` / status=`pass`
- `hd95`: sample_mean=`27.428104624748197` / aggregate=`27.428104624748197` / status=`pass`
- `object_hausdorff`: sample_mean=`98.11409352674322` / aggregate=`98.11409352674323` / status=`pass`

