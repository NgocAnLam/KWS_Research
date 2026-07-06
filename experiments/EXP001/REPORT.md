# EXP001 Report

> **Experiment:** Feature × Metric Learning (2×3 Factorial Design)
> **Design baseline:** `research-design-v2.0`
> **Date:** YYYY-MM-DD
> **Status:** Draft

---

## 1. Objective

Validate the interaction between audio feature extraction and metric learning loss functions for user-defined few-shot keyword spotting.

### Research Questions

| RQ | Question | Hypothesis |
|---|---|---|
| RQ1 | How do Log-Mel vs PCEN affect FS-KWS accuracy? | PCEN improves accuracy at fixed FAR |
| RQ2 | How do ProtoNet vs GE2E vs Triplet compare? | GE2E may outperform; no direct evidence |

### Experimental Design

ProtoNet is the primary metric-learning approach investigated in this study. Therefore, all ProtoNet experiments are repeated with three independent random seeds to enable statistical analysis. GE2E and Triplet are included as secondary baselines for qualitative comparison and are executed with a single seed to reduce computational cost. If a secondary method demonstrates promising performance, it will be promoted to a primary method and evaluated with three seeds in a follow-up experiment.

**Promotion criteria for secondary methods:**

| Secondary result vs ProtoNet | Action |
|---|---|
| Clearly worse (ΔAccuracy > 5% gap) | Not promoted |
| Comparable (ΔAccuracy < 3% gap) | Run 2 additional seeds |
| Clearly better (ΔAccuracy > 3% lead) | Promote to primary, evaluate fully |

### Design

| Feature | Loss | Seeds | Role |
|---|---|---|---|
| Log-Mel | ProtoNet | 42, 43, 44 | Primary |
| Log-Mel | GE2E | 42 | Secondary |
| Log-Mel | Triplet | 42 | Secondary |
| Log-Mel+PCEN | ProtoNet | 42, 43, 44 | Primary |
| Log-Mel+PCEN | GE2E | 42 | Secondary |
| Log-Mel+PCEN | Triplet | 42 | Secondary |

**Total: 10 cells** (6 primary + 4 secondary)

### Machine-readable results

| File | Contents |
|---|---|
| `summary.csv` | All 10 cells: Feature, Loss, Seed, Accuracy, F1, EER, Acc@1%FAR, Acc@5%FAR, Params, Latency |
| `ranking.csv` | Ranked configurations by composite score |

---

## 2. Configuration

| Parameter | Value |
|---|---|
| Dataset | GSCv2 (84,843 train / 11,005 test) |
| Backbone | BC-ResNet-32 (111K params) |
| Embedding dim | 64 |
| Episode | 5-way, 5-shot, 5-query |
| Training episodes | 1,000 per epoch |
| Evaluation episodes | 600 |
| Epochs | 40 |
| Optimizer | Adam (lr=1e-3, wd=4e-5) |
| Scheduler | Cosine annealing |
| Seed verification | ✅ Deterministic |

---

## 3. Results

### 3.1. Primary Cells (mean ± std, n=3)

| Feature | Loss | Accuracy | F1 | AUC | EER | Acc@1%FAR | Acc@5%FAR | Latency (ms) |
|---|---|---|---|---|---|---|---|---|
| LogMel | ProtoNet | | | | | | | |
| PCEN | ProtoNet | | | | | | | |

### 3.2. Secondary Cells (1 seed)

| Feature | Loss | Accuracy | F1 | AUC | EER | Acc@1%FAR | Acc@5%FAR | Latency (ms) |
|---|---|---|---|---|---|---|---|---|
| LogMel | GE2E | | | | | | | |
| LogMel | Triplet | | | | | | | |
| PCEN | GE2E | | | | | | | |
| PCEN | Triplet | | | | | | | |

### 3.3. Comparison Summary

| Comparison | ΔAccuracy | ΔEER | ΔLatency | Effect Size | Conclusion |
|---|---|---|---|---|---|
| PCEN vs Log-Mel (ProtoNet) | | | | | |
| GE2E vs ProtoNet (LogMel) | | | | | |
| Triplet vs ProtoNet (LogMel) | | | | | |

---

## 4. Statistical Analysis

| Test | Value | Significance |
|---|---|---|
| ProtoNet: LogMel vs PCEN (paired t-test) | | |
| GE2E vs ProtoNet (LogMel, 1 seed — descriptive) | | |
| 95% CI width (ProtoNet cells) | | |

---

## 5. Decision Impact

| Decision ID | Decision | Impact | Action |
|---|---|---|---|
| D01 | Log-Mel → Primary feature | | |
| D02 | PCEN → Ablation | | |
| D04 | ProtoNet → Primary baseline | | |
| D05 | GE2E → Secondary | | |
| D06 | Triplet → Secondary | | |

---

## 6. Claim Update

| Claim ID | Claim | Previous Status | New Status | Evidence |
|---|---|---|---|---|
| C05 | ProtoNet provides competitive performance | Hypothesis | | |
| C06 | PCEN improves noise robustness | Hypothesis | | |

---

## 7. Threats to Validity

- **Internal:** Speaker overlap between seen/unseen in GSCv2 training split
- **External:** Results may not generalize to Vietnamese (different phonology)
- **Construct:** Episode-based eval approximates but doesn't match enrollment workflow

---

## 8. Next Steps

- [ ] Update `decisions_log.md` if any decisions changed
- [ ] Update `claims/` with experimental evidence
- [ ] Proceed to EXP002 (shot number) or EXP003 (training strategy)
