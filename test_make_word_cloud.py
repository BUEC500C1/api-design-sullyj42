'''
Run test case on classify_image
'''

# from unittest import TestCase
from os import remove as rm
from os.path import isfile
# import pytest
from .make_word_cloud import word_cloud_from_txt


def test_make_word_cloud():
    '''
    This function just tries to make an image from a text file

    Fails if the image file is not created
    '''
    try:
        rm('cloud_test/const.png')
    except FileNotFoundError:
        pass
    word_cloud_from_txt('cloud_test/const.txt')
    assert isfile('cloud_test/const.png'), 'File not created'


if __name__ == '__main__':
    '''
    Command-line debugging
    '''
    test_make_word_cloud()
