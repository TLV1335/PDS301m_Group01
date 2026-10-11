"""Module triển khai kiến thức Python Cơ bản và Cấu trúc dữ liệu lõi (Phase 1 & Phase 2).

Module này chỉ sử dụng thư viện tiêu chuẩn (Pure Python), hoàn toàn không phụ thuộc
vào Pandas hay NumPy, nhằm đáp ứng các tiêu chuẩn đánh giá về:
- Variables, Loops, Conditionals, Functions (Phase 1 - 10%)
- Lists, Dictionaries, Sets, Tuples (Phase 2 - 15%)
"""

import csv
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


# ==============================================================================
# PHẦN 1: 4 HÀM PYTHON CƠ BẢN (FUNCTIONS, LOOPS, CONDITIONALS)
# ==============================================================================

def classify_rating(score: float) -> str:
    """Phân loại chất lượng phim dựa trên điểm số đánh giá.

    Sử dụng cấu trúc rẽ nhánh if / elif / else thuần Python.

    Args:
        score (float): Điểm đánh giá của bộ phim (thang điểm 10).

    Returns:
        str: "Excellent" (>= 8), "Good" (6 - 8), "Average" (4 - 6), hoặc "Poor" (< 4).
    """
    if score >= 8.0:
        return "Excellent"
    elif score >= 6.0:
        return "Good"
    elif score >= 4.0:
        return "Average"
    else:
        return "Poor"


def filter_by_year_range(movies: List[Dict[str, Any]], start: int, end: int) -> List[Dict[str, Any]]:
    """Lọc danh sách các bộ phim được phát hành trong khoảng năm chỉ định.

    Sử dụng vòng lặp for và câu lệnh điều kiện if để lọc dữ liệu.

    Args:
        movies (List[Dict[str, Any]]): Danh sách các dict, mỗi dict chứa key 'year'.
        start (int): Năm bắt đầu (inclusive).
        end (int): Năm kết thúc (inclusive).

    Returns:
        List[Dict[str, Any]]: Danh sách các bộ phim thỏa mãn điều kiện start <= year <= end.
    """
    filtered_list: List[Dict[str, Any]] = []
    for movie in movies:
        year = movie.get("year")
        if year is not None and start <= int(year) <= end:
            filtered_list.append(movie)
    return filtered_list


def calculate_bayesian_score(v: int, r: float, m: int, c: float) -> float:
    """Tính điểm bình chọn có trọng số Bayesian Weighted Rating bằng Python thuần.

    Công thức:
        WR = (v / (v + m)) * r + (m / (v + m)) * c

    Args:
        v (int): Số lượt bình chọn của phim (numVotes).
        r (float): Điểm đánh giá trung bình của phim (averageRating).
        m (int): Ngưỡng số lượt bình chọn tối thiểu (threshold).
        c (float): Điểm đánh giá trung bình của toàn bộ tập phim (global mean).

    Returns:
        float: Điểm số có trọng số tính toán theo thuật toán IMDb.
    """
    weight_votes: float = v / (v + m)
    weight_threshold: float = m / (v + m)
    weighted_score: float = (weight_votes * r) + (weight_threshold * c)
    return weighted_score


def count_genre_frequency(records: List[Dict[str, Any]]) -> Dict[str, int]:
    """Đếm tần suất xuất hiện của từng thể loại phim.

    Sử dụng vòng lặp for duyệt qua danh sách các bản ghi có chứa danh sách thể loại.

    Args:
        records (List[Dict[str, Any]]): Danh sách các dict có key 'genres' là một List các thể loại.

    Returns:
        Dict[str, int]: Từ điển chứa tên thể loại làm key và số lần xuất hiện làm value.
    """
    frequency: Dict[str, int] = {}
    for item in records:
        genres_list = item.get("genres", [])
        for genre in genres_list:
            if genre in frequency:
                frequency[genre] += 1
            else:
                frequency[genre] = 1
    return frequency


# ==============================================================================
# PHẦN 2: 4 VÍ DỤ MINH HỌA CẤU TRÚC DỮ LIỆU LÕI (DATA STRUCTURES)
# ==============================================================================

