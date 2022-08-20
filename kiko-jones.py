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
		self.runes = []
		self.runes.append(match[15])
		self.runes.append(match[16])
		self.runes.append(match[17])
		self.runes.append(match[18])
		self.runes.append(match[19])
		self.runes.append(match[20])

class ChampTracker:
	def __init__(self, champ):
		self.name = champ
		self.wins = 0
		self.losses = 0
		self.games_played = 0
		self.ratio = 0
	
	def update_with_win(self):
		self.wins = self.wins + 1
		self.games_played = self.games_played + 1
		self.ratio = round(self.wins/self.games_played)
	
	def update_with_loss(self):
		self.losses = self.losses + 1
		self.games_played = self.games_played + 1
		self.ratio = round(self.wins/self.games_played)
		
def analysis(Games):
	tracked_champs = {}
	for game in Games:
		if game.champ in tracked_champs:
			pass
		else:
			tracked_champs[game.champ] = ChampTracker(game.champ)
		if game.win == "TRUE":
			tracked_champs[game.champ].update_with_win
		else:
			tracked_champs[game.champ].update_with_loss

@app.route('/')
def match_history():
	GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
	SHEET_ID = os.environ['SHEET_ID']

	headers = {'Authorization': 'Bearer '+GOOGLE_API_KEY}
	spreadsheet = requests.get("https://sheets.googleapis.com/v4/spreadsheets/"+SHEET_ID+"/values/A1:V30?key="+GOOGLE_API_KEY)
	data = spreadsheet.json()
	matches = data["values"]
	Games = []
	for match in matches:
		g = Game(match)
		Games.append(g)
	Analysis = analysis(Games)
	return render_template('index.html', games=Games, analysis=Analysis)
