from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def nube(diccionario):
    wc = WordCloud(background_color='black').generate_from_frequencies(diccionario)
    fig = plt.figure(figsize = (9,6))
    plt.axis("off")
    return plt.imshow(wc)
    
