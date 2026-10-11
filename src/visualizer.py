import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class MovieVisualizer:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_style('whitegrid')
    
    def plot_genre_rating(self, genre_stats):
        plt.figure(figsize=(12, 7))
        top = genre_stats.head(15)
        sns.barplot(data=top, x='mean_weighted', y='genres_list', hue='genres_list', palette='viridis', legend=False)
        plt.title('Top 15 Thể Loại Theo Weighted Rating (IMDb)', fontsize=14, fontweight='bold')
        plt.xlabel('Weighted Rating')
        plt.ylabel('Thể Loại')
        plt.tight_layout()
        plt.savefig(self.output_dir / '01_genre_rating.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def plot_votes_vs_rating(self, movies, global_mean):
        plt.figure(figsize=(11, 7))
        sample = movies.sample(n=min(50000, len(movies)), random_state=42)
        plt.scatter(sample['numVotes'], sample['averageRating'], alpha=0.15, s=8)
        plt.xscale('log')
        plt.axhline(global_mean, color='red', linestyle='--', alpha=0.5,
                    label=f'Global Mean = {global_mean:.2f}')
        plt.xlabel('Số Lượng Vote (log)')
        plt.ylabel('Rating Trung Bình')
        plt.title('Số Vote vs Rating — Nghịch Lý Phổ Biến', fontsize=14, fontweight='bold')
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.output_dir / '02_votes_vs_rating.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    def plot_rating_by_decade(self, decade_stats):
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=decade_stats, x='decade', y='mean_rating',
                     marker='o', linewidth=2.5, color='darkgreen')
        plt.title('Rating Trung Bình Theo Thập Niên', fontsize=14, fontweight='bold')
        plt.xlabel('Thập Niên')
        plt.ylabel('Rating Trung Bình')
        plt.tight_layout()
        plt.savefig(self.output_dir / '03_rating_by_decade.png', dpi=150, bbox_inches='tight')
        plt.close()

    def plot_rating_histogram(self, movies) -> None:
        """Vẽ biểu đồ histogram phân phối điểm averageRating kèm đường KDE."""
        plt.figure(figsize=(10, 6))
        sns.histplot(movies['averageRating'].dropna(), bins=30, kde=True, color='royalblue')
        plt.title('Phân Bố Điểm Đánh Giá Phim (IMDb Rating Distribution)', fontsize=14, fontweight='bold')
        plt.xlabel('Điểm Rating Trung Bình', fontsize=12)
        plt.ylabel('Số Lượng Phim', fontsize=12)
        plt.tight_layout()
        plt.savefig(self.output_dir / '04_rating_histogram.png', dpi=150, bbox_inches='tight')
        plt.close()

    def plot_correlation_heatmap(self, movies) -> None:
        """Vẽ ma trận tương quan dạng Heatmap giữa các thuộc tính quan trọng của phim."""
        plt.figure(figsize=(8, 6))
        corr_cols = ['numVotes', 'averageRating', 'startYear', 'weighted_rating']
        corr_matrix = movies[corr_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.3f', vmin=-1, vmax=1, square=True, linewidths=0.5)
        plt.title('Ma Trận Tương Quan Giữa Các Thuộc Tính Phim', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(self.output_dir / '05_correlation_heatmap.png', dpi=150, bbox_inches='tight')
        plt.close()