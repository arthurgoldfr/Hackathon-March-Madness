#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:01:36 2020

@author: arthurgold
"""

import pandas as pd
import numpy as np



################### IMPORT DATA ###################

df = pd.read_csv('../Data/MDataFiles_Stage1/MRegularSeasonDetailedResults.csv')
df = df.loc[(df['Season'] >= 2003) & (df['Season'] <= 2019)]

################### Somme des matchs ###################

df1 = df.groupby(["Season","WTeamID"]).count()["DayNum"]
df1=df1.reset_index()
df1.columns = ["Season","TeamID","victoires"]
df1= df1.reindex(columns = ["Season","victoires","TeamID"] )
df1.to_csv("Victoires.csv")
df2 = df.groupby(["Season","LTeamID"]).count()["DayNum"]
df2=df2.reset_index()   

    
df2.columns = ["Season","TeamID","defaites"]
df2 = df2.reindex(columns = ["Season","defaites","TeamID"] )
df2.to_csv("Défaites.csv")
df_tot = df1.merge(df2,left_on=["Season","TeamID"],right_on=["Season","TeamID"])
df_tot.to_csv("Victoires_Défaites.csv")
df_tot["sum_matchs"] = df_tot["victoires"]+ df_tot["defaites"]

################### Somme et pourcentage des derniers matchs avant le MNCAA ###################


dfLast = df.groupby(["Season","WTeamID","DayNum"]).filter(lambda x : x['DayNum']>120).groupby(["WTeamID","Season"]).count()["DayNum"]
dfLast =dfLast.reset_index()
dfLast.columns = ["TeamID","Season","last_victories"]
dfLast =  dfLast.reindex(columns = ["Season","last_victories","TeamID"] )
#dfLast.to_csv("last_victories.csv") 

dfLast2 = df.groupby(["Season","LTeamID","DayNum"]).filter(lambda x : x['DayNum']>120).groupby(["LTeamID","Season"]).count()["DayNum"]
dfLast2 =dfLast2.reset_index()
dfLast2.columns = ["TeamID","Season","last_defeats"]
dfLast2 =  dfLast2.reindex(columns = ["Season","last_defeats","TeamID"] )
#dfLast2.to_csv("last_defeats.csv")

dfLast = dfLast.merge(dfLast2)
dfLast["pourcentage_victoires_last"] = dfLast["last_victories"]/(dfLast["last_victories"]+ dfLast["last_defeats"])
dfLast["sum_last"] = dfLast["last_victories"]+ dfLast["last_defeats"]
df_tot2 = df_tot.merge(dfLast,left_on=["Season","TeamID"],right_on=["Season","TeamID"],how="inner")
df_tot2 = df_tot2.drop(["victoires","defaites","last_victories","last_defeats"],axis=1)
#df_tot2.to_csv("features_match.csv")