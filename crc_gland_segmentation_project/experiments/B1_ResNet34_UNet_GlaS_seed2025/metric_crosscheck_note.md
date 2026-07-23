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
- `objdice`: sample_mean=`0.8427371224576777` / aggregate=`0.8427371224576777` / status=`pass`
- `dice`: sample_mean=`0.9074167969025648` / aggregate=`0.9074167969025648` / status=`pass`
- `iou`: sample_mean=`0.8403905883725332` / aggregate=`0.8403905883725333` / status=`pass`
- `f1`: sample_mean=`0.762936719808002` / aggregate=`0.7629367198080022` / status=`pass`
- `boundary_f1`: sample_mean=`0.7593630378172581` / aggregate=`0.7593630378172584` / status=`pass`
- `hd95`: sample_mean=`33.71966076294579` / aggregate=`33.71966076294579` / status=`pass`
- `object_hausdorff`: sample_mean=`65.07221497903258` / aggregate=`65.07221497903261` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.7997027863563335` / aggregate=`0.7997027863563335` / status=`pass`
- `dice`: sample_mean=`0.8828327235383029` / aggregate=`0.8828327235383029` / status=`pass`
- `iou`: sample_mean=`0.8094274307610115` / aggregate=`0.8094274307610118` / status=`pass`
- `f1`: sample_mean=`0.6888547791218069` / aggregate=`0.6888547791218069` / status=`pass`
- `boundary_f1`: sample_mean=`0.6999549008158361` / aggregate=`0.6999549008158361` / status=`pass`
- `hd95`: sample_mean=`36.65344099998471` / aggregate=`36.65344099998471` / status=`pass`
- `object_hausdorff`: sample_mean=`106.09864347577779` / aggregate=`106.09864347577778` / status=`pass`

