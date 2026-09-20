# INF601 - Advanced Programming in Python
# Kyle Horn
# Mini Project 3

'''
Goal
Use Pandas DataFrames to answer a question with data. This isn't a full data-science project  the point is to pose a question, find data, load it into a DataFrame, and visualize an answer.

Requirements and points
(5) Initial comments (name, class, project) at the top of your .py file.
(5) Proper import of packages used.
(20) Using a data source of your choice  data.gov, a Kaggle dataset, the Faker package, or the Practice Hub GET /api/v1/datasets/{people|movies|stocks} endpoint — gather data to answer a question you pose. For example: "How many homes in the US have access to 100Mbps Internet or more?" or "How many movies that Ridley Scott directed are on Netflix?"
(10) Store the data in a Pandas DataFrame (2D labeled tabular data).
(10) Use Matplotlib to graph the data in a way that visually answers your question. Build something nontrivial it helps with later projects.
(10) Save the graphs in a folder called charts as PNG files (generated on run, not committed). Add charts/ to .gitignore.
(10) At least 5 commits.
(10) I will check out the main branch. Include a requirements.txt.
(20) A thorough README.md explaining the project, install, and run steps. Include an ## AI Usage section.
'''

'''
Question
Is there a relationship between year and rating, broken out by genre?
(Practice Hub /api/v1/datasets/movies: title, director, year, genre, rating)

Planned charts
1. Scatter of year vs rating, colored by genre.
2. Line chart of average rating by year, one line per genre.
3. Bar chart of overall average rating by genre.
4. Box plot (or histograms) of rating distribution by genre.
'''

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Gets the Practice Hub site address from the computer's environment variables
BASE_URL = os.environ.get("PRACTICE_API_URL")
# Gets the API token from the computer's environment variables
TOKEN = os.environ.get("PRACTICE_API_TOKEN")

headers = {"Authorization": f"Bearer {TOKEN}"}

# Pull the movies dataset (title, director, year, genre, rating)
response = requests.get(
    f"{BASE_URL}/api/v1/datasets/movies",
    headers=headers,
    params={"count": 500},
)
response.raise_for_status()
movies_data = response.json()

movies_df = pd.DataFrame(movies_data["rows"])

# Inspect the DataFrame before doing any analysis
print("Shape (rows, columns):", movies_df.shape)
print("\nColumn names:", list(movies_df.columns))
print("\nData types:\n", movies_df.dtypes)
print("\nSample rows:\n", movies_df.sample(5))

# Data-quality check: missing values and duplicate rows
print("\nMissing values per column:\n", movies_df.isnull().sum())
print("\nNumber of duplicate rows:", movies_df.duplicated().sum())

# Average rating per genre
avg_rating_by_genre = movies_df.groupby("genre")["rating"].mean()
print("\nAverage rating by genre:\n", avg_rating_by_genre)

# Average rating per year and genre
avg_rating_by_year_genre = movies_df.groupby(["year", "genre"])["rating"].mean().reset_index()
print("\nAverage rating by year and genre:\n", avg_rating_by_year_genre)

# Create the charts folder if it doesn't already exist
CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

# Chart 1: scatter of year vs rating, one color per genre
plt.figure(figsize=(10, 6))
for genre in movies_df["genre"].unique():
    genre_subset = movies_df[movies_df["genre"] == genre]
    plt.scatter(genre_subset["year"], genre_subset["rating"], label=genre, alpha=0.6)

plt.title("Movie Rating vs Year by Genre")
plt.xlabel("Year")
plt.ylabel("Rating")
plt.legend(title="Genre")
plt.savefig(os.path.join(CHARTS_DIR, "rating_vs_year_by_genre.png"))
plt.close()

# Chart 2: average rating by year, one line per genre
plt.figure(figsize=(10, 6))
for genre in avg_rating_by_year_genre["genre"].unique():
    genre_trend = avg_rating_by_year_genre[avg_rating_by_year_genre["genre"] == genre]
    plt.plot(genre_trend["year"], genre_trend["rating"], marker="o", label=genre)

plt.title("Average Movie Rating by Year and Genre")
plt.xlabel("Year")
plt.ylabel("Average Rating")
plt.legend(title="Genre")
plt.savefig(os.path.join(CHARTS_DIR, "avg_rating_by_year_genre.png"))
plt.close()

# Chart 3: overall average rating by genre
plt.figure(figsize=(10, 6))
plt.bar(avg_rating_by_genre.index, avg_rating_by_genre.values)

plt.title("Overall Average Movie Rating by Genre")
plt.xlabel("Genre")
plt.ylabel("Average Rating")
plt.savefig(os.path.join(CHARTS_DIR, "avg_rating_by_genre.png"))
plt.close()
