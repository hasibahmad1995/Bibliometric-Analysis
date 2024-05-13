import pandas as pd

from utils.visualization.author_analysis import AuthorAffiliations, AuthorCollaborationNetwork, \
    AuthorProductivity, WorldHeatMapAuthor
from utils.visualization.publication_analysis import YearlyPublicationTrends, SourceTitleAnalysis, citation_rank, \
    influence_factor_rank


def author_analysis(top_n, author_data, author_publication_data, image_path):
    print('2. Author Analysis: '
          '\n①Author Affiliations: Visualize the distribution of authors across different affiliations to understand '
          'which institutions are most represented in the dataset.'
          '\n③Author Productivity: Histogram or bar chart showing the distribution of the number of publications per '
          'author. ')
    AuthorAffiliations(author_data, top_n, image_path + 'author_aff.jpg')
    AuthorProductivity(author_data, author_publication_data, top_n, image_path + 'author_productivity.jpg')
    WorldHeatMapAuthor(author_data, image_path + 'world_heat_map_author.jpg')


def publication_analysis(top_n, literature_data, image_path):
    print('3. Publication Analysis:'
          '\nCitation count.'
          '\nYearly Publication Trends: Line chart showing the number of publications over the years to identify '
          'trends.'
          '\nSource Title Analysis: Bar chart or word cloud showing the most frequent source titles to identify the '
          'most common publishing outlets. ')
    # citation_rank(top_n, literature_data, image_path + 'citation_rank.jpg')
    influence_factor_rank(top_n, literature_data, image_path + 'influence_factor_rank.jpg')
    YearlyPublicationTrends(literature_data, image_path + 'yearly_publication_trends.jpg')
    SourceTitleAnalysis(literature_data, top_n, image_path + 'source_title_analysis.jpg')

def eda(author_data, literature_data, author_publication_data):
    top_n = 10
    image_path = 'static/image/vision/'

    author_analysis(top_n, author_data, author_publication_data, image_path )
    publication_analysis(top_n, literature_data, image_path)
