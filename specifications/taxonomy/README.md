# Taxonomy

> **Mục đích:** Gắn tag cho papers theo chủ đề. Khi cần biết "bao nhiêu paper dùng PCEN?", tra taxonomy thay vì nhớ.
>
> **Khi nào dùng:** Khi số lượng papers vượt 40-50.
> **Hiện tại:** ~13 papers — chưa cần taxonomy.

## Categories

| Category | Description | Papers |
|---|---|---|
| **Feature** | Feature extraction methods | MFCC, Log-Mel, PCEN, LEAF |
| **Backbone** | Neural network architectures | DS-CNN, BC-ResNet, MobileNet, Conformer |
| **Loss** | Loss functions | ProtoNet, Triplet, GE2E, ArcFace, Contrastive |
| **Training** | Training strategies | Scratch, Pretrain+FT, SSL, KD |
| **Enrollment** | Enrollment methods | Audio, Text, Zero-shot |
| **Evaluation** | Evaluation protocols | Episode, Split, FAR-constrained, Streaming |
| **Streaming** | Streaming/online detection | VAD, Sliding Window, Temporal Smoothing |
| **Deployment** | Edge deployment | TFLite, INT8, Raspberry Pi, MCU |
| **Dataset** | Datasets | GSCv2, MSWC, Custom Vietnamese |
| **Vietnamese** | Vietnamese speech | ASR, TTS, KWS |

## Usage

Khi thêm paper mới, ghi tags vào metadata:

```yaml
# papers/metadata/<paper>.md
tags:
  - Feature: PCEN
  - Backbone: BC-ResNet
  - Deployment: Edge
  - Streaming: Yes
```
