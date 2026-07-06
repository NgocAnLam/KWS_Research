# Evidence: Evaluation Protocols

> **Mục đích:** Đánh giá hiện trạng evaluation protocols trong literature và xác định contribution.
> **Nguồn:** ~30 papers từ few-shot KWS và UDKWS literature.
> **Last updated:** 2026-07-06

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

## 3. Kết luận cho thiết kế

| Quyết định | Mức độ chắc chắn | Cơ sở |
|---|---|---|
| Evaluation Protocol là contribution mạnh | ✅ Cao | Không có unified protocol trong literature |
| Giữ episode-based cho Stage 1 | ✅ Cao | Standard trong few-shot literature |
| Giữ streaming eval cho Stage 2 | ✅ Cao | Chỉ GE2E-KWS 2024 có streaming |
| Thêm FAR-constrained metrics | 🔶 Nên thêm | EdgeSpot 2026, GE2E-KWS 2024 dùng |
| Thêm speaker leakage analysis | ✅ Đã có | Rusci 2023 là reference duy nhất |
| Public code/config | ✅ Đã có trong reproducibility section | Không paper nào làm đầy đủ |
