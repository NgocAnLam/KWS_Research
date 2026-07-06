# Evidence: Metric Learning Methods

> **Research Question:** Which metric learning method (ProtoNet, GE2E, Triplet/SCAF) has the strongest evidence for user-defined few-shot keyword spotting?
> **Nguồn:** 50 papers surveyed, 20+ metric-learning-specific papers analyzed
> **Last updated:** 2026-07-06 (post-SLR consolidation)

---

## 1. Method Usage in Papers

| Method | Papers (n) | FS-KWS Edge Papers | SOTA Claim |
|---|---|---|---|
| **Prototypical Networks** | 7 | Rusci 2023, Yang 2023 | Baseline |
| **Triplet Loss** | 4 | Rusci 2023, Vygon 2021 | Outperformed by GE2E |
| **GE2E Loss** | 2 | **GE2E-KWS 2024** | **Best: +60.7% AUC over triplet** |
| **Sub-center ArcFace (SCAF)** | 2 | EdgeSpot 2026, Gok 2025 | Best for open-set |
| **InfoNCE (Contrastive)** | 3 | Xi 2024 (CLAD), Li 2025 (PLCL) | SOTA for phoneme-level |
| **Circle Loss** | 1 | Reuter 2023 | Moderate |

---

## 2. Key Comparison: GE2E vs ProtoNet

| Comparison | Evidence | Verdict |
|---|---|---|
| **GE2E > Triplet** | GE2E-KWS 2024: +60.7% AUC | ✅ Confirmed |
| **GE2E vs ProtoNet** | **No direct comparison in any paper** | ❌ Unknown |
| **Triplet > ProtoNet** | Rusci 2023 (open-set only) | 🟡 Context-dependent |
| **SCAF > ProtoNet** | EdgeSpot 2026, Gok 2025 (different setting) | 🟡 Not directly comparable |

**Critical gap:** No paper has compared GE2E vs ProtoNet in the same setting (same backbone, same dataset, same shot). Until this comparison exists, ProtoNet remains a valid baseline.

---

## 3. Open-Set Methods

| Method | Papers | FAR Control | Edge Ready |
|---|---|---|---|
| **Dummy prototypes** | Kim 2022 | ✅ | ✅ |
| **Triplet + normalized** | Rusci 2023 | ✅ | ✅ |
| **Sub-center ArcFace** | EdgeSpot 2026, Gok 2025 | ✅ (best) | ✅ |
| **Cosine + threshold** | Parnami 2022 | ✅ | ✅ |

---

## 4. Contradictory Evidence

- GE2E > Triplet (Zhu 2024) **≠** GE2E > ProtoNet.
- Rusci 2023: Triplet > ProtoNet for open-set **but not necessarily for closed-set**.
- ProtoNet usage is **declining** (0 papers 2024-2026) but **not invalidated**.

## 5. Impact on Our Project

| Decision | Evidence | Confidence |
|---|---|---|
| **ProtoNet = primary baseline** | Valid for audio enrollment; declining but not invalidated | Strong |
| **GE2E = secondary ablation** | Strongest loss in literature but no ProtoNet comparison | Moderate |
| **Triplet = secondary** | Valid for open-set (Rusci 2023) | Strong |
| **No method replacement needed** | Insufficient evidence to overturn current design | Strong |
