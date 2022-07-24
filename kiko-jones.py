import requests
from flask import Flask
import os

app = Flask(__name__)

class Game:
	def __init__(self):
		self.win = True
		self.minutes = 0
		self.championName = "None"
		self.gpm = 0
		self.kda = 0
		self.kills = 0
		self.deaths = 0
		self.assists = 0

	def toString(self):
		r = ""
		if self.win:
			r = "WIN"
		else:
			r = "LOSS"
		r = r + "\t" + self.championName + "\t" + str(self.minutes) + "m \n"
		r = r + "\t" + str(self.gpm) + "gold per minute \n"
		r = r + "\t" + str(self.kills) + "/" + str(self.deaths)+"/"+str(self.assists)+"\t("+str(self.kda)+" k.d.a.)"

Games = []

@app.route('/')
def match_history():
	RIOT_KEY = os.environ['RIOT_API_KEY']
	summoner_name = "KIKO JONES"
	summoner_name_html_safe = "KIKO%20JONES"

	r = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summoner_name_html_safe+"?api_key="+RIOT_KEY)

	rjson = r.json()

	puuid = rjson["puuid"]

	r = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=20&api_key="+RIOT_KEY)

	matches = r.json()

	i = 0
	total_kda = 0
	total_gpm = 0
	total_win = 0

	for match in matches:
		game = Game()
		print ("---")

		r = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+match+"?api_key="+RIOT_KEY)

		rjson = r.json()

		game.minutes = round(rjson["info"]["gameDuration"]/60)

		for participant in rjson["info"]["participants"]:
			if (participant["summonerName"] == summoner_name):
				game.win = participant["win"]
				game.championName = participant["championName"]
				game.kills = participant["kills"]
				game.assists = participant["assists"]
				game.deaths = participant["deaths"]
				kda = (participant["kills"]+participant["assists"]/participant["deaths"])
				game.kda = round(kda, 1)

				i = i + 1
				total_gpm = total_gpm + participant["challenges"]["goldPerMinute"]
				total_kda = total_kda + kda

		Games.append(game)

	wr = round(total_win/i, 2) * 100
	avg_kda = round(total_kda/i, 2)
	avg_gpm = round(total_gpm/i, 2)

	print (str(total_win)+" wins\t"+str(wr)+"%")
	print ("avg kda: "+str(avg_kda))
	print ("avg gpm: "+str(avg_gpm))

	r = ""
	for game in Games:
		r = r + game.toString() + "\n"

	return r
