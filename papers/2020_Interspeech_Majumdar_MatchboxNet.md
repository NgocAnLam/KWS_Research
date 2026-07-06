# Paper Review: MatchboxNet (INTERSPEECH 2020)

**1D Time-Channel Separable CNN with Attention for KWS**

| Field | Value |
|---|---|
| **Authors** | Majumdar, Ginsburg |
| **Method** | 1D time-channel separable conv + squeeze-excitation attention |
| **Results** | 96.5% (23K params), 97.1% (58K params) on SCv2 12-class |
| **Relevance** | Medium — pre-2024, but established baseline. MatchboxNet-3×1×64 has only 23K params. |

**Key Takeaway:** MatchboxNet is the most parameter-efficient backbone for KWS (23K params for 96.5%). Reference for extreme edge deployment.

**BibTeX:** `@inproceedings{majumdar2020matchboxnet, title={MatchboxNet}, booktitle={Interspeech 2020}}`
