"""Module thu thập và làm giàu dữ liệu phim từ OMDb RESTful API.

Module này đọc danh sách top phim từ outputs/top_movies.csv, gửi request đến OMDb API
để lấy thêm thông tin chi tiết (Director, Country, Awards, BoxOffice, Runtime),
lưu trữ raw JSON và xuất file CSV enriched theo chuẩn yêu cầu đề bài.
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_api_key() -> str:
    """Lấy OMDb API key từ biến môi trường OMDb_API_KEY hoặc OMDB_API_KEY.

    Returns:
        str: OMDb API Key hợp lệ.

    Raises:
        ValueError: Nếu biến môi trường chưa được thiết lập.
    """
    api_key = os.getenv("OMDb_API_KEY") or os.getenv("OMDB_API_KEY")
    if not api_key:
        raise ValueError(
            "Biến môi trường 'OMDb_API_KEY' chưa được thiết lập. "
            "Vui lòng chạy: export OMDb_API_KEY='<your_api_key>'"
        )
    return api_key.strip()


def fetch_movie_from_omdb(
    title: str,
    year: Optional[int],
    api_key: str,
    tconst: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Gửi request tới OMDb API để lấy thông tin chi tiết về một bộ phim.

    Args:
        title (str): Tên phim.
        year (Optional[int]): Năm phát hành phim.
        api_key (str): Khóa OMDb API.
        tconst (Optional[str]): Mã định danh IMDb (tt...) dùng để dự phòng nếu tìm theo tên không thấy.

    Returns:
        Optional[Dict[str, Any]]: Dữ liệu JSON từ API nếu thành công, None nếu thất bại.
    """
    url = "http://www.omdbapi.com/"
    params: Dict[str, Any] = {"apikey": api_key, "t": title}
    if year and year > 0:
        params["y"] = int(year)

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Nếu tìm theo title + year không thấy mà có tconst, thử fallback tìm theo imdbID
        if data.get("Response") == "False" and tconst:
            fallback_params = {"apikey": api_key, "i": tconst}
            fallback_resp = requests.get(url, params=fallback_params, timeout=10)
            fallback_resp.raise_for_status()
            fallback_data = fallback_resp.json()
            if fallback_data.get("Response") == "True":
                data = fallback_data

        if data.get("Response") == "False":
            logger.warning(f"Bỏ qua phim '{title}' ({year}): {data.get('Error', 'Không tìm thấy')}")
            return None

        # Gắn kèm tconst nếu API không trả về hoặc bị thiếu
        if tconst and "imdbID" not in data:
            data["imdbID"] = tconst
        elif tconst and not data.get("imdbID"):
            data["imdbID"] = tconst

        return data
    except requests.RequestException as e:
        logger.error(f"Lỗi kết nối khi lấy phim '{title}': {e}")
        return None


def collect_omdb_data(
    input_csv_path: str = "outputs/top_movies.csv",
    output_json_path: str = "data/raw/omdb_responses.json",
    max_movies: int = 100
) -> List[Dict[str, Any]]:
    """Thu thập thông tin từ OMDb API cho danh sách phim và lưu vào file JSON.

    Args:
        input_csv_path (str): Đường dẫn file CSV chứa danh sách phim cần lấy.
        output_json_path (str): Đường dẫn lưu file raw JSON.
        max_movies (int): Số lượng phim tối đa cần lấy.

    Returns:
        List[Dict[str, Any]]: Danh sách các response JSON hợp lệ thu thập được.
    """
    api_key = get_api_key()
    input_path = Path(input_csv_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {input_csv_path}")

    df_top = pd.read_csv(input_path)
    total = min(len(df_top), max_movies)
    responses: List[Dict[str, Any]] = []

    print(f"Bắt đầu thu thập dữ liệu từ OMDb API cho {total} phim...")
    for idx, row in df_top.head(total).iterrows():
        title = str(row.get("primaryTitle", "")).strip()
        year_val = row.get("startYear")
        year = int(year_val) if pd.notna(year_val) else None
        tconst = str(row.get("tconst", "")).strip()

        print(f"Đang lấy phim {idx + 1}/{total}: {title}")

        movie_data = fetch_movie_from_omdb(title=title, year=year, api_key=api_key, tconst=tconst)
        if movie_data:
            # Bảo đảm luôn lưu lại tconst gốc
            if "tconst" not in movie_data and tconst:
                movie_data["tconst"] = tconst
            responses.append(movie_data)

        # Xử lý rate limit: nghỉ 0.2s giữa các request
        time.sleep(0.2)

    # Lưu raw JSON vào data/raw/omdb_responses.json
    out_json = Path(output_json_path)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)

    print(f"Đã lưu {len(responses)} response vào {output_json_path}")
    return responses


def parse_omdb_json(
    json_path: str = "data/raw/omdb_responses.json",
    output_csv_path: Optional[str] = "data/raw/omdb_enriched.csv"
) -> pd.DataFrame:
    """Đọc raw JSON từ OMDb và chuyển thành DataFrame chuẩn hóa.

    Các cột đầu ra: tconst, director, country, awards, box_office, runtime.

    Args:
        json_path (str): Đường dẫn file JSON chứa các response từ OMDb.
        output_csv_path (Optional[str]): Đường dẫn xuất file CSV đã chuẩn hóa.

    Returns:
        pd.DataFrame: DataFrame chứa các trường thông tin đã làm giàu.
    """
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file JSON: {json_path}")

    with open(path, "r", encoding="utf-8") as f:
        raw_list = json.load(f)

    records: List[Dict[str, Any]] = []
    for item in raw_list:
        tconst = item.get("tconst") or item.get("imdbID") or ""
        director = item.get("Director", "N/A")
        country = item.get("Country", "N/A")
        awards = item.get("Awards", "N/A")
        box_office = item.get("BoxOffice", "N/A")
        runtime = item.get("Runtime", "N/A")

        records.append({
            "tconst": tconst,
            "director": director,
            "country": country,
            "awards": awards,
            "box_office": box_office,
            "runtime": runtime
        })

    df = pd.DataFrame(records)

    if output_csv_path:
        out_csv = Path(output_csv_path)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_csv, index=False, encoding="utf-8")
        print(f"Đã xuất DataFrame làm giàu ({len(df)} dòng) vào {output_csv_path}")

    return df


if __name__ == "__main__":
    collect_omdb_data()
    parse_omdb_json()
