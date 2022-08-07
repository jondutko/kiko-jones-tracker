import requests
from flask import Flask
from datetime import datetime
import os
import time

app = Flask(__name__)

def match_to_html(match):
	r = ""
	if match[1]:
		r = r + "<font color=\"cornflowerblue\">WIN"
	else:
		r = r + "<font color=\"coral\">LOSS"
	r = r + "</font></br>"
	return r

@app.route('/')
def match_history():
	GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
	SHEET_ID = os.environ['SHEET_ID']

	headers = {'Authorization': 'Bearer '+api_key}
	spreadsheet = requests.get("https://sheets.googleapis.com/v4/spreadsheets/"+SHEET_ID+"/values/A1:F20?key="+GOOGLE_API_KEY)
	data = spreadsheet.json()
	matches = data["values"]
	r = ""
	for match in matches:
		r = r + match_to_html(match)

	return r
