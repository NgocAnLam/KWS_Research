# Evidence: Feature Extraction (MFCC vs Log-Mel vs PCEN)

> **Mục đích:** Tổng hợp bằng chứng về feature extraction methods cho KWS.
> **Nguồn:** ~160 papers 2024-2026, foundational papers from 2017.
> **Last updated:** 2026-07-06

---

## 1. MFCC

### 1.1. Papers dùng MFCC làm primary feature trong 2024-2026

| Kết quả | Số lượng |
|---|---|
| Papers dùng MFCC làm primary | **Gần như 0** |
| Papers dùng MFCC làm historical baseline | ~2-3 |

### 1.2. Phân tích

- MFCC (13 coefficients) từng là standard cho KWS (pre-2022).
- Từ 2024, hầu hết papers dùng Log-Mel (40-80 dim) hoặc learnable frontends.
- MFCC vẫn có giá trị để:
  - So sánh với literature cũ.
  - Baseline cho feature comparison.
  - Edge deployment (13 dim → nhanh hơn).

**Kết luận: Không còn là primary feature, nhưng nên giữ làm historical baseline.**

---

## 2. Log-Mel Spectrogram

### 2.1. Papers dùng Log-Mel trong 2024-2026

| Paper | Venue | Year | Parameters |
|---|---|---|---|
| BC-ResNet (Kim et al.) | INTERSPEECH | 2021 | 40 mel bins |
| EdgeSpot (Buyuksolak et al.) | ICASSP | 2026 | 40 mel bins + PCEN |
| GE2E-KWS (Zhu et al.) | IEEE SLT | 2024 | 80 mel bins |
| Hầu hết papers 2024-2026 | — | — | 40-80 mel bins |

### 2.2. Đánh giá

- Log-Mel là feature chuẩn trong 2024-2026.
- 40 bins là phổ biến nhất (cân bằng accuracy vs compute).
- 80 bins cho accuracy cao hơn nhưng tăng kích thước input.

**Kết luận: Log-Mel là primary feature choice.**

---

## 3. PCEN

### 3.1. Papers sử dụng PCEN

| Paper | Venue | Year | Kết quả |
|---|---|---|---|
| Wang et al. (PCEN gốc) | ICASSP | 2017 | Per-channel energy normalization, dynamic compression |
| EdgeSpot (Buyuksolak et al.) | ICASSP | 2026 | PCEN + BC-ResNet, +2-3% trong noisy conditions |
| LEAF analysis (2024) | — | 2024 | Most of LEAF's benefit comes from PCEN layer |

### 3.2. Đặc điểm

| Đặc điểm | Giá trị |
|---|---|
| Inference cost | Zero (trainable parameters only) |
| Noise robustness | +2-3% trong noisy conditions |
| Edge compatibility | ✅ (trainable, không tăng inference latency) |
| Implementation complexity | Thấp (thay thế log compression) |

**Kết luận: PCEN là ablation chi phí thấp, lợi ích tiềm năng cao. Nên thêm.**

---

## 4. So sánh tổng hợp

| Feature | Popularity 2024-2026 | Edge Cost | Noise Robustness | Recommendation |
|---|---|---|---|---|
| Log-Mel | ★★★★★ (standard) | Thấp | Trung bình | **Primary** |
| PCEN | ★★★☆☆ (growing) | Zero | Cao | **Ablation** |
| MFCC | ★☆☆☆☆ (declining) | Thấp nhất | Thấp | **Historical baseline** |

---

## 5. Kết luận cho thiết kế

| Quyết định | Mức độ chắc chắn | Cơ sở |
|---|---|---|
| Log-Mel → Primary | ✅ Cao | Consensus 2024-2026 literature |
| PCEN → Ablation | 🔶 Trung bình | EdgeSpot 2026, cost thấp |
| MFCC → Historical baseline | ✅ Cao | Không còn dùng primary, nhưng valid cho so sánh |
| Xóa MFCC | ❌ Không nên | Mất kết nối với literature cũ |
