# api-design-sullyj42
This file repository contains a series of structures to help analyze a users twitter feed. The end-goal was to create a word-cloud summarizing a users Twitter history.

See pytest files for example usage. Basic usage can be tried with the command: 
>> ./runcommand.sh

This command should download the necessary requirements and attempt to run the function for three interesting twitter users. The output will be found by scrolling around in the "output" directory. 

There are a number of files saved to the output directory which an end-user may not care about. However, these outputs are very useful for debugging.

There are three Python Files in this repository. Code is documented throughout. 

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

## TO-DO
Improve the retrieval of past tweets; currently only analyzing the 200 (ish) most recent tweets
