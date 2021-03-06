#!/usr/bin/env python3
'''
This file contains  a class to import twitter data

The tweet_import class takes a username and pulls the picture data

If called from the command-line, the function will pull data
'''

import tweepy
# import csv      # Format things nicely
import re         # Clean up tweets (remove "RT", @(...), etc)

from datetime import datetime
import sys

# Create and manipulate files
from os.path import isfile, sep, isdir, join as fullfile
from os import makedirs, environ
from requests import get as pywget

# Perform image classification
from twittertools.classify_image import python_image

# Generate a word cloud
from twittertools.make_word_cloud import word_cloud_from_txt

# Create simple pathnames to the data directories
# from pkgutil import get_data as packagedir
from pathlib import Path
import configparser


class tweet_import():
    '''
    This class provides a set of methods to analyze Twitter data
    '''
    def __init__(self, keyspath=''):
        '''
        This attempts to initialize a twitter API interface

        Attempts to read from the keys (stored locally),
        Throws error if connection unsuccessful
        '''
        try:
            # Try using local files -- My original method
            filepath = Path(__file__)
            tokenspath = fullfile(filepath.parent, 'tokens')
            print(f'\nFile TOKEN path: {tokenspath}\n', file=sys.stderr)
            consumerfile = fullfile(tokenspath, 'twitter_consumer.token')
            consumer_key = getKeyFromTxt(consumerfile)
            fullfile(tokenspath, 'twitter_consumer_secret.token')
            consecfile = fullfile(tokenspath, 'twitter_consumer_secret.token')
            consumer_secret = getKeyFromTxt(consecfile)
            access_file = fullfile(tokenspath, 'twitter_access.token')
            access_token = getKeyFromTxt(access_file)
            acsecfile = fullfile(tokenspath, 'twitter_access_secret.token')
            access_secret = getKeyFromTxt(acsecfile)
            auth = tweepy.OAuthHandler(consumer_key,
                                       consumer_secret)
            auth.set_access_token(access_token, access_secret)

        except FileNotFoundError:
            print('\nCould not find .token files, trying to find "key" file\n',
                  file=sys.stderr)
            # Stephan's block
            try:
                filepath = Path(__file__)
                tokenspath = fullfile(filepath.parent, 'tokens')
                print(f'File KEY path: {tokenspath}', file=sys.stderr)
                config = configparser.ConfigParser()
                keyfile = fullfile(tokenspath, 'keys')
                if not isfile(keyfile):
                    print(f'File "key" not found: {keyfile}', file=sys.stderr)
                    raise FileNotFoundError()
                config.read(keyfile)
                conskey = config.get('auth', 'consumer_key')  # .strip()
                consecret = config.get('auth', 'consumer_secret')  # .strip()
                accesstok = config.get('auth', 'access_token')  # .strip()
                accesssec = config.get('auth', 'access_secret')  # .strip()
                # print(f'Consumer key: "{conskey}"')
                # print(f'Consumer sec: "{consecret}"')
                # print(f'access key: "{accesstok}"')
                # print(f'access sec: "{accesssec}"')
                auth = tweepy.OAuthHandler(conskey, consecret)
                auth.set_access_token(accesstok, accesssec)
            except FileNotFoundError:
                try:
                    print('\nCould not find .token or "key" file' +
                          'Checking environmental variables (Github actions\n',
                          file=sys.stderr)
                    # Use environmental variables (Github Actions)
                    consumer_key = environ['CONSUMER_KEY']
                    consumer_secret = environ['CONSUMER_SECRET']
                    access_token = environ['ACCESS_TOKEN']
                    access_secret = environ['ACCESS_SECRET']
                    auth = tweepy.OAuthHandler(consumer_key,
                                               consumer_secret)
                    auth.set_access_token(access_token, access_secret)
                except:
                    print('Tried three methods and could not find key files.',
                          file=sys.stderr)
                    raise
        print('\nGenerated auth. Attempting to connect\n', file=sys.stderr)
        self.client = tweepy.API(auth)
        if not self.client.verify_credentials():
            # except tweepy.TweepError as e:
            # Print a more helpful debug message and rethrow
            print('\nERROR : connection failed. Check your Twitter keys.\n')
            raise tweepy.TweepError

        print(f'Connected as {self.client.me().screen_name}, you can tweet !')
        self.client_id = self.client.me().id
        self.max_id = None  # For aquiring past tweets
        self.iteration = 0  # For saving iterative tweets in new pages
        self.tweet_count = 0  # This API is limited to 3200 tweets
        # Throw a specific error when this is reached

    def makeoutputfolder(self):
        '''
        This module creates a unique file structure for analysis

        Saves the root file in curFolder for access by other methods

        Folder structure: output/date/user_X/[files]
        -- X is a simple iterator
        '''
        if self.iteration > 0:
            self.curFolder = re.sub(
                'iter\\d+',
                'iter' + str(self.iteration),
                self.curFolder)
            makedirs(self.curFolder)
            if not isdir(fullfile(self.curFolder, 'images')):
                # Make a unique directory to save images as well
                makedirs(fullfile(self.curFolder, 'images'))
            return

        if not isdir('output'):
            makedirs('output')
        datestr = datetime.now().strftime('%Y_%m_%d')
        # timestr = datetime.now().strftime('%H_%M%S')
        curFolder = fullfile('output', datestr, '')
        if not isdir(curFolder):
            # Create the first folder from scratch
            curFolder = curFolder
            makedirs(curFolder)

        curFolder = fullfile(curFolder,
                             self.user + '_iter' + str(self.iteration))

        if not isdir(curFolder):
            makedirs(curFolder)
        else:
            # Make a unique directory
            i = 1
            temp = curFolder
            while isdir(temp):  # Loop until the directory no longer exists
                temp = curFolder.replace(
                    self.user,
                    self.user + '_' + str(i))
                i += 1
            curFolder = temp
            curFolder = curFolder   # + '_iter' + str(self.iteration)
            makedirs(curFolder)

        if not isdir(fullfile(curFolder, 'images')):
            # Make a unique directory to save images as well
            makedirs(fullfile(curFolder, 'images'))

        self.curFolder = curFolder

    def analyzeUsername(self,           username, 
                        tweetcount=200, noverlap=0, 
                        work_images=True):
        '''
        Given a valid username, makes call to tweepy to donwload recent tweets

        Grabs full texts of tweets and retweets
        -- Full Retweets are not simple to analyze, this may deprecate

        Stores two lists into the structure:
            1. Tweetdata
            -- A list of full-text tweets
            2. imagedata
            -- A list of image paths to pass to google-vision

        Saves several files to the directory generated by makeoutfolder method
            1. A text file of all tweets
            -- Lightly cleaned to remove certain non-sentimental features
            -- Cleaning performed in next function

            2. A text file containing a list of URL's that we will download
            -- Useful for debugging

            3. The images from the list above, saved to "images" subdirectory

            noverlap should be made more robust to reduce recalculations
        '''
        if noverlap < 0 or noverlap >= tweetcount:
            raise ValueError()

        if self.tweet_count >= 3199:  # Eer on the side of caution
            print(f'Cannot obtain more tweets (API limits)', file=sys.stderr)
            return
        self.user = username
        self.makeoutputfolder()
        # Obtain a 'ResultSet' of new tweets

        new_tweets = self.client.user_timeline(screen_name=self.user,
                                               count=tweetcount,
                                               tweet_mode="extended",
                                               max_id=self.max_id)
        if len(new_tweets) == 0:
            print('No tweets returned, perhaps you reached the end?',
                  file=sys.stderr)
            return
        # Parse text
        tweetsText = []
        for tweet in new_tweets:
            # This could easily deprecate, or break if starts with 'RT '...
            if tweet.full_text[0:3] == 'RT ':
                try:
                    # Try to get the full text of the retweet
                    tweetsText.append(tweet._json["retweeted_status"]
                                                 ["full_text"])
                except KeyError:
                    # If it can't be found, just add the "full text"
                    tweetsText.append(tweet.full_text)

            else:
                tweetsText.append(tweet.full_text)

        # Parse URL's
        urlData = []
        for tweet in new_tweets:
            try:
                urlData.append(tweet.entities['media'][0]['media_url'])
            except (NameError, KeyError):
                pass
        max_ids = ([tweet.id for tweet in new_tweets])
        max_ids.sort()
        self.max_id = max_ids[noverlap] - 1
        self.tweet_count += len(new_tweets) - noverlap
        # We want to know if the next requests will reach over the maxima

        self.iteration += 1
        dates = [tw.created_at for tw in new_tweets]
        self.daterange = max(dates).strftime('%Y%m%d') + '_' + \
            min(dates).strftime('%Y%m%d')
        self.tweetsText = tweetsText  # Save for offline testing
        self.urlData = urlData  # Save for offline testing
        cleanTweetFile = self.writeTweetData(tweetsText)
        # print(f'work images: {work_images}')
        self.work_images = work_images
        if work_images:
            print('Working image data from analyzeUsername')
            imageFiles = self.work_picture_data(urlData)
        else:
            imageFiles = []
            self.images = []
            self.image_labels = []
        return imageFiles, cleanTweetFile
        # self.tweet_text = tweetsText # WRITE THIS AFTER CLEANING

    def writeTweetData(self, textData):
        '''
        This method saves the tweet data, and image url's to an output folder

        Also downloads the images for convenience

        Writes the dirty and clean tweets to files for comparisons
        '''
        dirty_tweet_file = self.curFolder + sep + 'DirtyTweetData_' +\
            self.user + '.txt'
        with open(dirty_tweet_file, 'w') as dirty_fid:
            print(*textData, sep='\n\n', file=dirty_fid)

        clean_tweet_file = self.curFolder + sep + 'CleanTweetData_' +\
            self.user + '.txt'
        clean_tweets = remove_words(textData)
        with open(clean_tweet_file, 'w') as clean_fid:
            print(*clean_tweets, sep='\n\n', file=clean_fid)
        self.tweet_text = clean_tweets
        return clean_tweet_file

    def work_picture_data(self, urlData):
        '''
        Google Vision API reqiures local files to be worked

        Download files and return a list of these filepaths
        '''
        # print('working image data')
        urlFile = self.curFolder + sep + 'imageData_' + self.user + '.txt'
        outfolder = fullfile(self.curFolder, 'images', '')
        with open(urlFile, 'w') as f_url:
            image_list = []
            for url in urlData:
                fname = image_downloader(url, outfolder)
                f_url.write(url + '\n')
                if fname == 0:
                    # Did not download image, currently not doing anything
                    pass
                else:
                    if isfile(fname):
                        image_list.append(fname)
                    else:
                        print(f'Imagedownloader returned ({fname})\n' +
                              'but did not download', file=sys.stderr)
        self.images = image_list
        return image_list

    def classify_images(self, images=[]):
        '''
        This function passes the images into Google Vision

        Leverages the existing lists in the class

        images parameter added to use this module independently, multithreaded

        If there are no images, return an empty list

        If there are images, return a list containing the labels for each image
        '''
        print('Classifying images, this takes some time...\n')
        
        self.image_labels = []
        try:
            g_vision = python_image()  # Try to connect to google vision
        except:  # Add options
            return self.image_labels
            
        if not images:  # If the argument is empty
            image_files = self.images
        else:
            image_files = images

        if not image_files:  # If this is empty, return an empty list
            return []
        # print(*image_files, sep='\n')
        # print(images)
        # sleep(5)

        if any([not isfile(images) for images in image_files]):
            raise FileNotFoundError
        for image_file in image_files:
            # print(f'\nClassifying: {image_file}')
            g_vision.process_file(image_file)
            # print('Classified, obtained labels: ')
            # print(*g_vision.labels, sep=' ')
            self.image_labels += g_vision.labels    # Append list into our list
            # Metadata from labels
        return self.image_labels

    def write_summaryfile(self, image_labels=[]):
        '''
        Write a summary file from the list of tweets and image labels
        '''
        outfile = fullfile(self.curFolder,
                           'twitter_' + self.user + '_' +
                           self.daterange + '.txt')
        print(f'\nWriting output file: {outfile}\n')

        if image_labels == []:
            image_labels = self.image_labels

        with open(outfile, 'w') as summary_file:
            print(*self.tweet_text, sep='\n\n', file=summary_file)
            print('\n\n', file=summary_file)
            if image_labels:  # Test if list is not empty
                for i in range(1):
                    # Make the image files more significant, arbitrarily
                    print(*image_labels, sep='\n', file=summary_file)
                    print('')
        print('Output file complete.')
        return outfile


