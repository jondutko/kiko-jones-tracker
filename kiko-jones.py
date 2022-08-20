import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
import os
import time

app = Flask(__name__)
Bootstrap(app)

class Rune:
	def __init__(self, id, runesreforged):
		self.id = id
		self.json = ""
		for category in runesreforged:
			#print (category)
			for slot in category["slots"]:
				for rune in slot["runes"]:
					#print (rune)
					if rune["id"] == self.id:
						print (rune)
						self.json = rune
		self.name = self.json["name"]
		self.icon = self.json["icon"]
		

class Game:
	def __init__(self, match, runesreforged):
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
		self.runes.append(Rune(match[15], runesreforged))
		self.runes.append(Rune(match[16], runesreforged))
		self.runes.append(Rune(match[17], runesreforged))
		self.runes.append(Rune(match[18], runesreforged))
		self.runes.append(Rune(match[19], runesreforged))
		self.runes.append(Rune(match[20], runesreforged))
		print (self.runes[0].name+" "+self.runes[0].icon)
	

@app.route('/')
def match_history():
	GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
	SHEET_ID = os.environ['SHEET_ID']

	headers = {'Authorization': 'Bearer '+GOOGLE_API_KEY}
	spreadsheet = requests.get("https://sheets.googleapis.com/v4/spreadsheets/"+SHEET_ID+"/values/A1:V20?key="+GOOGLE_API_KEY)
	data = spreadsheet.json()
	runesreforged_response = requests.get("http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/runesReforged.json")
	runesreforged = runesreforged_response.json()
	matches = data["values"]
	Games = []
	for match in matches:
		g = Game(match, runesreforged)
		Games.append(g)
	return render_template('index.html', games=Games)
