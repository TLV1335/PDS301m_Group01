import pandas as pd
import gzip

# Đọc file ratings
with gzip.open('data/imdb/title.ratings.tsv.gz', 'rt', encoding='utf-8') as f:
    ratings = pd.read_csv(f, sep='\t', na_values='\\N')

# Đọc file basics (nên đọc từng phần vì file lớn)
with gzip.open('data/imdb/title.basics.tsv.gz', 'rt', encoding='utf-8') as f:
    # Chỉ lấy phim, bỏ qua TV series, game, v.v.
    basics = pd.read_csv(f, sep='\t', na_values='\\N', 
                         usecols=['tconst', 'titleType', 'primaryTitle', 'startYear', 'genres'])
    basics = basics[basics['titleType'] == 'movie']
    
# Merge ratings với basics qua tconst
movies = basics.merge(ratings, on='tconst', how='inner')

# Xử lý năm phát hành
movies['startYear'] = pd.to_numeric(movies['startYear'], errors='coerce')
movies = movies[movies['startYear'].notna()]

# Tách genres
movies['genres_list'] = movies['genres'].str.split(',')