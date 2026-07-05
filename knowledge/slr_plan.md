# Systematic Literature Review (SLR) Plan

> **Mục tiêu:** Xác thực research gap, novelty, và mọi quyết định kỹ thuật trong research design.
> **Thời gian:** 4 tuần (dự kiến).
> **Output:** Research Gap Analysis, Related Work section cho luận văn/paper.

---

## 1. Research Questions cho SLR

| ID | Question | Liên quan đến |
|---|---|---|
| SQ1 | What existing datasets and evaluation protocols are used for Few-shot KWS? | Gap #4, Protocol |
| SQ2 | Which audio features (MFCC, Log-Mel, PCEN) are most effective for few-shot keyword spotting? | Backbone, Feature |
| SQ3 | What metric learning methods (ProtoNet, Siamese, Triplet) have been applied to KWS, and how do they compare? | Method selection |
| SQ4 | What lightweight backbones are commonly used for on-device KWS (Tiny CNN, DS-CNN, BC-ResNet, MobileNet)? | Backbone |
| SQ5 | What training strategies (pretrain + fine-tune vs scratch) are used for few-shot KWS? | Training strategy |
| SQ6 | How is unknown detection / open-set handled in user-defined KWS systems? | Threshold, Runtime |
| SQ7 | What streaming / deployment pipelines exist for real-time KWS on edge devices? | Deployment |
| SQ8 | Are there any existing studies on Vietnamese KWS or Vietnamese speech commands? | Gap #1 |

---

## 2. Search Strategy

### 2.1 Databases

| Database | URL | Priority |
|---|---|---|
| IEEE Xplore | https://ieeexplore.ieee.org | High |
| ACM Digital Library | https://dl.acm.org | High |
| arXiv | https://arxiv.org | High (for preprints) |
| Google Scholar | https://scholar.google.com | Medium (for broad search) |
| Semantic Scholar | https://www.semanticscholar.org | Medium |
| Scopus | https://www.scopus.com | High (if accessible) |
| Web of Science | https://www.webofknowledge.com | Medium (if accessible) |

### 2.2 Search Strings

```text
# Primary (combine with AND/OR)
("keyword spotting" OR "keyword detection" OR "wake word" OR "speech commands")
AND
("few-shot" OR "few shot" OR "metric learning" OR "prototypical" OR "siamese" OR "triplet")
AND
("edge" OR "embedded" OR "on-device" OR "raspberry" OR "mobile" OR "tflite" OR "quantization")
```

```text
# Vietnamese-specific
("vietnamese" OR "tiếng việt")
AND
("keyword spotting" OR "speech recognition" OR "voice command")
```

```text
# Feature extraction
("mfcc" OR "log-mel" OR "pcen" OR "spectrogram")
AND
("keyword spotting" OR "speech commands")
AND
("few-shot" OR "metric learning")
```

```text
# Streaming / Deployment
("streaming" OR "real-time" OR "low latency")
AND
("keyword spotting" OR "wake word")
AND
("raspberry pi" OR "edge" OR "embedded")
```

### 2.3 Time Range

- **Primary:** 2018–2026 (Speech Commands v0.02 released 2018)
- **Classic papers:** Không giới hạn (ProtoNet 2017, Siamese 2005, Triplet 2015)

---

## 3. Inclusion / Exclusion Criteria

### 3.1 Inclusion

| Criterion | Rationale |
|---|---|
| Peer-reviewed conference, journal, or arXiv preprint | Đảm bảo chất lượng |
| Published 2018–2026 | After Speech Commands v0.02 |
| Focus on keyword spotting or wake word detection | Core topic |
| Uses few-shot learning or metric learning | Core method |
| Addresses edge deployment, quantization, or low-resource | Application |
| English or Vietnamese | Ngôn ngữ |

### 3.2 Exclusion

| Criterion | Rationale |
|---|---|
| Large-vocabulary continuous speech recognition | Không phải KWS |
| Speaker verification / identification only | Không liên quan |
| Non-speech audio event detection | Khác domain |
| Not available in full text | Không thể review |

