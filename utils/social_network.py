import pickle

from icecream import ic
import numpy as np
import pandas as pd
import hashlib

from tqdm import tqdm, trange

from utils.visualization.network_visu import network_visu

def initialize_keyword_info(author_keywords_series, path):
    print('1. Initialize keyword hash function set and keyword information hash map.')
    keywords_set = set()
    keyword_info_map = {}

    total_rows = len(author_keywords_series)

    for i in trange(total_rows, desc="Processing Keywords"):
        keywords = author_keywords_series.iloc[i]
        if pd.notna(keywords):
            keywords = [keyword.strip() for keyword in keywords.split(';')]
            for keyword in keywords:
                # calculate hash code
                keyword_hash = hashlib.sha1(keyword.encode()).hexdigest()
                # add to set
                keywords_set.add(keyword_hash)
                # count the number of occurrences of keyword
                if keyword_hash in keyword_info_map:
                    keyword_info_map[keyword_hash]['count'] += 1
                else:
                    # If the hash value does not exist, create a new dictionary and initialize it
                    keyword_info_map[keyword_hash] = {'keyword': keyword, 'count': 1}

    # store keywords_set
    with open(path + 'set.pkl', 'wb') as keywords_set_file:
        pickle.dump(keywords_set, keywords_set_file)

    # store keyword_info_map
    with open(path + 'info_map.pkl', 'wb') as keyword_info_map_file:
        pickle.dump(keyword_info_map, keyword_info_map_file)

    return keywords_set, keyword_info_map


def calculate_coOccurrence_matrix(keywords_set, author_keywords_series, path):
    print('2. Create an empty co-occurrence matrix with the dimensions equal to the number of keyword.')
    co_occurrence_matrix = np.zeros((len(keywords_set), len(keywords_set)), dtype=int)

    progress_bar = tqdm(total=len(author_keywords_series), desc="Calculating Co-Occurrence Matrix")

    for keywords in author_keywords_series.dropna():
        keywords = [keyword.strip() for keyword in keywords.split(';')]
        for i in range(len(keywords)):
            for j in range(i + 1, len(keywords)):
                # Calculate the hash value of a keyword using a hash function
                keyword1_hash = hashlib.sha1(keywords[i].encode()).hexdigest()
                keyword2_hash = hashlib.sha1(keywords[j].encode()).hexdigest()
                if (keyword1_hash in keywords_set) and (keyword2_hash in keywords_set):
                    keyword1_index = list(keywords_set).index(keyword1_hash)
                    keyword2_index = list(keywords_set).index(keyword2_hash)
                    co_occurrence_matrix[keyword1_index, keyword2_index] += 1
        progress_bar.update(1)

    progress_bar.close()

    # store coOccurrence_matrix
    np.save(path + 'coOccurrence_matrix.npy', co_occurrence_matrix)

    return co_occurrence_matrix

def select_top_n_keywords(keywords_set, keyword_info_map, co_occurrence_matrix, top_n):
    # Sort keyword_info_map by count in descending order and keep the top N
    sorted_keyword_info = sorted(keyword_info_map.items(), key=lambda x: x[1]['count'], reverse=True)[:top_n]
    selected_keywords_info = {keyword_hash: info for keyword_hash, info in sorted_keyword_info}
    ic(sorted_keyword_info,selected_keywords_info)

    # Filter keywords_set to keep only the top N keyword
    selected_keywords_set = {keyword_hash for keyword_hash, _ in sorted_keyword_info}
    ic(selected_keywords_set)

    # Select relevant part of co_occurrence_matrix
    selected_keywords_list = list(selected_keywords_set)
    keywords_list = list(keywords_set)
    selected_co_occurrence_matrix = np.zeros((len(selected_keywords_set), len(selected_keywords_set)), dtype=int)
    for i in selected_keywords_set:
        for j in selected_keywords_set:
            selected_co_occurrence_matrix[selected_keywords_list.index(i)][selected_keywords_list.index(j)] = (
                co_occurrence_matrix)[keywords_list.index(i)][keywords_list.index(j)]
    ic(selected_co_occurrence_matrix)

    return selected_keywords_set, selected_keywords_info, selected_co_occurrence_matrix


def social_network_parameter_generate(data, path):
    # initialize keywords_set & keyword_info_map
    keywords_set, keyword_info_map = initialize_keyword_info(data, path)

    # Calculate co-occurrence matrix
    co_occurrence_matrix = calculate_coOccurrence_matrix(keywords_set, data, path)

    return keywords_set, keyword_info_map, co_occurrence_matrix


def load_network_data(data, path):
    try:
        with open(path + 'set.pkl', 'rb') as keywords_set_file:
            keywords_set = pickle.load(keywords_set_file)
        ic(keywords_set)

        with open(path + 'info_map.pkl', 'rb') as keyword_info_map_file:
            keyword_info_map = pickle.load(keyword_info_map_file)
        ic(keyword_info_map)

        coOccurrence_matrix = np.load(path + 'coOccurrence_matrix.npy')
        ic(coOccurrence_matrix)

        return keywords_set, keyword_info_map, coOccurrence_matrix

    except FileNotFoundError:
        return social_network_parameter_generate(data, path)



