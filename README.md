# youtube-transcript-scraper

## description
Since YouTube does not provide automatically generated transcripts via its API and normal scraping does not work with YT's ajaxy interface, this script uses browser automation to click through the YouTube web interface and download the transcript file.

## requirements
* a functioning webdriver environment (tested with [https://github.com/mozilla/geckodriver/releases][1]);
* the selenium package for Python;
* webdriver-manager https://pypi.org/project/webdriver-manager/
* a CSV file with a column for video ids as input;

## use
* download script;
* create a directory called "subtitles" and make sure the script can write to it;
* modify captions.py with your CSV filename;
* make sure that webdriver and selenium are installed;
* run the script;

[1]:	https://github.com/mozilla/geckodriver/releases
