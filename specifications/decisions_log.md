# Decisions Log

> **Mục đích:** Ghi lại mọi quyết định thiết kế, lý do, và evidence hỗ trợ.
>
> **Mỗi quyết định chỉ được thay đổi khi có evidence mới đủ mạnh.**
>
> Link tới `specifications/evidence/` để trace ngược.

---

## Cách sử dụng

Mỗi entry gồm:

| Trường | Ý nghĩa |
|---|---|
| **Date** | Ngày quyết định |
| **Decision** | Nội dung quyết định |
| **Reason** | Lý do ngắn gọn |
| **Evidence** | Link tới evidence file |
| **Status** | Active / Superseded / Deprecated |
| **Superseded by** | Nếu Status = Superseded, link tới decision mới |

---

## Decisions

| Date | Decision | Reason | Evidence | Status |
|---|---|---|---|---|
| 2026-07-06 | **Feature: Log-Mel → Primary** | MFCC không còn là primary feature trong 2024-2026 literature. Log-Mel là standard (28/33 papers). | feature_extraction.md | **Active (confirmed)** |
| 2026-07-06 | **Feature: PCEN → Ablation** | PCEN có noise robustness, zero inference cost. EdgeSpot 2026: +8.3% acc. | feature_extraction.md | **Active (confirmed)** |
| 2026-07-06 | **Feature: MFCC → Historical baseline** | Giữ lại để so sánh với literature cũ (5/33 papers, declining). | feature_extraction.md | **Active (confirmed)** |
| 2026-07-06 | **Metric Learning: ProtoNet → Primary baseline** | Chưa có evidence GE2E > ProtoNet trong audio enrollment. ProtoNet vẫn valid (7 papers). | proto_vs_ge2e.md | **Active (confirmed)** |
| 2026-07-06 | **Metric Learning: GE2E → Secondary ablation** | GE2E > Triplet (Zhu 2024), nhưng chưa so sánh với ProtoNet. Cần benchmark riêng. | proto_vs_ge2e.md | **Active (confirmed)** |
| 2026-07-06 | **Metric Learning: Triplet → Secondary** | Valid cho open-set (Rusci 2023). Bị GE2E outperform (+60.7% AUC). | proto_vs_ge2e.md | **Active (confirmed)** |
| 2026-07-06 | **Backbone: BC-ResNet-32 → Primary** | EdgeSpot 2026 xác nhận. 98.7% accuracy, 128K params, phù hợp edge. | backbone_models.md | **Active (confirmed)** |
| 2026-07-06 | **Backbone: DS-CNN → Baseline** | Hello Edge 2017, widely deployed (5 papers). | backbone_models.md | **Active (confirmed)** |
| 2026-07-06 | **Enrollment: Audio-based → Giữ nguyên** | Zero-shot text enrollment khác bài toán (cần màn hình). DMA-KWS confirms speech > text. | zero_shot_enrollment.md | **Active (confirmed)** |
| 2026-07-06 | **Evaluation Protocol → Contribution chính** | 18/18 papers use different protocols. Heterogeneity confirmed. | evaluation_protocol.md | **Active (confirmed)** |
| 2026-07-06 | **Edge: TFLite INT8 + RPi4 → Giữ nguyên** | De facto standard (10/12 edge papers). | deployment.md | **Active (confirmed)** |
| 2026-07-06 | **Vietnamese case study → Giữ nguyên** | 0 papers across all databases — genuine gap confirmed. | deployment.md | **Active (confirmed)** |
| 2026-07-06 | **Streaming pipeline → Giữ nguyên** | Chỉ 1/18 paper có streaming eval. Gap remains. | deployment.md | **Active (confirmed)** |
| 2026-07-06 | **Metrics: Thêm FAR-constrained** | Emerging standard (3 papers 2024-2026). | evaluation_protocol.md | **Active (confirmed)** |
| 2026-07-06 | **Knowledge Distillation → Optional ablation** | EdgeSpot 2026, Gok 2025: KD cải thiện edge accuracy. | deployment.md | **Active (confirmed)** |

---

## SLR Verification (2026-07-06)

All 15 decisions reviewed against 50-paper SLR. **Result: All 15 decisions confirmed as valid. No changes needed.**
