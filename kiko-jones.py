import requests
from flask import Flask
from datetime import datetime
import os
import time

app = Flask(__name__)

class Game:
	def __init__(self):
		self.win = True
		self.date = ""
		self.minutes = 0
		self.championName = "None"
		self.gpm = 0
		self.kda = 0
		self.kills = 0
		self.deaths = 0
		self.assists = 0
		self.deluxe = False

	def toHTML(self, avg_kda, avg_gpm):
		r = ""
		if self.deluxe:
			r = "<font size=\"2\">&#x2B50;  </font>"
		if self.win:
			r = r + "<font color=\"blue\">WIN"
		else:
			r = r + "<font color=\"red\">LOSS"
		r = r + "</font>  " + self.championName + "  " + str(self.minutes) + "m -- "+self.date+"</br>"
		r = r + "  " + str(self.gpm) + "  gpm"
		if (self.gpm > avg_gpm):
			r = r + "  <font color=\"blue\">&uarr;"
		else:
			r = r + "  <font color=\"red\">&darr;" 
		r = r + str(round(self.gpm - avg_gpm,1))+ "</font></br>"
		r = r + "  " + str(self.kills) + "/" + str(self.deaths)+"/"+str(self.assists)+"  ("+str(self.kda)+" kda)"
		if (self.kda > avg_kda):
			r = r + "  <font color=\"blue\">&uarr;"
		else:
			r = r + "  <font color=\"red\">&darr;"
		r = r + str(round(self.kda - avg_kda,1)) + "</font></br></br>"
		return r

	
Games = []

RIOT_KEY = os.environ['RIOT_API_KEY']
summoner_name = "KIKO JONES"
summoner_name_html_safe = "KIKO%20JONES"

r = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summoner_name_html_safe+"?api_key="+RIOT_KEY)

rjson = r.json()

puuid = rjson["puuid"]
summid = rjson["id"]

def process_matches():
	g  = []
	r = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=30&api_key="+RIOT_KEY)
	matches = r.json()

	i = 0
	total_kda = 0
	total_gpm = 0
	total_win = 0

	for match in matches:
		game = Game()
		print ("Processing "+match+" match id")

		r = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+match+"?api_key="+RIOT_KEY)

		rjson = r.json()

		game.minutes = round(rjson["info"]["gameDuration"]/60)
		unix_timestamp = rjson["info"]["gameEndTimestamp"]
		unix_timestamp = unix_timestamp/1000
		game.date = datetime.fromtimestamp(unix_timestamp).strftime('%a %b %d')

		for participant in rjson["info"]["participants"]:
			if (participant["summonerName"] == summoner_name):
				game.win = participant["win"]
				game.championName = participant["championName"]
				game.kills = participant["kills"]
				game.assists = participant["assists"]
				game.deaths = participant["deaths"]
				kda = (participant["kills"]+participant["assists"])/max(participant["deaths"], 1)
				game.kda = round(kda, 1)
				game.gpm = round(participant["challenges"]["goldPerMinute"],1)
				i = i + 1
				total_gpm = total_gpm + participant["challenges"]["goldPerMinute"]
				total_kda = total_kda + kda
				if (participant["challenges"]["takedownOnFirstTurret"] == 1):
					game.deluxe = True
				if game.win:
					total_win = total_win + 1

		g.append(game)

	wr = round((total_win/i) * 100)
	avg_kda = round(total_kda/i, 1)
	avg_gpm = round(total_gpm/i, 1)

	print (str(total_win)+" wins\t"+str(wr)+"%")
	print ("avg kda: "+str(avg_kda))
	print ("avg gpm: "+str(avg_gpm))

	return g, avg_kda, avg_gpm, i, wr

while True:
	print ("Refreshing match history")
	avg_kda = 0
	avg_gpm = 0
	i = 0
	wr = 0
	Games, avg_kda, avg_gpm, i, wr = process_matches()
	time.sleep(600)

@app.route('/refresh')
def refresh():
	Games = process_matches()
	return "Games set refreshed"

@app.route('/')
def match_history():
	
	r = requests.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+summid+"?api_key="+RIOT_KEY)
	rjson = r.json()
	elo = ""	
	for queue in rjson:
		print (queue)
		if(queue["queueType"] == 'RANKED_SOLO_5x5'):
			elo = elo + queue["tier"] + " " + queue["rank"] + " " +str(queue["leaguePoints"]) + "LP</br>"
			 
	r = "<h2>KIKO JONES<h2>"
	r = r + "<h3>Match History</h3>"
	r = r + elo + "<br>"
	r = r + str(avg_kda) + " avg kda  | "+str(avg_gpm)+" avg gpm  | "+str(i)+" games  | "+str(wr)+"% wins</br></br>"
	for game in Games:
		r = r + game.toHTML(avg_kda, avg_gpm) + "\n"

	return r
