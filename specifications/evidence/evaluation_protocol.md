# Evidence: Evaluation Protocols

> **Research Question:** Is there a unified evaluation protocol for user-defined few-shot keyword spotting?
>
> **Nguồn:** ~30 papers từ few-shot KWS và UDKWS literature.
> **Last updated:** 2026-07-06
> **Evidence Strength:** Strong — heterogeneity confirmed across all papers surveyed.

---

## 1. Hiện trạng: Heterogeneous Protocols

| Paper | Split Method | Metrics | Evaluation Mode | Streaming? |
|---|---|---|---|---|
| Parnami 2022 | 5-way episode | Accuracy | Offline | No |
| Kim 2022 (Dummy ProtoNets) | Leave-out classes | Accuracy, F1 | Offline | No |
| Rusci 2023 | Leave-out + FAR | Accuracy, FAR, FRR | Offline (enrollment) | No |
| EdgeSpot 2026 | Multi-speaker subset | Accuracy@1%FAR, AUC | Offline (enrollment) | No |
| GE2E-KWS 2024 | Custom split | Accuracy, AUC, FAR | Offline + streaming | Yes |
| Vygon 2021 | GSC standard | Accuracy | Offline | No |
| Yang 2023 | Episode + FAR | Accuracy, FAR | Offline | No |
| TCLP-KWS 2025 | Leave-out | Accuracy, EER | Offline | No |

---

## 2. Phân tích

### 2.1. Vấn đề

| Vấn đề | Biểu hiện | Impact |
|---|---|---|
| Split khác nhau | 5-way episode, leave-out, custom split | Không so sánh được kết quả giữa các paper |
| Metrics khác nhau | Accuracy, AUC, EER, FAR, F1 | Cùng accuracy không có ý nghĩa nếu khác FAR |
| Enrollment mode khác nhau | Episode (hỗ trợ/query), enrollment (3/5/10-shot) | Không clear protocol |
| Streaming eval | Chỉ GE2E-KWS 2024 có streaming evaluation | Thiếu benchmark cho edge deployment |

### 2.2. Cơ hội

| Cơ hội | Mô tả |
|---|---|
| Unified protocol | Chưa có paper nào đề xuất protocol thống nhất cho UDKWS |
| Enrollment + streaming | Chưa có paper nào kết hợp cả enrollment workflow và streaming eval |
| Speaker leakage analysis | Rất ít paper đề cập (chỉ Rusci 2023 có phân tích) |
| Reproducibility checklist | Hầu hết paper không public code/config/seed |

---

## 3. Contradictory Evidence

- GE2E-KWS (Zhu 2024) có streaming evaluation, nhưng chỉ là 1 paper — chưa đủ để gọi là standard.
- EdgeSpot (2026) có FAR-constrained metrics, nhưng không có streaming eval.

## 4. Remaining Gaps

- Chưa có paper nào đề xuất unified protocol kết hợp: episode-based benchmark + enrollment workflow + streaming evaluation.
- Chưa có paper nào công bố public code/config/seed cho KWS experiments.

## 5. Evidence Strength

**Strong.** Heterogeneity confirmed across all papers surveyed.

## 6. Impact on Our Project (not a decision)

- Unified protocol là contribution tiềm năng mạnh.
- FAR-constrained metrics là standard mới nên thêm.
- Streaming evaluation protocol vẫn còn gap trong literature.
