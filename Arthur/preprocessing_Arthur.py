#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:01:36 2020

@author: arthurgold
"""

import pandas as pd
import numpy as np

df = []
MNCAA = pd.read_csv('../Data/MDataFiles_Stage1/MNCAATourneyDetailedResults.csv',",")
MNCAA["table"]="MNCAA"
Regular = pd.read_csv('../Data/MDataFiles_Stage1/MRegularSeasonDetailedResults.csv')
Regular["table"]="Regular"
df.append(MNCAA)
df.append(Regular)
df = pd.concat(df)
df = df.loc[(df['Season'] >= 2003) & (df['Season'] <= 2014)]
df = df.loc[(df['Season'] >= 2003) & (df['Season'] <= 2014)]
df.head()
df["WTeamID"] = df["WTeamID"].astype(str)
df["LTeamID"] =  df["LTeamID"].astype(str)
df["Season"] =  df["Season"].astype(str)
df["paire"] = df["Season"]+"_"+df["WTeamID"] +"_"+ df["LTeamID"]
def tri(x):
    if int(x[5:9])<int(x[10:]):
        return x
    else :
        return x[:4]+"_"+ x[10:]+"_"+x[5:9]
    
def premier(x):
    return x[5:9]

df["paire"]=df["paire"].apply(tri)
df["ID_1"] = df["paire"].apply(lambda x:x[5:9])
df["ID_2"] = df["paire"].apply(lambda x:x[10:])

df["W/L"]= (df["WTeamID"]==df["paire"].apply(premier))
df["W/L"]= df["W/L"].replace({True: 1, False: -1})
def deuxieme(x):
    return x[10:]
df["W/L_2"]= (df["WTeamID"]==df["paire"].apply(deuxieme))
df["W/L_2"]= df["W/L_2"].replace({True: 1, False: -1})
df2 = df.groupby(["ID_1","table","Season"])["W/L"].sum()
df3 = df.groupby(["ID_2","table","Season"])["W/L_2"].sum()
df2 = df2.reset_index()
df3 = df3.reset_index()
new_df = pd.DataFrame()
new_df["paire"] = df["paire"]
new_df["Season"] = df["Season"]
new_df["ID_1"] = df["ID_1"]
new_df["ID_2"] = df["ID_2"]

df2 = df2.loc[df2["table"]=="Regular"]

df3 = df3.loc[df3["table"]=="Regular"]

new_df["WTeamID"] = df["WTeamID"]
test = new_df.merge(df2)
new_df = test.merge(df3)

#new_df.to_csv("Winner-Looser.csv")

df_before = df.groupby(["ID_1","ID_2","Season","table","DayNum"]).filter(lambda x: x['DayNum'] >110)
df_before1 = df_before.loc[df_before["table"]=="Regular"].groupby(["ID_1","Season"]).sum()["W/L"]
df_before2 = df_before.loc[df_before["table"]=="Regular"].groupby(["ID_2","Season"]).sum()["W/L_2"]
df_before1 = df_before1.reset_index()
df_before2 = df_before2.reset_index()
df_before1.rename({"W/L":"lastW_1"},axis = 1, inplace=True)
df_before2.rename({"W/L_2":"lastW_2"},axis = 1, inplace=True)

new_df = new_df.merge(df_before1)
new_df = new_df.merge(df_before2,left_on=["ID_2","Season"],right_on=["ID_2","Season"])

#new_df.to_csv("Winner-Looser-lastW.csv")

df_conf = df.loc[df["table"]=="Regular"].groupby(["ID_1","ID_2","Season"]).sum()["W/L"]
df_conf = df_conf.reset_index()
df_conf.rename({"W/L":"confrontation"},axis = 1, inplace=True)
new_df = new_df.merge(df_conf)

new_df.to_csv("Winner-Looser-lastW-Confrontation.csv")





#new_df["WIN_ID1","WIN_ID2"]=



