# Community Trends & Design Impact Analysis (2024–2026)

> **Mục đích:** Tài liệu trung gian giữa SLR và Research Design. Phân tích xu hướng cộng đồng, đánh giá mức độ ảnh hưởng đến thiết kế luận văn.
> **Trạng thái:** Draft — chưa update vào summary_project.md. Sẽ cập nhật sau khi SLR hoàn thành.
> **Nguồn:** ~160 papers (92 arXiv + 68 non-arXiv) từ 2024–2026.

---

## 1. Phương pháp luận

Mỗi trend được đánh giá theo 3 tiêu chí:

| Tiêu chí | Ý nghĩa |
|---|---|
| **Bằng chứng** | Số lượng paper ủng hộ, chất lượng venue |
| **Mức độ áp dụng** | Đã là mainstream hay chỉ mới nổi |
| **Liên quan đến đề tài** | Ảnh hưởng trực tiếp đến design của luận văn |

Kết luận được phân loại:

| Loại | Ý nghĩa | Hành động |
|---|---|---|
| **✅ Confirmed** | Nhiều bằng chứng, consensus cao | Cần cập nhật design |
| **🔶 Emerging** | Đang tăng, chưa thống trị | Theo dõi, thêm ablation/tham khảo |
| **❌ Unsubstantiated** | Chưa đủ bằng chứng | Không hành động, cần thêm dữ liệu |
| **ℹ️ Not applicable** | Không liên quan đến bài toán | Ghi nhận, không thay đổi |

---

## 2. Metric Learning Methods

### 2.1. Prototypical Networks

| Tiêu chí | Đánh giá |
|---|---|
| Số paper 2024-2026 | ~1-2 (non-top venue) |
| Paper dùng ProtoNet cho UDKWS | Parnami 2022, Kim 2022, Rusci 2023 (so sánh), Yang 2023 |
| Community consensus | Đang giảm, nhưng chưa "chết" |

**Phân tích:**
- ProtoNet ít xuất hiện trong 2024-2026 vì cộng đồng chuyển sang bài toán zero-shot text-based, open-vocabulary CTC, và các loss function mới (GE2E, ArcFace).
- ProtoNet vẫn là **baseline kinh điển** trong metric learning. Reviewer sẽ không reject vì dùng ProtoNet — miễn là nó được đặt đúng vai trò (baseline, không phải SOTA claim).
- Trong bài toán **cụ thể của luận văn** (audio enrollment UDKWS on Edge), ProtoNet vẫn là phương pháp hợp lệ.

**Kết luận: 🔶 Emerging — Không thay ngay, nhưng cần thêm alternative**

| Hành động | Mức ưu tiên |
|---|---|
| Giữ ProtoNet làm baseline cho factorial experiment | ✅ Giữ |
| Thêm GE2E loss như primary/secondary method (cùng 3 seeds) | 🔶 Nên thêm (ablation) |
| Không xóa ProtoNet | ✅ |

### 2.2. GE2E Loss

| Tiêu chí | Đánh giá |
|---|---|
| Số paper 2024-2026 | ~3-4 (SLT 2024, ICASSP 2024-2026) |
| Paper chính | Zhu 2024 (GE2E-KWS: beat triplet 60.7% AUC) |
| So sánh với ProtoNet | **Chưa có paper nào so sánh GE2E vs ProtoNet trong cùng benchmark** |

**Phân tích:**
- GE2E outperform triplet (Zhu 2024), nhưng chưa outperform ProtoNet.
- "GE2E > Triplet" không suy ra "GE2E > ProtoNet".
- Cần thận trọng trước khi thay ProtoNet bằng GE2E.

**Kết luận: 🔶 Emerging — Thêm làm ablation, chưa thay thế**

| Hành động | Mức ưu tiên |
|---|---|
| Thêm GE2E loss làm secondary method (1 seed) | 🔶 Nên thêm |
| Giữ ProtoNet làm primary | ✅ Giữ |
| Sau benchmark mới kết luận | ✅ |

### 2.3. Triplet Loss

| Tiêu chí | Đánh giá |
|---|---|
| Số paper 2024-2026 | Giảm mạnh, nhưng vẫn xuất hiện |
| Edge support | Rusci 2023: triplet outperform ProtoNet cho open-set on-device |

**Kết luận: ℹ️ Giữ nguyên secondary — valid cho open-set edge scenario**

---

## 3. Feature Extraction

### 3.1. MFCC

| Tiêu chí | Đánh giá |
|---|---|
| Số paper 2024-2026 dùng MFCC primary | Gần như 0 |
| Paper dùng MFCC | Mostly pre-2022, hoặc historical baseline |

**Phân tích:**
- Log-Mel (40-80 dim) là tối thiểu trong 2024-2026.
- MFCC vẫn có giá trị để so sánh với literature cũ.

**Kết luận: ✅ Confirmed — cần điều chỉnh**

