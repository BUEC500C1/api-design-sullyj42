# api-design-sullyj42
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

## Tokens 
Currently, tokens are accessed from the local run directory. The end-user should create four files for the twitter tokens. Name them appropriately as called by the code. And paste the appropriate keys in. 

The Google JSON key should also be pasted in this directory.

The tokens should be automatically ignored by Git, but this is always worth checking.
