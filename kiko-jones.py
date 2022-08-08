import requests
from flask import Flask
from datetime import datetime
import os
import time

app = Flask(__name__)

class Game:
	def __init__(self, match):
		self.matchID = match[0]
		self.timestamp = match[1]
		self.date = datetime.fromtimestamp(match[1]/1000).strftime('%a %b %d')
		self.duration = match[2]
		self.minutes = round(match[2]/60)
		self.win = match[3]
		self.champ = match[4]
		self.kills = match[5]
		self.deaths = match[6]
		self.assists = match[7]

	def toHtml(self):
		r = ""
		if self.win == "TRUE":
			r = r + "<font color=\"cornflowerblue\">WIN"
		else:
			r = r + "<font color=\"coral\">LOSS"
		r = r + "</font>  " + self.champ + "</br>"
		r = r + self.date + " (" + self.minutes + ")</br>"
		r = r + "  " + str(self.kills) + "/" + str(self.deaths)+"/"+str(self.assists)+"</br>"
		r = r + "</br>"
		return r

def addHeader(r):
	r = r + "<html><body style=\"background-color:black;color:white;font-family:Helvetica, sans-serif\"><h3>KIKO JONES</h3>"
	return r

def addFooter(r):
	r = r + "</body></html>"
	return r

@app.route('/')
def match_history():
	GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
	SHEET_ID = os.environ['SHEET_ID']

	headers = {'Authorization': 'Bearer '+GOOGLE_API_KEY}
	spreadsheet = requests.get("https://sheets.googleapis.com/v4/spreadsheets/"+SHEET_ID+"/values/A1:H20?key="+GOOGLE_API_KEY)
	data = spreadsheet.json()
	matches = data["values"]
	r = ""
	r = addHeader(r)
	for match in matches:
		g = Game(match)
		r = r + g.toHtml()
	r = addFooter(r)
	return r
