'''
Run test case on tweet_image
'''
# from unittest import TestCase
# import pytest
from tweet_import import tweet_import


def test_tweet_import_connection():
    '''
    This function tests if a connection can be established
    '''
    tweet_api = tweet_import()
    assert isinstance(tweet_api, tweet_import), \
        'The connection was not established'


if __name__ == '__main__':
    test_tweet_import_connection()
