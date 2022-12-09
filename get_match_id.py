import pandas as pd
import time
from riotwatcher import LolWatcher
import requests


api_key = 'RGAPI-0da4c525-a2b9-488c-ad27-43878dd718cb'
lol_watcher = LolWatcher(api_key)

region = "euw1"


"""timeline = https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_6080418928/timeline
timeline = timeline + "?api_key=" + api_key
resp = requests.get(timeline)
match_timeline = resp.json()


#Versucht die List der Match data besser zu lesen können /umwandeln
#create new df
df_sum = pd.DataFrame({'col': match_timeline})

#Rows and Columns getauscht
df_sum = df_sum.T

player_url = https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5
player_url = player_url + "?api_key=" + api_key

resp = requests.get(player_url)

match_data = resp.json()
match_data = match_data.get("entries")
df_sum = pd.DataFrame(match_data)
#df_sum = df_sum.loc[:, ["summonerName", "leaguePoints"]]

#defined as set to deny to get the same match_id twice
all_match_id = set()

"""

df_summoner_names = pd.read_csv("summoner_names.csv")

df_with_puuid = df_summoner_names
df_with_puuid["PUUID"] = None
df_with_puuid["matchID"] = None
for i, summoner in enumerate(df_summoner_names.summonerName):
    # Um an die PuuID der Spieler zu kommen
    if i > 1000:
        url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summoner+"?api_key="+api_key
        player = requests.get(url).json()
        #player = lol_watcher.summoner.by_name(region, summoner)

        try:
            puuid = player['puuid']
            df_with_puuid.at[i, "PUUID"] = puuid
            url = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?api_key=" + api_key
            match_id = requests.get(url).json()
            df_with_puuid.at[i, "matchID"] = match_id[0]
            time.sleep(2.5)
        except:
            print(f"Player {summoner} not found")

        if i%5 == 0:
            df_with_puuid.to_csv('summoner_names_matchID'+str(i)+'.csv')
        # Spiel ID der letzten 10 Spiele von dem Spieler mithilfe der PUUID erzeugt
        # https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/pM11ghFXQwxEunYazIOD4SP4vFhuN8pwdoLVlKkkHcGTMNtbZQd2VuE1z1lI3ZwVH5LWyqlfRYxfvA/ids?start=0&count=10
        # matches = lol_watcher.match.matchlist_by_puuid(region, player['puuid'])
        # all_match_id.update(matches)
df_with_puuid.to_csv('summoner_names_matchID_final.csv')