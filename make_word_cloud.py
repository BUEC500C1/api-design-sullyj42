from os import path
from wordcloud import WordCloud
from re import sub as regexprep
# Instantiates a client
class word_cloud_from_txt():
    def __init__(self, file_name):
        if not path.isfile(file_name):
            raise Exception('Could not find File')

        text = open(file_name).read()
        wordcloud = WordCloud().generate(text)
        import matplotlib.pyplot as plt
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        # lower max_font_size
        wordcloud = WordCloud(max_font_size=40).generate(text)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        out_file = regexprep('\.\w+', '.png', file_name)

        plt.savefig(out_file)

testCloud = word_cloud_from_txt('test/const.txt')
