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

# I don't hardcode the URL/token here so I never accidentally commit them to GitHub.
# Instead I set them as environment variables in my own terminal before running this.
BASE_URL = os.environ.get("PRACTICE_API_URL")
TOKEN = os.environ.get("PRACTICE_API_TOKEN")

# If I forget to set the env vars, this stops the program right away with a
# message that actually tells me what's wrong, instead of a confusing crash later.
if not BASE_URL or not TOKEN:
    print("Missing PRACTICE_API_URL or PRACTICE_API_TOKEN environment variable.")
    print("Set both in your terminal before running this script.")
    sys.exit(1)

# Every Practice Hub endpoint (besides register/token/health) needs this header.
headers = {"Authorization": f"Bearer {TOKEN}"}

# Ask the Practice Hub for 500 movies (the max allowed) so I have enough data
# per genre/year to make the averages meaningful instead of just a few rows.
try:
    response = requests.get(
        f"{BASE_URL}/api/v1/datasets/movies",
        headers=headers,
        params={"count": 500},
    )
    response.raise_for_status()  # raises an error if the API sent back 401/404/etc.
    movies_data = response.json()
except requests.exceptions.RequestException as e:
    # Catches network problems or bad responses so I get a short readable
    # message here instead of a big Python traceback.
    print(f"Could not fetch data from the Practice Hub API: {e}")
    sys.exit(1)

# The API wraps the actual data in a "rows" key - this is what turns
# that list of dictionaries into an actual Pandas DataFrame I can work with.
movies_df = pd.DataFrame(movies_data["rows"])

print("=" * 60)
print("QUESTION: Is there a relationship between year and rating,")
print("broken out by genre?")
print("=" * 60)

# Before I trust any of the math below, I want to actually look at what I got back:
# how big it is, what columns/types it has, and a random sample of real rows.
print("\n--- DataFrame overview ---")
print("Shape (rows, columns):", movies_df.shape)
print("Column names:", list(movies_df.columns))
print("Data types:\n", movies_df.dtypes)
print("Sample rows:\n", movies_df.sample(5))

# Checking for missing values and duplicate rows because either one would
# throw off my averages later (a missing rating skews the math, a duplicate
# row counts the same movie twice).
print("\n--- Data quality check ---")
print("Missing values per column:\n", movies_df.isnull().sum())
print("Number of duplicate rows:", movies_df.duplicated().sum())

# groupby("genre") splits the DataFrame into one bucket per genre, then
# ["rating"].mean() averages just the rating column inside each bucket.
print("\n--- Average rating by genre ---")
avg_rating_by_genre = movies_df.groupby("genre")["rating"].mean()
print(avg_rating_by_genre)

# Same idea, but grouping by year AND genre together so I can see how each
# genre's average rating moves year to year. reset_index() turns year/genre
# back into normal columns instead of leaving them as the row labels.
print("\n--- Average rating by year and genre ---")
avg_rating_by_year_genre = movies_df.groupby(["year", "genre"])["rating"].mean().reset_index()
print(avg_rating_by_year_genre)

# Makes a "charts" folder if one doesn't exist yet. exist_ok=True means it
# won't error out if the folder is already there from a previous run - this
# is also why charts/ is never committed to GitHub, it just gets rebuilt here.
CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

# Chart 1 - the main visual for my question: every single movie plotted as
# year vs rating, with one color per genre so I can see if any genre clusters
# differently. Looping genre-by-genre is what gives each one its own color/legend entry.
plt.figure(figsize=(10, 6))
for genre in movies_df["genre"].unique():
    genre_subset = movies_df[movies_df["genre"] == genre]
    plt.scatter(genre_subset["year"], genre_subset["rating"], label=genre, alpha=0.6)

plt.title("Movie Rating vs Year by Genre")
plt.xlabel("Year")
plt.ylabel("Rating")
plt.legend(title="Genre")
plt.savefig(os.path.join(CHARTS_DIR, "rating_vs_year_by_genre.png"))
plt.close()  # frees the figure so it doesn't bleed into the next chart

# Chart 2 - same genre-by-genre idea as Chart 1, but plotting the averages
# from the groupby above instead of every raw point, so I can actually see
# a trend line (if there is one) per genre instead of a wall of dots.
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

# Chart 3 - a simple summary bar for each genre's overall average, reusing
# the Series from the groupby earlier instead of recalculating it again.
plt.figure(figsize=(10, 6))
plt.bar(avg_rating_by_genre.index, avg_rating_by_genre.values)

plt.title("Overall Average Movie Rating by Genre")
plt.xlabel("Genre")
plt.ylabel("Average Rating")
plt.savefig(os.path.join(CHARTS_DIR, "avg_rating_by_genre.png"))
plt.close()

# Chart 4 - the bar chart only shows one number (the average) per genre,
# so this box plot shows the full spread of ratings within each genre
# instead, which is a better way to see how consistent/spread out they are.
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
