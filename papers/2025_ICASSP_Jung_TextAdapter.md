# Paper Review: Text-Aware Adapter (ICASSP 2025)

---

## 1. Summary

TA-adapter: text enrollment for KWS. Uses jointly pre-trained text encoder to generate keyword embedding, then fine-tunes only 0.14% of network parameters via adapter modules. Eliminates need for audio enrollment.

## 2. Research

| Field | Value |
|---|---|
| **Problem** | Text-based keyword enrollment for KWS |
| **Method** | TA-adapter: text encoder + adapter modules (0.14% params) |
| **Dataset** | GSC v2 (35 keywords) |
| **Backbone** | Pre-trained acoustic encoder + text encoder |
| **Feature** | — |
| **Metric Learning** | — |
| **Enrollment** | **Text-based (zero-shot)** |
| **Edge deployment** | Lightweight adapters (0.14% increase) |

## 3. Quality Assessment: 8/10

## 4. Key Takeaways

- **Different paradigm from our project**: text enrollment, not audio enrollment
- Confirms that text-based enrollment is a major 2024-2026 trend
- Adapter efficiency (0.14% params) is impressive for edge deployment
- Does NOT invalidate our audio enrollment approach — different use case
- Important for Related Work section to address text-based alternative

## 5. Citation for Related Work

Use to show awareness of text-based enrollment trend while justifying audio enrollment for voice-only devices.

## 6. BibTeX

```bibtex
@inproceedings{jung2025textadapter,
  title={Text-Aware Adapter for Few-Shot Keyword Spotting},
  author={Jung, Youngmoon and Lee, Jinyoung and Lee, Seungjin and Jung, Myunghun and Lee, Yong-Hyeok and Cho, Hoon-Young},
  booktitle={ICASSP 2025},
  year={2025}
}
```
