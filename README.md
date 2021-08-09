# CFC Insight Technical Challenge

The challenge involves writing a program that:

1. Scrapes the index webpage hosted at `cfcunderwriting.com`

2. Writes a list of *all externally loaded resources* (e.g. images/scripts/fonts not hosted on cfcunderwriting.com) to a JSON output file.

3. Enumerates the page's hyperlinks and identifies the location of the "Privacy Policy" page.

4. Uses the privacy policy URL identified in step 3 and scrapes the page's content. Produces a case-insensitive word frequency count for all of the visible text on the page and writes it to a JSON output file.

## Setup and running instructions

1. Install the required dependencies.
`$ pip install -r requirements.txt`

2. Execute the program
`$ python webscraper.py`

3. Find the JSON output files `external_resources.json` and `word_frequency.json` created in the current directory.