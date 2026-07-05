# Tóm tắt dự án

## Tên đề tài (định hướng)

**A Modular Research Framework and Evaluation Protocol for User-defined Vietnamese Few-shot Keyword Spotting on Edge Devices**

> [!NOTE]
> Đây là research design specification. Các quyết định kỹ thuật được đánh dấu `[SLR]` cần được xác nhận sau Systematic Literature Survey.

---

# 1. Bối cảnh

Keyword Spotting (KWS) là bài toán phát hiện các từ khóa ngắn trong tín hiệu âm thanh và là thành phần quan trọng của các hệ thống Voice Assistant, Human-Computer Interaction, IoT và Edge AI.

Tuy nhiên, hầu hết các hệ thống KWS truyền thống đều yêu cầu tập từ khóa cố định và phải huấn luyện lại mô hình khi muốn bổ sung từ khóa mới. Điều này không phù hợp với các ứng dụng mà người dùng muốn tự định nghĩa keyword của riêng mình.

Trong khi đó, Few-shot Learning cho phép mô hình học khái niệm của một keyword chỉ từ rất ít mẫu (ví dụ 1–5 mẫu) mà không cần huấn luyện lại toàn bộ mô hình. Điều này mở ra khả năng xây dựng hệ thống **User-defined Keyword Spotting (UDKWS)**, trong đó mỗi người dùng có thể tự đăng ký các keyword của riêng mình và sử dụng ngay trên thiết bị Edge như Raspberry Pi.

---

# 2. Research Gap và Novelty

**Khoảng trống nghiên cứu được xác định dựa trên khảo sát tài liệu sơ bộ (cần được củng cố bằng Systematic Literature Survey trước khi implement):** <!-- SLR: cần số liệu cụ thể, ví dụ "102 English papers vs 2 Vietnamese papers" -->

1. **Ngôn ngữ**: Phần lớn nghiên cứu UDKWS tập trung vào tiếng Anh (Google Speech Commands) hoặc tiếng Trung. Nghiên cứu cho tiếng Việt còn rất hạn chế, đặc biệt là với keyword đa âm tiết có dấu.

2. **Enrollment-centric Evaluation**: Các nghiên cứu Few-shot KWS hiện có thường đánh giá trên benchmark chuẩn (episode-based classification), nhưng ít đánh giá theo **workflow enrollment thực tế của người dùng** — nơi user tự định nghĩa keyword, thu âm, và sử dụng trên thiết bị Edge trong thời gian thực.

3. **End-to-end Framework**: Existing studies often focus on algorithmic improvements rather than providing an end-to-end research framework integrating training, enrollment, deployment, and evaluation within a consistent pipeline.

4. **Heterogeneous Evaluation**: Existing studies adopt heterogeneous evaluation protocols (different seen/unseen splits, episode generation strategies, metrics), making fair comparison between methods difficult. <!-- SLR: cần citation cụ thể, VD "Paper A dùng leave-one-class-out, Paper B dùng random split" -->

**Novelty của đề tài (3 novelty, Contribution 1 là primary):**

1. **Unified Research Framework and Evaluation Protocol (Primary Novelty):** Một framework nghiên cứu modular kết hợp evaluation protocol thống nhất cho UDKWS tiếng Việt trên Edge Devices, bao gồm pipeline từ data → feature → backbone → metric learning → enrollment → streaming detection → deployment, kèm unified episode generation, threshold optimization, streaming evaluation, và enrollment protocol.

2. **Comprehensive Empirical Study**: Systematic benchmark (factorial design) về Feature Extraction × Metric Learning dưới cùng evaluation protocol, kèm primary/secondary experiment design, training strategy ablation, speaker leakage analysis.

3. **Vietnamese Deployment Case Study**: Thiết kế và triển khai một demonstration dataset cho UDKWS tiếng Việt (topic smart home), kèm dataset design guideline, quy trình đánh giá enrollment workflow, và streaming deployment trên Raspberry Pi 4.

**Các phân tích hỗ trợ (supporting analysis, không phải novelty):**
- Speaker leakage analysis, enrollment strategy comparison, threshold strategy, error analysis.

---

# 3. Mục tiêu nghiên cứu

Mục tiêu của đề tài là xây dựng một framework nghiên cứu hoàn chỉnh cho bài toán **User-defined Vietnamese Keyword Spotting** sử dụng **Few-shot Metric Learning**, đồng thời tối ưu để triển khai trên các thiết bị Edge AI có tài nguyên hạn chế.

Trong quá trình phát triển, framework được benchmark trên Google Speech Commands v2 như development dataset nhằm đánh giá tính đúng đắn và ổn định trước khi áp dụng cho bộ dữ liệu tiếng Việt. GSCv2 không phải đối tượng nghiên cứu cuối cùng, mà là công cụ hỗ trợ phát triển.

Đề tài không chỉ tập trung vào việc xây dựng một mô hình, mà hướng tới xây dựng một framework có thể dùng để benchmark, đánh giá và mở rộng cho các nghiên cứu sau này.

---

# 4. Phạm vi nghiên cứu (Scope)

## 4.1. Trong phạm vi

- User-defined Vietnamese Keyword Spotting với các keyword chưa xuất hiện trong tập huấn luyện.
- Keyword gồm 1 đến tối đa 3 từ tiếng Việt.
- Few-shot Metric Learning (Prototypical Networks, Siamese Networks, Triplet Networks).
- **Framework Development Phase (trên GSCv2):** Xây dựng và benchmark framework trên Google Speech Commands v2 như development dataset. GSCv2 được sử dụng để kiểm tra pipeline, benchmark feature extraction và metric learning, lựa chọn backbone, debug implementation — trước khi áp dụng cho tiếng Việt. **Bao gồm cả offline benchmark (episode-based classification) và streaming deployment trên Raspberry Pi 4**.
- **Vietnamese Validation Phase:** Áp dụng framework đã phát triển lên bộ dữ liệu tiếng Việt. Bao gồm enrollment workflow, streaming deployment trên Raspberry Pi 4 với VAD + sliding window + temporal smoothing.
- Speaker-dependent evaluation (support và query từ cùng speaker).

## 4.2. Ngoài phạm vi

- Open Set Recognition / novel class discovery.
- Speaker verification / speaker embedding (d-vector, x-vector).
- Các phương pháp few-shot learning dạng generative (GANs, diffusion).
- Các phương pháp không dựa trên metric learning (fine-tuning, adapter, prompt tuning).
- Cross-speaker evaluation (support khác speaker với query).
- **Nghiên cứu thuật toán VAD:** Voice Activity Detection được coi là fixed front-end component (WebRTC VAD hoặc Silero VAD), không phải research contribution.

## 4.3. Vai trò của GSCv2 trong đề tài

Google Speech Commands v2 **không phải đối tượng nghiên cứu cuối cùng**, mà là **development dataset** được sử dụng trong giai đoạn xây dựng framework. Cụ thể:

- Kiểm chứng pipeline xử lý hoạt động đúng.
- Benchmark Feature Extraction (MFCC vs Log-Mel).
- Benchmark Metric Learning (ProtoNet vs Siamese vs Triplet).
- Lựa chọn backbone phù hợp.
- Phát hiện lỗi implementation sớm.
- Đảm bảo framework ổn định trước khi áp dụng cho tiếng Việt.

Sau khi framework ổn định, toàn bộ pipeline được áp dụng cho bộ dữ liệu tiếng Việt mà không thay đổi kiến trúc.

## 4.4. Hai giai đoạn của luận văn

| Khía cạnh | Framework Development (GSCv2) | Vietnamese Validation |
|---|---|---|
| Mục đích | Xây dựng, benchmark, debug framework | Xác nhận framework giải quyết đúng bài toán mục tiêu |
| Dataset | Google Speech Commands v2 (English) | Vietnamese Demonstration Dataset |
| Offline eval | Episode-based classification (segmented utterances) | Enrollment + classification trên test set |
| Streaming eval | Streaming deployment trên Raspberry Pi 4 (với unseen GSCv2 classes) | Streaming deployment trên Raspberry Pi 4 (với Vietnamese keywords) |
| Metrics (offline) | Accuracy, F1, EER | Accuracy, F1, EER |
| Metrics (streaming) | FA/hour, RTF, Detection Latency | FA/hour, RTF, Detection Latency |
| Đầu ra | Framework hoàn chỉnh + Baseline benchmarks | Case study: UDKWS tiếng Việt trên Raspberry Pi 4 |

---

# 5. Bài toán nghiên cứu

Người dùng có thể tự định nghĩa các keyword mới (không giới hạn trong tập keyword đã huấn luyện), sau đó ghi âm một số lượng rất nhỏ mẫu (ví dụ 1, 3 hoặc 5 mẫu) để hệ thống học và nhận diện keyword đó mà không cần huấn luyện lại toàn bộ mô hình.

Đặc điểm của bài toán:

- **User-defined**: Người dùng tự chọn keyword.
- **Unseen keywords**: Keyword chưa xuất hiện trong quá trình huấn luyện.
- **Few-shot**: Chỉ 1–5 mẫu cho mỗi keyword mới.
- **Multi-syllable**: Keyword tiếng Việt có thể gồm 1–3 từ (có dấu, từ ghép).
- **Personalized**: Mỗi người dùng có bộ keyword riêng.
- **Extensible**: Hỗ trợ bổ sung keyword mới bất kỳ lúc nào (incremental).
- **Edge deployment**: Hệ thống chạy thời gian thực trên Raspberry Pi 4.

---

# 6. Ý tưởng cốt lõi

Đề tài tập trung vào **User-defined Keyword Spotting** như một bài toán nghiên cứu.

Few-shot Metric Learning được sử dụng như phương pháp giải quyết bài toán này.

Điều này giúp phân biệt rõ:

- **Problem:** User-defined Keyword Spotting.
- **Method:** Few-shot Metric Learning.
- **Application:** Edge AI trên Raspberry Pi 4.

---

# 7. Framework nghiên cứu

Framework dự kiến gồm các thành phần:

1. Dataset Analysis
2. Speech Processing (VAD, pre-emphasis, normalization)
3. Audio Feature Extraction (MFCC, Log-Mel Spectrogram)
4. Embedding Backbone (DS-CNN, BC-ResNet-32, MobileNetV2, Tiny CNN)
5. Metric Learning (Prototypical Networks, Siamese, Triplet)
6. Enrollment (1-shot, 3-shot, 5-shot)
7. Runtime Detection (Cosine Similarity + Threshold)
8. Edge Deployment (Raspberry Pi 4, quantized INT8)
9. Benchmarking & Evaluation

Pipeline tổng quát:

```
Phase A — Framework Development (trên GSCv2):
  [Offline Benchmark]
    Pretrain Classification:
      Audio → Speech Processing → Feature Extraction → Backbone → 25-way FC → Cross-entropy Loss
    Metric Learning Fine-tune (remove FC):
      Audio → Speech Processing → Feature Extraction → Backbone → Embedding → ProtoNet Loss
    Episode-based Evaluation:
      Support set (K samples) → Backbone → Mean Prototype → Cosine Similarity → Threshold → Decision

  [Streaming Deployment on Raspberry Pi 4]
    GSCv2 unseen classes (enrolled via prototype)
    Microphone → Circular Buffer → VAD → Sliding Window → Feature → Backbone → Cosine Similarity → Temporal Smoothing → Threshold → Decision

Phase B — Vietnamese Validation:
  [Enrollment]
    User → Đăng ký keyword → Thu âm 10 mẫu → Chọn K-shot → Compute prototype → Prototype Database
  [Streaming Deployment on Raspberry Pi 4]
    Microphone → Circular Buffer → VAD → Sliding Window → Feature → Backbone → Cosine Similarity → Temporal Smoothing → Threshold → Decision
```

**Lưu ý quan trọng:** GSCv2 là development dataset, không phải đối tượng nghiên cứu cuối cùng. Framework Development Phase dùng GSCv2 để benchmark và hoàn thiện pipeline. Vietnamese Validation Phase áp dụng pipeline đã ổn định lên tiếng Việt.

---

# 8. Hai giai đoạn

## Phase A — Framework Development (trên GSCv2)

**Mục tiêu:** Xây dựng và benchmark framework trên Google Speech Commands v2.

**Dataset:** Google Speech Commands Dataset v2 (105,829 files, 35 words, 16kHz) — sử dụng như development dataset.

**Offline benchmark:**
- Dataset Analysis (phân bố lớp, độ dài audio, speaker, background noise).
- Benchmark Feature Extraction (MFCC vs Log-Mel).
- Benchmark Metric Learning (ProtoNet vs Siamese vs Triplet).
- Factorial experiment: Feature × Metric Learning (2 × 3 = 6 configurations).
- Training strategy ablation (Scratch vs Fine-tune All vs Freeze Backbone).
- Đánh giá khả năng tổng quát hóa lên unseen speech keywords qua episode-based evaluation.
- Thiết lập baseline cho framework.

**Streaming deployment trên Raspberry Pi 4:**
- Enroll các unseen classes từ GSCv2 (house, marvin, sheila, tree, wow).
- Chạy streaming pipeline với circular buffer + VAD + Sliding Window + Temporal Smoothing.
- Đo streaming metrics (FA/hour, Detection Latency, RTF).
- Mục đích: kiểm tra pipeline streaming hoạt động ổn định trên phần cứng thật trước khi triển khai cho tiếng Việt.

---

## Phase B — Vietnamese Validation

Sau khi framework ổn định qua Phase A, xây dựng bộ dữ liệu tiếng Việt quy mô nhỏ và áp dụng framework để đánh giá khả năng áp dụng thực tế.

Dataset này chỉ đóng vai trò **validation case study**, không phải mục tiêu chính của đề tài.

**Workflow thực tế (Streaming Deployment — không phải episode):**

```
User
  ↓
Đăng ký keyword (tối đa 3 từ, tiếng Việt có dấu)
  ↓
Thu âm 10 mẫu mỗi keyword
  ↓
Chọn K enrollment samples (1, 3, hoặc 5-shot)
  ↓
Compute prototype embedding (mean of K samples)
  ↓
Lưu prototype vào Prototype Database
  ↓

--- Streaming Inference ---

USB Microphone
  ↓
Audio Stream (16 kHz)
  ↓
Circular Buffer (~2s)
  ↓
VAD (WebRTC / Silero — fixed front-end)
  ↓
Sliding Window (1s window, stride 20-40ms)
  ↓
Feature Extraction
  ↓
Backbone → Embedding
  ↓
Cosine Similarity vs tất cả prototypes trong Prototype Database
  ↓
Temporal Smoothing (majority vote over last N windows / K consecutive detections)
  ↓
Threshold
  ↓
Raspberry Pi 4: Keyword / Unknown (+ timestamp)
```

**Mục tiêu:** Chứng minh framework có thể triển khai thành một hệ thống User-defined Keyword Spotting tiếng Việt streaming thực tế trên Raspberry Pi 4.

---

# 9. Bộ dữ liệu

## 9.1. Development Dataset: Google Speech Commands v2

- 105,829 file .wav, 16-bit PCM, 16kHz
- 35 classes (thư mục), mỗi thư mục là một từ:
  - 20 core words: yes, no, up, down, left, right, on, off, stop, go, zero, one, two, three, four, five, six, seven, eight, nine
  - 10 auxiliary: bed, bird, cat, dog, happy, house, marvin, sheila, tree, wow
  - 5 extra: backward, forward, visual, follow, learn
- `_background_noise_` folder chứa các file noise dài dùng để augment và làm silence samples.
- Mỗi file dài ~1 giây, 16-bit PCM, 16kHz.
- Partitioning: hash-based (80% train, 10% validation, 10% test) — dùng `validation_list.txt` và `testing_list.txt` có sẵn.

**Lưu ý:** Không có folder `silence` hay `unknown` riêng. Silence samples được trích từ `_background_noise_`. Tất cả 35 folder đều là speech keyword.

### Seen / Unseen / Validation Split (cố định)

```
Seen (25 speech keyword classes — dùng cho training classification và metric learning):
  20 core: yes, no, up, down, left, right, on, off, stop, go,
           zero, one, two, three, four, five, six, seven, eight, nine
  5 auxiliary: bed, bird, cat, dog, happy

Unseen (5 speech keyword classes — dùng cho episode-based evaluation):
  house, marvin, sheila, tree, wow
  → 5-way evaluation, tất cả đều là từ thật.

Threshold Validation (5 speech keyword classes + _background_noise_ — dùng để tối ưu threshold):
  backward, forward, visual, follow, learn
  + _background_noise_ (cắt thành đoạn ngắn ~1s để làm silence/noise samples)
  → Các class này KHÔNG xuất hiện trong episode evaluation.
  → Chỉ dùng để tìm threshold tối ưu (F1/EER) cho unknown detection.
```

Split này được cố định trong toàn bộ luận văn, không thay đổi giữa các thí nghiệm. <!-- SLR: verify split ratio consistency với few-shot KWS literature -->

### Xử lý Speaker Leakage

SCv2 có speaker overlap giữa các class (cùng một người nói nhiều từ khác nhau → có thể xuất hiện ở cả seen và unseen classes). Đây là confound tiềm ẩn lớn nhất của Framework Development Phase.

**Phân tích định lượng (bắt buộc):**
1. Xác định speaker IDs từ filename (phần `{speaker_id}_nohash_{trial}.wav`).
2. Với mỗi unseen class, xác định:
   - **Overlap samples**: những utterance mà speaker ID cũng xuất hiện trong seen set.
   - **Non-overlap samples**: những utterance mà speaker ID KHÔNG xuất hiện trong seen set.
3. Báo cáo accuracy riêng cho 2 nhóm này.
4. Nếu gap > 5% → speaker leakage là significant → cần discuss và qualification trong luận văn.

