#!/usr/bin/env python3

import tweepy
from tweepy import OAuthHandler
import json 
# import csv      # Format things nicely
import re         # Clean up tweets (remove "RT", @(...), etc)

from datetime import datetime
import sys
import subprocess

# Create and manipulate files
from   os.path import isfile, sep, isdir
from   os      import makedirs, remove
# Debug
from time import sleep

class tweet_import():
    '''
    This class provides a set of methods to analyze Twitter data
    '''
    def __init__(self): 
        ''' 
        This attempts to initialize a twitter API interface

        Attempts to read from the keys (stored locally),
        Throws error if connection unsuccessful 
        '''
        
        consumer_key        = getKeyFromTxt('./tokens/twitter_consumer.token')
        consumer_secret     = getKeyFromTxt('./tokens/twitter_consumer_secret.token')
        access_token        = getKeyFromTxt('./tokens/twitter_access.token')
        access_secret = getKeyFromTxt('./tokens/twitter_access_secret.token')
        try:
            auth = tweepy.OAuthHandler(consumer_key,
                                       consumer_secret)
            auth.set_access_token(access_token, access_secret)

            self.client = tweepy.API(auth)
            if not self.client.verify_credentials():
                raise tweepy.TweepError
        except tweepy.TweepError as e:
            print('ERROR : connection failed. Check your OAuth keys.')
        else:
            print(f'Connected as {self.client.me().screen_name}, you can start to tweet !')
            self.client_id = self.client.me().id

    def makeoutputfolder(self):
        datestr = datetime.now().strftime('%Y_%m_%d')
        timestr = datetime.now().strftime('%H_%M%S')
        if not isdir('output'):
            makedirs('output'); 
        curFolder = 'output' + sep + datestr
        if not isdir(curFolder):
            makedirs(curFolder)

        curFolder = curFolder + sep + self.user
        if not isdir(curFolder):
            makedirs(curFolder)
        else: 
            # This logic is useful if we are iterating over multiple tweets
            i = 1
            temp = curFolder
            while isdir(temp):
                temp = curFolder + '_' + str(i)
                i += 1; 
            makedirs(temp)
            curFolder  = temp; 
        self.curFolder = curFolder; 



    def analyzeUsername(self, username):
        '''
        Given a valid username, makes call to tweepy to donwload recent tweet data

        Grabs full texts of tweets and retweets
        -- Full Retweets are not simple to analyze, this may deprecate over time

        Produces two files. 
        1. A text file of all tweets
        -- Lightly cleaned to remove certain non-sentimental features
        -- Cleaning performed in next function

        2. A text file containing a list of URL's to pass  into google vision

        Currently looking at all tweets (replies, retweets, etc). This could be revisited
        '''

        self.user = username # Make this an optional parameter if it exists in self? 
        self.makeoutputfolder(); 
        # Ontain a 'ResultSet' of new tweets
        new_tweets = self.client.user_timeline(screen_name = self.user, \
                                            count=200, tweet_mode="extended")

        # Parse text
        tweetsText = []
        for tweet in new_tweets:
            # This could easily deprecate, or break if tweet happens to start with 'RT '...
            if tweet.full_text[0:3] == 'RT ':
                try: 
                    # Try to get the full text of the retweet
                    tweetsText.append(tweet._json["retweeted_status"]["full_text"])
                except KeyError:
                    # If it can't be found, just add the "full text"
                    tweetsText.append(tweet.full_text)

            else:
                tweetsText.append(tweet.full_text)

        # Parse URL's
        urlData = [];
        for tweet in new_tweets:
            try: 
                urlData.append(tweet.entities['media'][0]['media_url'])
            except (NameError, KeyError):
                pass

        self.writeTweetData(tweetsText, urlData)

        
    def writeTweetData(self, textData, urlData):
        ''' 
        This method saves the tweet data, and image url's to an output folder
        '''

        fName = self.curFolder + sep + 'tweetData_' + self.user + '.txt'
        fid = open(fName, 'w+')
        for text in textData:
            urlstrip = re.sub(r"http\S+", "", text) # Remove url
            atstrip  = re.sub('@\w*', "", urlstrip) # Remove mentions, this is questionable
            text = atstrip
            fid.write(text + '\n\n')
        fid.close();

        fName = self.curFolder + sep + 'imageData_' + self.user + '.txt'
        fid = open(fName, 'w+')
        for s in urlData:
            fid.write(s + '\n')
        fid.close();

def getKeyFromTxt(fName):
    '''
    This function reads Twitter tokens saved as simple text files
    '''
    if isfile(fName):
        fid = open(fName, 'r')
        key = fid.readline(); 
        fid.close(); 
        return(key)
    else:
        print('\nWas the key entered as a string?\n', file = sys.stderr)
        raise Exception('File not found');

if __name__ == '__main__':
    '''
    This provides command-line debugging 
    '''
    tweetClass = tweet_import()
    # a.analyzeUsername('brabbott42', range(0, 1000, 200))
    tweetClass.analyzeUsername('brabbott42')