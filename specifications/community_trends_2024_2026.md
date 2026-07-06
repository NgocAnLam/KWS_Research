# Community Trends & Design Impact Analysis (2024–2026)

> **Post-SLR consolidation — 50 papers analyzed.**
> **Mục đích:** Tổng hợp xu hướng cộng đồng cho Related Work và design decisions.

---

## 1. Trend Overview

| Trend | Maturity | Papers | Impact on Our Project |
|---|---|---|---|
| **Text-based zero-shot enrollment** | Growing (8 papers) | Jung 2025, Kim 2024, Navon 2024, Ai 2024, Xi 2024 | Add Related Work; no design change |
| **Phoneme-level contrastive learning** | Growing (5 papers) | Li 2025 (PLCL), Ai 2024 (MM-KWS), Pan 2026 (ProKWS) | 🔶 Consider for Vietnamese (tonal lang) |
| **SSL + KD for edge** | Growing (4 papers) | EdgeSpot 2026, Gok 2025, Kao 2022, Yang 2023 | 🔶 Optional ablation |
| **FAR-constrained evaluation** | Emerging (3 papers) | EdgeSpot 2026, GE2E-KWS 2024, Gok 2025 | ✅ Adopt acc@1% FAR, acc@5% FAR |
| **GE2E loss** | Emerging (2 papers) | GE2E-KWS 2024 | 🔶 Secondary ablation |
| **Continual adaptation** | Emerging (2 papers) | Ai 2026 (DMA-KWS), Dhungana 2026 | Future work |
| **Dual-stage matching (CTC + phoneme)** | Emerging (1 paper) | Ai 2026 (DMA-KWS) | 🟡 Reference for streaming |
| **ProtoNet (few-shot KWS)** | Declining (0 papers 2024-2026) | — | Still valid baseline |
| **MFCC as primary feature** | Declining (5/33 papers) | — | Move to historical baseline |
| **Pure triplet loss** | Declining | Replaced by GE2E (+60.7% AUC) | Keep as secondary |

---

## 2. Confirmed Trends (Strong Evidence)

| Trend | Confidence | Action |
|---|---|---|
| **Log-Mel is the standard feature** | Strong (28/33 papers) | Set as primary feature |
| **BC-ResNet is top accuracy backbone** | Strong (EdgeSpot 2026 confirms) | Set as primary backbone |
| **No Vietnamese KWS exists** | Strong (0 papers) | Genuine contribution |
| **Protocol heterogeneity** | Strong (18/18 different protocols) | Strong contribution |
| **TFLite INT8 is edge standard** | Strong (10/12 edge papers) | Stick with TFLite |

---

## 3. Emerging Trends (Moderate Evidence)

| Trend | Confidence | Action |
|---|---|---|
| **PCEN improves FS-KWS accuracy** | Moderate (EdgeSpot only) | Add as ablation |
| **GE2E may outperform ProtoNet** | Moderate (no direct comparison) | Add as secondary |
| **FAR-constrained metrics** | Moderate (3 papers) | Adopt |
| **Phoneme-level for tonal languages** | Moderate (PLCL, MM-KWS) | Consider for Vietnamese |
| **SSL + KD for edge deployment** | Moderate (4 papers) | Optional ablation |

---

## 4. Declining Methods

| Method | Evidence | Action |
|---|---|---|
| **MFCC as primary** | 5/33 papers (all pre-2024) | Move to historical baseline |
| **ProtoNet as SOTA** | 0 papers 2024-2026 | Keep as baseline only |
| **Pure triplet loss** | Outperformed by GE2E | Keep as secondary |
| **DS-CNN as primary** | Only baseline in 2024-2026 | Keep as baseline |
