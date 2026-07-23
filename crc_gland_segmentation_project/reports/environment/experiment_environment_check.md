# Experiment Environment Check

- project_root: `/home/featurize/work/Paper/crc_gland_segmentation_project`
- python: `/environment/miniconda3/bin/python`
- environment_status: `pass`

## Packages

| Distribution | Import | Required | Installed | Import status |
| --- | --- | --- | --- | --- |
| `torch` | `torch` | `2.2.2` | `2.2.2` | `pass` |
| `numpy` | `numpy` | `1.26.4` | `1.26.4` | `pass` |
| `scipy` | `scipy` | `1.17.1` | `1.17.1` | `pass` |
| `Pillow` | `PIL` | `10.3.0` | `10.3.0` | `pass` |
| `PyYAML` | `yaml` | `installed` | `6.0.1` | `pass` |

## Installation

```bash
/environment/miniconda3/bin/python -m pip install -r requirements.txt
```

- The training and testing entrypoints run this check before importing the project model/evaluation chain.
- A blocked check must be fixed before any formal training, testing, or runtime evidence run.