| Hành động | Mức ưu tiên |
|---|---|
| Log-Mel → Primary feature | ✅ Thay đổi |
| MFCC → Historical baseline (không xóa) | ✅ Giữ để so sánh |
| PCEN → Secondary/Ablation | ✅ Thêm |

### 3.2. PCEN

| Tiêu chí | Đánh giá |
|---|---|
| Số paper 2024-2026 | EdgeSpot 2026 (ICASSP), Wang 2017 (ICASSP) |
| Edge cost | Zero inference cost (trainable parameters only) |
| Accuracy impact | +2-3% trong noisy conditions |

**Kết luận: 🔶 Emerging — Thêm làm ablation (chi phí thấp, lợi ích tiềm năng)**

### 3.3. Learnable Frontends (LEAF, SincNet)

| Tiêu chí | Đánh giá |
|---|---|
| Phân tích 2024 | LEAF paper (2024) cho thấy phần lớn lợi ích đến từ PCEN layer |

**Kết luận: ℹ️ Future work — Không thêm vào benchmark chính**

---

## 4. Zero-shot Text-based Enrollment

### 4.1. Mức độ phổ biến

| Tiêu chí | Đánh giá |
|---|---|
| Số paper 2024-2026 | ~15 papers (INTERSPEECH, ICASSP, IEEE SPL, TASLP) |
| Venue quality | ICASSP, INTERSPEECH, IEEE TASLP — quality venues |
| Phương pháp | CLAP, Sentence-BERT, phoneme embeddings + projection |

### 4.2. Phân biệt bài toán

| Bài toán | Assumption | Input | Phù hợp luận văn? |
|---|---|---|---|
| **Audio enrollment** (luận văn) | User có thiết bị thu âm | Audio samples | ✅ **Trong phạm vi** |
| **Text-based zero-shot** (community trend) | User có bàn phím/màn hình | Text | ❌ **Ngoài phạm vi** (khác assumption) |

**Phân tích:**
- Zero-shot text enrollment giải quyết bài toán khác: user gõ keyword → detect.
- Luận văn giải quyết bài toán: user nói keyword → detect.
- Hai hướng không loại trừ nhau. Zero-shot tiện hơn nhưng không phải lúc nào cũng khả thi (smart home devices không có màn hình).

**Kết luận: ℹ️ Not applicable — Ghi nhận trong Related Work, không thay đổi design**

| Hành động | Mức ưu tiên |
|---|---|
| Thêm section "Text-based Enrollment Approaches" trong Related Work | ✅ Nên làm |
| Giải thích scope: audio enrollment là primary use case | ✅ |
| Không thay đổi design | ✅ |

---

## 5. Lightweight Backbones

### 5.1. BC-ResNet

| Tiêu chí | Đánh giá |
|---|---|
| Số paper | Kim 2021 (INTERSPEECH), EdgeSpot 2026 (ICASSP) |
| GSCv2 accuracy | 98.7% |
| Edge viability | 128K params (EdgeSpot-4), ~10ms RPi4 |

**Kết luận: ✅ Confirmed — Giữ nguyên**

### 5.2. DS-CNN

| Tiêu chí | Đánh giá |
|---|---|
| Vai trò 2024-2026 | Baseline, ít được dùng trong SOTA papers |

**Kết luận: ℹ️ Giữ làm baseline — valid cho edge comparison**

### 5.3. Conformer / Transformer

| Tiêu chí | Đánh giá |
|---|---|
| Số paper | GE2E-KWS (Conformer), SIDC-KWS (Spiking Neural Conformer) |
| Edge viability | GE2E-KWS: 419KB quantized Conformer |
| So sánh với BC-ResNet | Chưa có so sánh trực tiếp trên cùng task |

**Kết luận: 🔶 Emerging — Theo dõi, thêm vào future work**

---

## 6. Evaluation Protocol

### 6.1. Hiện trạng

| Protocol | Papers | Ghi chú |
|---|---|---|
| Episode-based | Parnami 2022, Kim 2022 | Few-shot setting |
| FAR-constrained | EdgeSpot 2026, GE2E-KWS 2024 | acc@1% FAR, acc@5% FAR |
| Streaming | GE2E-KWS 2024 | FA/hour, Detection Latency |
| Enrollment | Rất ít paper | Không có unified protocol |

### 6.2. Impact on design

**Kết luận: ✅ Confirmed — Evaluation Protocol là contribution mạnh**

| Hành động | Mức ưu tiên |
|---|---|
| Giữ nguyên protocol design | ✅ |
| Thêm FAR-constrained metrics (acc@1% FAR, acc@5% FAR) | 🔶 Nên thêm |
| Streaming metrics (FA/hour, RTF) đã có | ✅ |

---

## 7. Vietnamese KWS Gap

| Tiêu chí | Đánh giá |
|---|---|
| Số paper UDKWS tiếng Việt 2024-2026 | **0** |
| Số paper Vietnamese ASR | VIVOS, Common Voice Vietnamese (ASR, không phải KWS) |
| Mức độ tin cậy | Cao — search trên arXiv, IEEE, Google Scholar đều không có |