**Protocol cho Framework Development Phase:**
- **Speaker-dependent evaluation (trong phạm vi):** support và query trong cùng episode đến từ cùng speaker (khác trial). Protocol này được thiết kế để mô phỏng kịch bản thực tế: cùng một user enroll keyword của họ và sau đó sử dụng hệ thống (personalized enrollment). Trong thực tế, user A enroll keyword của A, user B sử dụng hệ thống của A → đây là cross-speaker scenario nằm ngoài phạm vi.
- **Speaker leakage analysis (bắt buộc):** So sánh accuracy trên overlap và non-overlap samples. Kết quả được báo cáo trong Error Analysis (§16.5).
- **Limit:** Do SCv2 không đảm bảo speaker disjoint, accuracy có thể bị inflate. Giới hạn này được khắc phục trong Vietnamese Validation Phase (dataset có speaker-disjoint split giữa seen và unseen để đảm bảo không có speaker overlap — tuy nhiên enrollment và test vẫn là cùng speaker, mô phỏng personalized use case).
- **Future work:** Cross-speaker evaluation với speaker-disjoint split.
- **Future work:** Cross-speaker evaluation với speaker-disjoint split.

## 9.2. Target Dataset: Vietnamese Demonstration Dataset

### 9.2.1. Dataset Design Specification

| Thuộc tính | Giá trị |
|---|---|
| Sampling Rate | 16 kHz |
| Bit Depth | 16-bit PCM |
| Format | WAV |
| Duration | ~1 giây mỗi mẫu |
| Số speaker | ~20 |
| Số keyword | ~10 |
| Số lần đọc mỗi keyword | 10 lần |
| Độ dài keyword | 1–3 từ tiếng Việt |
| Thiết bị thu | Microphone cố định (USB hoặc built-in laptop) |
| Môi trường thu | Phòng yên tĩnh, khoảng cách mic ~30cm |
| File naming | `{keyword}_{speaker_id}_{trial}.wav` |
| Metadata | File CSV kèm: speaker_id, keyword, trial, timestamp, device, environment |

### 9.2.2. Tiêu chí lựa chọn keyword

Keyword được chọn dựa trên các tiêu chí sau:

1. **Tần suất sử dụng thực tế**: Các lệnh điều khiển thiết bị thông dụng trong nhà thông minh.
2. **Độ phức tạp âm tiết**: Bao gồm cả từ đơn âm và đa âm tiết, có dấu và không dấu.
3. **Độ tương đồng âm học**: Một số cặp keyword có phát âm gần nhau để đánh giá khả năng phân biệt (discriminative power).
4. **Độ dài khác nhau**: 1 từ, 2 từ, 3 từ để đánh giá ảnh hưởng của độ dài keyword.

Dataset này được thiết kế như một **proof-of-concept demonstration** cho UDKWS tiếng Việt, không phải large-scale benchmark. Quy mô 20 speakers × 10 keywords là phù hợp để đánh giá tính khả thi của framework trong thời gian và nguồn lực của luận văn (tham khảo các study tương tự dùng 15-20 speakers cho few-shot KWS).

**Note về diversity:** Việc thu thập phụ thuộc vào người dùng tự nguyện tham gia, không có kiểm soát về giới tính, độ tuổi, vùng miền. Số lượng speaker kỳ vọng ~20, thu thập được bao nhiêu dùng bấy nhiêu.

Ứng viên keyword (dự kiến theo chủ đề "smart home"):

| Keyword | Âm tiết | Độ dài | Ghi chú |
|---|---|---|---|
| bật đèn | 2 | ngắn | Lệnh phổ biến |
| tắt đèn | 2 | ngắn | Dễ nhầm với "bật đèn" |
| bật quạt | 2 | ngắn | |
| tắt quạt | 2 | ngắn | |
| mở cửa | 2 | ngắn | |
| đóng cửa | 2 | ngắn | Tương tự "mở cửa" |
| tăng nhiệt độ | 3 | dài | |
| giảm nhiệt độ | 3 | dài | |
| dừng lại | 2 | ngắn | Từ đa âm tiết |
| tiếp theo | 2 | ngắn | |

### 9.2.3. Thu thập dữ liệu

- Mỗi speaker ký consent form.
- Ghi âm trong phòng yên tĩnh, khoảng cách mic ~30cm.
- **Mỗi keyword đọc 10 lần.**
- Khoảng nghỉ 2-3 giây giữa các lần đọc.
- **Quy trình thu âm hiệu quả:** Ghi âm liên tục toàn bộ session (~10 phút/speaker). User đọc từng keyword theo danh sách. Code tự động cắt (segmentation) dựa trên VAD. Cách này giảm thời gian xuống ~10 phút/speaker × 20 speakers = 3.3 giờ.
- File được kiểm tra thủ công để loại bỏ mẫu lỗi (nói sai, noise đột biến).
- **Cách sử dụng 10 mẫu:**
  - **Enrollment:** chọn K mẫu (K = 1, 3, hoặc 5) từ 10 mẫu để tính prototype.
  - **Test:** K mẫu còn lại (10 - K) dùng để đánh giá offline (classification accuracy).
  - **Streaming test:** Toàn bộ 10 mẫu được ghép thành file audio dài (~30 giây) với silence + noise giữa các mẫu, phục vụ đánh giá streaming detection.

### 9.2.4. Negative Samples cho Vietnamese Validation

Test set bao gồm 4 nhóm negative:

**Nhóm 1 — Background**
- Silence segments.
- Background noise (fan, TV, air conditioner, street noise).
- Thời lượng tương đương keyword (~1 giây).
- Số lượng: ~20 mẫu.

**Nhóm 2 — Random Vietnamese Speech**
- Các câu nói tiếng Việt ngẫu nhiên không chứa keyword đã đăng ký.
- Ví dụ: "Hôm nay trời đẹp", "Tôi đi học", "Cái bàn ở đâu".
- Số lượng: ~20 mẫu.

**Nhóm 3 — Other Registered Keywords**
- Khi user đăng ký keyword A (ví dụ "tắt đèn"), các keyword B, C, D khác đóng vai trò negative cho A.
- Đây là nhóm negative khó (hard negative).
- Số lượng: (số keyword - 1) × 2 mẫu mỗi keyword.

**Nhóm 4 — Phonetically Similar**
- Các từ/phrase có phát âm gần với keyword đã đăng ký.
- Ví dụ: "bật đèn" vs "tắt quạt", "mở cửa" vs "đóng cửa".
- Số lượng: ~10 mẫu.

Tất cả negative samples được collect từ cùng môi trường thu (cùng mic, cùng phòng) với enrollment/test samples.

---

# 10. Feature Extraction

## 10.1. Primary Benchmark (Feature Extraction × Metric Learning factorial design)

| Feature | Parameters |
|---|---|
| MFCC | n_mfcc=13, n_fft=512, hop_length=160, win_length=400, fmin=0, fmax=8000 |
| Log-Mel Spectrogram | n_mels=40, n_fft=512, hop_length=160, win_length=400, fmin=0, fmax=8000 |

## 10.2. Extension / Ablation (sau benchmark chính)

- **PCEN (Per-Channel Energy Normalization)**: Có thể cải thiện robustness trong môi trường noisy, phù hợp với edge deployment. Chỉ benchmark trên configuration tốt nhất từ factorial experiment, không đưa vào benchmark chính.
- Mel Spectrogram (không log)

## 10.3. Tiền xử lý

- Pre-emphasis: coefficient = 0.97
- Normalization: mean-variance normalization trên từng utterance hoặc global
- Framing: 25ms window, 10ms stride
- Feature được tính giống nhau trong cả training và inference (trên Raspberry Pi 4)

---

# 11. Embedding Backbone

## 11.1. Tiêu chí lựa chọn (Multi-objective Selection)

Backbone sẽ tạo embedding, không trực tiếp phân loại keyword. Việc chọn backbone dựa trên multi-objective trade-off giữa các tiêu chí sau (không gán trọng số cứng — kết quả benchmark sẽ quyết định):

| Tiêu chí | Ghi chú |
|---|---|
| Accuracy (trên validation set, classification) | Metric chính |
| Latency (Raspberry Pi 4, INT8) | Yêu cầu real-time (< 100ms per inference) |
| Model Size | Phù hợp Edge |
| Memory Usage (peak) | RAM Raspberry Pi 4 (4GB) |
| FLOPs | Độ phức tạp tính toán |

## 11.2. Ứng viên

| Backbone | Params | Ghi chú |
|---|---|---|
| Tiny CNN | ~80K | Cơ bản nhất, baseline <!-- SLR: verify typical accuracy range on SCv2 --> |
| DS-CNN (Depthwise Separable) | ~20K | Nhẹ nhất, phổ biến trong KWS <!-- SLR: verify deployment compatibility on Pi 4 --> |
| BC-ResNet-32 (Bottleneck-Conv) | ~110K | One of the strongest lightweight CNN backbones reported on Speech Commands benchmark <!-- SLR: confirm SOTA status with recent papers --> |
| MobileNetV2 (α=0.35) | ~2.5M | Nặng nhất, khả năng cao nhất <!-- SLR: check TFLite INT8 compatibility --> |

