# Evidence: Backbone Architectures

> **Mục đích:** So sánh các backbone architectures cho KWS trên edge devices.
> **Nguồn:** BC-ResNet (2021), Hello Edge (2017), EdgeSpot (2026), GE2E-KWS (2024), various 2024-2026 papers.
> **Last updated:** 2026-07-06

---

## 1. So sánh các backbone

| Backbone | Params | GSCv2 Acc | MACs | Edge Latency | Venue/Year |
|---|---|---|---|---|---|
| **DS-CNN** (Zhang) | 20K-80K | 95.4% | ~5M | ~2ms (MCU) | arXiv 2017 |
| **BC-ResNet-8** (Kim) | 27K | 97.0% | — | — | INTERSPEECH 2021 |
| **BC-ResNet-16** (Kim) | 56K | 98.2% | — | — | INTERSPEECH 2021 |
| **BC-ResNet-32** (Kim) | 110K | 98.7% | — | ~10ms (RPi4) | INTERSPEECH 2021 |
| **EdgeSpot-4** (Buyuksolak) | 128K | 82%@1%FAR (10-shot) | 29.4M | — | ICASSP 2026 |
| **MobileNetV2 α=0.35** | 2.5M | ~93% | ~300M | ~30ms (RPi4) | — |
| **Conformer (GE2E-KWS)** | — | Beat ASR encoder by 23.6% | — | 419KB quantized | IEEE SLT 2024 |
| **Tiny CNN** | ~80K | ~92% | — | ~1ms | — |

---

## 2. Phân tích

### 2.1. BC-ResNet-32
- **Accuracy cao nhất** trong các lightweight backbone (98.7% GSCv2).
- Được EdgeSpot 2026 (ICASSP) sử dụng và xác nhận.
- Bottleneck + depthwise conv → phù hợp edge.
- **Kết luận: Lựa chọn tối ưu cho luận văn.**

### 2.2. DS-CNN
- **Được triển khai rộng rãi nhất** trên edge (MCU, RPi).
- Accuracy thấp hơn BC-ResNet (~95.4% vs 98.7%).
- **Kết luận: Baseline tốt cho edge comparison.**

### 2.3. Conformer
- Accuracy cao (GE2E-KWS 2024).
- Nặng hơn BC-ResNet, cần quantization để deploy.
- Chưa có so sánh trực tiếp BC-ResNet vs Conformer trên edge.
- **Kết luận: Future work.**

### 2.4. MobileNetV2
- 2.5M params → quá nặng cho Raspberry Pi 4 real-time.
- **Kết luận: Có thể bỏ khỏi benchmark chính.**

---

## 3. Kết luận cho thiết kế

| Quyết định | Mức độ chắc chắn | Cơ sở |
|---|---|---|
| BC-ResNet-32 → Primary backbone | ✅ Cao | EdgeSpot 2026, accuracy 98.7% |
| DS-CNN → Baseline | ✅ Cao | Hello Edge 2017, widely deployed |
| Tiny CNN → Baseline | 🟡 Có thể giữ | Simple, interpretable |
| MobileNetV2 → Cân nhắc bỏ | 🟡 Có thể bỏ | Quá nặng cho Pi 4 |
| Conformer → Future work | ✅ | Chưa có edge benchmark |
