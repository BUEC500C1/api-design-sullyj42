import io
import os
import json
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
    def __init__(self, file_name):
        client = vision.ImageAnnotatorClient()
        if not os.path.exists(file_name):
            raise Exception('File not found');
#   Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content = content)

# Performs label detection on the image file
        response = client.label_detection(image = image)
        self.labels = [label.description for label in response.label_annotations]
        self.responses = response;

        out_file = regexprep('\.\w+', '_results.json', file_name)
        print(out_file)
        with open(out_file, 'w') as outputjson:
            print(response, file = outputjson)

        with open('images/image_labels.txt', 'a') as aggregateLabels:
            print(*self.labels, sep = ' ', file = aggregateLabels)