## 11.3. Decision Protocol

1. Train từng backbone với classification head trên Speech Commands v2 (25 seen classes).
2. Ghi nhận accuracy trên validation set (5 classes).
3. Loại bỏ backbone nào accuracy dưới ngưỡng (ví dụ < 85%).
4. Convert sang TFLite INT8, benchmark latency trên Raspberry Pi 4.
5. Chọn backbone tối ưu theo decision matrix trọng số.
6. Backbone selection chỉ thực hiện một lần trước tất cả thí nghiệm Metric Learning. Backbone được chọn sẽ được dùng cố định cho toàn bộ factorial experiment và ablations.

**Lý do backbone được cố định trước factorial experiment:** Nếu benchmark cả backbone + feature + metric learning đồng thời, số experiment sẽ là 4 × 2 × 3 = 24 (chưa kể seeds và ablations). Backbone selection được xem là **preliminary experiment**, không phải research variable chính. Việc cố định backbone cho phép tập trung vào nghiên cứu tương tác feature × metric learning, đồng thời giảm compute budget xuống mức khả thi cho luận văn Thạc sĩ.

## 11.4. Backbone Selection Analysis

Trước khi chọn backbone, cần trả lời các câu hỏi:

1. **Accuracy-Latency trade-off**: DS-CNN (20K params) có accuracy ~93% với latency rất thấp. BC-ResNet-32 (110K params) có accuracy ~96% nhưng latency gấp 3-4x. Nếu cả hai đều < 100ms, BC-ResNet-32 là lựa chọn tốt hơn dù nặng hơn.

2. **Quantization compatibility**: Các backbone có hỗ trợ TFLite INT8 không? Tiny CNN và DS-CNN thuần Conv → dễ quantize. MobileNetV2 có depthwise Conv → cần kiểm tra TFLite compatibility. BC-ResNet cũng dùng depthwise → cần verify.

3. **Literature baseline**: DS-CNN là backbone phổ biến nhất trong KWS literature. BC-ResNet là một trong những backbone mạnh nhất trên SCv2. MobileNetV2 phổ biến trong embedded vision nhưng ít được dùng cho KWS.

**Recommendation sơ bộ (cần literature survey để chốt):**
- Nếu ưu tiên simplicity + reproducibility: DS-CNN (safe choice).
- Nếu ưu tiên accuracy: BC-ResNet-32 (SOTA).
- Decision sẽ được chốt sau khi benchmark cả 4 backbones.

## 11.5. Training Strategy (Pretrain → Metric Learning)

Ba strategies được so sánh:

| Strategy | Mô tả | Kỳ vọng |
|---|---|---|
| **A — From Scratch** | Train backbone trực tiếp với ProtoNet loss, không pretrain. | Baseline thấp nhất. |
| **B — Fine-tune All** | Pretrain classification (25-way) → remove FC → fine-tube toàn bộ backbone với ProtoNet loss. | Kỳ vọng cao nhất (học được acoustic representation từ seen classes). |
| **C — Freeze Backbone** | Pretrain classification (25-way) → freeze backbone weights → optimize only the prototype-based metric objective (ProtoNet loss) without updating backbone parameters. | Kiểm tra xem embedding từ backbone pretrain đã sufficient cho metric learning chưa. |

**Chi tiết từng strategy:**

```
Strategy A — From Scratch:
  Input → Backbone → Embedding (128-d, L2-normalized) → ProtoNet Loss
  => Train từ scratch với episode-based metric learning.

Strategy B — Fine-tune All:
  Stage 1: Input → Backbone → 25-way FC → Cross-entropy Loss (pretrain)
  Stage 2: Remove FC → Input → Backbone → Embedding → ProtoNet Loss (fine-tune all layers)

Strategy C — Freeze Backbone:
  Stage 1: Input → Backbone → 25-way FC → Cross-entropy Loss (pretrain)
  Stage 2: Freeze backbone weights → Input → Frozen Backbone → Embedding → ProtoNet Loss
```

Strategy C giúp trả lời: representation từ classification task đã sufficient cho metric learning chưa? Nếu Strategy B ≈ Strategy C → không cần fine-tune, tiết kiệm compute. Nếu Strategy B >> Strategy C → fine-tune là cần thiết.

**Lưu ý về Strategy C (Freeze Backbone):** ProtoNet không có "head" riêng ngoài backbone. Khi freeze backbone, loss không cập nhật backbone weights. Điều này tương đương với việc dùng backbone như một feature extractor cố định — chỉ có prototype computation và cosine similarity hoạt động. Strategy C kiểm tra xem embedding từ pretrain đã đủ discriminative cho few-shot classification chưa.

**Thứ tự thực hiện:**
1. Train classification (Stage 1) cho từng backbone → chọn backbone tốt nhất.
2. Apply cả 3 strategies trên backbone đã chọn.
3. Chọn strategy tốt nhất cho factorial experiment.
4. (Optional) Chạy strategy tốt nhất trên các backbone khác để kiểm tra consistency.

---

# 12. Metric Learning

## 12.1. Phương pháp benchmark

Tất cả sẽ sử dụng cùng một backbone (đã chọn ở §11) và cùng feature extraction. Backbone được cố định trước factorial experiment để giảm số lượng experiment và tập trung vào nghiên cứu tương tác giữa feature extraction và metric learning.

**Primary experiment — Prototypical Networks (primary method):**
- Chạy với 3 seeds, báo cáo mean ± std.
- Đây là phương pháp chính để trả lời RQ1 (factorial design).

**Secondary experiments — Siamese & Triplet:**
- Chạy với 1 seed, chỉ trên feature tốt nhất từ factorial experiment.
- Nếu kết quả không competitive với ProtoNet, chỉ cần report và không cần chạy thêm seeds.
- Mục đích: có baseline để so sánh với literature, tránh bị reviewer hỏi "tại sao không so sánh với X?".

| Phương pháp | Loss | Vai trò |
|---|---|---|
| Prototypical Networks | Cross-entropy trên distances | Primary (3 seeds) |
| Siamese Networks | Contrastive Loss | Secondary (1 seed) |
| Triplet Networks | Triplet Loss (semi-hard) | Secondary (1 seed) |

**Chi tiết secondary protocol:**
- Siamese: dùng contrastive loss, margin=1.0, pair ratio 1:2 (pos:neg).
- Triplet: dùng semi-hard triplet mining, margin=0.2.
- Cùng số epochs, cùng learning rate schedule với ProtoNet (sau khi tuned riêng).

## 12.2. Negative Samples

**Trong training metric learning:**
- ProtoNet: episode-based — mỗi episode chọn N classes từ 25 seen classes. Mặc định N=5.
- Siamese/Triplet: tạo cặp positive (cùng class) và negative (khác class) với tỷ lệ 1:2. Negative được sample từ các class khác trong seen set, bao gồm cả background noise.

**Lưu ý về N (số classes mỗi episode) cho ProtoNet:**
- **Baseline: N=5** — phổ biến trong few-shot literature (ProtoNet gốc, Matching Networks). <!-- SLR: verify optimal N for KWS specifically -->
- **Ablation: N=20** — harder episodic training (có thể tạo embedding mạnh hơn). Chỉ thực hiện nếu còn thời gian. Cần citation để justify nếu sử dụng.

**Trong evaluation (enrollment & runtime detection):**
- Negative là tất cả audio không phải keyword đã đăng ký.
- Cụ thể: các unseen classes khác, unknown speech, background noise, silence.

**Xem thêm §9.2.4 cho Vietnamese negative samples chi tiết.**

## 12.3. Data Augmentation (2-phase)

**Phase 1 (Benchmark chính — không augmentation):**
- 6 configurations (Feature × Metric Learning) được benchmark KHÔNG augmentation.
- Mục tiêu: tìm configuration tốt nhất với cài đặt tối thiểu.

**Phase 2 (Augmentation benchmark — sau khi chọn model):**
- Chọn 1-2 configurations tốt nhất từ Phase 1.
- Benchmark với augmentation để xem mức cải thiện.
- Các augmentation dự kiến: SpecAugment (time/freq masking), noise injection, time shift.

**Lý do chia phase:** Nếu augmentation được đưa vào factorial experiment từ đầu, số thí nghiệm sẽ là 2 × 3 × A (số augmentation strategies) — quá nhiều.

## 12.4. So sánh công bằng

- Cùng backbone.
- Cùng feature extraction.
- Cùng episode-based evaluation protocol.
- Cùng seen/unseen split.
- Cùng seed và random split.
- Cùng episode generation strategy.

---

# 13. Enrollment

**Quy trình enrollment (Vietnamese Validation):**
- Mỗi user đăng ký N keyword.
- Với mỗi keyword, user thu âm 10 mẫu.
- Chọn K samples (K = 1, 3, hoặc 5) từ 10 mẫu để tạo prototype.
- Prototype được lưu vào **Prototype Database** để tra cứu khi inference.

