---
title: "EdgeSpot: Efficient and High-Performance Few-Shot Model for Keyword Spotting"
authors: "Oguzhan Buyuksolak, Alican Gok, Osman Erman Okman"
venue: "ICASSP"
year: 2026
doi: "10.48550/arXiv.2601.16316"
paper_url: "https://arxiv.org/abs/2601.16316"
pdf_path: "papers/2026_ICASSP_Buyuksolak_EdgeSpot.pdf"
---

# Paper Review: EdgeSpot

## 1. Summary

EdgeSpot pairs an optimized BC-ResNet backbone with a trainable PCEN frontend and lightweight temporal self-attention for few-shot KWS on edge devices. It uses knowledge distillation from a Wav2Vec2.0 teacher trained with Sub-center ArcFace loss. The largest variant (EdgeSpot-4) achieves 82.0% 10-shot accuracy at 1% FAR with only 128K parameters and 29.4M MACs.

## 2. Research

| Field | Value |
|---|---|
| **Problem** | Few-shot KWS with low false-alarm rate on edge devices |
| **Proposed Method** | BC-ResNet + PCEN frontend + temporal SDPA + KD from SSL teacher with Sub-center ArcFace |
| **Dataset** | MSWC (5.5M train, 680K test, 39K words), cross-domain GSC (100K, 35 commands) |
| **Backbone** | BC-ResNet (with Fused BC-ResBlocks in early stages) |
| **Audio Feature** | 40-band mel spectrogram (40x101), PCEN frontend (trainable per-channel AGC + root compression) |
| **Metric Learning** | Prototype-based (average K examples → prototype); trained with Sub-center ArcFace |
| **K-shot setting** | 1-shot, 10-shot |
| **Training strategy** | Teacher-student KD: Wav2Vec2.0 teacher (SSL) → EdgeSpot student; 40 epochs, Adam, cosine LR, SpecAugment |
| **Evaluation protocol** | Random trials (100 for GSC, 3 runs for MSWC with 100K positive/negative each); DET@X (detection rate at FAR X), AUROC |
| **Unknown detection** | Threshold-based on distance to prototypes (FAR-controlled) |
| **Edge deployment** | 128K params (EdgeSpot-4), 29.4M MACs; explicitly designed for edge |
| **Streaming evaluation** | No |

## 3. Key Results

| Metric | Value |
|---|---|
| **EdgeSpot-4 10-shot Acc@1% FAR (GSC)** | 82.0% (vs BC-ResNet 73.7%) |
| **EdgeSpot-4 10-shot DET@1% (MSWC)** | Higher than BC-ResNet across all scales |
| **EdgeSpot-4 1-shot (GSC)** | Near-teacher performance, best among student models |
| **Model size** | 128K parameters |
| **Computational cost** | 29.4M MACs |
| **Embedding dim** | 64-D |
| **Input size** | 40x101 mel spectrogram |

## 4. Quality Assessment (0-2 each)

| Criterion | Score | Notes |
|---|---|---|
| QA1: Problem clarity | 2 | Clear problem definition: edge FS-KWS with low FAR |
| QA2: Experimental rigor | 2 | Cross-dataset eval (MSWC + GSC), multiple shots, FAR sweep |
| QA3: Reproducibility | 1 | No code released; dataset and architecture detailed |
| QA4: Relevance to our work | 2 | Highly relevant: edge KWS, few-shot, PCEN, BC-ResNet |
| QA5: Edge evaluation | 2 | MACs/params reported; edge-friendly design explicit |
| **Total ( /10)** | **9** | |

## 5. Analysis

### Strengths
- Extremely efficient: 128K params, 29.4M MACs — edge-deployable
- PCEN frontend improves cross-domain generalization (proven via ablation)
- KD + Sub-center ArcFace yields strong low-FAR performance
- Comprehensive evaluation on both in-domain (MSWC) and cross-domain (GSC)

### Weaknesses
- Requires SSL teacher (Wav2Vec2.0) during training — complex distillation pipeline
- Only English datasets; no multilingual evaluation
- No latency or power measurements on actual edge hardware
- No streaming/online evaluation protocol

### Key Takeaways for Our Work
- BC-ResNet is a strong backbone choice for edge FS-KWS
- PCEN frontend could improve robustness for Vietnamese KWS
- KD from SSL models works well for few-shot but adds training complexity
- 64-D embedding + prototype-based inference is effective

### Open Questions
- How does PCEN perform on tonal languages like Vietnamese?
- Can the teacher be replaced with a smaller SSL model?
- What is actual on-device latency (in ms)?

## 6. BibTeX

```bibtex
@article{buydksolak2026edgespot,
  title={EdgeSpot: Efficient and High-Performance Few-Shot Model for Keyword Spotting},
  author={Buyuksolak, Oguzhan and Gok, Alican and Okman, Osman Erman},
  journal={arXiv preprint arXiv:2601.16316},
  year={2026}
}
```

---

## Review Log

| Field | Value |
|---|---|
| **Reviewed by** | Kilo (AI analysis) |
| **Date** | 2026-07-06 |
| **PDF file** | Not yet downloaded |
| **Metadata file** | `papers/metadata/2026_ICASSP_Buyuksolak_EdgeSpot.md` |
