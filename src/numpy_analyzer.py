"""Module phân tích dữ liệu chuyên sâu sử dụng thư viện NumPy.

Class NumpyAnalyzer cung cấp các phương thức tính toán thống kê mô tả,
ma trận tương quan và triển khai lại công thức Bayesian Weighted Rating
bằng kỹ thuật vector hóa (vectorization) trên mảng NumPy ndarray,
giúp tối ưu hóa hiệu năng tính toán so với Pandas apply thông thường.
"""

from typing import Any, Dict, Tuple
import numpy as np
import pandas as pd


class NumpyAnalyzer:
    """Lớp phân tích thống kê và tính toán vector hóa với NumPy ndarray."""

    def __init__(self, df: pd.DataFrame) -> None:
        """Khởi tạo NumpyAnalyzer từ DataFrame.

        Args:
            df (pd.DataFrame): DataFrame chứa các cột 'averageRating' và 'numVotes'.
        """
        self.df = df
        # Chuyển đổi Series của Pandas sang mảng 1D numpy.ndarray kiểu float64
        self.ratings: np.ndarray = self.df["averageRating"].to_numpy(dtype=np.float64)
        self.votes: np.ndarray = self.df["numVotes"].to_numpy(dtype=np.float64)

    def compute_descriptive_stats(self) -> Dict[str, Any]:
        """Tính toán các chỉ số thống kê mô tả bằng NumPy (hoàn toàn không dùng pandas .mean).

        Bao gồm:
        - Mean, Standard Deviation, Median
        - Percentiles [25, 50, 75, 95]
        - Hệ số tương quan Pearson giữa Rating và Votes thông qua np.corrcoef

        Returns:
            Dict[str, Any]: Từ điển chứa kết quả thống kê mô tả.
        """
        # Thống kê cho averageRating
        rating_mean: float = float(np.mean(self.ratings))
        rating_std: float = float(np.std(self.ratings))
        rating_median: float = float(np.median(self.ratings))
        rating_percentiles: np.ndarray = np.percentile(self.ratings, [25, 50, 75, 95])

        # Thống kê cho numVotes
        vote_mean: float = float(np.mean(self.votes))
        vote_std: float = float(np.std(self.votes))
        vote_median: float = float(np.median(self.votes))
        vote_percentiles: np.ndarray = np.percentile(self.votes, [25, 50, 75, 95])

        # Tính ma trận tương quan giữa Ratings và Votes
        corr_matrix: np.ndarray = np.corrcoef(self.ratings, self.votes)
        corr_rating_vote: float = float(corr_matrix[0, 1])

        results: Dict[str, Any] = {
            "rating_mean": rating_mean,
            "rating_std": rating_std,
            "rating_median": rating_median,
            "rating_percentiles_25_50_75_95": rating_percentiles.tolist(),
            "vote_mean": vote_mean,
            "vote_std": vote_std,
            "vote_median": vote_median,
            "vote_percentiles_25_50_75_95": vote_percentiles.tolist(),
            "correlation_rating_votes": corr_rating_vote,
        }

        print("\n=== KẾT QUẢ PHÂN TÍCH THỐNG KÊ NUMPY ===")
        print(f"- Rating: Mean = {rating_mean:.3f}, Std = {rating_std:.3f}, Median = {rating_median:.3f}")
        print(f"  Percentiles (25%, 50%, 75%, 95%): {np.round(rating_percentiles, 2).tolist()}")
        print(f"- Votes : Mean = {vote_mean:,.0f}, Std = {vote_std:,.0f}, Median = {vote_median:,.0f}")
        print(f"  Percentiles (25%, 50%, 75%, 95%): {np.round(vote_percentiles, 0).tolist()}")
        print(f"- Hệ số tương quan Pearson (Ratings vs Votes): {corr_rating_vote:.4f}")

        return results

    def compute_vectorized_weighted_rating(self, m: int = 1000) -> Tuple[np.ndarray, float]:
        """Tính toán Bayesian Weighted Rating bằng vector hóa NumPy.

        Công thức:
            WR = (v / (v + m)) * R + (m / (v + m)) * C

        Các bước vectorization:
        - Bước 1: Tính scalar C (điểm rating trung bình toàn cục) bằng np.mean trên mảng ratings.
        - Bước 2: Thực hiện phép cộng scalar `(v + m)` trên toàn bộ mảng `v` theo cơ chế broadcasting.
        - Bước 3: Tính mảng trọng số vote: `weight_v = v / (v + m)`.
        - Bước 4: Tính mảng trọng số tối thiểu: `weight_m = m / (v + m)`.
        - Bước 5: Nhân element-wise với mảng `R` và scalar `C`, sau đó cộng hai mảng kết quả:
                  `wr = weight_v * R + weight_m * C`.

        Args:
            m (int): Số lượt bình chọn tối thiểu làm ngưỡng cân bằng (mặc định 1000).

        Returns:
            Tuple[np.ndarray, float]: (Mảng 1D chứa weighted rating, giá trị scalar C).
        """
        # Bước 1: Tính điểm trung bình toàn cục scalar C
        c_scalar: float = float(np.mean(self.ratings))

        # Bước 2 & 3: Vector hóa phép tính trọng số cho v và m
        v = self.votes
        r = self.ratings
        denom = v + m  # NumPy element-wise addition (broadcasting scalar m)

        weight_v = v / denom  # NumPy element-wise division
        weight_m = m / denom  # NumPy broadcasting scalar m chia cho array

        # Bước 4 & 5: Tính điểm bình chọn có trọng số (element-wise multiplication & addition)
        wr_vectorized: np.ndarray = (weight_v * r) + (weight_m * c_scalar)

        return wr_vectorized, c_scalar

    def verify_with_pandas(self, m: int = 1000) -> bool:
        """So sánh kết quả của vector hóa NumPy với Pandas .apply() cũ để xác thực tính chính xác.

        Args:
            m (int): Ngưỡng số vote tối thiểu (mặc định 1000).

        Returns:
            bool: True nếu hai phương pháp cho kết quả trùng khớp (sai số <= 1e-6), ngược lại False.
        """
        print("\n=== XÁC THỰC VECTOR HÓA NUMPY VS PANDAS APPLY ===")

        # Tính bằng NumPy vectorization
        wr_numpy, c_scalar = self.compute_vectorized_weighted_rating(m=m)

        # Tính bằng Pandas apply (cách tính truyền thống dạng lặp qua từng dòng)
        c_pandas = self.df["averageRating"].mean()

        def _pandas_calc(row: pd.Series) -> float:
            v_val = row["numVotes"]
            r_val = row["averageRating"]
            return (v_val / (v_val + m)) * r_val + (m / (v_val + m)) * c_pandas

        wr_pandas = self.df.apply(_pandas_calc, axis=1).to_numpy(dtype=np.float64)

        # Đánh giá sự tương đồng và độ sai lệch tối đa
        max_diff = float(np.max(np.abs(wr_numpy - wr_pandas)))
        is_close = bool(np.allclose(wr_numpy, wr_pandas, atol=1e-6))

        print(f"- NumPy C scalar: {c_scalar:.6f}")
        print(f"- Pandas C scalar: {c_pandas:.6f}")
        print(f"- Độ lệch tuyệt đối tối đa giữa 2 phương pháp: {max_diff:.10e}")
        print(f"- Kết quả trùng khớp hoàn toàn (tolerance 1e-6): {is_close}")

        if is_close:
            print("=> XÁC THỰC THÀNH CÔNG: Vector hóa NumPy cho kết quả đồng nhất 100% với Pandas!")
        else:
            print("=> CẢNH BÁO: Phát hiện sai lệch kết quả giữa hai phương pháp!")

        return is_close


if __name__ == "__main__":
    from src.data_processor import IMDbDataProcessor

    processor = IMDbDataProcessor(data_dir="data/imdb", min_votes=1000, min_movies_per_genre=500)
    processor.load_data()
    processor.clean_data()

    analyzer = NumpyAnalyzer(processor.movies)
    analyzer.compute_descriptive_stats()
    analyzer.verify_with_pandas(m=1000)
