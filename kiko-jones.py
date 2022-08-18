import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
import os
import time

app = Flask(__name__)
Bootstrap(app)

class Game:
	def __init__(self, match):
		self.matchID = match[0]
		self.timestamp = match[1]
		self.date = datetime.fromtimestamp(int(match[1])/1000).strftime('%a %b %d')
		self.duration = match[2]
		self.minutes = round(int(match[2])/60)
		self.seconds = int(match[2]) % 60
		self.win = match[3]
		self.champ = match[4]
		self.kills = match[5]
		self.deaths = match[6]
		self.assists = match[7]
		self.items = []
		self.items.append(match[8])
		self.items.append(match[9])
		self.items.append(match[10])
		self.items.append(match[11])
		self.items.append(match[12])
		self.items.append(match[13])
		self.items.append(match[14])
	

@app.route('/')
def match_history():
	GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
	SHEET_ID = os.environ['SHEET_ID']

	headers = {'Authorization': 'Bearer '+GOOGLE_API_KEY}
	spreadsheet = requests.get("https://sheets.googleapis.com/v4/spreadsheets/"+SHEET_ID+"/values/A1:P20?key="+GOOGLE_API_KEY)
	data = spreadsheet.json()
	matches = data["values"]
	Games = []
	for match in matches:
		g = Game(match)
		Games.append(g)
	return render_template('index.html', games=Games)