**Kết luận: ✅ Confirmed — Genuine research gap**

| Hành động | Mức ưu tiên |
|---|---|
| Giữ nguyên Vietnamese case study | ✅ |
| Viết gap cẩn thận: "To the best of our knowledge..." | ✅ |

---

## 8. Training Strategies

### 8.1. SSL Pretrain + Fine-tune

| Tiêu chí | Đánh giá |
|---|---|
| Số paper | Kao 2022, Gok 2025, MT-HuBERT 2025 |
| Hiệu quả | 33.4% → 74.1% (Gok 2025) |
| Edge compatibility | Cần knowledge distillation (EdgeSpot, Gok 2025) |

**Kết luận: 🔶 Emerging — Thêm ablation nếu có compute budget**

| Hành động | Mức ưu tiên |
|---|---|
| Giữ training strategy ablation (Scratch vs FT vs Freeze) | ✅ |
| Thêm SSL pretrain (HuBERT) + KD → edge | 🔶 Optional ablation |

---

## 9. Tổng hợp thay đổi cần thiết

### 9.1. Thay đổi bắt buộc (Confirmed)

| Thay đổi | Lý do | Phần trong design |
|---|---|---|
| Log-Mel → Primary feature | MFCC không còn dùng trong 2024-2026 | §10 Feature Extraction |

### 9.2. Thay đổi khuyến nghị (Emerging)

| Thay đổi | Lý do | Mức ưu tiên |
|---|---|---|
| PCEN → Secondary/Ablation | Chi phí thấp, có evidence từ EdgeSpot 2026 | Nên thêm |
| GE2E loss → Secondary method | Chưa có so sánh GE2E vs ProtoNet, nhưng là hướng mới | Nên thêm (1 seed) |
| FAR-constrained metrics | Standard mới trong evaluation | Nên thêm |
| SSL pretrain + KD ablation | Có evidence mạnh từ 2024-2026 | Optional |

### 9.3. Không thay đổi

| Quyết định | Lý do |
|---|---|
| Giữ ProtoNet làm primary baseline | Vẫn valid cho bài toán audio enrollment; GE2E vs ProtoNet chưa được so sánh |
| Giữ enrollment workflow (audio) | Khác assumption với zero-shot text-based |
| Giữ BC-ResNet-32 làm backbone chính | Được EdgeSpot 2026 xác nhận |
| Giữ DS-CNN làm baseline | Valid cho edge comparison |
| Giữ MFCC trong benchmark | Historical baseline để kết nối với literature cũ |
| Giữ streaming pipeline design | Vẫn là hướng đúng cho edge deployment |

---

## 10. Cập nhật Research Design (sau khi SLR hoàn thành)

Sau khi hoàn thành SLR, `summary_project.md` sẽ được cập nhật 1 lần duy nhất với các thay đổi sau:

```diff
- Primary features: MFCC, Log-Mel
+ Primary features: Log-Mel, PCEN (ablation)
+ Historical baseline: MFCC

- Metric learning: ProtoNet (primary, 3 seeds), Siamese (secondary, 1 seed), Triplet (secondary, 1 seed)
+ Metric learning: ProtoNet (primary, 3 seeds), GE2E (secondary, 1 seed), Triplet (secondary, 1 seed)

- Metrics: Accuracy, F1, EER
+ Metrics: Accuracy, F1, EER, acc@1% FAR, acc@5% FAR
```

---

## 11. Tham khảo

Các paper chính hỗ trợ cho các kết luận trên:

| Paper | Venue | Year | Hỗ trợ cho |
|---|---|---|---|
| EdgeSpot (Buyuksolak et al.) | ICASSP | 2026 | BC-ResNet + PCEN + KD on edge |
| GE2E-KWS (Zhu et al.) | IEEE SLT | 2024 | GE2E loss, streaming eval, FAR-constrained metrics |
| BC-ResNet (Kim et al.) | INTERSPEECH | 2021 | Backbone architecture |
| Hello Edge (Zhang et al.) | arXiv | 2017 | DS-CNN edge baseline |
| PCEN (Wang et al.) | ICASSP | 2017 | PCEN dynamic compression |
| TCLP-KWS (Li et al.) | IEEE TASLP | 2025 | Triplet contrastive customizable KWS |
| Text-aware adapter (Jung et al.) | ICASSP | 2025 | Text conditioning (zero-shot direction) |
| Contrastive customizable KWS (Xi et al.) | ICASSP | 2024 | User-defined KWS in continuous speech |
| SSL + Meta-learning (Kao et al.) | IEEE SLT | 2022 | HuBERT + ProtoNet for UDKWS |
| Few-shot open-set on-device (Rusci et al.) | INTERSPEECH | 2023 | Triplet > ProtoNet for open-set on edge |
