echo "Checking Python environment"
python -m pip -q install -r requirements.txt
echo "Analyzing tweets from default user"
python tweet_import.py; # Runs with default username, currently WSJ journalist brianna abbott
echo "Analyzed tweets from Bri, working on Trump"
python tweet_import.py realdonaldtrump; # Runs with Trump's personal twitter
python tweet_import.py potus; # Runs with current POTUS
echo "Analyzed tweets from Trump. Done."

