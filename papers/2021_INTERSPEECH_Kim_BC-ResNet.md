---
title: "Broadcasted Residual Learning for Efficient Keyword Spotting"
authors: "Byeonggeun Kim, Simyung Chang, Jinkyu Lee, Dooyong Sung"
venue: "INTERSPEECH"
year: 2021
doi: "10.48550/arXiv.2106.04140"
paper_url: "https://arxiv.org/abs/2106.04140"
pdf_path: "papers/2021_INTERSPEECH_Kim_BC-ResNet.pdf"
---

# Paper Review: BC-ResNet

## 1. Summary

Proposes Broadcasted Residual Learning and the BC-ResNet architecture for efficient keyword spotting. The key idea: residual functions use mostly 1D temporal conv, but a broadcasted-residual connection expands temporal output to frequency-temporal dimension, enabling 2D conv jointly. BC-ResNets achieve 98.0% (GSC v1) and 98.7% (GSC v2) top-1 accuracy with fewer parameters and MACs than prior SOTA. Code is open-source.

## 2. Research

| Field | Value |
|---|---|
| **Problem** | Efficient KWS with minimal computation for mobile/edge devices |
| **Proposed Method** | Broadcasted Residual Learning: BC-ResBlock with 1D temporal conv + broadcasted skip to 2D; BC-ResNet stacks these blocks with scaling variants (BC-ResNet-2/3/4) |
| **Dataset** | GSC v1 (30 commands, 64K utts), GSC v2 (35 commands, 105K utts) |
| **Backbone** | BC-ResNet (BC-ResBlocks: temporal 1D depthwise conv + 2D pointwise; broadcasted residual connection) |
| **Audio Feature** | 40-dim log-mel spectrogram, 64ms window, 30ms hop; 32 freq bins; 98 time frames |
| **Metric Learning** | Softmax cross-entropy (classification) |
| **K-shot setting** | N/A (closed-set classification) |
| **Training strategy** | Scratch; 90 epochs, Adam, cosine LR decay, weight decay, SpecAugment |
| **Evaluation protocol** | Standard GSC train/test split; top-1 accuracy |
| **Unknown detection** | None (closed-set classification) |
| **Edge deployment** | Explicit mobile/edge target; MACs/params reported; scaled variants |
| **Streaming evaluation** | No |

## 3. Key Results

| Metric | Value |
|---|---|
| **BC-ResNet-2 GSC v1 accuracy** | 97.6% |
| **BC-ResNet-3 GSC v1 accuracy** | 98.0% |
| **BC-ResNet-4 GSC v1 accuracy** | 97.8% |
| **BC-ResNet-2 GSC v2 accuracy** | 97.5% |
| **BC-ResNet-3 GSC v2 accuracy** | 98.3% |
| **BC-ResNet-4 GSC v2 accuracy** | 98.7% |
| **BC-ResNet-2 params** | 32K |
| **BC-ResNet-3 params** | 89K |
| **BC-ResNet-4 params** | 181K |
| **BC-ResNet-2 MACs** | 5.7M |
| **BC-ResNet-3 MACs** | 12.5M |
| **BC-ResNet-4 MACs** | 33.6M |

Scaling variants: -2 (base), -3 (wider/time-dilated in later blocks), -4 (wider still).

## 4. Quality Assessment (0-2 each)

| Criterion | Score | Notes |
|---|---|---|
| QA1: Problem clarity | 2 | Clear: efficient KWS for mobile with broadcasted residual learning |
| QA2: Experimental rigor | 2 | GSC v1 + v2, compares against DNN, LSTM, CRNN, ResNet, TC-ResNet, Att-RNN, etc. |
| QA3: Reproducibility | 2 | Code on GitHub (Qualcomm-AI-research/bcresnet) |
| QA4: Relevance to our work | 2 | BC-ResNet is a key backbone for edge KWS; used by EdgeSpot and others |
| QA5: Edge evaluation | 2 | MACs and params reported for all variants; mobile-friendly design |
| **Total ( /10)** | **10** | |

## 5. Analysis

### Strengths
- Novel broadcasted residual connection elegantly merges 1D temporal + 2D frequency-temporal features
- Exceptional efficiency: BC-ResNet-2 (32K params, 5.7M MACs) achieves 97.6% on GSC v1
- Code open-source with pretrained models on GitHub
- SOTA on GSC at time of publication; still a strong baseline today
- Scaling variants (2/3/4) provide clear accuracy-compute tradeoff

### Weaknesses
- Closed-set classification only — no few-shot or zero-shot capability
- No unknown keyword rejection
- Evaluated only on clean GSC; no noise robustness study
- No streaming evaluation
- No latency/power measurements on actual devices

### Key Takeaways for Our Work
- BC-ResNet-2 (32K params) is an ideal backbone for resource-constrained edge KWS
- Broadcasted residual learning is worth exploring for Vietnamese KWS
- The architecture serves as a strong baseline for few-shot extensions (EdgeSpot builds on it)
- Open-source code enables direct adoption and modification

### Open Questions
- How does BC-ResNet perform on tonal languages (Vietnamese)?
- Can BC-ResNet be adapted for few-shot/zero-shot via embedding extraction?
- What is the actual inference latency on microcontrollers vs mobile GPUs?

## 6. BibTeX

```bibtex
@inproceedings{kim2021broadcasted,
  title={Broadcasted Residual Learning for Efficient Keyword Spotting},
  author={Kim, Byeonggeun and Chang, Simyung and Lee, Jinkyu and Sung, Dooyong},
  booktitle={Proceedings of INTERSPEECH 2021},
  year={2021},
  doi={10.48550/arXiv.2106.04140}
}
```

---

## Review Log

| Field | Value |
|---|---|
| **Reviewed by** | Kilo (AI analysis) |
| **Date** | 2026-07-06 |
| **PDF file** | Not yet downloaded |
| **Metadata file** | `papers/metadata/2021_INTERSPEECH_Kim_BC-ResNet.md` |
