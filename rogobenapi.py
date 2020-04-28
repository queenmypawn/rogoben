# 1. Pull data from a URL whenever there is a new data set.
# 2. Send an e-mail using Google API

# Pre-requisites:
# 1) Create a project at the Google API console at the top-left of GDC
# 2) Enable Gmail API by clicking 'Library' on the left sidebar
# 3) Create OAuth client ID credentials at the top sidebar
# 4) Quickstart guide for Python in URL (see below)
# 5) pip install --upgrade google-api-python-client \
# google-auth-httplib2 google-auth-oauthlib
# 6) Access to Gmail
# 7) Create the e-mail
# For more help, visit 'https://blog.mailtrap.io/send-emails-with-gmail-api/'
# or contact QueenMyPawn through Fiverr.

# Download a text file with the last updated date, or even data!
# If different, send an e-mail.

# Google API required modules
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Ability to download the page
# Also, the ability to read files without downloading them
# allowing us to check for real-time updates.
import requests

# Ability to run a loop using the time module
import time

# Ability to convert a time value to a datetime object
from datetime import datetime, timedelta
import math

# Ability to create the e-mail
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import os

# If modifying these scopes, delete the file token.pickle.
# You need this scope in particular for full access to Google Mail API.
SCOPES = 'https://mail.google.com/'

# Function required for Part 2: Send e-mail with Google API.
# a) Create the message
def create_message(sender, to, subject, csv):
	#message = MIMEMultipart()
	message = MIMEMultipart()
	message['from'] = sender
	message['to'] = to
	message['subject'] = subject

	# Send the time it was updated as the body of the e-mail
	dt_object = datetime.utcnow() - timedelta(hours = 7)
	msg = MIMEText('Hi! Your file was updated.' \
		'\nTime of update: ' + dt_object.strftime('%m/%d/%Y, %I:%M:%S %p') \
		+ ' (Los Angeles Time)')

	message.attach(msg)

	# Attach the .csv file
	record = MIMEBase('application', 'octet-stream')
	# print(csv)
	record.set_payload(csv)
	encoders.encode_base64(record)
	record.add_header('Content-Disposition', 'attachment', filename='medicare.csv')	
	message.attach(record)

	# Return the message
	raw = base64.urlsafe_b64encode(message.as_bytes())
	raw = raw.decode()
	return {'raw': raw}

# b) Send the message
def send_message(service, user_id, message):
	try:
		message = service.users().messages(). \
		send(userId=user_id, body=message).execute()
		print('Message Id: %s' % message['id'])
		return message
	except Exception as e:
		print('An error occurred: %s' % e)
		return None


# Part 1: Fetch the data.

# Get the webpage, store it in a Response object and assign the text
# About: https://requests.readthedocs.io/en/master/api/#requests.Response

# This URL contains the .csv download of
# 'https://catalog.data.gov/dataset/' \
#	'share-of-medicaid-enrollees-in-managed-care'
# used to send to the destination e-mail.
csvFileURL = 'https://data.medicaid.gov/api/' \
	'views/u72p-j37s/rows.csv?accessType=DOWNLOAD'
csvFileRequest = requests.get(csvFileURL)
csvFile = csvFileRequest.content

# COMMENTED OUT: The below is necessary if file is not .csv.
# Now we add the important SEP metadata command.
# This tells Excel to use a delimiter.
#decoded = csvFile.decode('utf-8')
#decoded = 'SEP=,\n' + decoded
#csvFile = decoded.encode('utf-8')

# This URL contains the .json download of
# 'https://catalog.data.gov/dataset/' \
#	'share-of-medicaid-enrollees-in-managed-care'
# used to compare files.
jsonOfFile = 'https://data.medicaid.gov/api/views/u72p-j37s/' \
	'rows.json?accessType=DOWNLOAD'

r = requests.get(jsonOfFile)
firstJSON = r.text

# Part 2: Use the Google API to send an e-mail with the updated metadata

# Find out whether the file was changed or not.
# Originally it checked for the last updated date,
# but it then occurred to me that there could be 
# multiple changes made in one day.
# Old code: print(BeautifulSoup(URL, 'html.parser). \
# find_all('td')[0].get_text())
# returns the last updated date based on the current site's layout.

# Now, the new code compares the .json version of the files every minute.

# This will run the code every 60 seconds (except for the first iteration)
# instead of time.sleep(60) which only runs the loop every 60 seconds.
# In the latter case, the code may take some time "x" to finish executing
# so your total time would have been 60 + x seconds (bad).
count = 0
while True:
	r = requests.get(jsonOfFile)
	secondJSON = r.text

	# If the site was updated or the script just began, send the message.
	if firstJSON != secondJSON or count == 0:

		# Create the message
		sender = 'jcalderon41@gmail.com'
		to = 'queenmypawn@gmail.com'
		subject = 'The Medicare metadata has been updated'
		message = create_message(sender, to, subject, csvFile)

		# Send the message using the Google API
		creds = None
		# The file token.pickle stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		if os.path.exists('token.pickle'):
			with open('token.pickle', 'rb') as token:
				creds = pickle.load(token)
		# If there are no (valid) credentials available, let the user log in.
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', SCOPES)
				creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open('token.pickle', 'wb') as token:
				pickle.dump(creds, token)

		service = build('gmail', 'v1', credentials=creds)
		send_message(service, sender, message)

		# Update the variable
		firstJSON = secondJSON

		print('Message sent')
	# Otherwise, do nothing.
	count += 1
	print('Loop ' + str(count) + ' complete')

	# Sleep 60 seconds.
	# Or, more accurately, between 0 and 60 seconds
	# Plus the time it took for the above process to run
	# If it takes longer than 60 seconds (which it shouldn't),
	# It will take an extra minute.
	time.sleep(60 - time.time() % 60)