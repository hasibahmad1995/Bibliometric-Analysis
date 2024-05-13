import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from tqdm import tqdm


def AuthorAffiliations(author_data, top_n, savePath):
    affiliations_list = author_data['Affiliations'].str.strip()

    # Count affiliation occurrences
    affiliation_counts = affiliations_list.value_counts()

    # Transpose the DataFrame
    top_affiliations = affiliation_counts.head(top_n).reset_index().rename(
        columns={'index': 'Affiliation', 'Affiliations': 'Number of Authors'})

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(top_affiliations['Affiliation'], top_affiliations['Number of Authors'], color='skyblue')
    plt.title('Top {} Author Affiliations'.format(top_n))
    plt.xlabel('Number of Authors')
    plt.ylabel('Affiliation')
    plt.tight_layout()
    plt.savefig(savePath)
    print('Author Affiliations saved in ', savePath)


def AuthorCollaborationNetwork(author_data, savePath):
    G = nx.Graph()

    # Iterate through the DataFrame and add nodes and edges
    for index, row in tqdm(author_data.iterrows(), total=len(author_data), desc="Building Collaboration Network"):
        user_id = row['Author(s) ID']
        affiliations = row['Affiliations']
        if pd.notna(affiliations):  # Check for missing values
            affiliations = affiliations.split(',')  # Split affiliations if not missing

            for affiliation in affiliations:
                G.add_node(user_id)  # Add author as a node
                G.add_edge(user_id, affiliation)  # Add edge between author and affiliation

    # Visualize the author collaboration network
    pos = nx.spring_layout(G, seed=42)  # Layout algorithm for the graph
    plt.figure(figsize=(10, 8))
    nx.draw_networkx(G, pos, with_labels=False, node_size=10, node_color='skyblue', edge_color='gray', alpha=0.7)
    plt.title('Author Collaboration Network Visualization')
    plt.savefig(savePath)
    # print('Author Collaboration Network saved in ', savePath)


def AuthorProductivity(author_data, author_publication_data, top_n, savePath):
    # Group authors by Author Name and count the number of publications for each author
    author_productivity = author_publication_data.groupby('Author(s) ID').size().reset_index(name='Publication Count')
    # print(author_productivity)
    # Sort authors by productivity
    author_productivity = author_productivity.sort_values(by='Publication Count', ascending=False)
    # print(author_productivity)

    # Transpose the DataFrame
    top_affiliations = author_productivity.head(top_n)
    # print(top_affiliations)
    # Create a bar chart
    plt.figure(figsize=(10, 6))

    merged_data = top_affiliations.merge(author_data, on='Author(s) ID', how='left')

    plt.figure(figsize=(12, 6))
    plt.bar(merged_data['Author Name'], merged_data['Publication Count'], color='skyblue')
    plt.xlabel('Author Name')
    plt.ylabel('Publication Count')
    plt.title('Publication Count by Author')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(savePath)
    # print('Author Productivity saved in ', savePath)


def WorldHeatMapAuthor(author_data, savePath):
    # Count the number of authors from each country
    country_counts = author_data['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'Author Count']
    # print(country_counts)

    # Load the world shapefile (replace with the actual file path)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    data = country_counts
    # Merge the world shapefile with the data using ISO country codes
    world_data = world.merge(pd.DataFrame(data), left_on='name', right_on='country')

    # Create a figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    # Plot the world map
    world.boundary.plot(ax=ax, linewidth=1)

    # Create a heatmap layer
    world_data.plot(column='Author Count', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

    # # Add labels with author counts for x, y, label in zip(world_data.geometry.centroid.x,
    # world_data.geometry.centroid.y, world_data['Author Count']): ax.text(x, y, f'{label}', fontsize=10,
    # ha='center', va='center')

    # Set axis title
    ax.set_title('Authors\' Country Heatmap')

    # Show the plot
    plt.savefig(savePath)
