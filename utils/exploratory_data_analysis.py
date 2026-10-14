import os

from utils.visualization.author_analysis import AuthorAffiliations, \
    AuthorProductivity, WorldHeatMapAuthor
from utils.visualization.publication_analysis import YearlyPublicationTrends, SourceTitleAnalysis, \
    influence_factor_rank

IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'image', 'vision'))


def author_analysis(top_n, author_data, author_publication_data, image_path):
    """Author Affiliations, Author Productivity and a world heat map of author countries."""
    AuthorAffiliations(author_data, top_n, os.path.join(image_path, 'author_aff.jpg'))
    AuthorProductivity(author_data, author_publication_data, top_n, os.path.join(image_path, 'author_productivity.jpg'))
    WorldHeatMapAuthor(author_data, os.path.join(image_path, 'world_heat_map_author.jpg'))


def publication_analysis(top_n, literature_data, image_path):
    """Influence factor ranking, yearly publication trend and top source titles."""
    influence_factor_rank(top_n, literature_data, os.path.join(image_path, 'influence_factor_rank.jpg'))
    YearlyPublicationTrends(literature_data, os.path.join(image_path, 'yearly_publication_trends.jpg'))
    SourceTitleAnalysis(literature_data, top_n, os.path.join(image_path, 'source_title_analysis.jpg'))


def eda(author_data, literature_data, author_publication_data):
    top_n = 10
    os.makedirs(IMAGE_DIR, exist_ok=True)

    author_analysis(top_n, author_data, author_publication_data, IMAGE_DIR)
    publication_analysis(top_n, literature_data, IMAGE_DIR)
