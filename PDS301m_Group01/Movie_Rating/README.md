# Movie ratings project — run and folder guide

This handoff has exactly three main folders:

1. **01_Movie_Rating_System** — the Streamlit app and its two quick-load datasets: MovieLens small and the 500k-rating sample.
2. **02_Databases** — year-separated MovieLens CSV datasets, the 1m-rating analysis sample, and the SQLite snapshot cache created by the app.
3. **03_Assignment_Requirements** — the notebook, data processor, required CSV files, three visualizations, and report.

The two largest full catalog imports are left out of this clean handoff. The year-separated data is stored in its own subfolder. Only movies.csv, ratings.csv, and README.txt are kept for each dataset to reduce extra files.

## Run the dashboard in VS Code

1. Open **01_Movie_Rating_System** as the VS Code folder.
2. Open Terminal → New Terminal and run:

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python -m streamlit run main.py

3. In the app sidebar, choose **Add a dataset**, select either **ml-latest-small** or **ml-32m-2000-2023-500k**, and import it. The import creates a database snapshot under **02_Databases\cache**.

If PowerShell blocks activation, run the install and Streamlit commands in the same VS Code terminal using the selected Python interpreter.

## Rebuild the assignment outputs

Use the same Python environment after installing the requirements. Open a terminal in **03_Assignment_Requirements** and run:

   python data_processor.py

The processor reads the 1m-rating sample from **02_Databases\samples** and recreates the CSV summaries, charts, and Markdown report in the assignment folder. The PDF is the supplied report export.

## What the app does

The app imports MovieLens CSV files into SQLite so charts and tables can query the data without loading every rating into memory. The small dataset is fastest for a quick start; the 500k sample gives a larger example. Rating counts show submitted ratings, not verified movie views.


The Streamlit first-run email prompt is disabled for this project in .streamlit\config.toml.
