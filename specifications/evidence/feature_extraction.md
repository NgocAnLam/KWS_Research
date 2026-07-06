# Evidence: Feature Extraction (MFCC vs Log-Mel vs PCEN)

> **Research Question:** What audio features are most effective for keyword spotting in 2024-2026 literature?
>
> **Nguồn:** ~160 papers 2024-2026, foundational papers from 2017.
> **Last updated:** 2026-07-06
> **Evidence Strength:** Strong — large consensus across many papers and venues.

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
|---|---|---|---|---|---|
| Log-Mel | ★★★★★ (standard) | Thấp | Trung bình | **Primary** |
| PCEN | ★★★☆☆ (growing) | Zero | Cao | **Ablation** |
| MFCC | ★☆☆☆☆ (declining) | Thấp nhất | Thấp | **Historical baseline** |

---

## 5. Contradictory Evidence

- MFCC vẫn được dùng trong một số paper edge deployment cũ (pre-2022) do số chiều thấp → latency thấp hơn.
- PCEN tuy có noise robustness nhưng chưa được adopt rộng rãi (chỉ EdgeSpot 2026 và Wang 2017).
- Log-Mel vs PCEN chưa được so sánh trực tiếp trong few-shot KWS setting (EdgeSpot dùng cả Log-Mel + PCEN).

## 5b. New Evidence from EdgeSpot (ICASSP 2026)

| Finding | Impact |
|---|---|
| PCEN + BC-ResNet: +8.3% acc @1% FAR vs BC-ResNet alone (82.0% vs 73.7%) | ✅ **Strong evidence for PCEN in FS-KWS** |
| PCEN improves cross-domain generalization (MSWC → GSC) | ✅ **PCEN beneficial for domain shift** |
| PCEN trained end-to-end, all parameters differentiable | ✅ **Zero inference cost** |
| Uses 40-band Log-Mel → PCEN (not replace, augment) | ✅ **Log-Mel + PCEN combination validated** |

## 6. Remaining Gaps

- Chưa có paper so sánh Log-Mel vs PCEN trong few-shot KWS (chỉ có trong closed-set KWS).
- Chưa rõ PCEN có lợi thế đáng kể trong môi trường ít noise hay không.
- EdgeSpot kết hợp PCEN với KD từ SSL teacher — không rõ PCEN đóng góp bao nhiêu nếu không có KD.

## 7. Evidence Strength

**Strong.** Consensus rộng khắp 2024-2026 literature. EdgeSpot (2026) cung cấp evidence trực tiếp cho PCEN trong FS-KWS.

## 8. Impact on Our Project (not a decision)

- Log-Mel là primary feature hợp lý.
- PCEN là ablation chi phí thấp, tiềm năng cao — EdgeSpot chứng minh +8.3% trong FS-KWS.
- MFCC nên giữ làm historical baseline để kết nối với literature cũ.
