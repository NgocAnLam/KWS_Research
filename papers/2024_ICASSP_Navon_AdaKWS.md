# Paper Review: AdaKWS (ICASSP 2024)

**Open-vocabulary Keyword-spotting with Adaptive Instance Normalization**

| Field | Value |
|---|---|
| **Authors** | Aviv Navon, Aviv Shamsian, Neta Glazer, Gill Hetz, Joseph Keshet |
| **arXiv** | 2309.08561 |
| **Method** | Text encoder outputs AdaIN parameters to condition audio encoder |
| **Key Innovation** | Condition audio processing with text via AdaIN (no joint embedding space) |
| **Results** | Significant improvements over KWS and ASR baselines on multilingual; gains on low-resource unseen languages |
| **Relevance** | Medium — text-enrolled paradigm. AdaIN conditioning is novel but different from our audio enrollment. |

**Key Takeaway:** AdaIN conditioning is a different architectural approach. Good for Related Work section to show diversity of text-enrolled methods.

**BibTeX:** `@inproceedings{navon2024adakws, title={AdaKWS}, booktitle={ICASSP 2024}}`
