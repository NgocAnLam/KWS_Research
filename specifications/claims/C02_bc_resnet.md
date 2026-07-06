# C02: BC-ResNet-32 offers best accuracy/size trade-off

> **Phát biểu:** Among lightweight backbones suitable for edge deployment, BC-ResNet-32 offers the best balance between accuracy (98.7% on GSCv2) and model size (~110K params).

| Field | Link |
|---|---|
| **Evidence** | `evidence/backbone_models.md` |
| **Decision** | `decisions_log.md` #7 |
| **Experiment** | (SLR — confirmed by EdgeSpot 2026) |
| **Status** | **Literature-supported** |

## Supporting Evidence

- BC-ResNet (Kim 2021): 98.7% GSCv2, 110K params
- EdgeSpot (Buyuksolak 2026): Uses BC-ResNet variant, 128K params, 82% @1% FAR
- DS-CNN (Zhang 2017): 95.4%, 20-80K params (baseline)

## Impact on Project

- BC-ResNet-32 selected as primary backbone in `summary_project.md` §11
