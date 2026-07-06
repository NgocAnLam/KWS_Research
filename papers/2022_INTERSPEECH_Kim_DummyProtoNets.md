---
title: "Dummy Prototypical Networks for Few-Shot Open-Set Keyword Spotting"
authors: "Byeonggeun Kim, Seunghan Yang, Inseop Chung, Simyung Chang"
venue: "INTERSPEECH"
year: 2022
doi: "10.48550/arXiv.2206.13691"
paper_url: "https://arxiv.org/abs/2206.13691"
pdf_path: "papers/2022_INTERSPEECH_Kim_DummyProtoNets.pdf"
---

# Paper Review: Dummy Prototypical Networks for Few-Shot Open-Set KWS

## 1. Summary

Proposes Dummy Prototypical Networks (D-ProtoNets) for few-shot open-set keyword spotting, introducing episode-known dummy prototypes to detect unknown/unseen utterances. Introduces splitGSC as a new benchmark for FSOSR in KWS. Also validates on miniImageNet, achieving SOTA open-set detection.

## 2. Research

| Field | Value |
|---|---|
| **Problem** | Few-shot KWS with open-set rejection (detecting unknown keywords) |
| **Proposed Method** | Dummy Prototypical Networks — metric learning with episode-known dummy prototypes |
| **Dataset** | splitGSC (new benchmark based on GSC), miniImageNet |
| **Backbone** | Not specified in abstract (requires PDF) |
| **Audio Feature** | Not specified in abstract (requires PDF) |
| **Metric Learning** | Prototypical Networks + dummy prototypes for open-set |
| **K-shot setting** | N-way M-shot (episode-based) |
| **Training strategy** | Episode-based training with dummy prototypes |
| **Evaluation protocol** | Episode-based few-shot open-set recognition (FSOSR) |
| **Unknown detection** | Yes — open-set via dummy prototypes |
| **Edge deployment** | None |
| **Streaming evaluation** | No |

## 3. Key Results

| Metric | Value |
|---|---|
| **Open-set detection (splitGSC)** | Clear margins over existing FSOSR approaches |
| **Open-set detection (miniImageNet)** | SOTA among FSOSR methods |

## 4. Quality Assessment (0-2 each)

| Criterion | Score | Notes |
|---|---|---|
| QA1: Problem clarity | 2 | Clear problem: few-shot + open-set jointly addressed |
| QA2: Experimental rigor | 2 | Evaluated on both audio (splitGSC) and vision (miniImageNet) |
| QA3: Reproducibility | 1 | No code mentioned; splitGSC is new benchmark (needs release) |
| QA4: Relevance to our work | 2 | Highly relevant for open-set KWS on edge |
| QA5: Edge evaluation | 0 | No edge deployment details |
| **Total ( /10)** | **7** | |

## 5. Analysis

### Strengths
- Addresses both few-shot AND open-set jointly — very practical for real-world KWS
- Dummy prototype concept is elegant and simple
- Evaluated on both audio and vision benchmarks (generalization)
- splitGSC provides standard benchmark for FSOSR in KWS

### Weaknesses
- No edge deployment or latency analysis
- Backbone architecture not clear from abstract (needs PDF)
- No code availability mentioned
- Does not address computational efficiency

### Key Takeaways for Our Work
- Dummy prototypes are a promising approach for open-set FS-KWS
- splitGSC is a relevant benchmark for our evaluation
- Open-set detection is critical for real-world deployment

### Open Questions
- What is the computational overhead of dummy prototypes?
- How does it perform on tonal languages like Vietnamese?
- Can dummy prototypes be combined with lightweight backbones?

## 6. BibTeX

```bibtex
@inproceedings{kim2022dummy,
  title={Dummy Prototypical Networks for Few-Shot Open-Set Keyword Spotting},
  author={Kim, Byeonggeun and Yang, Seunghan and Chung, Inseop and Chang, Simyung},
  booktitle={Proceedings of INTERSPEECH 2022},
  year={2022}
}
```

---

## Review Log

| Field | Value |
|---|---|
| **Reviewed by** | Kilo (AI analysis) |
| **Date** | 2026-07-06 |
| **PDF file** | Not yet downloaded |
| **Metadata file** | `papers/metadata/2022_INTERSPEECH_Kim_DummyProtoNets.md` |
