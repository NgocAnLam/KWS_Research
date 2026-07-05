# Papers Directory

> Mỗi paper quan trọng có thư mục riêng với 3 file.

## Structure

```text
papers/
├── README.md
│
├── <topic>/
│   └── <short-name>/
│       ├── paper.pdf          # Bản PDF (nếu available)
│       ├── notes.md           # Review notes (theo template)
│       └── bibtex.bib         # BibTeX citation
│
├── ProtoNet/
│   ├── snell2017_prototypical/
│   │   ├── paper.pdf
│   │   ├── notes.md
│   │   └── bibtex.bib
│   └── ...
│
├── DS-CNN/
│   └── ...
│
├── BC-ResNet/
│   └── ...
│
├── Few-shot-KWS/
│   └── ...
│
├── Streaming-KWS/
│   └── ...
│
└── Vietnamese-Speech/
    └── ...
```

## Naming Convention

```
<topic>/<firstauthor><year>_<short-title>/
```

Ví dụ:
- `Few-shot-KWS/snell2017_prototypical/`
- `DS-CNN/zhang2017_hello_edge/`

## notes.md Format

Sử dụng template tại `templates/paper_review.md`.

## Thêm paper mới

```bash
mkdir -p papers/<topic>/<author><year>_<short-title>
# Copy template từ templates/paper_review.md
# Download PDF
# Tìm BibTeX từ Google Scholar / Semantic Scholar
```
