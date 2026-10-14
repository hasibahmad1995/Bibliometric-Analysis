# DS Paper Universe

A small Flask app for exploring a bibliometric dataset of data-science papers. Search for a term and the app lists the matching papers, charts who wrote them and where they are based, and draws keyword and reference co-occurrence networks.

## What it does

1. **Search.** Finds every paper whose `Title` contains the text you typed. Matching is a literal, case-sensitive substring test on titles only.
2. **Papers.** Lists the matches in a sortable table (title, year, source).
3. **Visualize.** Draws six charts for the matched papers and their authors:
   top author affiliations, most productive authors, a world map of author countries,
   papers with the highest influence factor, papers per year, and top source titles.
4. **Network.** Draws two interactive force graphs from the matched papers:
   - *Keywords*: the 300 most frequent author keywords, linked when they appear on the same paper.
   - *Paper*: the 10 most frequent references, linked when cited by the same paper.

State is kept in module-level globals, so the app serves one user at a time.

## Getting started

Requires Python 3.10 or newer (developed and tested on 3.14).

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

Put the three data files in `database/` (see [Getting the data](#getting-the-data)), then:

```bash
python app.py
```

Open http://127.0.0.1:5000. If a data file is missing, the app stops at startup and names it.

The page loads Bootstrap, jQuery and the ECharts runtime from CDNs, so the browser needs internet access.

## Getting the data

The dataset is **not** included in this repository. It is an export from [Scopus](https://www.scopus.com), and Elsevier's terms restrict redistributing Scopus content, so you need to obtain it yourself under your own (or your institution's) Scopus access.

The app reads three CSV files from `database/`, all UTF-8:

**`literature_data.csv`**, one row per paper

| Column | Meaning |
|---|---|
| `EID` | Scopus document ID, for example `2-s2.0-85149526441` |
| `Title` | Paper title (this is what the search matches against) |
| `Year` | Publication year |
| `Source title` | Journal or conference name |
| `Cited by` | Citation count |
| `Abstract` | Abstract text |
| `Author Keywords` | Author-supplied keywords, `;`-separated |
| `Index Keywords` | Indexer keywords, `;`-separated |
| `References` | Cited references, `;`-separated |
| `Influence Factor` | Numeric per-paper score used to rank papers. It correlates with `Cited by` but is a derived value, not a Scopus export field |

**`author_data.csv`**, one row per author

| Column | Meaning |
|---|---|
| `Author(s) ID` | Scopus author ID |
| `Author Name` | Name as listed by Scopus |
| `country` | Country, taken from the affiliation text |
| `Affiliations` | Institution |

**`author_publication_data.csv`**, one row per author-paper link

| Column | Meaning |
|---|---|
| `Author(s) ID` | Matches `author_data.csv` |
| `PublicationEID` | Matches `EID` in `literature_data.csv` |

### Notes on how the original files were built

The script that produced these three files from a raw Scopus export is not in this repository, and these points were not recorded:

- **Search query and date range.** TODO(author): add the exact Scopus query, the date it was run, and the document types.
- **`Influence Factor`.** TODO(author): state how it was computed and from which source.
- **`country`.** It looks like the last comma-separated part of the affiliation string. As a result it is noisy: it contains some company names and city names, and a few small territories (Singapore, Hong Kong, Malta, Bahrain, Macao) are not on the bundled 110m map. Rows whose country is not on the map are simply left off the heat map.

## Project layout

```
app.py                         Flask routes and in-memory search
utils/
  exploratory_data_analysis.py runs the six charts
  social_network.py            keyword / reference co-occurrence counting
  visualization/
    author_analysis.py         affiliation, productivity and world-map charts
    publication_analysis.py    influence, yearly trend and source-title charts
    network_visu.py            renders the pyecharts force graph
templates/  static/            pages, styles and generated charts / networks
database/                      your data files (git-ignored) + world map
  naturalearth_lowres/         Natural Earth 110m countries, public domain
```

## Known limits

- Search is case-sensitive and title-only; there is no ranking.
- Single-user: results are stored in global variables.
- Titles and keywords are not normalized, so "machine learning" and "machine-learning" count as different keywords.
- `utils/visualization/network_visu_paper.py` and `utils/visualization/keyword_network1.html` are older standalone experiments that the app does not use.