**Cấu hình benchmark:**
- 1-shot: dùng 1 trong 10 mẫu làm prototype.
- 3-shot: dùng 3 trong 10 mẫu làm prototype.
- 5-shot: dùng 5 trong 10 mẫu làm prototype.
- Các mẫu còn lại (10 - K) dùng cho test.

**Prototype computation methods:**

| Method | Công thức | Ghi chú |
|---|---|---|
| **Mean Prototype** | p = mean(embeddings) | Baseline — đơn giản, hiệu quả |
| **Median Prototype** | p = median(embeddings) | Robust với outlier samples (optional ablation) |

Weighted Mean và các phương pháp phức tạp hơn được xếp vào Future Work.

**Đề xuất:** Mean Prototype là baseline. Median là optional ablation.

**Lưu ý:** Enrollment chỉ áp dụng trong Vietnamese Validation Phase. Trong Framework Development Phase, prototype được tính từ support set trong episode (luôn dùng mean).

---

# 14. Runtime Detection

## 14.1. Framework Development

### 14.1.1. Offline (segmented utterances)

Khi người dùng nói (audio đã được cắt sẵn ~1s):

```
Audio (1s utterance)
  ↓
Feature Extraction
  ↓
Embedding (qua backbone)
  ↓
Cosine Similarity với tất cả prototypes (từ support set trong episode)
  ↓
So sánh với Threshold
  ↓
Kết quả: Keyword (nếu similarity > threshold) / Unknown (nếu < threshold)
```

### 14.1.2. Streaming Deployment (Raspberry Pi 4)

Sau khi offline benchmark hoàn tất, pipeline streaming được triển khai trên Raspberry Pi 4 để kiểm tra tính ổn định trước khi áp dụng cho tiếng Việt:

```
USB Microphone (16 kHz)
  ↓
Audio Stream
  ↓
Circular Buffer (~2s)
  ↓
VAD (WebRTC VAD / Silero VAD — fixed front-end)
  ↓
Phát hiện có tiếng nói
  ↓
Sliding Window (1s window, stride 20-40ms)
  ↓
Feature Extraction
  ↓
Embedding (qua backbone)
  ↓
Cosine Similarity với prototypes của unseen GSCv2 classes (enrolled từ support set)
  ↓
Temporal Smoothing / Decision Fusion
  ↓
So sánh với Threshold
  ↓
Kết quả: GSCv2 keyword / Unknown
```

**Mục đích:** Kiểm tra pipeline streaming (VAD, sliding window, temporal smoothing, latency) hoạt động ổn định trên phần cứng thật với GSCv2 trước khi deploy cho tiếng Việt.

## 14.2. Vietnamese Validation — Streaming Deployment (Raspberry Pi 4)

Trên thiết bị thực tế, audio là luồng liên tục từ microphone:

```
USB Microphone (16 kHz)
  ↓
Audio Stream
  ↓
Circular Buffer (~2s)
  ↓
VAD (WebRTC VAD / Silero VAD — fixed front-end)
  ↓
Phát hiện có tiếng nói
  ↓
Sliding Window (1s window, stride 20-40ms)
  ↓
Feature Extraction
  ↓
Embedding (qua backbone)
  ↓
Cosine Similarity với tất cả prototypes trong Prototype Database
  ↓
Temporal Smoothing / Decision Fusion
  ↓
So sánh với Threshold
  ↓
Kết quả: Keyword (nếu similarity > threshold) / Unknown
```

**Chi tiết các thành phần:**

- **Circular Buffer (~2s):** Đệm audio stream để VAD và sliding window có đủ dữ liệu xử lý mà không bị mất frames.
- **Sliding Window:** Window size 1 giây (phù hợp với độ dài training). Stride 20-40ms (tương đương 25-50 frames/second).
- **Prototype Database:** Lưu tất cả prototype embeddings của các keyword đã đăng ký. Tra cứu bằng cosine similarity O(N) với N = số keyword.
- **Temporal Smoothing / Decision Fusion:** Các chiến lược:
  - **Majority vote:** Ghi nhận predictions trên last 5 windows, chọn label xuất hiện nhiều nhất.
  - **K consecutive detections:** Xác nhận keyword nếu similarity > threshold trong K/5 frames liên tiếp (K cần tuned, khởi tạo K=3).
  - **Threshold crossing:** Phát hiện temporal peak của similarity score, tránh trigger do noise ngẫu nhiên.
- **VAD:** Fixed front-end (WebRTC VAD hoặc Silero VAD), không phải research contribution.

## 14.3. Unknown Detection

**Bài toán:** Với User-defined KWS, hệ thống phải phân biệt được "keyword đã đăng ký" vs "mọi thứ khác" (unknown). Đây là bài toán open-set về bản chất, nhưng nằm ngoài phạm vi nghiên cứu Open Set Recognition chuyên sâu.

**Approach:**
- Dùng Cosine Similarity giữa query embedding và tất cả prototypes.
- Nếu max similarity > threshold → predict keyword tương ứng.
- Nếu max similarity ≤ threshold → predict "unknown".

**Chiến lược threshold:**

| Loại | Mô tả | Phase |
|---|---|---|
| **Fixed global threshold** | Một threshold duy nhất cho mọi keyword. Tối ưu theo EER trên threshold validation set. | Framework Development (baseline) |
| **Per-keyword threshold** | Mỗi keyword có threshold riêng (dựa trên intra-class distance của enrollment samples). | Vietnamese Validation (nếu cần) |
| **Adaptive / Calibration** | Threshold thay đổi hoặc temperature scaling. | Future Work |

**Đề xuất:** Fixed global threshold cho Framework Development. Per-keyword threshold cho Vietnamese Validation nếu enrollment samples đủ nhiều.

## 14.4. Threshold Selection Protocol

```
Training set (25 seen speech keyword classes)
  ↓ Train backbone + metric learning
Threshold Validation set (5 classes: backward, forward, visual, follow, learn + _background_noise_ samples)
  ↓ Optimize global threshold (tối ưu F1-score hoặc EER trên validation set)
Freeze threshold
  ↓
Test set (5 unseen speech keyword classes, episode-based)
  ↓ Báo cáo kết quả với threshold đã freeze
```

**Lưu ý:** Threshold KHÔNG được tối ưu trên test set (tránh data leakage). Threshold được cố định sau validation và dùng cho toàn bộ test episodes. Threshold validation set gồm 5 speech classes + background noise (cắt từ _background_noise_ thành segments ~1s) — đây là những mẫu "không phải keyword", phù hợp để tìm threshold tối ưu.

---

# 15. Evaluation Protocol

## 15.1. Framework Development – Episode-based Benchmark

**Mục tiêu:** Đánh giá khả năng tổng quát hóa trên unseen speech keywords.

**Chỉ sử dụng speech keyword classes cho episode evaluation:**
- Episode chỉ gồm các class là từ thật (house, marvin, sheila, tree, wow).
- backward, forward, visual, follow, learn và _background_noise_ KHÔNG xuất hiện trong episode.

**Fixed seen/unseen split:** (xem §9.1)

**Episode Generation Strategy:**
- Mỗi episode: chọn N = 5 (từ 5 unseen speech classes).
- Support và query samples đến từ DIFFERENT utterances, cùng speaker (speaker-dependent).
- Các utterance của unseen classes được chia: support (K samples) + query (phần còn lại).

**Protocol:**
1. Với mỗi episode:
   - Chọn N = 5 classes từ unseen speech keyword set.
   - Mỗi class chọn support samples (1, 3, hoặc 5) và query samples (phần còn lại).
2. Báo cáo trung bình trên nhiều episodes (tối thiểu 1000 episodes).
3. Báo cáo kèm standard deviation (độ tin cậy).

**Cấu hình:**
- 5-way 1-shot
- 5-way 3-shot
- 5-way 5-shot

### 15.1.1 Framework Development – Streaming Evaluation (Raspberry Pi 4)

Sau khi episode-based benchmark hoàn tất, pipeline streaming được đánh giá trên Raspberry Pi 4 để xác nhận tính ổn định trước khi áp dụng cho tiếng Việt.

- **Enrollment (cho streaming test):** Enroll 5 unseen GSCv2 classes (house, marvin, sheila, tree, wow) bằng cách dùng support set từ SCv2 để tính prototype.
- **Streaming test data:** Các file audio dài (~30-60 giây) được ghép từ SCv2 test samples + background noise + silence, mô phỏng luồng â thanh liên tục.
- **Streaming pipeline:** Circular Buffer → VAD → Sliding Window → Feature → Backbone → Cosine Similarity → Temporal Smoothing → Threshold.
- **Offline metrics:** Accuracy, Precision, Recall, F1-score, FAR, FRR, EER.
- **Streaming metrics:** Detection Latency (ms), FA/hour, Miss Rate, RTF, CPU Usage, Memory.
- **Mục đích:** Kiểm tra pipeline streaming hoạt động ổn định trên Pi 4 trước khi deploy cho tiếng Việt.

