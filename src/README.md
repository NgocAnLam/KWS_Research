# KWS Research Framework

> **Experimental pipeline for User-defined Vietnamese Few-shot Keyword Spotting.**
> Design baseline: `research-design-v2.0`

## Architecture

```text
src/
├── kws_framework/
│   ├── dataset/          # GSCv2 loader, episode generator
│   ├── features/         # Log-Mel, PCEN feature extraction
│   ├── models/           # BC-ResNet-32, DS-CNN backbones
│   ├── losses/           # ProtoNet, GE2E, Triplet (unified interface)
│   │   └── base.py       # BaseLoss interface
│   └── trainer/
│       ├── trainer.py    # Training loop
│       └── evaluator.py  # Evaluation + metrics
├── configs/
│   ├── exp001.yaml       # 2×3 factorial config
│   └── defaults.yaml     # Shared defaults
└── scripts/
    ├── run_experiment.py # Single experiment
    └── run_grid.py       # Full factorial grid
```

## Experiment Design (EXP001)

| Feature | Loss |
|---|---|
| Log-Mel | ProtoNet |
| Log-Mel | GE2E |
| Log-Mel | Triplet |
| Log-Mel + PCEN | ProtoNet |
| Log-Mel + PCEN | GE2E |
| Log-Mel + PCEN | Triplet |

Fixed: BC-ResNet-32, GSCv2, 64-D embedding, 3 seeds.