def getKeyFromTxt(fName):
    '''
    This function reads Twitter tokens saved as simple text files
    '''
    if isfile(fName):
        print(f'\nReading token from: {fName}\n', file=sys.stderr)
        fid = open(fName, 'r')
        key = fid.readline()
        fid.close()
        return(key)
    else:
        print(f'\nKey not found in file: {fName}\ngetKeyFromTxt failure\n',
              file=sys.stderr)
        raise FileNotFoundError


def image_downloader(url, directory):
    '''
    Accepts a URL string. Attempts to download the image to directory

    if download is successful
    - returns filename.
    else
    - returns 0
    '''
    if not isdir(directory):
        raise Exception(f'Directory not accessible: {directory}')
    fname = re.findall("(?<=/)\\w+\\.\\w+", url)[-1]
    fext = re.findall("(?<=\\.)\\w+", fname)[-1]
    if fext.lower() not in ['jpg', 'png', 'tif']:
        print(f'Invalid image detected: {url}\n, skipping', file=sys.stderr)
        return 0

    try:
        img_data = pywget(url).content
    except pywget.RequestException:
        print(f'Could not download from: {url}', file=sys.stderr)
        return 0
    fname = re.findall("(?<=/)\\w+\\.\\w+", url)[-1]

    filename = directory + fname
    with open(filename, 'wb') as handler:
        handler.write(img_data)

    return filename


