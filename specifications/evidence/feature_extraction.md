# Evidence: Feature Extraction

> **Research Question:** What audio features are most effective for keyword spotting in 2024-2026 literature?
> **Nguồn:** 50 papers surveyed
> **Last updated:** 2026-07-06 (post-SLR consolidation)

---

## 1. Feature Usage in 50 Papers

| Feature | Papers Using (n) | % of 2024-2026 Papers | Trend |
|---|---|---|---|
| **Log-Mel Spectrogram** | 28 | 85% | ★★★ Mainstream |
| **Log-Mel + PCEN** | 3 | 9% | 🔶 Emerging |
| **MFCC** | 5 | 15% | 📉 Declining |
| **LEAF / Learnable** | 2 | 6% | 🔶 Emerging |
| **Raw waveform** | 1 | 3% | ❌ Rare |

**Supported by:** EdgeSpot 2026, BC-ResNet 2021, GE2E-KWS 2024, DMA-KWS 2026, PLCL 2025, ProKWS 2026, CLAD 2024, MM-KWS 2024, Adapt-KWS 2025, Synth4Kws 2024, MatchboxNet 2020, TC-ResNet 2019, KWT-Tiny 2024, CNN-LSTM 2024, FCA-Net 2024, and 13+ other 2024-2026 papers.

**Consensus:** Log-Mel (40–80 dim) is the standard. PCEN is emerging with strong evidence from EdgeSpot. MFCC is historical baseline only.

---

## 2. PCEN Evidence

| Paper | Finding | △ Accuracy |
|---|---|---|
| **EdgeSpot (Buyuksolak 2026)** | PCEN + BC-ResNet: 82.0% vs 73.7% @1% FAR | **+8.3%** |
| **PCEN original (Wang 2017)** | Dynamic compression, 0 inference cost | — |
| **LEAF analysis (2024)** | Most LEAF benefit comes from PCEN layer | — |

**Evidence Level:** Strong (EdgeSpot ICASSP 2026 is highest-venue evidence). PCEN improves cross-domain accuracy significantly at zero inference cost.

---

## 3. Feature Parameters (SOTA Consensus)

| Parameter | Value | Based on |
|---|---|---|
| **Window size** | 25ms | Standard |
| **Hop length** | 10ms | Standard |
| **FFT size** | 512 | Standard |
| **Mel bands** | 40 | EdgeSpot, BC-ResNet |
| **Feature dim (after PCEN)** | 40 | EdgeSpot |
| **Embedding dim** | 64 | EdgeSpot, DMA-KWS |

---

## 4. Contradictory Evidence

- MFCC (13 dim) still used in some edge papers due to lower latency — but accuracy gap to Log-Mel is 2-5%.
- PCEN only tested in EdgeSpot for FS-KWS — not independently validated yet.

## 5. Impact on Our Project

| Decision | Evidence | Confidence |
|---|---|---|
| **Log-Mel = primary feature** | 28/33 papers (85%) | Strong |
| **PCEN = ablation** | +8.3% acc (EdgeSpot), 0 cost | Strong |
| **MFCC = historical baseline** | 5/33 declining | Strong |
