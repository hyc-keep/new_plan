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
- `objdice`: sample_mean=`0.7734403051583653` / aggregate=`0.7734403051583653` / status=`pass`
- `dice`: sample_mean=`0.8974401574610634` / aggregate=`0.8974401574610634` / status=`pass`
- `iou`: sample_mean=`0.8223175220547886` / aggregate=`0.8223175220547886` / status=`pass`
- `f1`: sample_mean=`0.6063562768262951` / aggregate=`0.6063562768262952` / status=`pass`
- `boundary_f1`: sample_mean=`0.6919474440169028` / aggregate=`0.6919474440169027` / status=`pass`
- `hd95`: sample_mean=`51.341028401056924` / aggregate=`51.34102840105691` / status=`pass`
- `object_hausdorff`: sample_mean=`102.53935950065775` / aggregate=`102.53935950065771` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.8039291753675716` / aggregate=`0.8039291753675716` / status=`pass`
- `dice`: sample_mean=`0.8922361875891378` / aggregate=`0.8922361875891378` / status=`pass`
- `iou`: sample_mean=`0.8134644820352117` / aggregate=`0.8134644820352117` / status=`pass`
- `f1`: sample_mean=`0.6271924412017291` / aggregate=`0.6271924412017291` / status=`pass`
- `boundary_f1`: sample_mean=`0.6434461816841813` / aggregate=`0.6434461816841812` / status=`pass`
- `hd95`: sample_mean=`39.37287527084349` / aggregate=`39.372875270843494` / status=`pass`
- `object_hausdorff`: sample_mean=`108.13230996115935` / aggregate=`108.13230996115935` / status=`pass`

