---
title: "Few-Shot Open-Set Learning for On-Device Customization of KeyWord Spotting Systems"
authors: "Manuele Rusci, Tinne Tuytelaars"
venue: "INTERSPEECH"
year: 2023
doi: "10.48550/arXiv.2306.02161"
paper_url: "https://arxiv.org/abs/2306.02161"
pdf_path: "papers/2023_INTERSPEECH_Rusci_FewShotOpenSetOnDevice.pdf"
---

# Paper Review: Few-Shot Open-Set Learning for On-Device Customization of KWS Systems

## 1. Summary

Investigates few-shot open-set KWS by combining a deep feature encoder with a prototype-based classifier. Compares triplet loss (with normalized outputs) vs prototypical networks with dummy unknown-class prototypes. Achieves 76% accuracy in 10-shot with 5% FAR. Triplet loss outperforms prototypical networks in the open-set setting.

## 2. Research

| Field | Value |
|---|---|
| **Problem** | On-device few-shot open-set KWS — user-defined keywords with unknown rejection |
| **Proposed Method** | Deep feature encoder + prototype classifier; compares Triplet loss vs ProtoNet + dummy prototypes |
| **Dataset** | GSC (10 user-defined keyword classes) |
| **Backbone** | Deep feature encoder (requires PDF for architecture details) |
| **Audio Feature** | Not specified in abstract (requires PDF) |
| **Metric Learning** | Triplet loss (with L2-normalized outputs) vs ProtoNet + dummy prototypes |
| **K-shot setting** | 10-shot scenario |
| **Training strategy** | Encoder pretraining with triplet loss or prototypical training |
| **Evaluation protocol** | Open-set KWS with FAR control |
| **Unknown detection** | Yes — open-set with FAR threshold |
| **Edge deployment** | On-device customization focus (explicit in title) |
| **Streaming evaluation** | No |

## 3. Key Results

| Metric | Value |
|---|---|
| **Accuracy (10-shot, 5% FAR)** | 76% |
| **False Acceptance Rate (unknown)** | 5% |
| **Triplet vs ProtoNet** | Triplet loss outperforms ProtoNet + dummy prototypes |
| **Model size** | Fewer parameters than iso-accuracy approaches |

## 4. Quality Assessment (0-2 each)

| Criterion | Score | Notes |
|---|---|---|
| QA1: Problem clarity | 2 | Clear: on-device customization with open-set |
| QA2: Experimental rigor | 2 | Compares two loss families fairly |
| QA3: Reproducibility | 1 | No code mentioned |
| QA4: Relevance to our work | 2 | Highly relevant: on-device, open-set, few-shot |
| QA5: Edge evaluation | 1 | On-device mentioned but no detailed edge metrics (latency/power) |
| **Total ( /10)** | **8** | |

## 5. Analysis

### Strengths
- Direct comparison of triplet loss vs prototypical networks for open-set KWS
- On-device customization scenario is very practical
- Triplet loss with normalized outputs is shown to be more effective
- Fewer parameters than iso-accuracy approaches

### Weaknesses
- Only evaluated on 10 classes from GSC
- 76% accuracy at 10-shot has room for improvement
- No Vietnamese or tonal language evaluation
- No actual on-device latency/power measurements

### Key Takeaways for Our Work
- Triplet loss with normalized features may be better than ProtoNet for open-set
- Prototype-based classifier is effective for on-device customization
- Open-set rejection is essential for practical KWS systems

### Open Questions
- What backbone architecture achieves these results?
- Can triplet loss + dummy prototypes be combined for better open-set?
- How does this approach scale to more keywords (e.g., 20+ classes)?

## 6. BibTeX

```bibtex
@inproceedings{rusci2023few,
  title={Few-Shot Open-Set Learning for On-Device Customization of KeyWord Spotting Systems},
  author={Rusci, Manuele and Tuytelaars, Tinne},
  booktitle={Proceedings of INTERSPEECH 2023},
  pages={2768--2772},
  year={2023}
}
```

---

## Review Log

| Field | Value |
|---|---|
| **Reviewed by** | Kilo (AI analysis) |
| **Date** | 2026-07-06 |
| **PDF file** | Not yet downloaded |
| **Metadata file** | `papers/metadata/2023_INTERSPEECH_Rusci_FewShotOpenSetOnDevice.md` |
