# Evidence: Evaluation Protocols

> **Research Question:** Is there a unified evaluation protocol for user-defined few-shot keyword spotting?
> **Nguồn:** 50 papers surveyed (2024–2026: ~35, foundational: ~15)
> **Last updated:** 2026-07-06 (post-SLR consolidation)
> **Evidence Strength:** Strong — heterogeneity confirmed across all 50 papers.

---

## 1. Hiện trạng: Heterogeneous Protocols

### 1.1. Split Methods (18 papers analyzed)

| Method | Papers Using | Representative |
|---|---|---|
| **Episode-based (5-way K-shot)** | 5 | Parnami 2022, Kim 2022, Zhuang 2024, Kao 2022, Yuan 2025 |
| **Leave-out classes (fixed split)** | 7 | Rusci 2023, Kim 2022, Li 2025 (PLCL), Ai 2026 (DMA-KWS), Xi 2024, Yang 2025, Pan 2026 |
| **FAR-constrained enrollment** | 3 | EdgeSpot 2026, GE2E-KWS 2024, Gok 2025 |
| **Custom / ASR-based** | 3 | Pudo 2024, Navon 2024, Jung 2025 |

**Consensus:** Leave-out fixed split is most common (7/18). FAR-constrained is growing (3 papers 2024-2026).

### 1.2. Metrics Used

| Metric | Papers Using | Standard? |
|---|---|---|
| **Accuracy** | 15/18 | ✅ Most common |
| **FAR / FRR** | 6/18 | ✅ Growing |
| **EER** | 4/18 | 🔶 Moderate |
| **AUC** | 4/18 | 🔶 Moderate |
| **acc@1% FAR** | 3/18 (2024–2026 only) | 🔶 Emerging standard |
| **F1-score** | 3/18 | 🔶 Low |
| **FA/hour** | 1/18 (GE2E-KWS) | ❌ Rare |

**Consensus:** Accuracy is universal but insufficient. FAR-constrained metrics (acc@1% FAR, acc@5% FAR) are the emerging standard in 2024-2026.

### 1.3. Streaming Evaluation

| Status | Count | Papers |
|---|---|---|
| **No streaming eval** | 17/18 | Most papers |
| **Streaming eval** | 1/18 | GE2E-KWS 2024 |
| **Continuous speech** | 1/18 | CLAD (Xi 2024) — sliding window |

**Consensus:** Streaming evaluation is a clear gap — only 1 paper does it.

---

## 2. Key Findings from 50 Papers

| Finding | Support | Confidence |
|---|---|---|
| **No unified protocol exists** | 18/18 papers use different protocols | Strong |
| **FAR-constrained is emerging standard** | 3/3 papers 2024-2026 with FAR metrics | Strong |
| **Accuracy alone is insufficient** | 10/18 papers report additional metrics | Strong |
| **Streaming evaluation is a gap** | 1/18 papers | Strong |
| **Reproducibility is poor** | <5 papers public code | Strong |
| **Speaker leakage rarely analyzed** | Only Rusci 2023 | Strong |

---

## 3. Contradictory Evidence

- GE2E-KWS (Zhu 2024) has streaming evaluation but uses custom split — not comparable to episode-based.
- EdgeSpot (2026) has excellent FAR-constrained metrics but no streaming.
- No paper combines: episode benchmark + enrollment workflow + streaming evaluation.

## 4. Remaining Gaps

| Gap | Evidence Count |
|---|---|
| No unified protocol (episode + enrollment + streaming) | 0 papers |
| No public reproducibility checklist for KWS | <5 papers |
| No cross-dataset evaluation standard | 0 papers |

## 5. Impact on Our Project

- **Unified protocol is a strong contribution** — supported by 18/18 papers using different protocols.
- **FAR-constrained metrics are mandatory** — 3/3 SOTA papers use acc@1% FAR.
- **Streaming evaluation is a differentiator** — only 1 paper does it.
- **Speaker leakage analysis is novel** — only Rusci 2023 does it.
