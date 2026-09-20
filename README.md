# miniproject3KyleHorn

### INF601 - Advanced Programming in Python
### Kyle Horn
### Mini Project 3


# Movie Ratings by Genre and Year

Pulls movie data from the INF601 Practice Hub API, loads it into a Pandas DataFrame, and uses Matplotlib to visually explore whether a movie's release year and genre have any relationship to its rating.

## Description

This project answers the question: **Is there a relationship between a movie's release year and its rating, broken out by genre?**

The data comes from the Practice Hub's `GET /api/v1/datasets/movies` endpoint, which generates 500 rows of deterministic, randomly-generated practice data with the columns `title, director, year, genre, rating`. The script:

1. Requests the data from the Practice Hub API using a personal API token.
2. Loads the returned rows into a Pandas DataFrame.
3. Inspects the DataFrame (shape, column types, sample rows) and checks for missing values or duplicate rows.
4. Calculates the average rating by genre, and the average rating by year and genre, using `groupby()`.
5. Builds four Matplotlib charts from that data and saves each one as a PNG in a `charts` folder:
   - `rating_vs_year_by_genre.png` — scatter plot of every movie's year vs. rating, colored by genre.
   - `avg_rating_by_year_genre.png` — line chart of average rating per year, one line per genre.
   - `avg_rating_by_genre.png` — bar chart of the overall average rating per genre.
   - `rating_distribution_by_genre.png` — box plot showing the spread of ratings within each genre.

Because the Practice Hub dataset is randomly generated rather than based on real movie data, the honest answer the charts show is that there is **no meaningful relationship** between year, genre, and rating — every genre's average and spread look similar across all years. The script prints this conclusion to the terminal along with all of its intermediate steps.

The `charts` folder is generated automatically every time the script runs and is **not** committed to GitHub (it's listed in `.gitignore`) — you will only see the PNGs after you run the script yourself.

## Getting Started

### Dependencies

* Python 3.10 or newer
* `pip` (comes with Python)
* An API token from the INF601 Practice Hub (`https://practice.fhsucyber.com/`) — see [Executing program](#executing-program) below for how to get one
* Internet access (the script calls a live API each time it runs)
* All Python packages are listed in `requirements.txt` and installed via `pip` (see below) — you do not need to install pandas/matplotlib/requests separately

Works on both Windows and Linux (Ubuntu). Commands for both are given at every step below.

### Installing

1. Clone the repository:

**Windows (PowerShell) and Linux (bash) — same command:**
```
git clone https://github.com/kchorn0/miniproject3KyleHorn.git
cd miniproject3KyleHorn
```

2. Create a virtual environment:

**Windows (PowerShell):**
```
python -m venv venv
```

**Linux (bash):**
```
python3 -m venv venv
```

3. Activate the virtual environment:

**Windows (PowerShell):**
```
.\venv\Scripts\Activate.ps1
```
> If PowerShell blocks this with a "running scripts is disabled" error, either run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once (in your own PowerShell, as yourself), or skip activation and call the venv's Python directly in every command below, e.g. `.\venv\Scripts\python.exe miniproject3.py`.

**Linux (bash):**
```
source venv/bin/activate
```

4. Install the required packages:

**Windows and Linux — same command (once the venv is activated):**
```
pip install -r requirements.txt
```

No files or folders need to be manually created or modified — the script creates its own `charts` folder automatically when it runs.

### Executing program

1. Get a Practice Hub API token (skip this if you already have one):

```
curl -X POST https://practice.fhsucyber.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Your Name","email":"you@example.com","password":"yourpassword123"}'
```
This returns JSON containing an `api_token` — copy that value.

2. Set the two required environment variables (the script reads these instead of having the URL/token hardcoded, so nothing sensitive is stored in the code):

**Windows (PowerShell):**
```
$env:PRACTICE_API_URL = "https://practice.fhsucyber.com"
$env:PRACTICE_API_TOKEN = "paste-your-token-here"
```

**Linux (bash):**
```
export PRACTICE_API_URL="https://practice.fhsucyber.com"
export PRACTICE_API_TOKEN="paste-your-token-here"
```

> These only last for the current terminal session. You'll need to set them again if you open a new terminal window.

3. Run the script (from the project's root folder, with the venv activated):

**Windows (PowerShell):**
```
python .\miniproject3.py
```

**Linux (bash):**
```
python3 miniproject3.py
```

4. Check the output:
   * The terminal will print the DataFrame's shape, columns, data types, a data-quality check, and the average-rating calculations, followed by the final answer to the question.
   * A new `charts` folder will appear in the project root containing the 4 PNG charts described above.

## Help

* **`ModuleNotFoundError: No module named 'pandas'`** — your virtual environment isn't activated, or the packages weren't installed into it. Re-run step 3 (activate) and step 4 (`pip install -r requirements.txt`) from Installing above.
* **`running scripts is disabled on this system` (Windows only)** — PowerShell's execution policy is blocking `Activate.ps1`. Use `.\venv\Scripts\python.exe miniproject3.py` instead of activating, or fix it permanently with `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
* **"Missing PRACTICE_API_URL or PRACTICE_API_TOKEN environment variable."** — the script printed this because one or both environment variables aren't set in your current terminal session. Re-run the `$env:` (Windows) or `export` (Linux) commands from step 2 of Executing program, in the same terminal you're running the script from.
* **"Could not fetch data from the Practice Hub API"** — this means the request to the API failed (bad token, wrong URL, or the server is unreachable). Double check the token and URL you set, and confirm `https://practice.fhsucyber.com/health` responds with `{"status": "ok"}` in a browser.
* **No `charts` folder / can't find the PNGs** — the folder is only created when the script runs successfully; check the terminal output for any error messages first.

## Authors

Kyle Horn
(kchorn@mail.fhsu.edu)


## Acknowledgments

Inspiration, code snippets, etc.

* https://practice.fhsucyber.com/docs-guide
* 
