# api-design-sullyj42

## Tokens 
All tokens should be placed in the src/twittertools/tokens directory.

Twitter tokens can either be placed in separate files names twitter_consumer_key.token, ..., placed in a single "keys" file (specification from config py), or set up as environmental variable. The program will automatically try to to detect keys in the format above. If keys are not detected, the program will fail.

## Usage
This repository contains a series of structures to help analyze a users twitter feed. The end-goal was to create a word-cloud summarizing a users Twitter history. Run on XUbuntu with an Anaconda Python 3.8.1 environment (requirements generated using pip freeze)

Example outputs can be viewed under "outputs/examples"

There are a number of files saved to the output directory which an end-user may not care about. However, these outputs are very useful for debugging. A future release should restrict or clean up these files

There are three files in the twittertools package
## worcloud
Given a text file, produces a wordcloud summary (png image). 

## python_image
Given a local image file (path string), upload to Google Vision and return the labels
-- Requires a json credentials file
-- -- locally accessed as a file in the "tokens" directory
-- -- remotely accessed as an environmental variable (Github Secrets)

## python_twitter
Using the tweepy API retrieve the 200(ish) most recent tweets

Downloads and cleans the text from tweets
-- Cleans any words matching ~100 most common english words as found in commonwords.txt (avoids "swamping" wordcloud"

Downloads images and makes calls to python_image to create a text description of each image
-- Remove common image labels ("photo", "text font")

-- Requires four token files for access to the API
-- Requires a json credentials file
-- -- locally accessed as a file in the "tokens" directory
-- -- remotely accessed as an environmental variable (Github Secrets)

## Testing
End-end testing is established by Github Secrets. 

Unit testing is established wherever possible. Including using intermediate "stubs" of python objects from Pickle. 
