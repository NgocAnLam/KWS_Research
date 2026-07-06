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

**Promotion criteria for secondary methods (multi-metric):**

| Condition | Action |
|---|---|
| ΔAccuracy ≤ 3% **or** ΔEER ≤ 2% | Promote (run 2 additional seeds) |
| Acc@1%FAR improves by ≥ 2% | Promote |
| Latency decreases ≥ 20% with comparable accuracy | Promote |
| None of the above | Not promoted |

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
| `ranking.csv` | Ranked configurations. **Primary ranking metric:** Acc@1%FAR. Secondary: Latency. Tertiary: Params. No weighted composite score used. |

---

## 2. Configuration

| Parameter | Value |
|---|---|
| Dataset | GSCv2 (84,843 train / 11,005 test), checksum verified |
| Primary metric | **Acc@1%FAR** (Acc@5%FAR secondary, Accuracy tertiary) |
| Backbone | BC-ResNet-32 (111K params) |
| Embedding dim | 64 |
| Episode | 5-way, 5-shot, 5-query |
| Training episodes | 1,000 per epoch |
| Evaluation episodes | 600 |
| Epochs | 40 |
| Optimizer | Adam (lr=1e-3, wd=4e-5) |
| Scheduler | Cosine annealing |
| Seed verification | ✅ Deterministic

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

| Comparison | ΔAccuracy | ΔEER | ΔLatency | Cohen's d | Conclusion |
|---|---|---|---|---|---|
| PCEN vs Log-Mel (ProtoNet) | | | | | |
| GE2E vs ProtoNet (LogMel) | | | | | |
| Triplet vs ProtoNet (LogMel) | | | | | |

---

## 4. Statistical Analysis

With n=3 seeds, hypothesis testing (e.g., paired t-test) has insufficient power. Analysis is therefore primarily descriptive:

| Metric | Method | Details |
|---|---|---|
| Primary cells | Mean ± std | ProtoNet × {LogMel, PCEN} across 3 seeds |
| 95% CI | Bootstrap (n=1000 resamples) | Reported for Accuracy, F1, EER |
| Effect size | Cohen's d | Reported for comparisons with d ≥ 0.2 (small), ≥ 0.5 (medium), ≥ 0.8 (large) |
| Secondary cells | Descriptive only | GE2E / Triplet with 1 seed — no statistical inference |

Effect size interpretation: Cohen's d = |μ₁ − μ₂| / σ_pooled. Reported for PCEN vs Log-Mel and each secondary vs ProtoNet.

---

## 5. Decision Impact

| Decision ID | Decision | Before EXP001 | After EXP001 | Evidence | Action |
|---|---|---|---|---|---|---|
| D01 | Log-Mel → Primary feature | Log-Mel = primary | | | |
| D02 | PCEN → Ablation | PCEN = ablation | | | |
| D04 | ProtoNet → Primary baseline | ProtoNet = primary | | | |
| D05 | GE2E → Secondary | GE2E = secondary | | | |
| D06 | Triplet → Secondary | Triplet = secondary | | | |

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
- **Statistical:** Only 3 seeds for primary cells (n=3 limits hypothesis testing); GE2E/Triplet only 1 seed; promotion criteria are heuristic

---

## 8. Next Steps

- [ ] Update `decisions_log.md` if any decisions changed
- [ ] Update `claims/` with experimental evidence
- [ ] Proceed to EXP002 (shot number) or EXP003 (training strategy)
