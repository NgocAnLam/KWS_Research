# Paper Review: DMA-KWS (IEEE TASLP 2026)

---

## 1. Summary

DMA-KWS: dual-stage matching (CTC phoneme search + QbyT phoneme matcher), multi-modal enrollment (speech + text), and continual adaptation (187K params). **97.85% AUC, 6.13% EER** on LibriPhrase Hard — SOTA for UDKWS.

## 2. Research

| Field | Value |
|---|---|
| **Problem** | UDKWS with confusable words, speaker inconsistency |
| **Method** | Dual-stage matching + multi-modal enrollment + continual adaptation |
| **Dataset** | LibriPhrase (Hard subset) |
| **Enrollment** | Multi-modal (speech + text) |
| **Backbone** | CTC + phoneme matcher + QbyT |
| **Continual adaptation** | 187K params only |
| **On-device** | Yes |
| **AUC** | 97.85% |
| **EER** | 6.13% |

## 3. Quality Assessment: 9/10

## 4. Key Takeaways for Our Project

| Finding | Impact |
|---|---|
| Dual-stage matching outperforms single-stage | Consider for streaming pipeline |
| Multi-modal enrollment (speech + text) > text-only | **Validates our audio enrollment approach** |
| Continual adaptation with 187K params | Reference for future incremental learning |
| Phoneme-level matching for confusable words | Important for Vietnamese (similar-sounding words) |
| 97.85% AUC is SOTA on LibriPhrase Hard | Benchmark target for our Vietnamese dataset |

## 5. BibTeX

```bibtex
@article{ai2026dmakws,
  title={DMA-KWS: Effective User-defined Keyword Spotting with Dual-stage Matching, Multi-modal Enrollment, and Continual Adaptation},
  author={Ai, Zhiqi and Cheng, Han and Mu, Shiyi and Li, Xinnuo and Zhou, Yongjin and Xu, Shugong},
  journal={IEEE/ACM Transactions on Audio, Speech, and Language Processing},
  year={2026}
}
```
