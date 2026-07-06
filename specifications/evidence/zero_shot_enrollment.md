# Evidence: Zero-shot Text-based Enrollment

> **Research Question:** Does the rise of zero-shot text-based enrollment invalidate the audio enrollment approach in this project?
>
> **Nguồn:** ~15 papers 2024-2026.
> **Last updated:** 2026-07-06
> **Evidence Strength:** Strong for trend existence; Not applicable to project scope.

---

## 1. Papers tiêu biểu

| Paper | Venue | Year | Phương pháp |
|---|---|---|---|
| Text-aware adapter (Jung et al.) | ICASSP | 2025 | Text conditioning cho few-shot KWS |
| Custom wake word via audio-text (INTERSPEECH) | INTERSPEECH | 2024 | Audio-text embedding for custom KWS |
| Open-vocab adaptive instance norm (Navon et al.) | ICASSP | 2024 | Text encoder conditions audio encoder |
| Parallel-attention (Kim et al.) | IEEE SPL | 2024 | Audio-text bridging for user-defined KWS |
| SynaSpot (ICASSP) | ICASSP | 2026 | Multi-modal audio-text spotting |
| No Word Left Behind (ICASSP) | ICASSP | 2026 | Open-vocabulary KWS with text embedding |
| CLAP-IPA | — | 2025 | 95-language phoneme embedding |
| GLAP | — | 2025 | 50-language global phoneme embedding |

---

## 2. Phân tích bài toán

### 2.1. Audio Enrollment (luận văn)

| Thuộc tính | Giá trị |
|---|---|
| Input | Audio samples (user nói keyword) |
| User action | Thu âm 3-5 mẫu |
| Thiết bị yêu cầu | Microphone |
| Use case | Smart home không màn hình, voice-only interaction |
| Community trend | Đang giảm |

### 2.2. Zero-shot Text Enrollment (community trend)

| Thuộc tính | Giá trị |
|---|---|
| Input | Text (user gõ keyword) |
| User action | Gõ bàn phím / chọn từ danh sách |
| Thiết bị yêu cầu | Màn hình, bàn phím |
| Use case | Mobile app, smart display |
| Community trend | Đang tăng mạnh |

### 2.3. So sánh

| Tiêu chí | Audio Enrollment | Text Enrollment |
|---|---|---|
| Convenience | Thấp (cần thu âm) | Cao (chỉ cần gõ) |
| Personalization | Cao (giọng user) | Thấp (text không mang thông tin giọng) |
| Speaker adaptation | Có (enroll bằng giọng user) | Không (cần adaptation riêng) |
| Noise robustness | Phụ thuộc vào môi trường thu | Không liên quan |
| Phù hợp smart home | ✅ (voice-only) | ❌ (cần màn hình) |

---

## 3. Contradictory Evidence

- Text-based zero-shot enrollment đang là trend mạnh trong 2024-2026, có thể khiến reviewer hỏi "sao không làm zero-shot?"
- Tuy nhiên, đây là bài toán khác (khác assumption input), không phải evidence chống lại audio enrollment.

## 4. Remaining Gaps

- Chưa có paper nào so sánh trực tiếp audio enrollment vs text enrollment trong cùng điều kiện.
- Chưa rõ trade-off giữa convenience (text) và personalization (audio) cho smart home use case.

## 5. Evidence Strength

- **Trend existence:** Strong (~15 papers, quality venues).
- **Impact on our project:** Not applicable (different problem scope).

## 6. Impact on Our Project (not a decision)

- Trend này không invalidate luận văn.
- Cần có section trong Related Work giải thích scope: audio enrollment cho voice-only devices.
- Không cần thay đổi design.

---

## 4. Cách viết trong luận văn

> "While recent works have explored text-based zero-shot enrollment for KWS (Jung et al., 2025; Navon et al., 2024), our work focuses on audio-based enrollment which remains essential for voice-only interaction scenarios such as smart home devices without a display interface."
