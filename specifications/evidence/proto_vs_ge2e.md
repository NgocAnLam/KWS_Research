# Evidence: Metric Learning Methods (ProtoNet vs GE2E vs Triplet)

> **Research Question:** Which metric learning method (ProtoNet, GE2E, Triplet) has the strongest evidence for user-defined few-shot keyword spotting?
>
> **Nguồn:** ~20 papers from arXiv, IEEE, ISCA 2017-2026.
> **Last updated:** 2026-07-06
> **Evidence Strength:** Moderate — nhiều paper nhưng chưa có so sánh trực tiếp giữa các methods trong cùng điều kiện.

---

## 1. Prototypical Networks

### 1.1. Papers sử dụng ProtoNet cho KWS

| Paper | Venue | Year | Kết quả | Ghi chú |
|---|---|---|---|---|
| Parnami & Lee | ICMLT | 2022 | ProtoNet + temporal conv cho FS-KWS | Foundational FS-KWS paper |
| Kim et al. (Dummy ProtoNets) | INTERSPEECH | 2022 | Dummy prototypes cho open-set | Mở rộng ProtoNet cho unknown |
| Yang et al. | INTERSPEECH | 2023 | Multi-task ProtoNet + auto-annotated data | Small footprint |
| Kao et al. | IEEE SLT | 2022 | HuBERT + ProtoNet/MatchingNet cho UDKWS | SSL + meta-learning |
| Rusci & Tuytelaars | INTERSPEECH | 2023 | ProtoNet vs Triplet cho on-device | Triplet > ProtoNet cho open-set |
| Chen et al. | IEEE Conf | 2024 | SSL pretrain + ProtoNet cho wake word | Non-top venue |

### 1.2. ProtoNet trong 2024-2026

- **Số lượng:** ~1-2 papers (non-top venue).
- **Xu hướng:** Giảm mạnh so với 2020-2022.
- **Nguyên nhân:** Cộng đồng chuyển sang:
  - Zero-shot text-based enrollment (audio-text embedding).
  - Open-vocabulary CTC-based KWS.
  - GE2E loss, ArcFace, contrastive learning.

### 1.3. Đánh giá

| Tiêu chí | Đánh giá |
|---|---|
| Còn valid cho audio enrollment? | ✅ Có — vẫn là baseline metric learning |
| Có bị reviewer reject không? | ❌ Không — nếu đặt đúng vai trò (baseline) |
| Có nên là primary method không? | 🟡 Có thể, nhưng cần alternative |

---

## 2. GE2E Loss

### 2.1. Papers sử dụng GE2E cho KWS

| Paper | Venue | Year | Kết quả | Ghi chú |
|---|---|---|---|---|
| Zhu et al. (GE2E-KWS) | IEEE SLT | 2024 | GE2E > Triplet: +60.7% AUC; 419KB quantized | **Paper chính** |
| Wan et al. (GE2E gốc) | ICASSP | 2018 | Generalized End-to-End loss cho speaker verification | Gốc |
| — | — | — | **Chưa có paper so sánh GE2E vs ProtoNet** | **GAP** |

### 2.2. Phân tích

- GE2E outperform triplet (Zhu 2024), nhưng:
  - So sánh trên zero-shot KWS, không phải few-shot KWS.
  - Chưa có paper nào so sánh GE2E vs ProtoNet trong cùng điều kiện.
- GE2E > Triplet không suy ra GE2E > ProtoNet.
- Cần benchmark riêng để kết luận.

**Kết luận: Chưa thể thay ProtoNet bằng GE2E. Cần ablation study.**

---

## 3. Triplet Loss

### 3.1. Papers sử dụng Triplet cho KWS

| Paper | Venue | Year | Kết quả |
|---|---|---|---|
| Vygon & Mikhaylovskiy | SPECOM | 2021 | 98.55% GSC V1, phonetic mining |
| Rusci & Tuytelaars | INTERSPEECH | 2023 | Triplet > ProtoNet cho open-set on-device |
| Li et al. (TCLP-KWS) | IEEE TASLP | 2025 | Triplet contrastive customizable KWS |

### 3.2. Đánh giá

- Triplet vẫn valid, đặc biệt cho open-set (Rusci 2023).
- Bị GE2E outperform (Zhu 2024).
- Nên giữ làm secondary method.

---

## 4. So sánh tổng hợp

| Method | Papers 2024-2026 | Edge Support | Open-set | So sánh trực tiếp |
|---|---|---|---|---|
| ProtoNet | 0-1 | ✅ (Yang 2023) | ✅ (Kim 2022) | Baseline |
| GE2E | 2-3 | ✅ (Zhu 2024, 419KB) | ✅ (implicitly) | Chưa so sánh với ProtoNet |
| Triplet | 2-3 | ✅ (Rusci 2023) | ✅ (Rusci 2023) | GE2E > Triplet (Zhu 2024) |

---

## 5. Contradictory Evidence

- Rusci 2023 cho thấy Triplet > ProtoNet cho open-set on-device KWS. Tuy nhiên, đây là bài toán open-set (có unknown class), không phải few-shot closed-set.
- Zhu 2024 cho thấy GE2E > Triplet, nhưng trên zero-shot KWS, không phải few-shot KWS.

---

## 5b. New Evidence from PLCL & CLAD (2024-2025)

| Paper | Finding | Impact |
|---|---|---|
| PLCL (Li 2025) | Phoneme-level contrastive outperforms utterance-level | 🔶 Consider phoneme-level for Vietnamese |
| CLAD (Xi 2024) | Audio-audio InfoNCE + sliding window for continuous speech | 🔶 Streaming pipeline reference |
| DMA-KWS (Ai 2026) | Dual-stage matching + phoneme-level verification | ✅ **97.85% AUC — SOTA framework** |
| ProKWS (Pan 2026) | Prosody + phoneme fusion for personalized KWS | 🔶 Important for Vietnamese (tonal) |

## 6. Remaining Gaps

- **Chưa có paper nào so sánh GE2E vs ProtoNet** trong cùng điều kiện (cùng backbone, cùng dataset, cùng shot setting).
- Chưa rõ GE2E có outperform ProtoNet trong audio enrollment setting không.

## 7. Evidence Strength

**Moderate.** Nhiều paper, quality venues, nhưng chưa có so sánh trực tiếp.

## 8. Impact on Our Project (not a decision)

- ProtoNet vẫn là baseline valid cho audio enrollment UDKWS.
- GE2E là ablation tiềm năng (chi phí thấp) nhưng chưa thể kết luận sẽ outperform.
- Triplet vẫn valid cho open-set scenario.
