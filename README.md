# PDS301M - IMDb & OMDb Movie Ratings and Metadata Analysis

> **Dự án Cuối kỳ Môn Học PSD301M — Python for Data Science**  
> **Chủ đề:** Nghệ thuật vs. Thương mại: Giải mã "Nghịch lý Phổ biến vs. Chất lượng" trong Điện ảnh.

---

## 📌 Tổng quan dự án (Project Overview)

Dự án này phân tích tập dữ liệu điện ảnh quy mô lớn từ **IMDb Official Datasets** (>337.000 phim điện ảnh) kết hợp làm giàu dữ liệu qua **OMDb RESTful Web API** nhằm giải mã mối tương quan giữa điểm số đánh giá, độ phổ biến (lượt bình chọn), doanh thu phòng vé và thể loại điện ảnh.

Dự án áp dụng công thức **Bayesian Weighted Rating** chuẩn của IMDb, tối ưu hóa tính toán bằng **NumPy Vectorization**, triển khai cấu trúc dữ liệu thuần **Pure Python** và trực quan hóa chuyên sâu bằng **Matplotlib/Seaborn**.

---

## 📂 Cấu trúc thư mục (Project Structure)

```text
Project/
├── main.py                     # Pipeline chạy tự động toàn diện từ A-Z
├── src/                        # Thư viện mã nguồn chính của dự án
│   ├── api_collector.py        # Module cào & làm giàu dữ liệu từ OMDb RESTful API
│   ├── data_processor.py       # Pipeline xử lý, làm sạch & tính điểm Bayesian
│   ├── numpy_analyzer.py       # Tính toán vector hóa bằng NumPy (WR, thống kê)
│   ├── basics_utils.py         # Cấu trúc dữ liệu & logic Pure Python
│   └── visualizer.py           # Bộ 5 biểu đồ trực quan hóa dữ liệu
├── notebooks/
│   └── read2.ipynb             # Jupyter Notebook báo cáo chi tiết kèm narrative
├── outputs/                    # Kết quả tính toán & biểu đồ xuất ra
│   ├── top_movies.csv          # Top 100 phim xếp hạng theo Weighted Rating
│   ├── genre_summary.csv       # Thống kê điểm số & số lượng theo thể loại
│   ├── decade_summary.csv      # Xu hướng điểm số qua các thập kỷ (1950 - 2020)
│   └── figures/                # 5 Biểu đồ chất lượng cao (PNG)
│       ├── 01_genre_rating.png
│       ├── 02_votes_vs_rating.png
│       ├── 03_rating_by_decade.png
│       ├── 04_rating_histogram.png
│       └── 05_correlation_heatmap.png
├── report/
│   ├── report.md               # Báo cáo học thuật chi tiết
│   └── report.pdf              # Báo cáo dạng PDF chuẩn format
├── PDS301m_Group01/
│   └── Movie_Rating/           # Ứng dụng Web Dashboard tương tác (Streamlit + Plotly)
├── requirements.txt            # Danh sách thư viện Python cần thiết
└── README.md                   # Tài liệu hướng dẫn dự án
```

---

## 🏆 Tiêu chí Đánh giá & Hoàn thành Rubric (100%)

| Thành phần | Tiêu chí Rubric | Trạng thái | Module thực thi |
| :--- | :--- | :---: | :--- |
| **API Data Collection** | Thu thập qua RESTful API, Rate limit, xử lý JSON | **25% / 25%** | `src/api_collector.py` |
| **NumPy Processing** | Mảng 1D float64, Vectorization, Thống kê mô tả | **15% / 15%** | `src/numpy_analyzer.py` |
| **Python Basics** | Pure Python logic (List, Dict, Set, Tuple), không dùng Pandas/NumPy | **25% / 25%** | `src/basics_utils.py` |
| **Visualizations** | 3 nhóm biểu đồ, 5 hình (Bar, Scatter, Line, Hist, Heatmap) | **20% / 20%** | `src/visualizer.py` |
| **Notebook & Report** | Storytelling narrative, giải thích ý nghĩa số liệu, Báo cáo PDF | **15% / 15%** | `notebooks/read2.ipynb`, `report/` |

---

## 🚀 Hướng dẫn Cài đặt & Chạy Dự án (Quick Start)

### 1. Chuẩn bị môi trường ảo Python
```bash
# Tạo và kích hoạt môi trường ảo
python3 -m venv .venv
source .venv/bin/activate  # Trên Linux / macOS
# .venv\Scripts\activate   # Trên Windows

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 2. Thiết lập OMDb API Key
Tạo file `.env` tại thư mục gốc của dự án hoặc export biến môi trường:
```bash
export OMDb_API_KEY='5b651fc0'
```

### 3. Thực thi Pipeline phân tích dữ liệu
Chạy toàn bộ pipeline chỉ với 1 câu lệnh duy nhất:
```bash
python main.py
```
Toàn bộ các tệp CSV tổng hợp và 5 biểu đồ trực quan sẽ được tự động xuất ra thư mục `outputs/`.

### 4. Thu thập dữ liệu từ OMDb API (Tùy chọn)
Để cào dữ liệu mới cho 100 bộ phim từ OMDb API:
```bash
python src/api_collector.py
```

### 5. Chạy Web Dashboard tương tác (Genre Lens)
```bash
cd PDS301m_Group01/Movie_Rating
streamlit run main.py
```
Truy cập trình duyệt tại địa chỉ `http://localhost:8501`.

---

## 👥 Thành viên nhóm (Group 01)
- Lương Văn Thắng (Leader)
- Thành viên nhóm PDS301M - Nhóm 01
