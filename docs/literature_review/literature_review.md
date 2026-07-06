# Literature Review Log

> **Mục tiêu:** Tổng hợp tất cả paper đã đọc, phục vụ viết Related Work cho luận văn và paper.

---

## Thống kê

| Category | Total | Read | In Progress |
|---|---|---|---|
| Few-shot KWS Methods | 7 | 7 | 0 |
| Feature Engineering | 2 | 2 | 0 |
| Lightweight Backbones | 3 | 3 | 0 |
| Training Strategies | 2 | 2 | 0 |
| Evaluation Protocols | 0 | 0 | 0 |
| Edge Deployment | 3 | 3 | 0 |
| Vietnamese Speech | 0 | 0 | 1 |
| Open-set / Unknown | 3 | 3 | 0 |
| **Total** | **20** | **13** | **7** |

---

## Danh sách paper đã đọc

> Sắp xếp theo thứ tự thời gian đọc (mới nhất ở trên).

### 2026

| Date | Paper | Venue | Category | Key Finding | Impact on Design |
|---|---|---|---|---|---|
| 2026-07-06 | EdgeSpot: Efficient FS-KWS Model | ICASSP 2026 | FS-KWS, Edge, Feature | BC-ResNet + PCEN + SDPA, 82% 10-shot @1% FAR, 128K params | BC-ResNet primary backbone candidate; PCEN frontend validated |
| 2026-07-06 | GE2E-KWS: Zero-shot KWS | IEEE SLT 2024 | FS-KWS, Edge | GE2E loss beats triplet by 60.7% AUC; 419KB quantized conformer | GE2E loss is a strong alternative to ProtoNet |
| 2026-07-06 | Hello Edge: DS-CNN on MCU | arXiv 2017 | Backbone, Edge | DS-CNN 95.4% on GSC, 250KB on MCU | DS-CNN is validated edge baseline |
| 2026-07-06 | BC-ResNet for KWS | INTERSPEECH 2021 | Backbone | 98.7% on GSC v2 at 181K params | BC-ResNet-32 is top accuracy choice |
| 2026-07-06 | On the Efficiency of SSL + Meta for UDKWS | IEEE SLT 2022 | Training, FS-KWS | HuBERT + MatchingNet best; SSL + meta-learning complementary | SSL pretrain + meta-learning fine-tune is validated |
| 2026-07-06 | Triplet Loss KWS | SPECOM 2021 | FS-KWS, Training | 98.55% GSC V1 with triplet + phonetic mining | Triplet loss works well but no edge deployment |
| 2026-07-06 | Few-Shot ProtoNets KWS | ICMLT 2022 | FS-KWS | ProtoNet with temporal convs for FS-KWS | Validates ProtoNet baseline |
| 2026-07-06 | Dummy ProtoNets Open-Set KWS | INTERSPEECH 2022 | FS-KWS, Open-set | Dummy prototypes for open-set rejection | Open-set strategy reference |
| 2026-07-06 | On-Device FS-KWS Open-Set | INTERSPEECH 2023 | FS-KWS, Edge, Open-set | Triplet + normalized > ProtoNet for open-set; 76% @5% FAR | Triplet preferred for on-device open-set |
| 2026-07-06 | PCEN Trainable Frontend | ICASSP 2017 | Feature | Dynamic compression replaces log-mel; 0 inference cost | PCEN is viable Log-Mel alternative |
| 2026-07-06 | Improving Small Footprint FS-KWS | INTERSPEECH 2023 | Training, Edge | Multi-task ProtoNet + auto-annotated LibriWord | Small-footprint FS-KWS training reference |
| 2026-07-06 | Enhancing FS-KWS via SSL Pretraining | IEEE SPL 2025 | Training, Edge | Wav2Vec 2.0 teacher + ResNet15 student, KD improves 33.4%→74.1% | Knowledge distillation reference for edge deployment |
| 2026-07-06 | MT-HuBERT for Mixed Speech FS-KWS | arXiv 2025 | FS-KWS, Training | HuBERT self-supervised + Mix-Training for overlapping keywords | SSL for challenging acoustic conditions |

---

## Synthesis Notes

### C1: Few-shot KWS Methods — Prototypical Networks dominate

| Method | Papers | Best Accuracy | Edge Support | Notes |
|---|---|---|---|---|
| **Prototypical Networks** | Parnami 2022, Kim 2022, Yang 2023, Zhuang 2024, Kao 2022 | ~76-82% (5-way 5-shot) | Yes (Yang 2023, Rusci 2023) | Most studied method; consistent performance |
| **Triplet Loss** | Vygon 2021, Rusci 2023 | 98.55% (closed-set), 76% @5% FAR (open-set) | Yes (Rusci 2023) | Better than ProtoNet for open-set (Rusci 2023) |
| **GE2E Loss** | Zhu 2024 | Beats triplet by 60.7% AUC | Yes (419KB quantized) | Strongest loss function for zero-shot KWS |
| **MAML + ProtoNet** | Zhuang 2024 | Outperforms plain ProtoNet | No | Higher compute cost |