---

## 4. Quality Assessment

Mỗi paper được đánh giá theo thang 0–2 cho từng tiêu chí:

| Tiêu chí | 0 | 1 | 2 |
|---|---|---|---|
| QA1: Problem clarity | Không rõ | Tương đối rõ | Rất rõ |
| QA2: Experimental rigor | Thiếu baseline, 1 seed | Có baseline, 1 seed | Baseline + multiple seeds |
| QA3: Reproducibility | Không có thông tin | Partial (dataset name) | Full (code, config, seed) |
| QA4: Relevance to our work | Không liên quan | Indirectly related | Directly applicable |
| QA5: Evaluation on edge device | Không | Simulation only | Real hardware benchmark |

**Quality score:** Sum of 5 criteria → max 10. Papers with score ≥ 6 are included in final analysis.

---

## 5. Data Extraction Form

```yaml
paper:
  title: ""
  authors: ""
  venue: ""
  year: 0
  doi: ""
  url: ""

research:
  problem: ""                          # What problem does it solve?
  method: ""                           # What method is proposed?
  dataset: ""                          # Which dataset?
  backbone: ""                         # Which backbone?
  feature: ""                          # Which audio feature?
  metric_learning: ""                  # ProtoNet / Siamese / Triplet / Other
  shot: ""                             # K-shot setting
  training_strategy: ""                # Scratch / Pretrain + FT / Other
  evaluation_protocol: ""              # Episode / Fixed split / Leave-out
  unknown_detection: ""                # Threshold / Open-set / None
  deployment: ""                       # Edge device / Simulation / None
  streaming: false                     # Streaming evaluation?

results:
  accuracy: ""                         # Best accuracy reported
  latency: ""                          # If edge deployment
  model_size: ""                       # If reported
  other_metrics: ""

assessment:
  quality_score: 0                     # 0-10
  strengths: [""]
  weaknesses: [""]
  relevance: ""                        # High / Medium / Low
  notes: ""
```

---

## 6. PRISMA Flow

```text
Records identified (n = ...)
  ├── IEEE Xplore (n = ...)
  ├── ACM DL (n = ...)
  ├── arXiv (n = ...)
  └── Google Scholar (n = ...)
          ↓
Duplicates removed (n = ...)
          ↓
Title & abstract screening (n = ...)
          ↓
Full-text assessment (n = ...)
          ↓
Included in final analysis (n = ...)
```

---

## 7. Thematic Analysis Categories

Sau khi thu thập papers, phân loại theo:

| Category | Description |
|---|---|
| **C1: Few-shot KWS Methods** | ProtoNet, Siamese, Triplet, MatchingNet, RelationNet |
| **C2: Feature Engineering** | MFCC, Log-Mel, PCEN, raw audio, learnable front-end |
| **C3: Lightweight Backbones** | DS-CNN, BC-ResNet, MobileNet, Tiny CNN, TC-ResNet |
| **C4: Training Strategies** | Pretrain + fine-tune, from scratch, knowledge distillation |
| **C5: Evaluation Protocols** | Episode, leave-out, cross-speaker, streaming |
| **C6: Edge Deployment** | TFLite, quantization, latency benchmarks, Raspberry Pi |
| **C7: Vietnamese Speech** | Any Vietnamese ASR/KWS datasets or systems |
| **C8: Open-set / Unknown** | Threshold, Open-Set Recognition, confidence calibration |

---

## 8. Timeline

| Week | Activity | Output |
|---|---|---|
| 1 | Search + title/abstract screening | Candidate list (n ~50) |
| 2 | Full-text reading + data extraction | Extracted data (n ~30) |
| 3 | Quality assessment + thematic analysis | Quality scores, category mapping |
| 4 | Synthesis + research gap confirmation | Gap analysis, updated protocol |

---

## 9. SLR Log

See `specifications/slr_notes.md` for daily progress tracking.

> **Note:** This plan will be filled with actual numbers and findings during the SLR process.
