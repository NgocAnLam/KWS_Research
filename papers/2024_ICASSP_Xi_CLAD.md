# Paper Review: CLAD (ICASSP 2024)

**Contrastive Learning with Audio Discrimination for Customizable KWS in Continuous Speech**

| Field | Value |
|---|---|
| **Authors** | Yu Xi, Baochen Yang, Hao Li, Jiaqi Guo, Kai Yu |
| **arXiv** | 2401.06485 |
| **Method** | InfoNCE with audio-text + audio-audio pairs at sliding-window level |
| **Key Innovation** | Continuous speech (not segmented), audio-audio discrimination |
| **Results** | Comparable to prior CL on LibriPhrase; significant gain on continuous LibriSpeech |
| **Relevance** | High — sliding-window evaluation for continuous speech is similar to our streaming pipeline |

**Key Takeaway:** CLAD validates sliding-window InfoNCE for continuous speech KWS. Relevant for our streaming deployment pipeline. Shows audio-audio discrimination is as important as audio-text matching.

**BibTeX:** `@inproceedings{xi2024clad, title={CLAD}, booktitle={ICASSP 2024}}`