**Key takeaway:** ProtoNet is the safest baseline. Triplet loss is better for open-set. GE2E is the strongest but less studied for few-shot.

### C2: Feature Engineering — PCEN emerges as Log-Mel alternative

| Feature | Papers | Accuracy Impact | Edge Cost | Notes |
|---|---|---|---|---|
| **MFCC** | Most papers | Baseline | Low | Standard, 13 coeffs |
| **Log-Mel Spectrogram** | BC-ResNet, DS-CNN | +1-2% vs MFCC | Low | 40-80 coeffs, common in SOTA |
| **PCEN** | Wang 2017, EdgeSpot 2026 | +2-3% in noisy conditions | Zero (trainable) | Dynamic compression, robust to noise |
| **LEAF (learned frontend)** | 2024 analysis | PCEN layer learns most | Low | Most of LEAF benefit comes from PCEN |

**Key takeaway:** Log-Mel is the safe choice. PCEN adds noise robustness at zero inference cost.

### C3: Lightweight Backbones — BC-ResNet leads

| Backbone | Params | GSCv2 Acc | Edge Latency | Notes |
|---|---|---|---|---|
| **DS-CNN** (Zhang 2017) | ~20K-80K | 95.4% | ~2ms (MCU) | Most edge-deployed; reference baseline |
| **BC-ResNet-32** (Kim 2021) | ~110K | 98.7% | ~10ms (RPi4) | Highest accuracy; depthwise + bottleneck |
| **Tiny CNN** | ~80K | ~92% | ~1ms | Simplest; weak accuracy |
| **MobileNetV2 (α=0.35)** | ~2.5M | ~93% | ~30ms | Too heavy for Pi 4? |
| **EdgeSpot-4** (2026) | 128K | 82% @1% FAR (10-shot) | — | BC-ResNet + SDPA |

**Key takeaway:** BC-ResNet-32 offers best accuracy/size trade-off. DS-CNN is the reliable edge baseline.

### C4: Training Strategies — Pretrain + Fine-tune wins

| Strategy | Papers | Verdict |
|---|---|---|
| **From scratch (ProtoNet)** | Parnami 2022, Kim 2022 | Works but accuracy lower |
| **Pretrain classification → FT metric** | Kao 2022 | SSL (HuBERT) + meta-learning best |
| **SSL pretrain → KD to student** | Gok 2025 | 33.4% → 74.1% improvement |
| **Multi-task (classification + metric)** | Yang 2023 | Improves over plain ProtoNet |

**Key takeaway:** Pretrain + fine-tune is clearly superior. SSL pretraining (HuBERT, Wav2Vec2) gives the biggest boost.

### C5: Evaluation Protocols — No standard for FS-KWS

| Protocol | Papers | Notes |
|---|---|---|
| **Episode-based (5-way K-shot)** | Parnami 2022, Kim 2022 | Most common; follows ProtoNet original |
| **Leave-out classes** | Rusci 2023 | Train on N classes, test on held-out |
| **FAR-constrained evaluation** | EdgeSpot 2026, GE2E-KWS 2024 | Report accuracy at 1% or 5% FAR |
| **Streaming evaluation** | GE2E-KWS 2024 | Metrics: FA/hour, Detection Latency |

**Key takeaway:** No unified protocol exists. Our unified protocol is itself a contribution.

### C6: Edge Deployment — TFLite INT8 is standard

| Approach | Papers | Model Size | Device | Latency |
|---|---|---|---|---|
| **TFLite INT8** | Hello Edge 2017, Rusci 2023 | 250KB-1MB | MCU, RPi | 2-50ms |
| **Knowledge distillation** | Gok 2025, EdgeSpot 2026 | 128K-500K params | RPi | — |
| **Quantization-aware training** | GE2E-KWS 2024 | 419KB | Mobile | Real-time |

**Key takeaway:** TFLite INT8 is the de facto standard. Knowledge distillation helps bridge the accuracy gap.

### C7: Vietnamese Speech — No existing KWS dataset

| Paper | Dataset | Task | Notes |
|---|---|---|---|
| (No dedicated Vietnamese KWS paper found) | — | — | Clear research gap |
| VIVOS | Vietnamese ASR | ASR | Not KWS |
| Common Voice Vietnamese | Mozilla | ASR | Not KWS |

**Key takeaway:** Zero existing Vietnamese KWS papers confirmed. This is a strong research gap.

### C8: Open-set / Unknown Detection

| Method | Papers | FAR Control | Notes |
|---|---|---|---|
| **Cosine similarity + threshold** | Parnami 2022, Rusci 2023 | Yes | Simplest; threshold needs tuning |
| **Dummy prototypes** | Kim 2022 | Yes | Train additional prototype for unknown |
| **Sub-center ArcFace** | EdgeSpot 2026 | Yes | Margin-based; combines with KD |
| **GE2E loss** | Zhu 2024 | Yes | Generalized end-to-end |

**Key takeaway:** Global threshold + cosine similarity is the baseline. Dummy prototypes and Sub-center ArcFace are more advanced options.
