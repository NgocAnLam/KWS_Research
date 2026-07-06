# SLR Progress Notes

> **Working document cho Systematic Literature Review**
> Cập nhật: 2026-07-06

---

## Daily Log

| Date | Activity | Papers found | Papers read | Notes |
|---|---|---|---|---|
| 2026-07-06 | Search + read all databases | 20+ | 13 | Completed initial SLR across all 8 categories |

---

## Search Results Summary

| Source | Queries | Results | Screened | Read |
|---|---|---|---|---|
| arXiv | 10+ queries | 50+ | 20 | 13 |
| IEEE Xplore (via search) | 5 queries | — | 5 | 0 (need DOI for access) |

## Papers Read (Completed)

| ID | Title | Quality Score | Relevance |
|---|---|---|---|
| P1 | EdgeSpot (Buyuksolak 2026) | 9/10 | ★★★★★ |
| P2 | GE2E-KWS (Zhu 2024) | 8/10 | ★★★★★ |
| P3 | BC-ResNet (Kim 2021) | 9/10 | ★★★★★ |
| P4 | Hello Edge (Zhang 2017) | 9/10 | ★★★★☆ |
| P5 | PCEN (Wang 2017) | 8/10 | ★★★★☆ |
| P6 | On-Device FS-KWS (Rusci 2023) | 8/10 | ★★★★★ |
| P7 | SSL+Meta (Kao 2022) | 7/10 | ★★★★☆ |
| P8 | Triplet KWS (Vygon 2021) | 7/10 | ★★★☆☆ |
| P9 | ProtoNet KWS (Parnami 2022) | 7/10 | ★★★★☆ |
| P10 | Dummy ProtoNets (Kim 2022) | 7/10 | ★★★☆☆ |
| P11 | Small Footprint FS-KWS (Yang 2023) | 7/10 | ★★★★☆ |
| P12 | Enhancing FS-KWS via SSL (Gok 2025) | 7/10 | ★★★★☆ |
| P13 | MT-HuBERT (Yuan 2025) | 6/10 | ★★☆☆☆ |

---

## Decisions Log (Updated after SLR)

| Decision | Before SLR | After SLR | Impact |
|---|---|---|---|
| **Backbone** | DS-CNN / BC-ResNet-32 | **BC-ResNet-32** (primary), DS-CNN (baseline). EdgeSpot validates BC-ResNet at 128K params | Backbone locked |
| **Feature** | MFCC, Log-Mel | **Log-Mel** (primary), **PCEN** (ablation). PCEN adds noise robustness at zero cost | PCEN elevated from "future work" to ablation |
| **Metric learning** | ProtoNet (primary), Siamese/Triplet (secondary) | **ProtoNet** (primary baseline), **Triplet** (primary alternative). Rusci 2023 shows triplet outperforms ProtoNet for open-set | Triplet upgraded; Siamese dropped to lowest priority |
| **Training strategy** | Fine-tune all | **SSL pretrain (HuBERT) + ProtoNet fine-tune** (Kao 2022). KD to student (Gok 2025) for edge | SSL pretrain added as ablation |
| **N-way episode** | N=5 | **N=5**. Consistent with literature | Confirmed |
| **Seen/unseen split** | 25/5/5 | **25/5/5**. Need to check consistency with EdgeSpot's 11-class subset approach | Confirmed |
| **Threshold** | Global EER | **Global EER**. Sub-center ArcFace (EdgeSpot 2026) and dummy prototypes (Kim 2022) are more advanced options | Threshold strategy confirmed |
| **Open-set** | Cosine + threshold | **Triplet + normalized outputs** (Rusci 2023) or **dummy prototypes** (Kim 2022) | Open-set strategy refined |
| **Streaming eval** | FA/hour, RTF, detection latency | **GE2E-KWS protocol** (streamable pipeline evaluation) | Streaming metrics confirmed |
| **Edge framework** | TFLite INT8 | **TFLite INT8** + knowledge distillation. EdgeSpot shows quantization + KD works well | KD added to plan |

---

## Key Research Gap Evidence

### Gap 1: Vietnamese KWS — CONFIRMED with zero papers

| Search | # Results | Relevant |
|---|---|---|
| "Vietnamese keyword spotting" arXiv | 0 | 0 |
| "Vietnamese" + "speech commands" | 0 | 0 |
| "Vietnamese" + "wake word" | 0 | 0 |
| "tiếng Việt" + "keyword spotting" | 0 | 0 |

**Conclusion:** No existing Vietnamese KWS research found. This is a clear, well-defined research gap.

### Gap 2: Enrollment-centric Evaluation — CONFIRMED

Most papers use episode-based evaluation (Parnami 2022, Kim 2022). Only Rusci 2023 and EdgeSpot 2026 evaluate with enrollment-style workflow. No paper combines enrollment + streaming + edge deployment.

### Gap 3: End-to-end Framework — CONFIRMED

No paper provides a complete framework from training through edge deployment. EdgeSpot 2026 is closest (BC-ResNet + PCEN + KD + open-set) but doesn't include Vietnamese language or streaming pipeline.

### Gap 4: Heterogeneous Evaluation — CONFIRMED

Papers use different:
- Seen/unseen splits (5-way, 10-way, leave-out)
- Metrics (accuracy, AUC, EER, FA-constrained accuracy)
- Evaluation modes (episode, enrollment, streaming)
- No standard benchmark exists

---

## Notes & Ideas

### EdgeSpot (Buyuksolak 2026) — Most Relevant Paper
- BC-ResNet backbone: validates our choice
- PCEN frontend: validates adding PCEN ablation
- Sub-center ArcFace for open-set: alternative to simple threshold
- 128K params, 29.4M MACs: feasibility for Pi 4
- Knowledge distillation from large to small model

### Rusci 2023 — Key Finding
- Triplet loss + normalized features > ProtoNet for open-set
- "Normalization matters more than loss function choice" — important insight
- On-device customization workflow similar to our enrollment

### Gaps in SOTA not addressed by existing work:
1. Vietnamese language KWS (zero papers)
2. Combined enrollment + streaming evaluation
3. Complete framework from training → edge deployment
4. Unified evaluation protocol with speaker leakage analysis
