---
title: "GE2E-KWS: Generalized End-to-End Training and Evaluation for Zero-shot Keyword Spotting"
authors: "Pai Zhu, Jacob W. Bartel, Dhruuv Agarwal, Kurt Partridge, Hyun Jin Park, Quan Wang"
venue: "IEEE SLT"
year: 2024
doi: "10.1109/SLT61566.2024.10832206"
paper_url: "https://arxiv.org/abs/2410.16647"
pdf_path: "papers/2024_SLT_Zhu_GE2E-KWS.pdf"
---

# Paper Review: GE2E-KWS

## 1. Summary

Applies Generalized End-to-End (GE2E) loss from speaker verification to zero-shot keyword spotting, simulating enrollment vs verification during training. Uses a quantized conformer model (419KB) that beats a 7.5GB ASR encoder by 23.6% relative AUC and a same-size triplet loss model by 60.7% AUC. Proposes a new evaluation protocol over GSC that directly measures utterance-matching accuracy via DET curves, AUC, and EER.

## 2. Research

| Field | Value |
|---|---|
| **Problem** | Zero-shot custom KWS — detect user-defined keywords without retraining |
| **Proposed Method** | GE2E loss: per-batch enrollment centroids (Y/2 utterances) vs all test utterances; cosine similarity + softmax loss |
| **Dataset** | Train: MSWC (38K phrases, 5.3M utts, 27K speakers); Eval: GSC (11K utts, 35 phrases) |
| **Backbone** | 3-layer LSTM (various sizes) and Conformer (5-12 blocks, MHSA tuned) |
| **Audio Feature** | 40-dim log-mel spectral features, 25ms frame, 10ms shift |
| **Metric Learning** | GE2E loss (adapted from speaker verification) |
| **K-shot setting** | N/A (zero-shot — enrollment utterances seen once at runtime) |
| **Training strategy** | Scratch, TensorFlow/Lingvo, 8 phrases/batch, 10 utts/phrase, 5 enrollment + 5 test |
| **Evaluation protocol** | Enrollment centroid (10 utts) → cosine sim with all test utts → DET/AUC/EER per phrase; clean + noisy (3-way MTR 3-15dB) |
| **Unknown detection** | Threshold-based on cosine similarity to enrollment centroid |
| **Edge deployment** | 419KB quantized conformer; dynamic range quantization (TFLite); natively streamable |
| **Streaming evaluation** | Yes (model designed for streaming, automatic conversion in Lingvo) |

## 3. Key Results

| Metric | Value |
|---|---|
| **GE2E Conformer (419KB) aggregated AUC** | 0.504% (lower is better) |
| **ASR Encoder (7.5GB) aggregated AUC** | 0.66% |
| **Triplet Loss Conformer (419KB) aggregated AUC** | 1.283% |
| **Speech Classification Encoder (1.4MB) aggregated AUC** | 6.44% |
| **GE2E vs ASR (relative AUC improvement)** | 23.6% |
| **GE2E vs Triplet (relative AUC improvement)** | 60.7% |
| **LSTM 15MB raw (1.2MB quant) best AUC** | 0.344% (clean) |
| **Conformer 24MB raw (2.4MB quant) AUC** | 0.382% |
| **Conformer 2.8MB raw (419KB quant) EER clean** | 2.94% |
| **Conformer 2.8MB raw (419KB quant) EER noisy** | 9.69% |

## 4. Quality Assessment (0-2 each)

| Criterion | Score | Notes |
|---|---|---|
| QA1: Problem clarity | 2 | Very clear: zero-shot KWS with practical enrollment simulation |
| QA2: Experimental rigor | 2 | Extensive comparison vs ASR encoder, classification model, triplet loss; clean+noisy; multiple model sizes |
| QA3: Reproducibility | 1 | No code released; uses TensorFlow/Lingvo (proprietary-adjacent); MSWC+GSC are public |
| QA4: Relevance to our work | 2 | Directly relevant: zero-shot KWS, embedding-based, conformer, on-device |
| QA5: Edge evaluation | 2 | Explicit quantized model sizes (419KB), streaming design, on-device ready |
| **Total ( /10)** | **9** | |

## 5. Analysis

### Strengths
- GE2E loss enables stable training (multiple enrollment utts → reduced variance, matrix operations → faster) vs triplet
- Quantized conformer at 419KB achieves better AUC than a 7.5GB ASR encoder — massive efficiency gain
- Comprehensive evaluation protocol (DET, AUC, EER per-word + aggregated) sets a standard for zero-shot KWS
- Evaluates on unseen words (zero-shot) — "up", "no", "go", "on" not in training data
- Streaming-native model architecture

### Weaknesses
- Only English datasets (MSWC English subset, GSC)
- No ablation study isolating GE2E contributions vs other sampling strategies
- Conformer advantage over LSTM is marginal at larger sizes (LSTM slightly better clean, Conformer better noisy)
- No actual on-device latency or power benchmarks
- GE2E requires even batch structure (Y/2 enrollment + Y/2 test per phrase)

### Key Takeaways for Our Work
- GE2E loss is a strong alternative to triplet loss for embedding-based zero-shot KWS
- Conformer at ultra-small sizes (419KB) is remarkably effective for on-device deployment
- The evaluation methodology (split enrollment/test, cosine similarity, DET/AUC/EER) should be adopted
- The 40-dim log-mel feature pipeline is a good baseline

### Open Questions
- Can GE2E loss be combined with prototypical networks for few-shot (not zero-shot) KWS?
- How does GE2E perform on tonal languages (Vietnamese)?
- What is the actual on-device latency in ms?
- Could an even smaller conformer (sub-200KB) work?

## 6. BibTeX

```bibtex
@inproceedings{zhu2024ge2e,
  title={GE2E-KWS: Generalized End-to-End Training and Evaluation for Zero-shot Keyword Spotting},
  author={Zhu, Pai and Bartel, Jacob W. and Agarwal, Dhruuv and Partridge, Kurt and Park, Hyun Jin and Wang, Quan},
  booktitle={2024 IEEE Spoken Language Technology Workshop (SLT)},
  year={2024},
  doi={10.1109/SLT61566.2024.10832206}
}
```

---

## Review Log

| Field | Value |
|---|---|
| **Reviewed by** | Kilo (AI analysis) |
| **Date** | 2026-07-06 |
| **PDF file** | Not yet downloaded |
| **Metadata file** | `papers/metadata/2024_SLT_Zhu_GE2E-KWS.md` |
