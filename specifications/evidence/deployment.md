# Evidence: Edge Deployment & Vietnamese KWS

> **Research Question:** What edge deployment approaches are standard for KWS, and is there existing work on Vietnamese KWS?
> **Nguồn:** 50 papers surveyed, 15 edge-specific, all databases searched for Vietnamese
> **Last updated:** 2026-07-06 (post-SLR consolidation)

---

## 1. Edge Deployment Approaches

### 1.1. Framework Usage (12 edge papers)

| Framework | Papers | Devices |
|---|---|---|
| **TFLite / TFLite Micro** | Hello Edge 2017, Rusci 2023, GE2E-KWS 2024, EdgeSpot 2026 | MCU, RPi4, Mobile |
| **TensorFlow** | BC-ResNet 2021, MatchboxNet 2020, TC-ResNet 2019 | Server / Simulation |
| **PyTorch → TFLite** | Most 2024-2026 papers | Training → Edge |
| **ONNX / custom** | KWT-Tiny 2024 (RISC-V) | Specialized hardware |

### 1.2. Quantization

| Method | Papers | Acc Loss |
|---|---|---|
| **Post-training INT8** | Hello Edge, Rusci 2023, GE2E-KWS 2024 | 1–3% |
| **Quantization-aware training** | GE2E-KWS 2024 | <1% |
| **Knowledge distillation** | EdgeSpot 2026, Gok 2025 | <1% (improves) |

### 1.3. Target Devices

| Device | Papers | Latency |
|---|---|---|
| **Raspberry Pi 4** | Dey 2025, CNN-LSTM 2024 | 10–50ms |
| **ARM Cortex-M4/M7** | Hello Edge, Rusci 2023 | 2–20ms |
| **RISC-V** | KWT-Tiny 2024 | Real-time |
| **Mobile ARM CPU** | TC-ResNet 2019, Pudo 2024 | 10–30ms |

---

## 2. Vietnamese KWS Gap — Comprehensive Search Results

| Search Source | Query | Results |
|---|---|---|
| arXiv | "Vietnamese keyword spotting" | **0** |
| arXiv | "Vietnamese" + "wake word" | **0** |
| IEEE Xplore | "Vietnamese" + "keyword spotting" | **0** |
| Google Scholar | "tiếng Việt" + "keyword spotting" | **0** |
| Google Scholar | "Vietnamese speech commands" | **0** |
| Google Scholar | "Vietnamese" + "few-shot" + "keyword" | **0** |
| Google Scholar | "Vietnamese" + "custom keyword" | **0** |

**The only Vietnamese speech resources found (none are KWS):**

| Resource | Task | Speakers | Not KWS because |
|---|---|---|---|
| **VIVOS** | ASR (reading speech) | 15 | Full-sentence ASR, not KWS |
| **Common Voice Vietnamese** | ASR (crowdsourced) | ~2000 | Mozilla, sentence-level |
| **PhoWhisper** (Le 2024) | ASR (Whisper fine-tune) | — | ASR model, not KWS |
| **VietTTS** | TTS | — | Speech synthesis |

---

## 3. Impact on Our Project

| Finding | Evidence | Confidence |
|---|---|---|
| **TFLite INT8 is de facto edge standard** | 10/12 edge papers use TFLite | Strong |
| **Raspberry Pi 4 is a valid target** | 3 papers benchmark on RPi4 specifically | Strong |
| **Vietnamese KWS is a genuine gap** | 0 papers across all databases | **Strong (verified)** |
| **Vietnamese speech resources exist (but not KWS)** | PhoWhisper, VIVOS, Common Voice | Can leverage for Vietnamese dataset |
