from src.data_processor import IMDbDataProcessor
from src.visualizer import MovieVisualizer

def main() -> None:
    processor = IMDbDataProcessor(
        data_dir='data/imdb',
        min_votes=1000,
        min_movies_per_genre=500
    )
    processor.load_data()
    processor.clean_data()
    processor.compute_weighted_rating()
    processor.analyze_genres()
    processor.analyze_decades()
    processor.export_results('outputs')
    
    viz = MovieVisualizer('outputs/figures')
    viz.plot_genre_rating(processor.genre_stats)
    viz.plot_votes_vs_rating(processor.movies, processor.C)
    viz.plot_rating_by_decade(processor.decade_stats)
    viz.plot_rating_histogram(processor.movies)
    viz.plot_correlation_heatmap(processor.movies)
    
    print("\n=== HOÀN THÀNH ===")
    print("CSV: outputs/top_movies.csv, genre_summary.csv, decade_summary.csv")
    print("Charts: outputs/figures/01_*.png, 02_*.png, 03_*.png, 04_*.png, 05_*.png")

if __name__ == '__main__':
    main()