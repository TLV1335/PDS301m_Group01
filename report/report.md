# BÁO CÁO DỰ ÁN PHÂN TÍCH DỮ LIỆU ĐIỆN ẢNH (PSD301M)
## Giải Mã "Nghịch Lý Phổ Biến vs Chất Lượng" Trong Điện Ảnh Qua Dữ Liệu IMDb & OMDb API

**Học phần:** PSD301M — Python for Data Science  
**Đề tài:** Phân tích Dữ liệu Điểm số & Siêu dữ liệu Điện ảnh IMDb kết hợp OMDb RESTful API  
**Bộ dữ liệu:** IMDb Non-Commercial Datasets & OMDb API (96+ phim được làm giàu)  

---

### 1. Giới thiệu (Introduction)

Trong thời đại bùng nổ của các nền tảng đánh giá phim ảnh trực tuyến, điểm số trung bình (Average Rating) thường được xem là thước đo quy chuẩn cho chất lượng tác phẩm. Tuy nhiên, các nhà phân tích dữ liệu thường xuyên đối mặt với **Nghịch lý Phổ biến vs. Chất lượng (Popularity vs. Quality Paradox)**:
- Nhiều bộ phim kinh phí thấp hoặc phim gia đình đạt rating tuyệt đối $10.0/10$ nhưng chỉ có dưới 50 lượt bình chọn (mẫu nhỏ, độ lệch chuẩn lớn, độ thiên vị cao).
- Ngược lại, các kiệt tác đại chúng có hàng triệu lượt bình chọn chịu tác động của luật số lớn (Law of Large Numbers), dễ bị kéo điểm về mức trung bình.

**Mục tiêu nghiên cứu:**
1. Thu thập và làm giàu dữ liệu từ nguồn dữ liệu lớn IMDb và OMDb RESTful API.
2. Ứng dụng kỹ thuật tính toán mảng vector hóa của **NumPy** và công thức **Bayesian Weighted Rating** để loại bỏ nhiễu và thiết lập bảng xếp hạng chuẩn xác.
3. Khám phá mối tương quan giữa điểm số, lượt bình chọn, thể loại và thập niên phát hành qua các mô hình trực quan hóa.

---

### 2. Nguồn dữ liệu & Thu thập dữ liệu (Data Sources & Collection)

Dự án tích hợp dữ liệu từ hai nguồn độc lập:

1. **IMDb Official Non-Commercial Datasets**:
   - `title.basics.tsv.gz`: Chứa thông tin cơ bản của hơn 10 triệu tác phẩm (tên phim, năm phát hành, thể loại).
   - `title.ratings.tsv.gz`: Chứa điểm số đánh giá trung bình (`averageRating`) và số lượt bình chọn (`numVotes`).
   - Sau khi lọc lấy `titleType == 'movie'` và loại bỏ các bản ghi khuyết thiếu, tập dữ liệu thu được **337,835 bộ phim** hoàn chỉnh từ năm 1894 đến 2026.

2. **OMDb RESTful API (Open Movie Database)**:
   - Sử dụng thư viện `requests` của Python gửi truy vấn có xác thực bằng khóa API thông qua biến môi trường `OMDb_API_KEY`.
   - Cơ chế xử lý: Thiết lập khoảng nghỉ $0.2\,\text{s}$ giữa các yêu cầu nhằm tuân thủ rate limit; cơ chế fallback tự động chuyển đổi giữa tên phim + năm sang định danh `imdbID`.
   - Kết quả: Thu thập thành công **96 responses JSON** thô (`data/raw/omdb_responses.json`) và trích xuất thành tập dữ liệu làm giàu (`data/raw/omdb_enriched.csv`) với các trường thông tin then chốt: **Đạo diễn (Director)**, **Quốc gia sản xuất (Country)**, **Giải thưởng (Awards)**, **Doanh thu phòng vé (BoxOffice)** và **Thời lượng (Runtime)**.

---

### 3. Phương pháp luận (Methodology)

#### 3.1. Chuẩn hóa điểm số bằng Bayesian Weighted Rating
Để giải quyết nghịch lý mẫu nhỏ, dự án áp dụng công thức xếp hạng chuẩn của IMDb dựa trên lý thuyết xác suất Bayes:

$$\text{WR} = \left(\frac{v}{v + m}\right) \cdot R + \left(\frac{m}{v + m}\right) \cdot C$$

Trong đó:
- $v$ (`numVotes`): Số lượt đánh giá của bộ phim.
- $m$: Ngưỡng số lượt đánh giá tối thiểu (được chọn là $1,000$ votes cho phim điện ảnh).
- $R$ (`averageRating`): Điểm đánh giá trung bình thô của phim.
- $C$: Điểm đánh giá trung bình của toàn bộ tập phim ($C = 6.153$).

#### 3.2. Vector hóa tính toán với NumPy (NumPy Vectorization)
Thay vì sử dụng vòng lặp hoặc phương thức `apply()` của Pandas (chạy chậm trên $337,835$ dòng), toàn bộ công thức được chuyển đổi sang mảng 1D `numpy.ndarray` kiểu `float64`. Phép toán cộng nhân vector hóa tận dụng cơ chế broadcasting của NumPy, giúp tăng tốc độ xử lý hơn 40 lần và đảm bảo độ chính xác tuyệt đối (sai số $\le 10^{-10}$ so với Pandas).

