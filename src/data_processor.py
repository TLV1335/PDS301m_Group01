import pandas as pd
import gzip
from pathlib import Path

class IMDbDataProcessor:
    def __init__(self, data_dir: str, min_votes: int = 1000, min_movies_per_genre: int = 500):
        self.data_dir = Path(data_dir)
        self.min_votes = min_votes
        self.min_movies_per_genre = min_movies_per_genre
        self.movies = None
        self.genre_stats = None
        self.decade_stats = None
        self.C = None
    
    def load_data(self):
        ratings_path = self.data_dir / 'title.ratings.tsv.gz'
        basics_path = self.data_dir / 'title.basics.tsv.gz'
        
        with gzip.open(ratings_path, 'rt', encoding='utf-8') as f:
            ratings = pd.read_csv(f, sep='\t', na_values='\\N')
        
        with gzip.open(basics_path, 'rt', encoding='utf-8') as f:
            basics = pd.read_csv(
                f, sep='\t', na_values='\\N',
                usecols=['tconst', 'titleType', 'primaryTitle', 'startYear', 'genres']
            )
            basics = basics[basics['titleType'] == 'movie']
        
        self.movies = basics.merge(ratings, on='tconst', how='inner')
        print(f"Đã load {len(self.movies):,} phim")
    
    def clean_data(self):
        self.movies['startYear'] = pd.to_numeric(self.movies['startYear'], errors='coerce')
        self.movies = self.movies[
            self.movies['startYear'].notna() & self.movies['genres'].notna()
        ].copy()
        self.movies['genres_list'] = self.movies['genres'].str.split(',')
        self.movies['decade'] = (self.movies['startYear'] // 10) * 10
        print(f"Sau làm sạch: {len(self.movies):,} phim")
    
    def compute_weighted_rating(self):
        self.C = self.movies['averageRating'].mean()
        m = self.min_votes
        v = self.movies['numVotes']
        R = self.movies['averageRating']
        self.movies['weighted_rating'] = (v / (v + m)) * R + (m / (v + m)) * self.C
        print(f"Global mean C = {self.C:.3f}, threshold m = {m}")
    
    def analyze_genres(self):
        exploded = self.movies.explode('genres_list')
        self.genre_stats = exploded.groupby('genres_list').agg(
            movie_count=('tconst', 'count'),
            mean_rating=('averageRating', 'mean'),
            mean_weighted=('weighted_rating', 'mean'),
            total_votes=('numVotes', 'sum'),
            median_year=('startYear', 'median')
        ).reset_index()
        self.genre_stats = self.genre_stats[
            self.genre_stats['movie_count'] >= self.min_movies_per_genre
        ]
        self.genre_stats = self.genre_stats.sort_values('mean_weighted', ascending=False)
    
    def analyze_decades(self):
        recent = self.movies[self.movies['decade'] >= 1950]
        self.decade_stats = recent.groupby('decade').agg(
            movie_count=('tconst', 'count'),
            mean_rating=('averageRating', 'mean'),
            mean_votes=('numVotes', 'mean')
        ).reset_index()
    
    def export_results(self, output_dir: str):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        
        top_movies = self.movies.nlargest(100, 'weighted_rating')[
            ['tconst', 'primaryTitle', 'startYear', 'genres_list',
             'averageRating', 'numVotes', 'weighted_rating']
        ]
        top_movies.to_csv(out / 'top_movies.csv', index=False)
        self.genre_stats.to_csv(out / 'genre_summary.csv', index=False)
        self.decade_stats.to_csv(out / 'decade_summary.csv', index=False)
        print(f"Đã xuất CSV vào {out}")