import requests
from flask import Flask
from datetime import datetime
import os
import time

app = Flask(__name__)

@app.route('/')
def match_history():
	#GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
	GOOGLE_API_KEY = "AIzaSyCnX0UZyag_7Kfx0mLyblr7WnF_SqWluTE"
	#SHEET_ID = os.environ['SHEET_ID']
	SHEET_ID = "14GD1vi82SRnKD5aVw-q4PcQF3t895HPd2OjS2krpPsc"

	headers = {'Authorization': 'Bearer '+api_key}
	spreadsheet = requests.get("https://sheets.googleapis.com/v4/spreadsheets/"+SHEET_ID+"/values/A1:F20?key="+GOOGLE_API_KEY)
	data = spreadsheet.json()
	matches = data["values"]
	for match in matches:
		for item in match:
			print (item)

	return "Check the Heroku logs."