def remove_words(dirty_tweets):
    '''
    This is a computationally complex way to remove a set of words from string

    Check to make sure dirty_tweets is a list of strings
    '''
    clean_tweets = []
    filepath = Path(__file__)
    filename = fullfile(filepath.parent, 'textfiles', 'commonwords.txt')
    if not isfile(filename):
        print(f'Could not find file {filename}', file=sys.stderr)
        raise Exception
    with open(filename, 'r') as wordlist:
        words_to_remove = wordlist.readlines()
    words_to_remove = [word.lower().strip() for word in words_to_remove]
    for text in dirty_tweets:
        temp_string = re.sub(r"http\S+", "", text.lower().strip())
        temp_string = re.sub('@\\w*', "",    temp_string)  # Remove mentions
        # print("removing common words")
        # print(temp_string)
        for word in words_to_remove:
            # Remove anything matching the list with surronding spaces
            temp_string = temp_string.lower().replace(" " + word + " ", " ")
        # print('Removed common words')
        # print(temp_string)
        # sleep(5)
        clean_tweets.append(temp_string)

    return clean_tweets


if __name__ == '__main__':
    '''
    This provides a full interface to summarize a users twitter feed
    -- Currently looks at both text (tweets, retweets, replies) and images
    -- -- images are summarized by labels generated by Google Vision

    May be interesting to allow specific dates and so fourth eventually
    '''
    if len(sys.argv) == 1:
        username = 'brabbott42'
    elif len(sys.argv) == 2:
        username = sys.argv[1]
        pages = 1
    elif len(sys.argv) == 3:
        username = sys.argv[1]
        pages = int(sys.argv[2])
    else:
        raise Exception('Invalid number of inputs')
    tweetClass = tweet_import()
    # a.analyzeUsername('brabbott42', range(0, 1000, 200))
    for i in range(pages):
        tweetClass.analyzeUsername(username)
        # This updates the page number incrementally
        tweetClass.classify_images()
        word_cloud_from_txt(tweetClass.write_summaryfile())
