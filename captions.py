# modify these values
filename = 'coronavirus.csv'										# filname with video ids
colname = 'videoId'													# column storing video ids
delimiter = ','														# delimiter, e.g. ',' for CSV or '\t' for TAB
waittime = 7														# seconds browser waits before giving up
sleeptime = [5,10]													# random seconds range before loading next video id
headless = True														# select True if you want the browser window to be invisible (but not inaudible)

#do not modify below
from time import sleep
import csv
import random
import os.path
from datetime import datetime
import pytz
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# logging config
logging.basicConfig(filename = 'captions.log', filemode = 'w', level = logging.INFO, format = '%(message)s', force = True)

# datetime config
datetimesp = datetime.now(pytz.timezone('America/Sao_Paulo'))
dt = datetimesp.strftime('%d/%m/%Y %H:%M')

def gettranscript(videoid):

	# check if transcript file already exists	
	writefilename = 'subtitles/transcript_' + videoid + '.txt'
	if os.path.isfile(writefilename):
		msg = 'transcript file already exists'
		return msg

	sleep(random.uniform(sleeptime[0],sleeptime[1]))

	options = Options()
	options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	#options.binary_location = r'C:/Program Files/Mozilla Firefox/firefox.exe'
	#service = FirefoxService('geckodriver.exe')

	# Create a new instance of the Firefox driver
	if headless:
		#driver = webdriver.Firefox(options=options, service=service)
		driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
	else:
		driver = webdriver.Firefox()

	# navigate to video
	driver.get("https://www.youtube.com/watch?v="+videoid)

	try:
		element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-menu-renderer.ytd-watch-metadata > yt-button-shape:nth-child(4) > button:nth-child(1) > yt-touch-feedback-shape:nth-child(2) > div:nth-child(1) > div:nth-child(2)')))
	except:
		msg = 'could not find options button'
		driver.quit()
		return msg

	try:
		element.click()
	except:
		msg = 'could not click'
		driver.quit()
		return msg

	try:
		element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, '//yt-formatted-string[text()="Mostrar transcrição"]')))
	except:
		msg = 'could not find transcript in options menu'
		driver.quit()
		return msg

	try:
		element.click()
	except:
		msg = 'could not click'
		driver.quit()
		return msg

	try:
		element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.ID, "segments-container")))
	except:
		msg = 'could not find transcript text'
		driver.quit()
		return msg

	# print(element.text)

	file = open(writefilename,"w")
	file.write(element.text)
	file.close() 

	driver.quit()

	return 'ok'

# read CSV file
csvread = open(filename, newline='\n')
csvreader = csv.DictReader(csvread, delimiter=delimiter, quoting=csv.QUOTE_NONE)
rowcount = len(open(filename).readlines())

for row in csvreader:
	msg = gettranscript(row[colname])
	logging.info(f'{dt} | {str(rowcount)} | {row[colname]} | {msg}')
	rowcount -= 1
	print(dt + " | " + str(rowcount) + " | " + row[colname] + " | " + msg)