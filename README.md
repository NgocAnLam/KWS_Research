# KWS_Research

**A Modular Research Framework and Evaluation Protocol for User-defined Vietnamese Few-shot Keyword Spotting on Edge Devices**

## Project Structure

```
KWS_Research/
│
├── docs/                 # Single Source of Truth (quyết định đã chốt)
├── specifications/       # Working documents, draft, TODO (living document)
├── knowledge/            # Kiến thức tổng hợp từ SLR
├── papers/              # PDF + notes + BibTeX
│
├── notebooks/           # EDA, visualization, exploratory analysis
├── src/                 # Source code
├── tests/
├── experiments/         # Logs, checkpoints, metrics, plots
├── assets/             # Figures, diagrams, images
├── templates/          # Templates for reviews, experiments, decisions
│
├── thesis/             # Luận văn
├── paper/              # Conference/Journal manuscript
│
├── Makefile
├── .gitignore
└── README.md
```

## Quick Start

```bash
make setup    # Install dependencies
make test     # Run tests
make run      # Run experiment
```

## Documentation

See [docs/index.md](docs/index.md) for full research documentation.

## License

Creative Commons Attribution 4.0 International
