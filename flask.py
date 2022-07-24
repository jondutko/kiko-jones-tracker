import requests

import os

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
	print ("---")

	r = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+match+"?api_key="+RIOT_KEY)

	rjson = r.json()

	minutes = round(rjson["info"]["gameDuration"]/60)

	for participant in rjson["info"]["participants"]:
		if (participant["summonerName"] == summoner_name):
			if(participant["win"]):
				header = "WIN"
				total_win = total_win + 1
			else:
				header = "LOSS"

			header = header + "\t" + participant["championName"] + "\t" + str(minutes)+"m"
			print (header)
			print ("\t"+str(round(participant["challenges"]["goldPerMinute"]))+"gpm")
			kda = (participant["kills"]+participant["assists"]/participant["deaths"])
			kda = round(kda, 1)
			print ("\t"+str(participant["kills"])+"\t"+str(participant["deaths"])+"\t"+str(participant["assists"])+"\t"+str(kda)+" kda")

			i = i + 1
			total_gpm = total_gpm + participant["challenges"]["goldPerMinute"]
			total_kda = total_kda + kda

print ("---")

wr = round(total_win/i, 2) * 100
avg_kda = round(total_kda/i, 2)
avg_gpm = round(total_gpm/i, 2)

print (str(total_win)+" wins\t"+str(wr)+"%")
print ("avg kda: "+str(avg_kda))
print ("avg gpm: "+str(avg_gpm))