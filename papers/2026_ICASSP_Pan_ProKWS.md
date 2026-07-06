# Paper Review: ProKWS (ICASSP 2026)

**Personalized KWS via Collaborative Learning of Phonemes and Prosody**

| Field | Value |
|---|---|
| **Authors** | Jianan Pan, Yuanming Zhang, Kejie Huang |
| **arXiv** | 2603.18024 |
| **Method** | Dual-stream encoder (phoneme contrastive + prosody extraction) + collaborative fusion |
| **Key Innovation** | Prosody modeling (intonation, stress, rhythm) for personalized KWS |
| **Results** | SOTA on standard benchmarks |
| **Relevance** | High — Vietnamese is a tonal language with 6 tones. Prosody modeling could be crucial for Vietnamese UDKWS. |

**Key Takeaway:** No existing KWS work models prosody for Vietnamese. This is a gap we can leverage. ProKWS validates that prosody + phoneme together outperform phoneme alone for personalized KWS.

**BibTeX:** `@inproceedings{pan2026prokws, title={ProKWS}, booktitle={ICASSP 2026}}`
