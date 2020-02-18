'''
This file makes a word cloud file from the input text file

Produces an image in the same directory as the text file
'''
from os import path
from wordcloud import WordCloud
from re import sub as regexprep
# Instantiates a client


class word_cloud_from_txt():
    '''
    Class to interface with the wordcloud module
    '''
    def __init__(self, file_name):
        '''
        Builds wordcloud from filename
        '''
        if not path.isfile(file_name):
            raise Exception('Could not find File')
        print(f'Generating wordcloud from {file_name}')
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
        out_file = regexprep('\\.\\w+', '.png', file_name)
        print(f'Saving word cloud to: {out_file}')

        plt.savefig(out_file)
        self.out_file = out_file

if __name__ == '__main__':
    '''
    Provide command-line interface for ease of use

    Run as a simple command with a valid ascii file name as the only argument
    '''
    testCloud = word_cloud_from_txt('cloud_test/const.txt')
