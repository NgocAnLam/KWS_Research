# Paper Review: PLCL (ICASSP 2025)

**Phoneme-Level Contrastive Learning for UDKWS with Flexible Enrollment**

| Field | Value |
|---|---|
| **Authors** | Li Kewei, Zhou Hengshun, Shen Kai, Dai Yusheng, Du Jun |
| **arXiv** | 2412.20805 |
| **Method** | Phoneme-level contrastive alignment + phoneme memory bank + third-category hard-negative discriminator |
| **Enrollment** | Audio-text AND audio-audio (flexible) |
| **Dataset** | LibriPhrase |
| **Results** | SOTA on LibriPhrase |
| **Relevance** | High — phoneme-level approach important for Vietnamese (tone language with confusable words) |

**Key Takeaway:** Phoneme-level contrastive learning is effective for confusable word discrimination. Vietnamese has 6 tones — phoneme-level matching could help distinguish similar-sounding keywords.

**BibTeX:** `@inproceedings{li2025plcl, title={PLCL}, booktitle={ICASSP 2025}}`
