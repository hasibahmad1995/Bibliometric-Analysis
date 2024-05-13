from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

def citation_rank(top_n, literature_data, savePath):
    top_twenty_cited = literature_data.sort_values(by='Cited by', ascending=False).head(top_n)
    colors = [(0.0, 0.5, 1.0), (1.0, 0.0, 0.0)]
    gradient = LinearSegmentedColormap.from_list('CustomGradient', colors, N=len(top_twenty_cited))

    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_twenty_cited['Title'], top_twenty_cited['Cited by'],
                    color=[gradient(i / len(top_twenty_cited)) for i in range(len(top_twenty_cited))])
    plt.xlabel('Citation Count')
    plt.ylabel('Paper Title')
    plt.title('Citation Counts for Papers')
    plt.gca().invert_yaxis()
    for bar, count, title in zip(bars, top_twenty_cited['Cited by'], top_twenty_cited['Title']):
        label_position = bar.get_width() + 1  # Adjust this value as needed
        if label_position < 10:  # Check if the label is too close to the edge
            ha = 'left'  # Align the label to the left of the bar
            label_position = 10  # Move the label inside the plot
        else:
            ha = 'right'  # Align the label to the right of the bar
        plt.text(label_position, bar.get_y() + bar.get_height() / 2, str(count), va='center', ha=ha)
    plt.savefig(savePath)


def influence_factor_rank(top_n, literature_data, savePath):
    top_ten_influence = literature_data.sort_values(by='Influence Factor', ascending=False).head(top_n)

    colors = [(0.40, 0.85, 0.50), (1.0, 0.38, 0.45)]
    gradient = LinearSegmentedColormap.from_list('CustomGradient', colors, N=len(top_ten_influence))

    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_ten_influence['Title'], top_ten_influence['Influence Factor'],
                    color=[gradient(i / len(top_ten_influence)) for i in range(len(top_ten_influence))])
    plt.xlabel('Citation Count')
    plt.ylabel('Paper Title')
    plt.title('Citation Counts for Papers')
    plt.gca().invert_yaxis()
    plt.savefig(savePath)


def YearlyPublicationTrends(literature_data, savePath):
    # Group data by year and count the publications
    yearly_publications = literature_data.groupby('Year').size().reset_index(name='Publication Count')

    # Create a line plot
    plt.figure(figsize=(14, 10))
    plt.plot(yearly_publications['Year'], yearly_publications['Publication Count'], marker='o', linestyle='-')
    plt.title('Yearly Publication Trends')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.grid(True)
    # Set x-axis ticks to show every year
    plt.xticks(yearly_publications['Year'], rotation=45)  # Adjust rotation for better readability
    plt.savefig(savePath)


def SourceTitleAnalysis(literature_data, top_n, savePath):
    # Select the top N source titles with the highest publication counts
    top_source_titles = literature_data['Source title'].value_counts().head(top_n)
    # Create a bar chart
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_source_titles.values, y=top_source_titles.index, palette='viridis')
    plt.title('Top Source Titles by Publication Count')
    plt.xlabel('Publication Count')
    plt.ylabel('Source Title')
    plt.grid(axis='x')
    plt.tight_layout()
    plt.savefig(savePath)