def demo_list_structure(csv_path: str = "outputs/top_movies.csv") -> List[Dict[str, Any]]:
    """Minh họa List: Đọc top 100 dòng từ CSV thành danh sách các dictionary.

    Args:
        csv_path (str): Đường dẫn file CSV.

    Returns:
        List[Dict[str, Any]]: Danh sách chứa 100 bản ghi phim.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {csv_path}")

    movies_list: List[Dict[str, Any]] = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            if idx >= 100:
                break
            # Phân tách chuỗi genres_list thành Python list thuần
            raw_genres = row.get("genres_list", "").strip("[]").replace("'", "").split(", ")
            genres = [g.strip() for g in raw_genres if g.strip()]

            movies_list.append({
                "tconst": row.get("tconst", ""),
                "title": row.get("primaryTitle", ""),
                "year": int(float(row.get("startYear", 0))),
                "genres": genres,
                "rating": float(row.get("averageRating", 0.0)),
                "votes": int(float(row.get("numVotes", 0))),
                "weighted_rating": float(row.get("weighted_rating", 0.0))
            })
    return movies_list


def demo_dict_structure(movies_list: List[Dict[str, Any]]) -> Dict[str, str]:
    """Minh họa Dictionary: Tạo bảng tra cứu nhanh theo mã phim {tconst: title}.

    Args:
        movies_list (List[Dict[str, Any]]): Danh sách phim.

    Returns:
        Dict[str, str]: Dictionary ánh xạ từ tconst sang primaryTitle.
    """
    lookup_dict: Dict[str, str] = {}
    for movie in movies_list:
        tconst = movie.get("tconst", "")
        title = movie.get("title", "")
        if tconst:
            lookup_dict[tconst] = title
    return lookup_dict


def demo_set_structure(movies_list: List[Dict[str, Any]]) -> Set[str]:
    """Minh họa Set: Trích xuất tập hợp tất cả các thể loại phim duy nhất (unique genres).

    Args:
        movies_list (List[Dict[str, Any]]): Danh sách phim.

    Returns:
        Set[str]: Tập hợp các thể loại độc nhất không trùng lặp.
    """
    unique_genres: Set[str] = set()
    for movie in movies_list:
        for genre in movie.get("genres", []):
            unique_genres.add(genre)
    return unique_genres


def demo_tuple_structure(movies_list: List[Dict[str, Any]]) -> List[Tuple[str, int]]:
    """Minh họa Tuple: Lưu trữ các cặp thông tin bất biến (tconst, year).

    Args:
        movies_list (List[Dict[str, Any]]): Danh sách phim.

    Returns:
        List[Tuple[str, int]]: Danh sách các tuple bất biến chứa mã phim và năm phát hành.
    """
    tuples_list: List[Tuple[str, int]] = []
    for movie in movies_list:
        tconst = movie.get("tconst", "")
        year = movie.get("year", 0)
        tuples_list.append((tconst, year))
    return tuples_list


# ==============================================================================
# UNIT TEST VỚI ASSERT
# ==============================================================================

def run_tests() -> None:
    """Chạy toàn bộ unit test để kiểm thử tính chính xác của các hàm thuần Python."""
    print("Bắt đầu chạy unit tests cho src/basics_utils.py...")

    # Test 1: classify_rating
    assert classify_rating(9.2) == "Excellent"
    assert classify_rating(8.0) == "Excellent"
    assert classify_rating(7.5) == "Good"
    assert classify_rating(6.0) == "Good"
    assert classify_rating(5.5) == "Average"
    assert classify_rating(4.0) == "Average"
    assert classify_rating(3.2) == "Poor"

    # Test 2: filter_by_year_range
    sample_movies = [
        {"title": "Film A", "year": 1994},
        {"title": "Film B", "year": 2008},
        {"title": "Film C", "year": 1972},
        {"title": "Film D", "year": 2020},
    ]
    filtered_90s = filter_by_year_range(sample_movies, 1990, 2000)
    assert len(filtered_90s) == 1
    assert filtered_90s[0]["title"] == "Film A"
    filtered_all = filter_by_year_range(sample_movies, 1970, 2030)
    assert len(filtered_all) == 4

    # Test 3: calculate_bayesian_score
    # Với v=1000, m=1000, r=8.0, c=6.0: (1000/2000)*8 + (1000/2000)*6 = 0.5*8 + 0.5*6 = 7.0
    score = calculate_bayesian_score(v=1000, r=8.0, m=1000, c=6.0)
    assert abs(score - 7.0) < 1e-9

    # Test 4: count_genre_frequency
    sample_records = [
        {"genres": ["Drama", "Crime"]},
        {"genres": ["Drama", "Action"]},
        {"genres": ["Comedy"]},
    ]
    counts = count_genre_frequency(sample_records)
    assert counts.get("Drama") == 2
    assert counts.get("Crime") == 1
    assert counts.get("Action") == 1
    assert counts.get("Comedy") == 1

    # Test Data Structures Demos
    if Path("outputs/top_movies.csv").exists():
        lst = demo_list_structure("outputs/top_movies.csv")
        assert len(lst) > 0
        assert isinstance(lst, list)

        dt = demo_dict_structure(lst)
        assert isinstance(dt, dict)
        assert len(dt) == len(lst)

        st = demo_set_structure(lst)
        assert isinstance(st, set)
        assert len(st) > 0

        tp = demo_tuple_structure(lst)
        assert isinstance(tp, list)
        assert isinstance(tp[0], tuple)

    print("✅ TẤT CẢ UNIT TESTS ĐỀU ĐẠT CHUẨN THÀNH CÔNG!")


if __name__ == "__main__":
    run_tests()
