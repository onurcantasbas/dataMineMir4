# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 21:25:04 2022

@author: Begy
"""

import requests 
import json
import pandas as pd
import numpy as np
import datetime


req_url_part1 = "https://webapi.mir4global.com/nft/lists?listType=recent&page="
req_url_part2 = "&class=0&levMin=0&levMax=0&powerMin=0&powerMax=0&priceMin=0&priceMax=0&languageCode=en"

data = {'seq': [],
        'transportID': [],
        'nftID': [],
        'price':[],
        'powerScore':[],
        'level':[],
        'class':[],
        'time':[],
        'timeUnix':[]
        }



for x in range(1,2000):
    
    
    final_url = req_url_part1+str(x)+req_url_part2
    krjson = final_url
    krcek = requests.get(krjson)
    jsonreq = json.loads(krcek.text)
    
    for y in range(10):
    
        data["seq"].append(jsonreq.get("data")["lists"][y]["info"]["seq"])
        data["transportID"].append(jsonreq.get("data")["lists"][y]["info"]["transportID"])
        data["nftID"].append(jsonreq.get("data")["lists"][y]["info"]["nftID"])
        data["price"].append(jsonreq.get("data")["lists"][y]["info"]["price"])
        data["powerScore"].append(jsonreq.get("data")["lists"][y]["info"]["powerScore"])
        data["level"].append(jsonreq.get("data")["lists"][y]["info"]["lv"])
        data["class"].append(jsonreq.get("data")["lists"][y]["info"]["class"])
        data["time"].append(datetime.datetime.fromtimestamp(jsonreq.get("data")["lists"][y]["info"]["tradeDT"]).strftime('%Y-%m-%d'))
        data["timeUnix"].append(jsonreq.get("data")["lists"][y]["info"]["tradeDT"])
        
        

    

dataF = pd.DataFrame(data) 

dataF.drop(dataF.index[np.where(dataF["transportID"] == 0)], inplace=True)
dataF.drop(dataF.index[np.where(dataF["nftID"] == 0)], inplace=True)
dataF.drop(dataF.index[np.where(dataF["seq"] == 0)], inplace=True)
dataF.drop(dataF.index[np.where(dataF["price"] == 0)], inplace=True)
dataF.drop(dataF.index[np.where(dataF["powerScore"] == 0)], inplace=True)
dataF.drop(dataF.index[np.where(dataF["level"] == 0)], inplace=True)

dataF.dropna(inplace=True)

dataHolder = {
            "data":[]
             }


CharracterStats = {
                    "HP":[],
                    "HP % REGEN":[],
                    "MP":[],
                    "MP % REGEN":[],
                    "PHYS ATK":[],
                    "Spell ATK":[],
                    "PHYS DEF":[],
                    "Spell DEF":[],
                    "Accuracy":[],
                    "EVA":[],
                    "CRIT":[],
                    "CRIT EVA":[],
                    "CRIT ATK DMG Boost":[],
                    "CRIT DMG Reduction":[],
                    "Bash ATK DMG Boost":[],
                    "Bash DMG Reduction":[],
                    "PvP ATK DMG Boost":[],
                    "PvP DMG Reduction":[],
                    "Monster ATK DMG Boost":[],
                    "Boss ATK DMG Boost":[],
                    "Monster DMG Reduction":[],
                    "Boss DMG Reduction":[],
                    "Skill ATK DMG Boost":[],
                    "Skill DMG Reduction % REGEN":[],
                    "All ATK DMG Boost":[],
                    "All DMG Reduction":[],
                    "Stun Success Boost":[],
                    "Stun RES Boost":[],
                    "Debilitation Success Boost ":[],
                    "Debilitation RES Boost":[],
                    "Silence Success Boosty":[],
                    "Silence RES Boost":[],
                    "Hunting EXP Boost":[],
                    "Hunting Copper Gain Boost":[],
                    "Energy Gain Boost":[],
                    "Darksteel Gain Boost":[],
                    "Drop Chance Boost":[],
                    "Lucky Drop Chance Boost":[],
                    "Gathering Boost":[],
                    "Energy Gathering Boost":[],
                    "Mining Boost":[],
                    "Skill Cool Reduction":[],
                    "Knockdown Success Boost":[],
                    "Knockdown RES Boost":[],
                    "HP Potion Effect Boost":[],
                    "MP Potion Effect Boost":[],
                    "Skill HP Recovery Am't Boost":[],
                    "Life":[],
                    "Basic ATK DMG Boost":[],
                    
                }

errorList = []
transportID_req_url_1 = "https://webapi.mir4global.com/nft/character/stats?transportID="
transportID_req_url_2 = "&languageCode=en"

for x in range(len(dataF)):
    
    final_transportID_url = transportID_req_url_1+str((dataF.iloc[x,1]))+transportID_req_url_2
    krjson = final_transportID_url
    krcek = requests.get(krjson)
    dataHolder["data"].append(json.loads(krcek.text))
    
for k in range(len(dataF)):
    i = 0
    if(dataHolder.get("data")[k].get('code') == 200 ):
        for elem in CharracterStats.keys():
                    CharracterStats[elem].append(dataHolder.get("data")[k].get("data")["lists"][i]["statValue"])
                    i = i+1
    else:
        errorList.append(k)
        print("hatalı indeks : ",k)
        

    

dataFinal = pd.DataFrame(CharracterStats)     

dataFinal = dataFinal.applymap(lambda x: str(x.replace('%','')))
dataFinal = dataFinal.applymap(lambda x: str(x.replace(',','')))


dataFinal["nftID"] = dataF["seq"]
dataFinal["price"] = dataF["price"]
dataFinal["powerScore"] = dataF["powerScore"]
dataFinal["level"] = dataF["level"]
dataFinal["class"] = dataF["class"]
dataFinal["time"] =  dataF["time"]
dataFinal["timeUnix"] = dataF["timeUnix"]

# erorList = errorList.reverse()
# for indexes in errorList:
#         dataF.drop(indexes,inplace=True)    

dataFinal.to_excel("yeniKarakterData.xlsx")


# dataFinal["nftID"] = dataF.iloc[0:16172,0]

# dataFinal["price"] = dataF.iloc[0:16172,3]

# dataFinal["powerScore"] = dataF.iloc[0:16172,4]

# dataFinal["level"] = dataF.iloc[0:16172,5]

# dataFinal["class"] = dataF.iloc[0:16172,6]

# dataFinal["page"] = dataF.iloc[0:16172,7]    

    

    
