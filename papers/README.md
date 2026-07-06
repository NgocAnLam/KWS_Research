# Papers Directory

> **Quy trình Literature Review:** Mọi phân tích chỉ được thực hiện sau khi đã tải bản PDF chính thức và lưu vào thư mục `papers/`. Không đọc paper trực tiếp trên web rồi tóm tắt.

---

## 1. Tiêu chí lựa chọn paper

### 1.1. Thời gian

| Loại | Yêu cầu |
|---|---|
| State-of-the-art papers | Xuất bản từ **2024 trở đi** |
| Foundational papers | Được phép trước 2024 nếu là công trình gốc hoặc có ảnh hưởng lớn (ProtoNet 2017, Siamese 2005, Triplet 2015, GSCv2 2018) |

### 1.2. Chất lượng

| Loại | Yêu cầu |
|---|---|
| Conference | **CORE Rank A\*, A, hoặc B** |
| Journal | **Q1, Q2, hoặc Q3** |
| arXiv preprint | Chỉ chấp nhận nếu có kế hoạch peer-review hoặc đã được citation rộng |

### 1.3. Khả năng truy cập

- **Open Access** hoặc có thể truy cập toàn văn hợp pháp.
- Paper phải có **DOI**.

### 1.4. Tiêu chí ưu tiên

Ưu tiên các paper có:
- Source code / GitHub repository
- Pretrained model / checkpoint
- Public dataset
- Reproducible experiments
- Supplementary materials

---

## 2. Cấu trúc thư mục

```text
papers/
├── README.md
│
├── metadata/                   # Metadata cho mỗi paper (YAML)
│   ├── 2025_ICASSP_Smith_ProtoKWS.md
│   └── ...
│
├── <Year>_<Venue>_<FirstAuthor>_<ShortTitle>.pdf
├── <Year>_<Venue>_<FirstAuthor>_<ShortTitle>_supp.pdf   # (nếu có)
│
└── <topic>/                    # (optional) phân loại theo chủ đề
    └── symlink -> ../../<file>.pdf
```

## 3. Quy tắc đặt tên file

> **Không giữ tên mặc định của publisher.**

Định dạng:

```
<Year>_<Venue>_<FirstAuthor>_<ShortTitle>.pdf
```

| Phần | Quy tắc | Ví dụ |
|---|---|---|
| Year | Năm xuất bản | `2025` |
| Venue | Tên viết tắt hội nghị/tạp chí | `ICASSP`, `INTERSPEECH`, `TASLP`, `CVPR`, `NeurIPS` |
| FirstAuthor | Họ tác giả đầu | `Smith`, `Nguyen`, `Chen` |
| ShortTitle | 3–5 từ, PascalCase, bỏ ký tự đặc biệt | `ProtoKWS`, `EfficientEdgeKWS` |

Ví dụ hoàn chỉnh:

```
2025_ICASSP_Smith_ProtoKWS.pdf
2025_ICASSP_Smith_ProtoKWS_supp.pdf
2024_INTERSPEECH_Lee_FSKWS.pdf
2025_CVPR_Wang_MAML++.pdf
2024_TASLP_Chen_VietKWS.pdf
2017_NeurIPS_Snell_PrototypicalNetworks.pdf
```

## 4. Metadata

Mỗi paper phải có metadata file riêng trong `papers/metadata/`.

Định dạng:

```yaml
# papers/metadata/<Year>_<Venue>_<FirstAuthor>_<ShortTitle>.md
---
title: ""
authors: ""
venue: ""
year: 0
doi: ""
publisher: ""
conference_rank: ""       # A* / A / B / None
journal_quartile: ""      # Q1 / Q2 / Q3 / None
open_access: true
github: ""                # URL hoặc null
dataset: ""               # URL hoặc null
checkpoint: ""            # URL hoặc null
paper_url: ""
pdf_path: "papers/<filename>.pdf"
keywords: []
```

## 5. Workflow đọc paper

```text
┌─────────────────────────────────────────────────┐
│  1. Tìm paper (theo search strategy trong SLR)  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  2. Kiểm tra tiêu chí (year, venue, DOI, OA)    │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  3. Tải PDF → lưu vào papers/                   │
│     Tên file theo quy tắc đặt tên               │
│     Nếu có supplementary → lưu kèm              │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  4. Tạo metadata file → papers/metadata/         │
│     (YAML front matter)                          │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  5. Đọc PDF → điền paper_review template        │
│     templates/paper_review.md                   │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  6. Cập nhật literature_review log              │
│     docs/literature_review/literature_review.md │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  7. Cập nhật reading_list.md (status → ✅)      │
│     knowledge/reading_list.md                   │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  8. Cập nhật slr_notes.md (findings, decisions) │
│     specifications/slr_notes.md                 │
└─────────────────────────────────────────────────┘
```

## 6. Lưu ý quan trọng

- **Không đọc paper trực tiếp trên web rồi tóm tắt.** Mọi phân tích chỉ được thực hiện sau khi đã tải bản PDF chính thức.
- Quy định này giúp kiểm chứng lại nguồn sau này, tránh AI tóm tắt từ abstract hoặc bản sao không đầy đủ.
- Đảm bảo toàn bộ quá trình literature review có tính tái lập (reproducibility).
