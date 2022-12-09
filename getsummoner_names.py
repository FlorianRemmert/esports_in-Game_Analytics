import pandas as pd
import requests
import time

region = "euw1"
api_key = 'RGAPI-11e37334-312f-47c5-9d72-25889a7cb65e'

division = ["challengerleagues", "grandmasterleagues", "masterleagues"]
for div in division:
    url = "https://euw1.api.riotgames.com/lol/league/v4/{}/by-queue/RANKED_SOLO_5x5?api_key={}".format(
        div, api_key)
    summoner_list = requests.get(url).json()
    entries = summoner_list.get("entries")
    df = pd.DataFrame(entries)
    df.drop(df.columns.difference(['summonerName']), axis=1, inplace=True)
    if div == "challengerleagues":
        df["tier"] = "CHALLENGER"
    elif div == "grandmasterleagues":
        df["tier"] = "GRANDMASTER"
    else:
        df["tier"] = "MASTER"
    df["rank"] = ""

    df = df.iloc[:, [1, 2, 0]]
    #mode
    df.to_csv('summoner_names.csv', mode='a', header=False, index=False)
    time.sleep(1.5)



def get_summoner_names(division, tier, page):
    url = "https://euw1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{}/{}?page={}&api_key={}".format(
        division, tier, page, api_key)
    summoner_list = requests.get(url).json()
    df = pd.DataFrame(summoner_list)
    df.drop(df.columns.difference(['summonerName','rank', "tier"]), axis=1, inplace=True)
    #mode
    df.to_csv('summoner_names.csv', mode='a', header=False, index=False)


for page in range(1,5):
    # for division in ["CHALLENGER", "grandmaster", "master", "diamond", "platin", "gold", "silver", "bronze", "iron"]:
    for division in ["DIAMOND", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]:
        for tier in ["I", "II", "III", "IV"]:
            get_summoner_names(division,tier,page)
            time.sleep(1.5)





