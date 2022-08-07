import requests
from flask import Flask
from datetime import datetime
import os
import time

app = Flask(__name__)

@app.route('/')
def match_history():
	GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
	SHEET_ID = os.environ['SHEET_ID']

	headers = {'Authorization': 'Bearer '+GOOGLE_API_KEY}
	spreadsheet = requests.get("https://sheets.googleapis.com/v4/spreadsheets/"+SHEET_ID+"/values/A1:F20?key="+GOOGLE_API_KEY)
	data = spreadsheet.json()
	matches = data["values"]
	for match in matches:
		for item in match:
			print (item)

	return "Check the Heroku logs."