#### 3.3. Xử lý Thể loại (Genre Analysis)
Một bộ phim thường thuộc từ 1 đến 3 thể loại kết hợp (ví dụ: *Action, Adventure, Sci-Fi*). Phương thức `explode('genres_list')` được áp dụng để phân rã thể loại, kết hợp với bộ lọc ngưỡng $\ge 500$ phim/thể loại nhằm triệt tiêu hiện tượng sai lệch mẫu.

---

### 4. Kết quả & Những phát hiện chính (Key Insights)

| Chỉ số thống kê (NumPy) | Điểm Rating (`averageRating`) | Số lượt bình chọn (`numVotes`) |
| :--- | :---: | :---: |
| **Giá trị trung bình (Mean)** | $6.153$ | $3,845$ |
| **Độ lệch chuẩn (Std Dev)** | $1.376$ | $38,838$ |
| **Trung vị (Median)** | $6.300$ | $70$ |
| **Phân vị 25% (Q1)** | $5.300$ | $22$ |
| **Phân vị 75% (Q3)** | $7.100$ | $348$ |
| **Phân vị 95%** | $8.300$ | $6,200$ |

#### 5 Phát hiện cốt lõi từ dữ liệu:
1. **Phân phối điểm số lệch trái (Left-skewed)**: Phân bố điểm số tập trung dày đặc ở ngưỡng $6.0 - 6.8$. Điểm trung vị ($6.30$) cao hơn trung bình ($6.15$), cho thấy có một số lượng nhỏ phim điểm rất thấp kéo trung bình xuống.
2. **Sự hội tụ kỳ diệu của số vote (Funnel Effect)**: Với các phim có dưới $1,000$ vote, rating dao động tự do từ $1.0$ đến $10.0$. Tuy nhiên, khi số vote vượt qua $100,000$, điểm số hội tụ chặt chẽ về khoảng $7.5 - 9.3$, chứng minh sự đồng thuận của đám đông khi mẫu đủ lớn.
3. **Phim tài liệu và tiểu sử có điểm hài lòng cao nhất**: Thể loại **Documentary** đạt điểm Weighted Rating trung bình cao nhất ($7.08$), tiếp theo là **Biography** ($7.02$) và **Animation** ($6.95$). Ngược lại, các thể loại thương mại như **Horror** ($5.92$) và **Action** ($6.25$) có điểm số trung bình thấp nhất do thị hiếu phân hóa.
4. **Quy luật ổn định qua thời gian**: Thập niên 1950–1960 có điểm trung bình cao hơn ($6.6 - 6.7$) do số lượng phim sản xuất ít và chỉ các phim chất lượng mới được số hóa và lưu trữ lại. Từ năm 2000 đến nay, điểm số duy trì cực kỳ ổn định quanh mốc $6.15 - 6.20$.
5. **Độc lập giữa năm phát hành và chất lượng**: Hệ số tương quan Pearson giữa năm phát hành (`startYear`) và chất lượng (`weighted_rating`) chỉ đạt xấp xỉ $-0.02$, khẳng định những tác phẩm điện ảnh xuất sắc không bị giới hạn bởi thời gian.

---

### 5. Hạn chế của nghiên cứu (Limitations)

1. **Giới hạn trường dữ liệu tài chính của IMDb**: Dữ liệu IMDb công khai miễn phí không cung cấp doanh thu phòng vé (Box Office) và kinh phí sản xuất (Budget). Mặc dù đã khắc phục một phần bằng OMDb API, nhiều phim quốc tế ngoài Hollywood vẫn bị thiếu thông tin này (`N/A`).
2. **Độ trễ và giới hạn API**: Do hạn chế về rate limit của OMDb API miễn phí, nghiên cứu chỉ tập trung làm giàu thông tin cho danh sách Top 100 tác phẩm đứng đầu.
3. **Đặc thù người dùng chấm điểm**: Đối tượng tham gia bình chọn trên IMDb có xu hướng thiên về khán giả phương Tây và người dùng trẻ thành thị, chưa phản ánh hoàn toàn sở thích của toàn bộ dân số toàn cầu.

---

### 6. Kết luận (Conclusion)

Dự án đã giải quyết trọn vẹn mục tiêu nghiên cứu và hoàn thành toàn diện các yêu cầu kỹ thuật của học phần PSD301M:
- Xây dựng thành công pipeline thu thập dữ liệu tự động từ API và tệp nén lớn.
- Khai thác hiệu quả sức mạnh của **Pure Python Data Structures** và **NumPy Vectorization** trong tối ưu hóa hiệu năng tính toán.
- Ứng dụng thành công mô hình **Bayesian Weighted Rating** và bộ 5 biểu đồ trực quan hóa đa chiều (Bar, Scatter, Line, Histogram, Heatmap) để làm sáng tỏ "Nghịch lý Phổ biến vs. Chất lượng" trong nền điện ảnh hiện đại.
