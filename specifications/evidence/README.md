# Evidence Layer

> **Mục đích:** Tầng trung gian giữa `papers/` (dữ liệu thô) và `community_trends.md` (phân tích xu hướng).
>
> **Mỗi evidence file chỉ trả lời một câu hỏi:** "Các paper trong chủ đề này chứng minh điều gì?"
>
> **Không chứa quyết định thiết kế.** Quyết định thuộc về `summary_project.md`.

---

## Cấu trúc thư mục

```text
specifications/evidence/
├── README.md                   # File này
├── proto_vs_ge2e.md            # Metric learning methods
├── feature_extraction.md       # MFCC vs Log-Mel vs PCEN
├── backbone_models.md          # BC-ResNet vs DS-CNN vs Conformer
├── evaluation_protocol.md      # Evaluation protocol heterogeneity
├── deployment.md               # Edge deployment + Vietnamese gap
└── zero_shot_enrollment.md     # Audio vs text-based enrollment
```

## Quy tắc

### 1. Evidence chỉ ghi nhận bằng chứng

Mỗi evidence file chỉ tổng hợp **những gì literature nói**.

Không đưa ra quyết định như:
- "Dự án sẽ dùng GE2E." → ❌ (thuộc `summary_project.md`)
- "Evidence chưa đủ để so sánh GE2E vs ProtoNet trong audio enrollment." → ✅

### 2. Cấu trúc thống nhất

Mỗi file tuân theo format:

```markdown
# Topic

## Research Question
(Câu hỏi evidence cần trả lời)

## Evidence Summary
(Tổng hợp ngắn gọn)

## Supporting Papers
(Bảng paper ủng hộ)

## Contradictory Evidence
(Paper hoặc lập luận ngược lại — nếu có)

## Evidence Strength
(Strong / Moderate / Weak / Insufficient)

## Remaining Gaps
(Câu hỏi chưa được trả lời)

## Impact on Our Project
(Tác động tiềm năng — không phải quyết định)
```

### 3. Evidence Strength scale

| Level | Ý nghĩa |
|---|---|
| **Strong** | Nhiều paper (≥5) consensus, quality venues |
| **Moderate** | 2-4 papers, hoặc consensus nhưng chưa rộng |
| **Weak** | 1 paper, hoặc indirect evidence |
| **Insufficient** | Chưa có paper, hoặc evidence mâu thuẫn |

### 4. Khi thêm evidence mới

1. Thêm paper vào `papers/` (nếu chưa có)
2. Cập nhật evidence file tương ứng
3. Không sửa `summary_project.md`

### 5. Liên kết

| Tầng trên | Tầng dưới |
|---|---|
| `community_trends.md` ← tổng hợp từ evidence | |
| Evidence ← tổng hợp từ `papers/` | |
