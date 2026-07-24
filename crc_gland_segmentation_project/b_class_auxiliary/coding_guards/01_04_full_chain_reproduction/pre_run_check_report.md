# 01-04 Full Chain Pre-run Check Report

- status: `pass`
- scope: `pre-run only / pending_not_run`
- contract: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/full_chain_contract.yaml`
- freeze_manifest: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/01_data_freeze_manifest.json`
- error_count: `0`
- warning_count: `0`

## Checked
- seven new experiment configs: identity, seed, stage, pending version/tag, and config references
- one new batch root and all seven new output directories: required to be absent and confined to the contract batch root
- current four data hashes: actual files versus contract and generated freeze manifest
- 02→03→04 seven-field lineage, 04 new-A2-manifest-only consumption, and no-rerun-A2 policy
- historical run exclusions

## Errors
- none

## Warnings
- none
