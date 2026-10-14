import os

import matplotlib
matplotlib.use('Agg')  # charts are drawn on Flask worker threads, so no GUI backend

import pandas as pd
from flask import Flask, render_template, request
from icecream import ic

from utils.exploratory_data_analysis import eda
from utils.social_network import build_network_data
from utils.visualization.network_visu import network_visu

ic.disable()  # printing whole DataFrames is slow and noisy; call ic.enable() to debug

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'database')
VISION_DIR = os.path.join(BASE_DIR, 'static', 'image', 'vision')
DATA_FILES = ('literature_data.csv', 'author_data.csv', 'author_publication_data.csv')

app = Flask(__name__)

literature_data = None
author_data = None
author_publication_data = None
user_input = None
literature_results = None
filtered_literature = None
author_results = None
publication_results = None
image_files = []

top_n_keyword = 300
top_n_paper = 10

NO_SEARCH_HTML = '<h3>Run a search first</h3><p>Enter a keyword on the home page, then open this tab.</p>'
NO_MATCH_HTML = '<h3>No papers matched</h3><p>Matching is case-sensitive and looks only at paper titles.</p>'


def delete_files_in_folder(folder_path):
    """Remove the files (not sub-folders) in folder_path; a missing folder is fine."""
    if not os.path.isdir(folder_path):
        return
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def load_data():
    global literature_data, author_data, author_publication_data

    missing = [f for f in DATA_FILES if not os.path.isfile(os.path.join(DATA_DIR, f))]
    if missing:
        raise SystemExit(
            'Missing data file(s) in database/: ' + ', '.join(missing) + '\n'
            "See README.md, section 'Getting the data'.")

    literature_data = pd.read_csv(os.path.join(DATA_DIR, 'literature_data.csv'), encoding='utf-8')
    author_data = pd.read_csv(os.path.join(DATA_DIR, 'author_data.csv'), encoding='utf-8')
    author_publication_data = pd.read_csv(os.path.join(DATA_DIR, 'author_publication_data.csv'), encoding='utf-8')


os.makedirs(VISION_DIR, exist_ok=True)
load_data()


def search_literature(text):
    """Papers whose title contains text, plus their author links and author records."""
    global filtered_literature, author_results, publication_results

    matches = literature_data['Title'].str.contains(text, regex=False, na=False)
    filtered_literature = literature_data[matches]

    publication_ids = filtered_literature['EID'].unique()
    publication_results = author_publication_data[author_publication_data['PublicationEID'].isin(publication_ids)]

    author_ids = publication_results['Author(s) ID'].unique()
    author_results = author_data[author_data['Author(s) ID'].isin(author_ids)]

    return filtered_literature, author_results, publication_results


def show_network(column, name, top_n, template):
    if filtered_literature is None:
        return NO_SEARCH_HTML
    if filtered_literature.empty:
        return NO_MATCH_HTML
    keywords, info, matrix = build_network_data(filtered_literature[column], top_n)
    network_visu(keywords, info, matrix, name)
    return render_template(template)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/search.html', methods=['POST'])
def search():
    global user_input, literature_results, image_files

    if user_input != request.form['user_input']:
        user_input = request.form['user_input']
        delete_files_in_folder(VISION_DIR)
        image_files = []
        literature_results, _, _ = search_literature(user_input)

    return render_template('search.html', user_input=user_input, literature_results=literature_results)


@app.route('/Papers.html')
def papers():
    if literature_results is None:
        return NO_SEARCH_HTML
    return render_template('Papers.html', user_input=user_input, literature_results=literature_results)


@app.route('/direction.html')
def direction():
    return render_template('direction.html')


@app.route('/keywordsNetwork.html')
def keywords_network():
    return show_network('Author Keywords', 'keyword', top_n_keyword, 'keywordsNetwork.html')


@app.route('/paperNetwork.html')
def paper_network():
    return show_network('References', 'paper', top_n_paper, 'paperNetwork.html')


@app.route('/visualize', methods=['GET'])
def visualize():
    if filtered_literature is None:
        return NO_SEARCH_HTML
    if filtered_literature.empty:
        return NO_MATCH_HTML
    if not image_files:
        generate_visualizations()
    return render_template('visualize.html', image_files=image_files)


def generate_visualizations():
    eda(author_results, filtered_literature, publication_results)

    image_files.extend([
        'author_aff.jpg',
        'author_productivity.jpg',
        'world_heat_map_author.jpg',
        'influence_factor_rank.jpg',
        'source_title_analysis.jpg',
        'yearly_publication_trends.jpg',
    ])


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # the reloader would load the 237 MB CSV twice
