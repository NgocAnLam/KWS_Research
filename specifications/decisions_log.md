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
| 2026-07-06 | **Feature: Log-Mel → Primary** | MFCC không còn là primary feature trong 2024-2026 literature. Log-Mel là standard. | feature_extraction.md | Active |
| 2026-07-06 | **Feature: PCEN → Ablation** | PCEN có noise robustness, zero inference cost. EdgeSpot 2026 xác nhận. | feature_extraction.md | Active |
| 2026-07-06 | **Feature: MFCC → Historical baseline** | Giữ lại để so sánh với literature cũ, không xóa. | feature_extraction.md | Active |
| 2026-07-06 | **Metric Learning: ProtoNet → Primary baseline** | Chưa có evidence GE2E > ProtoNet trong audio enrollment. ProtoNet vẫn valid. | proto_vs_ge2e.md | Active |
| 2026-07-06 | **Metric Learning: GE2E → Secondary ablation** | GE2E > Triplet (Zhu 2024), nhưng chưa so sánh với ProtoNet. Cần benchmark riêng. | proto_vs_ge2e.md | Active |
| 2026-07-06 | **Metric Learning: Triplet → Secondary** | Valid cho open-set (Rusci 2023). Bị GE2E outperform. | proto_vs_ge2e.md | Active |
| 2026-07-06 | **Backbone: BC-ResNet-32 → Primary** | EdgeSpot 2026 xác nhận. 98.7% accuracy, phù hợp edge. | backbone_models.md | Active |
| 2026-07-06 | **Backbone: DS-CNN → Baseline** | Hello Edge 2017, widely deployed. Valid cho edge comparison. | backbone_models.md | Active |
| 2026-07-06 | **Enrollment: Audio-based → Giữ nguyên** | Zero-shot text enrollment khác bài toán (cần màn hình). Scope đã định. | zero_shot_enrollment.md | Active |
| 2026-07-06 | **Evaluation Protocol → Contribution chính** | Không có unified protocol trong literature. Protocol thay đổi chậm hơn model. | evaluation_protocol.md | Active |
| 2026-07-06 | **Edge: TFLite INT8 + RPi4 → Giữ nguyên** | De facto standard. EdgeSpot, GE2E-KWS đều dùng. | deployment.md | Active |
| 2026-07-06 | **Vietnamese case study → Giữ nguyên** | Zero existing Vietnamese KWS papers — genuine gap. | deployment.md | Active |
| 2026-07-06 | **Streaming pipeline → Giữ nguyên** | Chỉ GE2E-KWS 2024 có streaming eval. Còn gap. | deployment.md | Active |
| 2026-07-06 | **Metrics: Thêm FAR-constrained** | Standard mới (EdgeSpot 2026, GE2E-KWS 2024). | evaluation_protocol.md | Active |
| 2026-07-06 | **Knowledge Distillation → Optional ablation** | EdgeSpot 2026, Gok 2025 cho thấy KD cải thiện edge accuracy. | deployment.md | Active |
