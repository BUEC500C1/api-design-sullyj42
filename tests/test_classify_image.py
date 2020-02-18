'''
Run test case on classify_image
'''

# from unittest import TestCase
import os
# import pytest
from twittertools.classify_image import python_image
from os.path import join as fullfile


def test_classify_image():
    '''
    This function runs two simple tests over a Google Cloud Image wrapper
    '''
    image_file = fullfile('vision_test', 'samples', 'mountains.jpg')
    if not os.path.isfile(image_file):
        raise Exception('Test image file not found')

    report_file = 'vision_test/samples/mountains_results.json'
    if os.path.isfile(report_file):
        os.remove(report_file)
    image_classifier = python_image(image_file)
    print(f'Report file: {os.path.isfile(report_file)}')
    assert os.path.isfile(report_file), 'json report file not generated'

    # Make sure it contains the top-three labels
    # This could change over time, but is just a spot-check for now
    truth_labels = ['Mountainous landforms', 'Mountain', 'Mountain range']
    truth_labels = [label.lower() for label in truth_labels]
    image_labels = [label.lower() for label in image_classifier.labels]
    validLabels = set(truth_labels).issubset(set(image_labels))
    print(f'Valid labels file: {validLabels}')
    if not validLabels:
        print(*truth_labels, sep=' ')
        print(*image_classifier.labels, sep=', ')
    errmsg = 'The current results do not contain the old, top results\n'
    assert validLabels, errmsg


if __name__ == '__main__':
    '''
    Command-line debugging
    '''
    test_classify_image()
