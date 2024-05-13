import os
import csv
import pandas as pd
from flask import Flask, render_template, request, jsonify
from icecream import ic

from utils.exploratory_data_analysis import eda
from utils.social_network import load_network_data, select_top_n_keywords
from utils.visualization.network_visu import network_visu

app = Flask(__name__)

literature_data = None
author_data = None
author_publication_data = None
user_input = None
literature_results = None
filtered_literature = None
author_results = None
publication_results =None
image_files = []

top_n_keyword = 300
top_n_paper = 10
keywords_set = None
keyword_info_map = None
co_occurrence_matrix = None

def delete_files_in_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("All files in the folder have been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")

delete_files_in_folder('database/keyword')
delete_files_in_folder('database/paper')

def update_key_network(author_keywords_series, path, top_n):
    # caculate socail network parameter
    keywords_set, keyword_info_map, co_occurrence_matrix = load_network_data(author_keywords_series, os.path.abspath(
        '.') + '\\database\\'+path+'\\')

    # print(keywords_set, keyword_info_map, co_occurrence_matrix)
    # Visualize co-occurrence matrix with dynamic top_n
    selected_keywords_set, selected_keywords_info, selected_co_occurrence_matrix = select_top_n_keywords(keywords_set,
                                                                                                         keyword_info_map,
                                                                                                         co_occurrence_matrix,
                                                                                                         top_n)

    # Visualize the co-occurrence matrix with top N keyword
    network_visu(selected_keywords_set, selected_keywords_info, selected_co_occurrence_matrix, path)

@app.route('/keywordsNetwork.html')
def network():
    global filtered_literature, top_n_keyword, keywords_set, keyword_info_map, co_occurrence_matrix

    author_keywords_series = filtered_literature['Author Keywords']
    update_key_network(author_keywords_series, 'keyword',top_n_keyword)
    return render_template('keywordsNetwork.html')

def load_data():
    global literature_data, author_data, author_publication_data

    # literature_data.csv
    literature_data = pd.read_csv('database/literature_data.csv', encoding='utf-8')

    # author_data.csv
    author_data = pd.read_csv('database/author_data.csv', encoding='utf-8')

    # author_publication_csv.csv
    author_publication_data = pd.read_csv('database/author_publication_data.csv', encoding='utf-8')
    ic(literature_data, author_data, author_publication_data)
load_data()


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/search.html', methods=['POST'])
def search():
    global user_input, literature_results, search_results, image_files
    if user_input != request.form['user_input']:
        ic(user_input, request.form['user_input'])
        user_input = request.form['user_input']
        delete_files_in_folder('static/image/vision')
        delete_files_in_folder('database/keyword')
        delete_files_in_folder('database/paper')
        image_files = []
        literature_results, author_results, publication_results = search_literature(user_input)

        search_results = {
            'user_input': user_input,
            'literature_results': literature_results,
            'author_results': author_results,
            'publication_results': publication_results
        }

    return render_template('search.html', user_input=user_input, literature_results=literature_results)

@app.route('/Papers.html')
def papers():
    global user_input, literature_results
    print(user_input)
    return render_template('Papers.html', user_input=user_input, literature_results=literature_results)



# @app.route('/visualize.html')
# def visualize():
#     return render_template('visualize.html')


@app.route('/direction.html')
def direction():
    return render_template('direction.html')

@app.route('/paperNetwork.html')
def paperNetwork():
    global filtered_literature, top_n_paper, keywords_set, keyword_info_map, co_occurrence_matrix

    author_keywords_series = filtered_literature['References']
    update_key_network(author_keywords_series, 'paper',top_n_paper)
    return render_template('paperNetwork.html')

# @app.route('/keywordsNetwork.html')
# def keywordsNetwork():
#     return render_template('keywordsNetwork.html')

def search_literature(user_input):
    global literature_data, author_data, author_publication_data,filtered_literature, author_results, publication_results
    ic(literature_data)
    ic(user_input)
    # filtered_literature = literature_data[literature_data['Title'].str.contains(user_input)]
    filtered_literature = literature_data[literature_data['Title'].str.contains(user_input, regex=False)]

    publication_ids = filtered_literature['EID'].unique()
    publication_results = author_publication_data[author_publication_data['PublicationEID'].isin(publication_ids)]

    author_ids = publication_results['Author(s) ID'].unique()
    author_results = author_data[author_data['Author(s) ID'].isin(author_ids)]

    ic(filtered_literature, author_results, publication_results)
    return filtered_literature, author_results, publication_results

from flask import send_from_directory, render_template
IMAGE_PATH = 'static/images/vision/'

@app.route('/visualize', methods=['GET'])
def visualize():
    global image_files
    ic(image_files)
    if image_files == []:
        generate_visualizations()
    return render_template('visualize.html', image_files=image_files)

def generate_visualizations():

    global filtered_literature, author_results, publication_results, image_files

    eda(author_results, filtered_literature, publication_results)

    image_files.append('author_aff.jpg')
    image_files.append('author_productivity.jpg')
    image_files.append('world_heat_map_author.jpg')
    image_files.append('influence_factor_rank.jpg')
    image_files.append('source_title_analysis.jpg')
    image_files.append('yearly_publication_trends.jpg')

    # return image_files

@app.route('/static/images/<path:filename>')
def download_file(filename):
    return send_from_directory(IMAGE_PATH, filename)


if __name__ == '__main__':
    app.run(debug=True)
