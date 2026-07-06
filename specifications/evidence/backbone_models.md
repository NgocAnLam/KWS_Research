# Evidence: Backbone Architectures

> **Research Question:** What lightweight backbone architectures are most effective for on-device keyword spotting?
>
> **Nguồn:** BC-ResNet (2021), Hello Edge (2017), EdgeSpot (2026), GE2E-KWS (2024), various 2024-2026 papers.
> **Last updated:** 2026-07-06
> **Evidence Strength:** Strong — BC-ResNet consistently leads accuracy/size trade-off.

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

## 4. Contradictory Evidence

- GE2E-KWS (Zhu 2024) dùng Conformer và cho thấy accuracy cao, nhưng chưa so sánh trực tiếp với BC-ResNet trên cùng dataset.
- MobileNetV2 tuy nặng (2.5M) nhưng có optimized version (α=0.35) có thể deploy được trên RPi4 với latency chấp nhận được (~30ms) nếu quantization tốt.

## 5. Remaining Gaps

- Chưa có so sánh trực tiếp BC-ResNet vs Conformer trên edge device.
- Chưa rõ BC-ResNet-32 có latency < 100ms trên RPi4 sau INT8 quantization không (cần benchmark).

## 6. Evidence Strength

**Strong.** BC-ResNet consistently leads accuracy/size trade-off.

## 7. Impact on Our Project (not a decision)

- BC-ResNet-32 là primary candidate hợp lý cho edge UDKWS.
- DS-CNN là baseline phổ biến.
- Conformer là hướng phát triển tương lai.
