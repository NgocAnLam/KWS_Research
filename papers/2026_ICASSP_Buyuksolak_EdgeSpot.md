# Paper Review: EdgeSpot (ICASSP 2026)

---

## 1. Summary

EdgeSpot proposes an efficient few-shot KWS model for edge devices combining BC-ResNet backbone + trainable PCEN frontend + temporal self-attention. Knowledge distillation from a Wav2Vec2.0 teacher with Sub-center ArcFace loss. EdgeSpot-4 achieves 82.0% 10-shot accuracy at 1% FAR (vs BC-ResNet baseline 73.7%) with only 128K params and 29.4M MACs.

---

## 2. Research

| Field | Value |
|---|---|
| **Problem** | Few-shot KWS on edge devices with low FAR |
| **Proposed Method** | BC-ResNet + PCEN + SDPA + KD + Sub-center ArcFace |
| **Dataset** | MSWC (5.5M samples, 39K words) + GSCv2 (cross-domain) |
| **Backbone** | BC-ResNet (optimized with Fused BC-ResBlocks + temporal self-attention) |
| **Audio Feature** | Log-Mel 40-band → PCEN |
| **Metric Learning** | Sub-center ArcFace (teacher: Wav2Vec2.0 + attention head) |
| **K-shot setting** | 1-shot, 10-shot |
| **Training strategy** | SSL teacher → KD to student with SCAF loss |
| **Evaluation protocol** | FAR-constrained: accuracy at 1% and 5% FAR |
| **Unknown detection** | Threshold-based, prototype similarity |
| **Edge deployment** | Yes — 128K params, 29.4M MACs |
| **Streaming evaluation** | No |

## 3. Key Results

| Metric | Value |
|---|---|
| **10-shot acc @1% FAR (GSC)** | 82.0% (EdgeSpot-4) |
| **10-shot acc @1% FAR (GSC, BC-ResNet baseline)** | 73.7% |
| **Params** | 128K (EdgeSpot-4) |
| **MACs** | 29.4M |
| **Embedding dim** | 64-D |
| **Input feature** | 40×101 Mel-spectrogram + PCEN |

## 4. Quality Assessment

| Criterion | Score | Notes |
|---|---|---|
| QA1: Problem clarity | 2 | Clear motivation for edge FS-KWS |
| QA2: Experimental rigor | 2 | Multiple seeds, FAR-constrained metrics |
| QA3: Reproducibility | 1 | No public code |
| QA4: Relevance to our work | 2 | **Most relevant paper — BC-ResNet + PCEN + KD** |
| QA5: Edge evaluation | 2 | Reports MACs, params, compares with baselines |
| **Total ( /10)** | **9** | |

## 5. Analysis

### Strengths
- BC-ResNet + PCEN: directly validates our backbone and feature choices
- FAR-constrained evaluation (acc@1% FAR) — standard we should adopt
- Knowledge distillation pipeline: SSL teacher → lightweight student
- 128K params, 29.4M MACs — feasible for RPi4
- Cross-domain evaluation (MSWC → GSC) shows generalization

### Weaknesses
- No streaming evaluation (VAD/sliding window)
- No Vietnamese/multilingual evaluation
- No open-source code
- No comparison with ProtoNet (uses SCAF loss instead)
- Only evaluated at 1-shot and 10-shot (not 3-shot or 5-shot)

### Key Takeaways for Our Work
1. **BC-ResNet validates our backbone choice** — can cite EdgeSpot as evidence
2. **PCEN improves cross-domain accuracy** — should include PCEN ablation
3. **64-D embeddings** — matches our design
4. **acc@1% FAR** — should adopt this metric
5. **KD from SSL teacher** — optional ablation for us
6. **Log-Mel (40-band) + PCEN** — feature configuration to use

### Open Questions
- Can EdgeSpot's 64-D embeddings work with ProtoNet instead of SCAF?
- Would PCEN help as much without KD from SSL teacher?

## 6. BibTeX

```bibtex
@inproceedings{buyuksolak2026edgespot,
  title={EdgeSpot: Efficient and High-Performance Few-Shot Model for Keyword Spotting},
  author={Buyuksolak, Oguzhan and Gok, Alican and Okman, Osman Erman},
  booktitle={IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  year={2026}
}
```

---

## Review Log

| Field | Value |
|---|---|
| **Reviewed by** | AI Agent |
| **Date** | 2026-07-06 |
| **PDF file** | `papers/2026_ICASSP_Buyuksolak_EdgeSpot.pdf` (to download) |
| **Metadata file** | `papers/metadata/2026_ICASSP_Buyuksolak_EdgeSpot.md` |