## 15.2. Vietnamese Validation – Streaming Deployment Evaluation

Vietnamese Validation KHÔNG sử dụng episode-based evaluation. Thay vào đó, nó triển khai hệ thống streaming thực tế:

- **Enrollment**: User đăng ký N keyword. Với mỗi keyword, dùng 5 mẫu enrollment để tính prototype (mean embedding).
- **Streaming pipeline**: Microphone → VAD → Sliding Window → Feature → Backbone → Cosine Similarity → Threshold.
- **Evaluation trên test set**: test set gồm các file audio dài (10-30 giây) chứa cả keyword và non-keyword (xem §9.2.4), được phát qua microphone hoặc injected trực tiếp vào pipeline.
- **Offline metrics**: Accuracy, Precision, Recall, F1-score, FAR, FRR, EER.
- **Streaming metrics**: Detection Latency, FA/hour, Miss Rate, RTF.
- **Phân tích chi tiết:**
  - Confusion matrix giữa các keyword tiếng Việt (cặp nào hay nhầm).
  - FAR theo từng nhóm negative (background vs random speech vs other keywords vs phonetically similar).
  - Detection latency distribution.
  - FA/hour vs threshold trade-off curve.

**Khác biệt chính giữa hai phase:**

| Framework Development (GSCv2) | Vietnamese Validation |
|---|---|
| **Keyword Classification** (offline) | **Keyword Detection** (streaming) |
| Episode-based evaluation | Streaming deployment pipeline |
| Support set → Query (trong cùng episode) | Enrollment set (5 mẫu) → Prototype → Sliding Window |
| N classes mỗi episode | User tự chọn số lượng keyword |
| Speaker-dependent (cùng speaker, khác trial) | Cùng user enrollment và test |
| Chỉ speech keywords trong episode | Gồm cả positive và negative (4 nhóm) + trigger |
| Threshold từ validation set | Threshold từ Development Phase (tuned lại với streaming data) |
| Metrics: Acc, F1, EER | Metrics: Acc, F1, EER, FA/hour, RTF, Detection Latency |

---

# 16. Evaluation Metrics

## 16.1. Classification Metrics

- Accuracy
- Precision (macro, micro)
- Recall (macro, micro)
- F1-score (macro, micro)
- Confusion Matrix

## 16.2. Verification Metrics (Keyword vs Unknown)

- FAR (False Acceptance Rate)
- FRR (False Rejection Rate)
- ROC Curve
- EER (Equal Error Rate)
- AUC (Area Under Curve)
- FAR breakdown theo từng nhóm negative (Vietnamese Validation)

## 16.3. Edge AI Metrics (Raspberry Pi 4)

- Latency (ms) – per inference (feature extraction + backbone + similarity).
- Memory Usage (MB) – peak RAM.
- CPU Usage (%).
- Power Consumption (W).
- Model Size (MB) – TFLite INT8.
- Enrollment Time (ms) – time to compute prototype.

## 16.4. Streaming Metrics (cho cả hai phase)

- **Detection Latency (ms):** thời gian từ khi keyword xuất hiện trong stream đến khi hệ thống đưa ra quyết định.
- **False Alarm Rate (FA/h hoặc FA/hour):** số lần false positive mỗi giờ — metric quan trọng cho KWS thực tế.
- **Miss Rate:** tỷ lệ bỏ sót keyword (false negative).
- **Real-time Factor (RTF):** thời gian xử lý / thời gian audio. RTF < 1 → real-time.
- **CPU Usage (%):** tải CPU trong quá trình streaming.
- **Decision Fusion Sensitivity:** số frames liên tiếp (K trong N) cần thiết để xác nhận keyword — ảnh hưởng đến detection latency và FA rate.
- **CPU Temperature (°C):** đo thermal throttling trên Raspberry Pi 4 trong quá trình streaming kéo dài.

## 16.5. Error Analysis (post-benchmark)

Sau khi có kết quả, phân tích chi tiết:

