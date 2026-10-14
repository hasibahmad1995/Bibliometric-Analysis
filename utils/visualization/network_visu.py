import os

from pyecharts import options as opts
from pyecharts.charts import Graph

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static'))

TITLES = {
    'keyword': 'Keyword Co-Occurrence Network',
    'paper': 'Reference Co-Occurrence Network',
}


def nor(value, min_value, max_value):
    """Scale a count into a node size between 5 and 50."""
    new_min, new_max = 5, 50
    if max_value == min_value:
        return (new_min + new_max) / 2
    return (value - min_value) / (max_value - min_value) * (new_max - new_min) + new_min


def create_keyword_network(keywords, keyword_info_map, coOccurrence_matrix):
    keywords = list(keywords)
    counts = [keyword_info_map[k]['count'] for k in keywords]
    min_count = min(counts, default=0)
    max_count = max(counts, default=0)

    nodes = []
    for key, count in zip(keywords, counts):
        nodes.append({
            "name": keyword_info_map[key]['keyword'],
            "symbolSize": nor(count, min_count, max_count),
            "itemStyle": {"color": "rgba(142, 192, 173, 0.9)"},
            "label": opts.LabelOpts(position="top", font_size=10),
        })

    edges = []
    for i in range(len(keywords)):
        for j in range(i + 1, len(keywords)):
            weight = int(coOccurrence_matrix[i, j])
            if weight > 0:
                edges.append({
                    "source": keyword_info_map[keywords[i]]['keyword'],
                    "target": keyword_info_map[keywords[j]]['keyword'],
                    "value": weight,
                })

    return nodes, edges


def visualize_keyword_network(nodes, edges, path):
    graph = (
        Graph()
        .add(
            "",
            nodes,
            edges,
            repulsion=500,  # node spacing
            layout="force",
            label_opts=opts.LabelOpts(is_show=True),
            is_focusnode=True,
            is_roam=True,
            is_draggable=True,
            edge_label=True,
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=TITLES.get(path, 'Co-Occurrence Network')))
    )
    graph.render(os.path.join(STATIC_DIR, path + '_network.html'))


def network_visu(keywords, keyword_info_map, coOccurrence_matrix, path):
    nodes, edges = create_keyword_network(keywords, keyword_info_map, coOccurrence_matrix)
    visualize_keyword_network(nodes, edges, path)
