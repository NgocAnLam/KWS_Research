# Claims Directory

> **Mục đích:** Lưu các claim (luận điểm) của luận văn/paper, kèm evidence và experiment hỗ trợ.
>
> Mỗi claim là một phát biểu có thể kiểm chứng. Khi viết paper, các claim này được sử dụng trực tiếp trong Introduction, Method, Discussion.

---

## Cấu trúc mỗi claim

```markdown
# Claim: <Phát biểu>

| Field | Link |
|---|---|
| **Evidence** | `evidence/<file>.md` |
| **Decision** | `decisions_log.md` #N |
| **Experiment** | EXP00N |
| **Figures** | `experiments/EXP00N/figures/` |
| **Citations** | Paper1, Paper2 |
| **Status** | Unverified / Verified / Rejected |
```

## Quy tắc

1. Mỗi claim phải có evidence từ literature hoặc experiment.
2. Status phải được cập nhật sau experiment.
3. Claim không có evidence là hypothesis, không phải claim.

## Danh sách claims

| ID | Claim | Status |
|---|---|---|
| C01 | Vietnamese UDKWS lacks a unified evaluation protocol | Verified (SLR) |
| C02 | BC-ResNet-32 offers the best accuracy/size trade-off for edge KWS | Verified (SLR) |
| C03 | Log-Mel is the standard feature for KWS in 2024-2026 literature | Verified (SLR) |
| C04 | There is no existing Vietnamese KWS dataset or research framework | Verified (SLR) |
| C05 | Prototypical Networks provide competitive few-shot performance for audio-enrolled UDKWS | Pending (EXP001) |
| C06 | PCEN improves noise robustness at zero inference cost | Pending (EXP001) |
| C07 | Our evaluation protocol enables fair comparison across methods | Pending (after EXP001-003) |
| C08 | The proposed framework achieves real-time streaming on Raspberry Pi 4 | Pending (EXP003) |