- **Confusion Matrix**: keyword nào hay bị nhầm với keyword nào? Cặp "bật đèn"/"tắt đèn" có tỷ lệ lỗi cao hơn không?
- **FAR decomposition**: false positive chủ yếu đến từ nhóm negative nào (background, random speech, other keywords, phonetically similar)?
- **Speaker leakage analysis (Development Phase)**: So sánh accuracy trên "overlap samples" (speaker ID xuất hiện cả trong seen và unseen sets) vs "non-overlap samples" (speaker ID chỉ xuất hiện trong unseen set). Báo cáo gap tuyệt đối và effect size (Cohen's d). Nếu gap > 5% → speaker leakage là significant.
- **Speaker-level analysis (Vietnamese Validation)**: speaker nào có accuracy thấp nhất? (giọng nam/nữ? giọng trầm/bổng?)
- **t-SNE visualization**: visualize embeddings của tất cả classes (seen + unseen) để kiểm tra cluster quality.
- **Threshold analysis**: ROC curve, EER comparison giữa fixed global threshold và per-keyword threshold.
- **Enrollment analysis**: So sánh accuracy khi dùng mean vs median prototype.
- **Case study**: chọn 1 user điển hình, phân tích chi tiết enrollment → detection → error.
- **(Optional) Calibration curve:** Phân tích mức độ calibration của similarity scores so với confidence thực tế.

---

# 17. Research Hypothesis

**H1 — Feature × Method Interaction:** Different combinations of feature extraction (MFCC, Log-Mel) and metric learning methods (ProtoNet, Siamese, Triplet) significantly affect UDKWS performance. The optimal combination depends on the interaction between feature representation and metric learning strategy.

**H2 — Shot Impact:** Accuracy increases with the number of enrollment samples (1, 3, 5-shot) with diminishing returns.

**H3 — Edge Feasibility:** A lightweight metric-learning framework can achieve real-time inference (< 100ms) on Raspberry Pi 4 with minimal accuracy degradation after INT8 quantization.

Các ablations (training strategy, augmentation, prototype method) không có hypothesis riêng — được xem là exploratory analysis.

# 18. Research Questions

## RQ1 — Feature Extraction × Metric Learning

> **How do different combinations of Audio Feature Extraction and Metric Learning strategies affect User-defined Few-shot Keyword Spotting performance?**

**Hypothesis (H2):** Different feature representations interact differently with metric learning methods. We expect the ranking of methods to vary across feature types.

**Thiết kế thí nghiệm:** Factorial Design 2 × 3

| Feature \ Metric Learning | Prototypical (N=5) | Siamese | Triplet |
|---|---|---|---|
| MFCC | Acc, F1, EER (3 seeds) | Acc, F1, EER (1 seed) | Acc, F1, EER (1 seed) |
| Log-Mel Spectrogram | Acc, F1, EER (3 seeds) | Acc, F1, EER (1 seed) | Acc, F1, EER (1 seed) |

- **Primary cells:** ProtoNet × {MFCC, Log-Mel} — 3 seeds each → 6 experiments.
- **Secondary cells:** Siamese/Triplet × {MFCC, Log-Mel} — 1 seed each → 4 experiments.
- Tổng: 10 experiments.
- Tất cả trên cùng episode-based protocol, cùng backbone (đã chọn từ §11).

**Expected outcome:** Xác định feature và metric learning method tốt nhất cho UDKWS.

---

## RQ2 — Shot Number

> **Số lượng enrollment samples (1, 3, 5-shot) ảnh hưởng như thế nào đến hiệu năng nhận diện?**

**Hypothesis (H1):** Accuracy tăng theo số lượng support samples, với diminishing returns (5-shot > 3-shot > 1-shot, nhưng gap 3→5 nhỏ hơn gap 1→3).

**Thiết kế thí nghiệm:**
- Dùng configuration tốt nhất từ RQ1 (feature + metric learning).
- So sánh accuracy và EER trên episode-based: 5-way 1-shot, 5-way 3-shot, 5-way 5-shot.
- 3 seeds.

**Expected outcome:** Xác định minimum number of enrollment samples cần thiết cho acceptable accuracy.

---

## RQ3 — Edge Deployment Trade-off

> **What is the trade-off between latency, memory footprint, and recognition accuracy when deploying the proposed framework on Raspberry Pi 4?**

**Hypothesis (H3):** A lightweight model can achieve per-inference latency < 100ms and real-time streaming operation (RTF < 1) on Raspberry Pi 4 with minimal accuracy degradation after INT8 quantization.

**Thiết kế thí nghiệm:**
- Dùng configuration tốt nhất từ RQ1-RQ2.
- Đo Edge AI metrics trên Raspberry Pi 4.
- So sánh accuracy trước và sau INT8 quantization.

**Metric:** latency (ms), model size (MB), memory (MB), accuracy before/after INT8.

---

## Ablations (không phải RQ riêng)

Các thí nghiệm phụ hỗ trợ interpretation:

| Ablation | Mô tả | Vị trí |
|---|---|---|
| **Training Strategy** | Scratch vs Fine-tune All vs Freeze Backbone (§11.5) | §11.5 |
| **Data Augmentation** | Phase 1 (no aug) vs Phase 2 (SpecAugment, noise) | §12.3 |
| **Prototype Method** | Mean vs Median | §13 |
| **Threshold Strategy** | Global vs Per-keyword | §14.3 |

## RQ-Hypothesis Mapping

| Research Question | Hypothesis | Experiment |
|---|---|---|
| RQ1: Feature × Metric Learning | H1: Feature-method interaction matters | Factorial design 2×3 |
| RQ2: Shot number | H2: Diminishing returns with more shots | Episode-based 1/3/5-shot |
| RQ3: Edge trade-off | H3: Real-time feasible on Pi 4 | Deployment metrics + INT8 |

---

# 19. Statistical Analysis

Để đảm bảo kết luận có ý nghĩa thống kê:

- **Primary experiments (ProtoNet × 2 features):** 3 seeds → báo cáo mean ± std. So sánh giữa MFCC và Log-Mel dùng **paired t-test** hoặc **Wilcoxon signed-rank test** (tùy normality).
- **Secondary experiments (Siamese, Triplet):** 1 seed — descriptive statistics, không kiểm định.
- **Training strategy ablation (3 strategies):** 3 seeds → **Repeated Measures ANOVA** hoặc **Friedman test** (non-parametric).
- **Shot number (1/3/5):** 3 seeds → so sánh pairwise với Bonferroni correction.
- **Threshold comparison:** So sánh EER giữa global và per-keyword threshold dùng bootstrap confidence intervals.
- **Effect size:** Báo cáo Cohen's d hoặc η² cho các so sánh chính.
- **Confidence intervals:** Báo cáo 95% CI cho accuracy, F1, và EER trên primary experiments.
- Tất cả kiểm định được thực hiện với α = 0.05.

---

# 20. Threats to Validity

## Internal Validity
- **Speaker leakage (Development Phase):** SCv2 có speaker overlap giữa seen và unseen → accuracy có thể bị inflate. Được kiểm soát qua speaker leakage analysis (so sánh overlap vs non-overlap samples).
- **Hyperparameter tuning:** Các method (ProtoNet, Siamese, Triplet) có optimal hyperparameters khác nhau. Được kiểm soát bằng cách tune riêng từng method trên validation subset trước khi benchmark chính thức.

## External Validity
- **Generalizability:** Development Phase chỉ benchmark trên SCv2 (tiếng Anh). Kết quả có thể không generalize hoàn toàn sang tiếng Việt. Vietnamese Validation Phase là bước kiểm tra generalizability đầu tiên.
- **Hardware specificity:** Deployment chỉ benchmark trên Raspberry Pi 4. Kết quả latency có thể khác trên Pi 5 hoặc các edge device khác.
- **Dataset scale:** Vietnamese dataset là proof-of-concept (20 speakers, 10 keywords). Kết quả có thể không scale lên large-scale deployment.

## Ecological Validity
- **Recording condition:** Vietnamese dataset được thu trong phòng yên tĩnh, khoảng cách mic ~30cm. Kết quả có thể không generalize sang môi trường thực tế (ồn ào, xa mic, multiple speakers). Đây là limitation được ghi nhận.
- **Trigger mechanism:** Hệ thống giả định có VAD hoặc nút bấm kích hoạt. Trong thực tế, có thể cần wake-word detection bổ sung.

## Construct Validity
- **Episode-based evaluation:** Protocol 5-way K-shot đo generalization lên unseen classes, nhưng không trực tiếp đo UDKWS workflow. Vietnamese Validation Phase bổ sung enrollment workflow để giải quyết gap này.
- **Threshold selection:** Threshold validation set gồm các classes không phải keyword thực tế (backward, forward, visual, follow, learn + noise). Performance trên threshold validation có thể khác với unseen keywords thật.

## Conclusion Validity
- **Statistical power:** 3 seeds cho primary experiments. Có thể thiếu statistical power để phát hiện small effect sizes. Được ghi nhận và báo cáo effect size để hỗ trợ interpretation.
- **Metric selection:** Accuracy và EER được chọn làm primary metrics. Các metrics khác (precision, recall) được báo cáo supplementary.

---

## RQ2 — Shot Number

> **Số lượng enrollment samples (1, 3, 5-shot) ảnh hưởng như thế nào đến hiệu năng nhận diện?**

**Hypothesis:** Accuracy tăng theo số lượng support samples, với diminishing returns (5-shot > 3-shot > 1-shot, nhưng gap 3→5 nhỏ hơn gap 1→3).

**Thiết kế thí nghiệm:**
- Dùng configuration tốt nhất từ RQ1 (feature + metric learning).
- So sánh accuracy và EER trên episode-based: 5-way 1-shot, 5-way 3-shot, 5-way 5-shot.
- 3 seeds.

**Expected outcome:** Xác định minimum number of enrollment samples cần thiết cho acceptable accuracy.

---

## RQ3 — Training Strategy

> **Pretrain classification có cải thiện hiệu năng metric learning so với train từ scratch không?**

**Hypothesis:** Fine-tune all (Strategy B) > Freeze backbone (Strategy C) > From scratch (Strategy A).

**Thiết kế thí nghiệm:**
- Dùng configuration tốt nhất từ RQ1-RQ2.
- So sánh 3 strategies (§11.5) trên episode-based evaluation.
- 3 seeds.

**Expected outcome:** Xác định training strategy tối ưu cho UDKWS.

---

## RQ4 — Edge Deployment Trade-off

> **What is the trade-off between latency, memory footprint, and recognition accuracy when deploying the proposed framework on Raspberry Pi 4?**

**Hypothesis:** A lightweight model can achieve per-inference latency < 100ms and real-time streaming operation (RTF < 1) on Raspberry Pi 4 with minimal accuracy degradation after INT8 quantization.

**Thiết kế thí nghiệm:**
- Dùng configuration tốt nhất từ RQ1-RQ3.
- Đo Edge AI metrics trên Raspberry Pi 4.
- So sánh accuracy trước và sau quantization.

**Metric:** latency (ms), model size (MB), memory (MB), accuracy before/after INT8.

---

# 19. Research Contributions

## Contribution 1 — Unified UDKWS Framework (Primary)

Một framework modular, hoàn chỉnh cho User-defined Vietnamese Keyword Spotting trên Edge Devices (Raspberry Pi 4), bao gồm:
- Pipeline modular từ data → feature → backbone → metric learning → enrollment → streaming detection → deployment.
- Phân tách rõ Problem (UDKWS) / Method (Few-shot Metric Learning) / Application (Edge AI).
- Phân biệt rõ Development Phase (few-shot classification benchmark trên GSCv2) và Vietnamese Validation Phase (UDKWS streaming deployment).

## Contribution 2 — Unified Evaluation Protocol + Comprehensive Benchmark

- **Protocol:** Unified seen/unseen split, episode generation, threshold optimization, streaming evaluation pipeline, enrollment protocol.
- **Benchmark:** Factorial design (2 × 3) Feature × Metric Learning, primary/secondary experiment design.
- **Ablations:** Training strategy (Scratch vs Fine-tune vs Freeze), data augmentation, prototype method.
- **Analysis:** Speaker leakage analysis, error analysis (confusion matrix, t-SNE, FAR decomposition), statistical testing.

## Contribution 3 — Vietnamese Deployment Case Study

Thiết kế và triển khai evaluation protocol cho UDKWS tiếng Việt trên Raspberry Pi 4:
- **Dataset design guideline:** tiêu chí chọn keyword (smart home), protocol thu âm, metadata, consent form.
- **Negative protocol:** 4 nhóm negative (background, random speech, other keywords, phonetically similar).
- **Enrollment protocol:** 10 recordings/keyword, benchmark 1/3/5-shot, prototype database.
- **Streaming protocol:** VAD + circular buffer + sliding window + temporal smoothing.
- Dataset là proof-of-concept demonstration (~20 speakers, ~10 keywords).

## Supporting Empirical Analysis (không phải contribution chính)

- Speaker leakage analysis (overlap vs non-overlap accuracy, Cohen's d).
- Enrollment strategy comparison (mean vs median).
- Threshold strategy (global vs per-keyword).
- Error analysis (confusion matrix, t-SNE, FAR decomposition, calibration curve).

---

# 19. Candidate Methods

## 19.1. Backbone Candidates

Benchmark 4 backbones với classification task (25-way). Thứ hạng dựa trên literature, con số cụ thể sẽ được cập nhật sau literature survey. Các backbone được chọn vì tính đại diện và phổ biến trong KWS literature.

| Backbone | Mô tả |
|---|---|
| Tiny CNN | Baseline — kiến trúc CNN cơ bản nhất |
| DS-CNN | Depthwise separable CNN — widely used trong KWS |
| BC-ResNet-32 | Bottleneck-Conv ResNet — một trong những backbone mạnh nhất trên Speech Commands benchmark |
| MobileNetV2 (α=0.35) | Lightweight backbone phổ biến trong embedded vision |

## 19.2. Metric Learning Candidates

So sánh 3 phương pháp trên cùng task episode-based (5-way K-shot, unseen classes). Thứ hạng dựa trên literature.

| Method | Ghi chú |
|---|---|
| Prototypical Networks (N=5) | Primary — đơn giản, hiệu quả, ổn định |
| Siamese Networks | Secondary — contrastive loss, pairwise |
| Triplet Networks | Secondary — triplet loss, semi-hard mining |

## 19.3. Không sử dụng

- d-vector, x-vector: speaker embedding, không phù hợp keyword embedding.
- TC-ResNet: có thể cân nhắc cho future work.

---

# 20. Deployment: Raspberry Pi 4

## Thông số phần cứng cố định

- Model: Raspberry Pi 4 Model B (4GB RAM)
- CPU: ARM Cortex-A72 (4 cores, 1.8GHz)
- OS: Raspberry Pi OS Lite (64-bit)
- Framework: TensorFlow Lite (TFLite)
- Quantization: INT8 (post-training quantization)
- Microphone: USB microphone

## Định nghĩa Real-time

**Hai loại latency cần phân biệt:**

| Loại | Định nghĩa | Target | Phase |
|---|---|---|---|
| **Per-inference latency** | Thời gian xử lý một window 1s (feature + backbone + similarity) | < 100ms | Cả hai phase (bắt buộc) |
| **End-to-end detection latency** | Thời gian từ khi keyword xuất hiện trong stream đến khi hệ thống đưa ra quyết định (bao gồm VAD + sliding window + temporal smoothing) | < 300ms | Cả hai phase |
| **Real-time Factor (RTF)** | Thời gian xử lý / thời gian audio. RTF < 1 → real-time | < 1 | Cả hai phase |

Per-inference latency là metric benchmark chính (đo trên cả hai phase). End-to-end detection latency phụ thuộc vào temporal smoothing strategy (số frames cần để confirm) và sẽ được báo cáo riêng.

Tất cả benchmark latency chỉ thực hiện trên Raspberry Pi 4, không benchmark trên Pi 3 hay Pi 5.

---

# 21. Tài liệu cần hoàn thành trước khi implement

Theo thứ tự ưu tiên:

1. **Research Design Specification** — tài liệu tổng thể (mục tiêu, research gap, RQ, contribution, phạm vi, timeline).
2. **Systematic Literature Survey** — khảo sát tài liệu có hệ thống để chốt mọi quyết định kỹ thuật (backbone, training strategy, episode generation, thresholding, augmentation) và chứng minh research gaps. Mỗi quyết định phải có paper làm cơ sở.
3. **Evaluation Protocol Specification** — định nghĩa chi tiết cách train/validation/benchmark (Framework Development & Vietnamese Validation), bao gồm xử lý speaker leakage.
4. **Dataset Design Specification** — mô tả chi tiết bộ dữ liệu tiếng Việt (tiêu chí chọn keyword, protocol thu âm, metadata, consent form).
5. **Backbone Survey & Selection Report** — khảo sát tài liệu + benchmark sơ bộ để chốt backbone.

---

# 22. Research Timeline (dự kiến)

| Phase | Nội dung | Thời gian |
|---|---|---|
| 1 | Systematic Literature Survey | 4 tuần |
| 2 | Dataset Analysis + Backbone Benchmark | 4 tuần |
| 3 | Metric Learning Benchmark (Factorial Design) | 6 tuần |
| 4 | Training Strategy Ablation + Error Analysis | 3 tuần |
| 5 | Streaming Deployment trên Pi 4 (với GSCv2) | 3 tuần |
| 6 | Vietnamese Dataset Collection | 4 tuần |
| 7 | Statistical Analysis + Final Evaluation | 3 tuần |
| 8 | Viết luận văn / Paper | 6 tuần |

**Tổng:** ~34 tuần (~8.5 tháng).

---

# 23. Mục tiêu cuối cùng

Kết quả kỳ vọng của dự án gồm:

- Framework nghiên cứu hoàn chỉnh (modular, có thể mở rộng).
- Research Gap và Novelty được xác định rõ ràng.
- Systematic Literature Survey cho các quyết định kỹ thuật.
- **Framework Development Phase (GSCv2):**
  - Benchmark Feature Extraction (MFCC vs Log-Mel).
  - Benchmark Metric Learning (ProtoNet vs Siamese vs Triplet).
  - Factorial experiment kết hợp Feature × Metric Learning.
  - Training strategy ablation (Scratch vs Fine-tune All vs Freeze Backbone).
  - Data Augmentation benchmark (Phase 2).
  - Error Analysis (confusion matrix, t-SNE, FAR decomposition, speaker-level analysis, case study).
  - Speaker leakage analysis.
- **Vietnamese Validation Phase:**
  - Vietnamese Case Study Dataset (~20 speaker, ~10 keyword, 4 nhóm negative, speaker-disjoint split).
  - Enrollment workflow benchmark (1/3/5-shot).
  - Streaming detection pipeline trên Raspberry Pi 4 (VAD + sliding window + temporal smoothing).
  - Streaming metrics (FA/hour, RTF, Detection Latency).
- Pipeline huấn luyện và đánh giá tái sử dụng được.
- Luận văn Thạc sĩ hoàn chỉnh.
- Ít nhất một bài báo khoa học hướng tới hội nghị quốc tế hoặc tạp chí Q2 trở lên.

---

# 23. Reproducibility

Để đảm bảo các thí nghiệm có thể tái lập sau 6 tháng:

- **Fixed random seed**: tất cả thí nghiệm dùng seed cố định (ví dụ seed=42). Các thí nghiệm chính chạy với 3 seeds khác nhau và báo cáo mean ± std.
- **Fixed class split**: seen/unseen/threshold split được cố định (§9.1), không random.
- **Fixed episode generation**: episode generator được seed và ghi log để có thể tái tạo.
- **Fixed train/val/test split**: dùng validation_list.txt và testing_list.txt từ SC v2.
- **Config files**: tất cả tham số được lưu trong YAML config files.
- **Experiment tracking**: dùng MLflow hoặc wandb để log metrics, configs, model weights.
- **Code versioning**: mọi thay đổi code được commit với mô tả rõ ràng. Git commit hash được ghi trong experiment log.
- **Dataset version**: Ghi rõ dataset version (SCv2 v0.02) và link download. Vietnamese dataset version được quản lý riêng.
- **Model checkpoint hash**: Mỗi trained model được lưu kèm SHA256 hash để đảm bảo integrity.
- **Evaluation script version**: Mỗi lần chạy evaluation được log với script version + git hash + timestamp.
- **Environment**: Dockerfile hoặc requirements.txt với versions cố định (Python, PyTorch/TF, librosa/torchaudio, TFLite). Feature extraction library (librosa version X.X) được ghi rõ để tránh khác biệt giữa các implementation.
- **Pipeline automation**: Makefile hoặc shell script tự động hóa toàn bộ pipeline từ download dataset → preprocessing → training → evaluation → logging.
- **Hardware reproducibility**: Ghi rõ CPU/GPU model, RAM, OS version cho cả training server và Raspberry Pi 4 deployment.

---

# 24. Lưu ý implement

- Tất cả code phải viết dạng modular: dataloader → feature extractor → backbone → metric learning → evaluator → deployment.
- Config bằng YAML, có logging và experiment tracking (MLflow hoặc wandb).
- Seed được fix để đảm bảo reproducibility (xem §23).
- Episode generation phải đảm bảo support và query đến từ different utterances (cùng speaker).
- Threshold chỉ optimize trên threshold validation set (5 classes + _background_noise_), không chạm vào test set cho đến final evaluation.
- Framework Development có **cả offline benchmark (segmented utterances) lẫn streaming deployment trên Pi 4** (với GSCv2 unseen classes). Vietnamese Validation là streaming deployment thuần (với Vietnamese keywords + enrollment workflow).
- Streaming pipeline (circular buffer + VAD + sliding window + temporal smoothing) được implement **chung cho cả hai phase**, chỉ khác dataset đầu vào.
- **Prototype Database** là thành phần bắt buộc trong streaming pipeline: lưu trữ và tra cứu prototype embeddings của tất cả keyword đã đăng ký.
- **Circular Buffer (~2s)** cần được implement để đệm audio stream cho VAD và sliding window.
- **Temporal Smoothing** cần được implement với ít nhất một strategy (majority vote hoặc K consecutive detections). Giá trị K cần tuned trên validation set.
- VAD là fixed front-end (WebRTC VAD hoặc Silero VAD), không phải research contribution.
- **Latency measurement:** Phân biệt per-inference latency (benchmark) và end-to-end detection latency (streaming deployment).
- Quyết định kỹ thuật (backbone, N, learning rate, v.v.) cần dựa trên literature survey, không chỉ intuition.
