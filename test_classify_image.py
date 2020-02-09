'''
Run test case on classify_image
'''

# from unittest import TestCase
import os
# import pytest
from classify_image import python_image


def test_classify_image():
    '''
    This function runs two simple tests over a Google Cloud Image wrapper
    '''
    image_file = 'images/samples/mountains.jpg'
    if not os.path.isfile(image_file):
        raise Exception('Tets image file not found')

    report_file = 'images/samples/mountains_results.json'
    if os.path.isfile(report_file):
        os.remove(report_file)
    image_classifier = python_image(image_file)
    truth_labels = ['Mountainous landforms', 'Mountain', 'Mountain range']
    print(f'Report file: {os.path.isfile(report_file)}')
    # Make sure it generates a test file
    assert os.path.isfile(report_file), 'json report file not generated'

    # Make sure it contains the top-three labels
    # This could change over time, but is just a spot-check for now
    validLabels = set(truth_labels).issubset(set(image_classifier.labels))
    print(f'Report file: {validLabels}')
    errmsg = 'The current results do not contain the old, top results\n' + \
        'Check log file for the current labels and update test-cases if valid'
    assert validLabels, errmsg


test_classify_image()
