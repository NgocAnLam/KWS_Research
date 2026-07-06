# Research Questions

> **Mục đích:** Mapping từng Research Question (RQ) → Evidence → Decision → Experiment.
>
> Mỗi RQ được định nghĩa trong `summary_project.md` (§18). File này trace kết nối giữa RQ, evidence, decision và experiment tương ứng.

---

## RQ1 — Feature Extraction × Metric Learning

> **How do different combinations of Audio Feature Extraction and Metric Learning strategies affect User-defined Few-shot Keyword Spotting performance?**

| Khoản mục | Link |
|---|---|
| **Hypothesis** | H1 — Feature × Method Interaction (§17) |
| **Evidence** | `evidence/feature_extraction.md`, `evidence/proto_vs_ge2e.md` |
| **Trend** | `community_trends_2024_2026.md` §2, §3 |
| **Decision** | `decisions_log.md` #1–#6 |
| **Design section** | `summary_project.md` §10 Feature Extraction, §12 Metric Learning |
| **Experiment ID** | EXP001 — Factorial Design 2 × 4 |
| **Metrics** | Accuracy, F1, EER, acc@1% FAR, acc@5% FAR |

### Experiment Design

```
Feature:  [Log-Mel, PCEN]
Metric:   [ProtoNet (3 seeds), GE2E (1 seed), Triplet (1 seed), Siamese (1 seed)]
Total:    2 × 4 = 8 cells, 6 primary + 2 secondary
Backbone: BC-ResNet-32 (fixed)
Eval:     Episode-based 5-way 5-shot
```

---

## RQ2 — Shot Number

> **Số lượng enrollment samples (1, 3, 5-shot) ảnh hưởng như thế nào đến hiệu năng nhận diện?**

| Khoản mục | Link |
|---|---|
| **Hypothesis** | H2 — Shot Impact (§17) |
| **Evidence** | `evidence/proto_vs_ge2e.md` |
| **Decision** | `decisions_log.md` #4 |
| **Experiment ID** | EXP002 |
| **Metrics** | Accuracy, EER |

### Experiment Design

```
Config:   Best from RQ1
Shots:    [1, 3, 5]
Eval:     Episode-based 5-way K-shot
Seeds:    3
```

---

## RQ3 — Edge Deployment Trade-off

> **What is the trade-off between latency, memory footprint, and recognition accuracy when deploying the proposed framework on Raspberry Pi 4?**

| Khoản mục | Link |
|---|---|
| **Hypothesis** | H3 — Edge Feasibility (§17) |
| **Evidence** | `evidence/backbone_models.md`, `evidence/deployment.md` |
| **Decision** | `decisions_log.md` #7–#8, #11–#12 |
| **Experiment ID** | EXP003 |
| **Metrics** | Latency, Model Size, Memory, Accuracy before/after INT8, RTF |

### Experiment Design

```
Device:   Raspberry Pi 4 Model B (4GB)
Framework: TFLite INT8
Models:   BC-ResNet-32 (primary), DS-CNN (baseline)
Eval:     Per-inference latency + streaming (FA/hour, RTF)
```

---

## Ablations

| Ablation | Evidence | Decision | Experiment ID |
|---|---|---|---|
| Training Strategy (Scratch vs FT vs Freeze) | `evidence/proto_vs_ge2e.md` | `decisions_log.md` #4–#6 | EXP004 |
| Data Augmentation (Phase 2) | `evidence/feature_extraction.md` | — | EXP005 |
| Prototype Method (Mean vs Median) | — | `decisions_log.md` #10 | EXP006 |
| Knowledge Distillation (optional) | `evidence/deployment.md` | `decisions_log.md` #14 | EXP007 |

---

## Full Traceability Map

```text
RQ1 ──→ evidence/feature_extraction.md ──→ EXP001
  │         │
  │         └── evidence/proto_vs_ge2e.md
  │
  ├──→ decisions_log.md (#1–#6)
  │
  └──→ summary_project.md (§10, §12)

RQ2 ──→ evidence/proto_vs_ge2e.md ──→ EXP002
  │
  ├──→ decisions_log.md (#4)
  │
  └──→ summary_project.md (§14, §15)

RQ3 ──→ evidence/backbone_models.md ──→ EXP003
  │         │
  │         └── evidence/deployment.md
  │
  ├──→ decisions_log.md (#7–#8, #11–#12)
  │
  └──→ summary_project.md (§20)
```
