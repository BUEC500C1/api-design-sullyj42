'''
Run test case on classify_image
'''

# from unittest import TestCase
from os import remove as rm
from os.path import isfile, join as fullfile
# import pytest
from twittertools.make_word_cloud import word_cloud_from_txt
from pathlib import Path


def test_make_word_cloud():
    '''
    This function just tries to make an image from a text file

    Fails if the image file is not created
    '''
    homedir = Path(fullfile(Path(__file__).parent, '..')).resolve(strict=True)
    textfile = fullfile(homedir, 'cloud_test', 'const.txt')
    picfile = fullfile(homedir, 'cloud_test', 'const.png')
    try:
        rm(picfile)
    except FileNotFoundError:
        pass
    word_cloud_from_txt(textfile)
    assert isfile(picfile), 'File not created'


if __name__ == '__main__':
    '''
    Command-line debugging
    '''
    test_make_word_cloud()
