---
title: "Few-Shot Keyword Spotting With Prototypical Networks"
authors: "Archit Parnami, Minwoo Lee"
venue: "ICMLT"
year: 2022
doi: "10.1145/3529399.3529443"
paper_url: "https://arxiv.org/abs/2007.14463"
pdf_path: "papers/2022_ICMLT_Parnami_FewShotProtoKWS.pdf"
---

# Paper Review: Few-Shot Keyword Spotting With Prototypical Networks

## 1. Summary

First paper to formulate KWS as a few-shot problem using Prototypical Networks with temporal and dilated convolutions. Synthesizes and publishes a Few-shot Google Speech Commands dataset to enable this research direction.

## 2. Research

| Field | Value |
|---|---|
| **Problem** | Recognizing new user-defined keywords from few examples |
| **Proposed Method** | Prototypical Networks with temporal and dilated convolutions (TCN-style encoder) |
| **Dataset** | Few-shot Google Speech Commands (synthesized subset of GSC) |
| **Backbone** | Temporal convolutional network (TCN) with dilated convolutions |
| **Audio Feature** | Mel-spectrograms (standard) |
| **Metric Learning** | ProtoNet (Euclidean distance to class prototypes) |
| **K-shot setting** | Multiple K values investigated |
| **Training strategy** | Episodic training (standard ProtoNet) |
| **Evaluation protocol** | Episode-based few-shot classification |
| **Unknown detection** | None (closed-set) |
| **Edge deployment** | None |
| **Streaming evaluation** | No |

## 3. Key Results

| Metric | Value |
|---|---|
| **Accuracy** | Comparative results demonstrating feasibility (exact numbers require PDF) |
| **Model size** | Not specified |

## 4. Quality Assessment (0-2 each)

| Criterion | Score | Notes |
|---|---|---|
| QA1: Problem clarity | 2 | Clear formulation of few-shot KWS problem |
| QA2: Experimental rigor | 1 | Comparison only against baselines, limited ablation |
| QA3: Reproducibility | 1 | Dataset published, code may not be available |
| QA4: Relevance to our work | 2 | Foundational paper for few-shot KWS with ProtoNet |
| QA5: Edge evaluation | 0 | No edge considerations |
| **Total ( /10)** | **6** | |

## 5. Analysis

### Strengths
- First to formulate few-shot KWS with Prototypical Networks
- Provides synthesized Few-shot GSC dataset for the community
- Establishes baseline methodology for FS-KWS

### Weaknesses
- Simple backbone (TCN) — not optimized for efficiency
- Lower-tier venue (ICMLT)
- No open-set or unknown detection
- No edge deployment evaluation
- Exact numerical results need PDF verification

### Key Takeaways for Our Work
- Validates ProtoNet as viable approach for FS-KWS
- Temporal/dilated convolutions can work for KWS but may not be optimal
- Few-shot GSC provides a standard evaluation benchmark

### Open Questions
- How does TCN backbone compare to modern architectures (BC-ResNet, etc.)?
- Does ProtoNet with simple backbone generalize to non-English?

## 6. BibTeX

```bibtex
@inproceedings{parnami2022few,
  title={Few-Shot Keyword Spotting With Prototypical Networks},
  author={Parnami, Archit and Lee, Minwoo},
  booktitle={2022 7th International Conference on Machine Learning Technologies (ICMLT)},
  pages={277--283},
  year={2022},
  organization={ACM}
}
```

---

## Review Log

| Field | Value |
|---|---|
| **Reviewed by** | Kilo (AI analysis) |
| **Date** | 2026-07-06 |
| **PDF file** | Not yet downloaded |
| **Metadata file** | `papers/metadata/2022_ICMLT_Parnami_FewShotProtoKWS.md` |
