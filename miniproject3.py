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
import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Gets the Practice Hub site address from the computer's environment variables
BASE_URL = os.environ.get("PRACTICE_API_URL")
# Gets the API token from the computer's environment variables
TOKEN = os.environ.get("PRACTICE_API_TOKEN")

# Stop early with a clear message if the env vars were never set,
# instead of failing later with a confusing connection error.
if not BASE_URL or not TOKEN:
    print("Missing PRACTICE_API_URL or PRACTICE_API_TOKEN environment variable.")
    print("Set both in your terminal before running this script.")
    sys.exit(1)

headers = {"Authorization": f"Bearer {TOKEN}"}

# Pull the movies dataset (title, director, year, genre, rating)
try:
    response = requests.get(
        f"{BASE_URL}/api/v1/datasets/movies",
        headers=headers,
        params={"count": 500},
    )
    response.raise_for_status()
    movies_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Could not fetch data from the Practice Hub API: {e}")
    sys.exit(1)

movies_df = pd.DataFrame(movies_data["rows"])

print("=" * 60)
print("QUESTION: Is there a relationship between year and rating,")
print("broken out by genre?")
print("=" * 60)

# Inspect the DataFrame before doing any analysis
print("\n--- DataFrame overview ---")
print("Shape (rows, columns):", movies_df.shape)
print("Column names:", list(movies_df.columns))
print("Data types:\n", movies_df.dtypes)
print("Sample rows:\n", movies_df.sample(5))

# Data-quality check: missing values and duplicate rows
print("\n--- Data quality check ---")
print("Missing values per column:\n", movies_df.isnull().sum())
print("Number of duplicate rows:", movies_df.duplicated().sum())

# Average rating per genre
print("\n--- Average rating by genre ---")
avg_rating_by_genre = movies_df.groupby("genre")["rating"].mean()
print(avg_rating_by_genre)

# Average rating per year and genre
print("\n--- Average rating by year and genre ---")
avg_rating_by_year_genre = movies_df.groupby(["year", "genre"])["rating"].mean().reset_index()
print(avg_rating_by_year_genre)

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

# Chart 4: distribution of ratings by genre
genres = movies_df["genre"].unique()
ratings_by_genre = [movies_df[movies_df["genre"] == genre]["rating"] for genre in genres]

plt.figure(figsize=(10, 6))
plt.boxplot(ratings_by_genre, tick_labels=genres)

plt.title("Distribution of Movie Ratings by Genre")
plt.xlabel("Genre")
plt.ylabel("Rating")
plt.savefig(os.path.join(CHARTS_DIR, "rating_distribution_by_genre.png"))
plt.close()

print("\n" + "=" * 60)
print("ANSWER: No meaningful relationship was found. Every genre")
print("hovers around a similar average rating with a wide, similar")
print("spread, and the scatter/line charts show noise rather than")
print("a trend. This is expected since the Practice Hub dataset is")
print("randomly generated rather than based on real movie ratings.")
print("=" * 60)
print(f"\nAll 4 charts saved to the '{CHARTS_DIR}' folder.")
