'''
Run test case on tweet_image
'''
# from unittest import TestCase
# import pytest
from tweet_import import tweet_import
from os.path import isfile, join
from make_word_cloud import word_cloud_from_txt


def test_tweet_import_connection():
    '''
    This function tests if a connection can be established
    '''
    tweet_api = tweet_import()
    assert isinstance(tweet_api, tweet_import), \
        'The connection was not established'


def test_tweet_total():
    '''
    This function tests the end-end results

    Expects to generate an image file
    -- passes if true, fails if false

    Should probably also check that various subfiles are not empty...
    '''
    username = 'brabbott42'
    tweetClass = tweet_import()
    # a.analyzeUsername('brabbott42', range(0, 1000, 200))
    tweetClass.analyzeUsername(username)
    tweetClass.classify_images()
    word_cloud_from_txt(tweetClass.write_summaryfile())
    assert isfile(join(tweetClass.curFolder, 'twitter_output.png')),\
        'The wordcloud image was not created'


if __name__ == '__main__':
    test_tweet_import_connection()
