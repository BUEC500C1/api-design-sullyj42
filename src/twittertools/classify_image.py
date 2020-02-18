#!/usr/bin/env python3
'''
Contains a class to pass an image file (stored locally) to Google Vision API
'''
import io
import os
from os.path import join as fullfile, exists as isfile, sep as filesep
from sys import argv, stderr
# import json
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from re import sub as regexprep


class python_image():
    '''
    This class is meant to handle all the calls to the Google Vision API

    Returns an easy to work with list of the image attributes

    better renamed as google_image
    '''
    def __init__(self, file_name=''):
        '''
        This starts a google image client and pushes a file through

        If initiated with a valid file name, it will process that file
        '''
        self.client = vision.ImageAnnotatorClient()
        if isfile(file_name):
            self.process_file(file_name)
        else:
            if file_name == '':
                pass
                # Just create a class instance and wait
            else:
                # We expected to get a file
                raise FileNotFoundError

    def process_file(self, file_name):
        '''
        This method passes the file_name to google vision

        Populates the filename and labels into the class

        Writes json data for image, and the labels

        If the labels are "text", or "font,"
        -- it may be interesting to pass into OCR module
        '''
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)

# Performs label detection on the image file
        response = self.client.label_detection(image=image)
        self.dirty_labels = [label.description for label in
                             response.label_annotations]
        self.labels = clean_labels(self.dirty_labels)
        self.responses = response

        out_file = regexprep('\\.\\w+', '_results.json', file_name)
        with open(out_file, 'w') as outputjson:
            print(response, file=outputjson)

        out_file = os.path.dirname(file_name) + filesep + 'image_labels.txt'
        with open(out_file, 'a') as aggregateLabels:
            print(*self.labels, sep=' ', file=aggregateLabels)
            print('\n', file=aggregateLabels)
        self.file_name = file_name
        return out_file


def clean_labels(dirty_labels):
    '''
    This is a computationally complex way to remove common words from labels

    There is probably a nicer way to do this, since each label is a list
    -- Adapted from a function which operated on tweets (paragraphs)
    '''
    clean_labels = []

    with open('/media/sf_JP-Macbook/Documents/ec500/video-sullyj42/apiDesignSullyj42/commonwords.txt', 'r') as wordlist:
        words_to_remove = wordlist.readlines()
    words_to_remove = [word.lower().strip() for word in words_to_remove]
    for label in dirty_labels:
        temp_string = label.lower().strip()
        appendFlag = True
        for word in words_to_remove:
            # Remove the matching word from the list
            if word == temp_string:
                appendFlag = False
        if appendFlag:
            clean_labels.append(temp_string)

    return clean_labels


if __name__ == '__main__':
    '''
    This provides command-line debugging
    '''
    img_class = python_image()
    # a.analyzeUsername('brabbott42', range(0, 1000, 200))
    if len(argv) == 2:
        in_file = argv[1]
    elif len(argv) == 1:
        in_file = fullfile('images', 'samples', 'mountains.jpg')

    if not isfile(in_file):
        # This error handling may also be handled in the class
        print(f'\nCould not find input file: {in_file}', file=stderr)
        raise FileNotFoundError
    img_class.process_file(in_file)
