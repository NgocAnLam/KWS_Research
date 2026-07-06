# Evidence: Edge Deployment & Vietnamese KWS

> **Mục đích:** Tổng hợp bằng chứng về edge deployment approaches và Vietnamese KWS gap.
> **Nguồn:** ~30 papers 2017-2026.
> **Last updated:** 2026-07-06

---

## 1. Edge Deployment Approaches

### 1.1. Papers tiêu biểu

| Paper | Device | Framework | Model Size | Latency | Accuracy |
|---|---|---|---|---|---|
| Hello Edge (Zhang 2017) | MCU (STM32) | TFLite Micro | 250KB | ~20ms | 95.4% |
| Rusci 2023 | MCU | TFLite | — | — | 76%@5%FAR |
| GE2E-KWS (Zhu 2024) | Mobile | TFLite INT8 | 419KB | Real-time | Beat 7.5GB ASR |
| EdgeSpot (Buyuksolak 2026) | Edge device | TFLite INT8 | 128K params | — | 82%@1%FAR |
| DS-CNN (various) | RPi4, MCU | TFLite | 20K-80K | 2-50ms | 95.4% |

### 1.2. TFLite INT8 Quantization

| Khía cạnh | Đánh giá |
|---|---|
| Mức độ phổ biến | De facto standard cho edge KWS |
| Accuracy degradation | 1-3% (có thể giảm bằng quantization-aware training) |
| Công cụ hỗ trợ | TFLite Converter, TFLite Micro, TFLite Runtime |

### 1.3. Raspberry Pi 4 Specs trong literature

| Thông số | Giá trị |
|---|---|
| CPU | ARM Cortex-A72, 4 cores @ 1.8GHz |
| RAM | 1-8GB (4GB phổ biến) |
| OS | Raspberry Pi OS (64-bit) |
| Framework | TFLite Runtime |
| Typical latency | 10-50ms (backbone dependent) |

---

## 2. Vietnamese KWS Gap

### 2.1. Search Results

| Search Query | Source | Results |
|---|---|---|
| "Vietnamese keyword spotting" | arXiv | 0 |
| "Vietnamese" + "keyword spotting" | IEEE Xplore | 0 |
| "Vietnamese" + "wake word" | Google Scholar | 0 |
| "tiếng Việt" + "keyword spotting" | Google Scholar | 0 |
| "Vietnamese speech commands" | All | 0 |

### 2.2. Existing Vietnamese Speech Resources (không phải KWS)

| Resource | Task | Ghi chú |
|---|---|---|
| VIVOS | ASR (Reading Speech) | 15 speakers, not KWS |
| Common Voice Vietnamese | ASR (Crowdsourced) | Mozilla, not KWS |
| PhoWhisper | ASR (Whisper fine-tune) | Not KWS |
| VietTTS | TTS | Not KWS |
| VSLP | ASR | Not KWS |

### 2.3. Kết luận

| Khẳng định | Evidence |
|---|---|
| Không có dataset UDKWS tiếng Việt | ✅ Confirmed (0 papers) |
| Không có research framework UDKWS tiếng Việt | ✅ Confirmed (0 papers) |
| Vietnamese KWS là research gap | ✅ Confirmed |

---

## 3. Kết luận cho thiết kế

| Quyết định | Mức độ chắc chắn | Cơ sở |
|---|---|---|
| Giữ TFLite INT8 làm deployment framework | ✅ Cao | De facto standard |
| Giữ Raspberry Pi 4 làm target device | ✅ Cao | Phổ biến trong literature |
| Giữ streaming pipeline design | ✅ Cao | Chỉ GE2E-KWS 2024 có streaming |
| Giữ Vietnamese case study | ✅ Cao | Zero existing work — genuine gap |
| Thêm knowledge distillation ablation | 🔶 Nên thêm | EdgeSpot 2026, Gok 2025 |
