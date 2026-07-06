# Evidence: Zero-shot Text-based Enrollment

> **Research Question:** Does the rise of zero-shot text-based enrollment invalidate the audio enrollment approach in this project?
> **Nguồn:** 50 papers surveyed, 8 text-enrollment-specific papers
> **Last updated:** 2026-07-06 (post-SLR consolidation)

---

## 1. Text-based Enrollment Papers (2024-2026)

| Paper | Venue | Method | Enrollment Type |
|---|---|---|---|
| **Text-aware adapter** (Jung 2025) | ICASSP 2025 | Adapter + text encoder | Text (0.14% params) |
| **ParallelKWS** (Kim 2024) | IEEE SPL 2024 | Parallel attention + phoneme alignment | Text |
| **AdaKWS** (Navon 2024) | ICASSP 2024 | AdaIN text conditioning | Text |
| **MM-KWS** (Ai 2024) | INTERSPEECH 2024 | Multi-modal (text + phoneme) prompts | Text + Phoneme |
| **CLAD** (Xi 2024) | ICASSP 2024 | InfoNCE audio-text pairs | Text + Audio |
| **PLCL** (Li 2025) | ICASSP 2025 | Phoneme-level contrastive | **Flexible (Text OR Audio)** |
| **DMA-KWS** (Ai 2026) | IEEE TASLP 2026 | Multi-modal (speech + text) enrollment | **Speech + Text** |
| **ProKWS** (Pan 2026) | ICASSP 2026 | Phoneme + prosody | Audio |

---

## 2. Key Finding: Two Distinct Problems

| Aspect | Audio Enrollment (Our Project) | Text Enrollment (Trend) |
|---|---|---|
| **Input** | User speaks keyword | User types keyword |
| **Interaction** | Voice-only (no screen needed) | Requires screen/keyboard |
| **Personalization** | Captures speaker voice | Speaker-independent |
| **Convenience** | Lower (needs recording) | Higher (just type) |
| **Smart home fit** | ✅ Voice-only devices | ❌ Devices without screen |
| **Papers trend** | Stable baseline | Growing rapidly |
| **Use case overlap** | Low — different assumptions | Low |

**Critical evidence:** DMA-KWS (Ai 2026) shows **multi-modal (speech + text) outperforms text-only in speaker-dependent settings** — directly supporting our audio enrollment approach.

---

## 3. Contradictory Evidence

- Text-based enrollment is growing (8 papers 2024-2026) and may become dominant for mobile apps.
- **However:** this does not invalidate audio enrollment for voice-only smart home devices.
- PLCL (Li 2025) supports both modes in a single framework — suggesting both are needed.

## 4. Impact on Our Project

| Decision | Evidence | Confidence |
|---|---|---|
| **Audio enrollment is valid** | DMA-KWS shows speech > text for speaker-dependent | Strong |
| **No design change needed** | Different problem, different use case | Strong |
| **Add Related Work section** | To acknowledge trend and explain scope | Mandatory |
