from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def economia_social(es):
    wc = WordCloud(background_color='black').generate_from_frequencies(es)
    fig = plt.figure(figsize = (9,6))
    #plt.imshow(wc)
    plt.axis("off")
    return plt.show()
