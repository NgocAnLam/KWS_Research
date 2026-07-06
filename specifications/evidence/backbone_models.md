# Evidence: Backbone Architectures

> **Research Question:** What lightweight backbone architectures are most effective for on-device keyword spotting?
> **Nguồn:** 50 papers surveyed, 15 backbone-specific papers analyzed
> **Last updated:** 2026-07-06 (post-SLR consolidation)

---

## 1. Backbone Comparison (GSCv2 Accuracy)

| Backbone | Params | Acc (GSCv2) | Edge Viability | Papers (n) |
|---|---|---|---|---|
| **BC-ResNet-32** | 110K | 98.7% | ✅ (EdgeSpot 2026) | 3 |
| **DS-CNN** | 20–80K | 95.4% | ✅ (Hello Edge 2017) | 5 |
| **MatchboxNet** | 23–58K | 96.5–97.1% | ✅ (TFLite) | 2 |
| **TC-ResNet** | 89K | 95.8% | ✅ (Mobile CPU) | 2 |
| **EdgeSpot-4** | 128K | 82% @1% FAR (FS) | ✅ (29.4M MACs) | 1 |
| **Conformer (quantized)** | — | 419KB model | ✅ (GE2E-KWS 2024) | 1 |
| **ResNet15 (KD)** | ~1M | 74% → 74.1% (FS) | ✅ (Gok 2025) | 1 |
| **KWT-Tiny** | ~60K | 96.3% | ✅ (RISC-V) | 1 |
| **FCANet** | small | — | ✅ | 1 |

**FS = Few-shot setting (not closed-set classification)**

---

## 2. Key Findings

| Finding | Support | Confidence |
|---|---|---|
| **BC-ResNet-32 has highest closed-set accuracy (98.7%)** | Kim 2021, EdgeSpot 2026 | Strong |
| **DS-CNN is most deployed on real edge hardware** | Hello Edge 2017, multiple MCU papers | Strong |
| **MatchboxNet is most parameter-efficient (23K @96.5%)** | Majumdar 2020 | Strong |
| **Conformer requires quantization for edge** | GE2E-KWS 2024 (419KB) | Moderate |
| **No single backbone dominates FS-KWS** | Different papers use different backbones | Strong |
| **EdgeSpot-4 is the only FS-KWS-optimized backbone** | EdgeSpot 2026 | Moderate |

---

## 3. EdgeSpot Validation

EdgeSpot (Buyuksolak 2026, ICASSP A*) is the **most directly relevant paper** — uses BC-ResNet variant for FS-KWS on edge:
- 128K params, 29.4M MACs
- 82.0% @1% FAR (10-shot)
- PCEN frontend + SDPA attention
- KD from SSL teacher

---

## 4. Contradictory Evidence

- Conformer (GE2E-KWS) may outperform BC-ResNet but no direct comparison exists.
- MatchboxNet is more parameter-efficient (23K vs 110K) but 1-2% less accurate.
- KWT-Tiny (60K, 96.3%) is a transformer alternative — promising but only 1 paper.

## 5. Impact on Our Project

| Decision | Evidence | Confidence |
|---|---|---|
| **BC-ResNet-32 = primary** | Highest accuracy, EdgeSpot-validated | Strong |
| **DS-CNN = baseline** | Most edge-deployed, well-understood | Strong |
| **MatchboxNet = optional reference** | Most parameter-efficient | Moderate |
| **Conformer = future work** | Only 1 edge paper | Low |
