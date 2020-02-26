'''
Run test case on tweet_image
'''
# from unittest import TestCase
# import pytest
from twittertools.tweet_import import tweet_import
from os.path import isfile, join, isdir
from pathlib import Path
from shutil import rmtree
from twittertools.make_word_cloud import word_cloud_from_txt
from glob import glob  # For file matching with wildcard
from pickle import load as pload

def test_tweet_import_connection():
    '''
    This function tests if a connection can be established
    '''
    tweet_api = tweet_import()
    assert isinstance(tweet_api, tweet_import), \
        'The connection was not established'

def test_tweet_partial():
    '''
    This function tests if 

    Useful if no network connection is obtained
    '''

    #  tweetClass.classify_images() This requires a Google Vsision connection


    # Run offline tests
    fname = Path(__file__)
    fdir = fname.parent
    fname = join(fdir, '../twitter_test/brabbott42_200tweets.p')
    outdir = join(fdir, 'output')
    if not isfile(fname):
        print(f'Could not find file: {fname}')
        assert False, 'Expected a twitter object to be saved for testing'
    try:
        twit_obj = pload(open(fname, 'rb'))
    except:
        assert False, 'could not load object'
    try:
        twit_obj.iteration = 0  # Make it build the dir for the first time
        if isdir(outdir):
            print(f'Detected output directory {outdir}')
            rmtree(outdir)
        twit_obj.makeoutputfolder()
    except:
        assert False, 'Could not make (or remove old) output directory'
    try:
        sumfile = twit_obj.write_summaryfile()
    except:
        assert False, 'Could not make summary file'
    try:
        word_cloud_from_txt(sumfile)
    except:
        assert False, 'Could not make word cloud'

    assert True
    # This is normally created with the object, but we are trying to cheat

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
    imagelist = glob(join(tweetClass.curFolder, 'twitter_*.png'))
    imagetest = len(imagelist) == 1
    assert imagetest, 'A single output wordcloud was not detected'


if __name__ == '__main__':
    test_tweet_import_connection()
    test_tweet_total()
    print('Passed')
