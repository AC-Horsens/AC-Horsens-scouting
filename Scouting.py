import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

st.set_page_config(layout='wide')

@st.cache_data(experimental_allow_widgets=True)
def ITA_Serie_B_2023_2024():
    try:
        df_pv = pd.read_csv(r'ITA_Serie_B_2023_2024/pv_all ITA_Serie_B_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'ITA_Serie_B_2023_2024/xA_all ITA_Serie_B_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'ITA_Serie_B_2023_2024/xA_all ITA_Serie_B_2023_2024.csv')
    df_matchstats = pd.read_csv(r'ITA_Serie_B_2023_2024/matchstats_all ITA_Serie_B_2023_2024.csv')
    df_xg = pd.read_csv(r'ITA_Serie_B_2023_2024/xg_all ITA_Serie_B_2023_2024.csv')
    squads = pd.read_csv(r'ITA_Serie_B_2023_2024/squads ITA_Serie_B_2023_2024.csv')   
    
    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def ITA_Serie_B_2024_2025():
    try:
        df_pv = pd.read_csv(r'ITA_Serie_B_2024_2025/pv_all ITA_Serie_B_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'ITA_Serie_B_2024_2025/xA_all ITA_Serie_B_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'ITA_Serie_B_2024_2025/xA_all ITA_Serie_B_2023_2024.csv')
    df_matchstats = pd.read_csv(r'ITA_Serie_B_2024_2025/matchstats_all ITA_Serie_B_2023_2024.csv')
    df_xg = pd.read_csv(r'ITA_Serie_B_2024_2025/xg_all ITA_Serie_B_2023_2024.csv')
    squads = pd.read_csv(r'ITA_Serie_B_2024_2025/squads ITA_Serie_B_2023_2024.csv')   
    
    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def BEL_First_Division_A_2023_2024():
    try:
        df_pv = pd.read_csv(r'BEL_First_Division_A_2023_2024/pv_all BEL_First_Division_A_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'BEL_First_Division_A_2023_2024/xA_all BEL_First_Division_A_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'BEL_First_Division_A_2023_2024/xA_all BEL_First_Division_A_2023_2024.csv')
    df_matchstats = pd.read_csv(r'BEL_First_Division_A_2023_2024/matchstats_all BEL_First_Division_A_2023_2024.csv')
    df_xg = pd.read_csv(r'BEL_First_Division_A_2023_2024/xg_all BEL_First_Division_A_2023_2024.csv')
    squads = pd.read_csv(r'BEL_First_Division_A_2023_2024/squads BEL_First_Division_A_2023_2024.csv')   
    
    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def BEL_First_Division_A_2024_2025():
    try:
        df_pv = pd.read_csv(r'BEL_First_Division_A_2024_2025/pv_all BEL_First_Division_A_2024_2025.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'BEL_First_Division_A_2023_2024/xA_all BEL_First_Division_A_2024_2025.csv')
    df_possession_xa = pd.read_csv(r'BEL_First_Division_A_2023_2024/xA_all BEL_First_Division_A_2024_2025.csv')
    df_matchstats = pd.read_csv(r'BEL_First_Division_A_2023_2024/matchstats_all BEL_First_Division_A_2024_2025.csv')
    df_xg = pd.read_csv(r'BEL_First_Division_A_2023_2024/xg_all BEL_First_Division_A_2024_2025.csv')
    squads = pd.read_csv(r'BEL_First_Division_A_2023_2024/squads BEL_First_Division_A_2024_2025.csv')   
    
    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def POL_Ekstraklasa_2023_2024():
    try:
        df_pv = pd.read_csv(r'POL_Ekstraklasa_2023_2024/pv_all POL_Ekstraklasa_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'POL_Ekstraklasa_2023_2024/xA_all POL_Ekstraklasa_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'POL_Ekstraklasa_2023_2024/xA_all POL_Ekstraklasa_2023_2024.csv')
    df_matchstats = pd.read_csv(r'POL_Ekstraklasa_2023_2024/matchstats_all POL_Ekstraklasa_2023_2024.csv')
    df_xg = pd.read_csv(r'POL_Ekstraklasa_2023_2024/xg_all POL_Ekstraklasa_2023_2024.csv')
    squads = pd.read_csv(r'POL_Ekstraklasa_2023_2024/squads POL_Ekstraklasa_2023_2024.csv')   
    
    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def SWE_Allsvenskan_2024():
    try:
        df_pv = pd.read_csv(r'SWE_Allsvenskan_2024/pv_all SWE_Allsvenskan_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'SWE_Allsvenskan_2024/xA_all SWE_Allsvenskan_2024.csv')
    df_possession_xa = pd.read_csv(r'SWE_Allsvenskan_2024/xA_all SWE_Allsvenskan_2024.csv')
    df_matchstats = pd.read_csv(r'SWE_Allsvenskan_2024/matchstats_all SWE_Allsvenskan_2024.csv')
    df_xg = pd.read_csv(r'SWE_Allsvenskan_2024/xg_all SWE_Allsvenskan_2024.csv')
    squads = pd.read_csv(r'SWE_Allsvenskan_2024/squads SWE_Allsvenskan_2024.csv')   
    
    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def ROU_Liga_I_2023_2024():
    try:
        df_pv = pd.read_csv(r'ROU_Liga_I_2023_2024/pv_all ROU_Liga_I_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'ROU_Liga_I_2023_2024/xA_all ROU_Liga_I_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'ROU_Liga_I_2023_2024/xA_all ROU_Liga_I_2023_2024.csv')
    df_matchstats = pd.read_csv(r'ROU_Liga_I_2023_2024/matchstats_all ROU_Liga_I_2023_2024.csv')
    df_xg = pd.read_csv(r'ROU_Liga_I_2023_2024/xg_all ROU_Liga_I_2023_2024.csv')
    squads = pd.read_csv(r'ROU_Liga_I_2023_2024/squads ROU_Liga_I_2023_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def Ligue_2_23_24():  
    try:
        df_pv = pd.read_csv(r'FRA_Ligue_2_2023_2024/pv_all FRA_Ligue_2_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'FRA_Ligue_2_2023_2024/xA_all FRA_Ligue_2_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'FRA_Ligue_2_2023_2024/xA_all FRA_Ligue_2_2023_2024.csv')
    df_matchstats = pd.read_csv(r'FRA_Ligue_2_2023_2024/matchstats_all FRA_Ligue_2_2023_2024.csv')
    df_xg = pd.read_csv(r'FRA_Ligue_2_2023_2024/xg_all FRA_Ligue_2_2023_2024.csv')
    squads = pd.read_csv(r'FRA_Ligue_2_2023_2024/squads FRA_Ligue_2_2023_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def Czech_liga_23_24():    
    try:
        df_pv = pd.read_csv(r'CZE_Czech_Liga_2023_2024/pv_all CZE_Czech_Liga_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'CZE_Czech_Liga_2023_2024/xA_all CZE_Czech_Liga_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'CZE_Czech_Liga_2023_2024/xA_all CZE_Czech_Liga_2023_2024.csv')
    df_matchstats = pd.read_csv(r'CZE_Czech_Liga_2023_2024/matchstats_all CZE_Czech_Liga_2023_2024.csv')
    df_xg = pd.read_csv(r'CZE_Czech_Liga_2023_2024/xg_all CZE_Czech_Liga_2023_2024.csv')
    squads = pd.read_csv(r'CZE_Czech_Liga_2023_2024/squads CZE_Czech_Liga_2023_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def HRV_HNL_2023_2024_23_24():
    try:
        df_pv = pd.read_csv(r'HRV_HNL_2023_2024/pv_all HRV_HNL_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'HRV_HNL_2023_2024/xA_all HRV_HNL_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'HRV_HNL_2023_2024/xA_all HRV_HNL_2023_2024.csv')
    df_matchstats = pd.read_csv(r'HRV_HNL_2023_2024/matchstats_all HRV_HNL_2023_2024.csv')
    df_xg = pd.read_csv(r'HRV_HNL_2023_2024/xg_all HRV_HNL_2023_2024.csv')
    squads = pd.read_csv(r'HRV_HNL_2023_2024/squads HRV_HNL_2023_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def DEU_3_Liga_2023_2024():
    try:
        df_pv = pd.read_csv(r'DEU_3_Liga_2023_2024/pv_all DEU_3_Liga_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'DEU_3_Liga_2023_2024/xA_all DEU_3_Liga_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'DEU_3_Liga_2023_2024/xA_all DEU_3_Liga_2023_2024.csv')
    df_matchstats = pd.read_csv(r'DEU_3_Liga_2023_2024/matchstats_all DEU_3_Liga_2023_2024.csv')
    df_xg = pd.read_csv(r'DEU_3_Liga_2023_2024/xg_all DEU_3_Liga_2023_2024.csv')
    squads = pd.read_csv(r'DEU_3_Liga_2023_2024/squads DEU_3_Liga_2023_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def FIN_Veikkausliiga_2024_23_24():
    try:
        df_pv = pd.read_csv(r'FIN_Veikkausliiga_2024/pv_all FIN_Veikkausliiga_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'FIN_Veikkausliiga_2024/xA_all FIN_Veikkausliiga_2024.csv')
    df_possession_xa = pd.read_csv(r'FIN_Veikkausliiga_2024/xA_all FIN_Veikkausliiga_2024.csv')
    df_matchstats = pd.read_csv(r'FIN_Veikkausliiga_2024/matchstats_all FIN_Veikkausliiga_2024.csv')
    df_xg = pd.read_csv(r'FIN_Veikkausliiga_2024/xg_all FIN_Veikkausliiga_2024.csv')
    squads = pd.read_csv(r'FIN_Veikkausliiga_2024/squads FIN_Veikkausliiga_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def NOR_Eliteserien_2024_23_24():
    try:
        df_pv = pd.read_csv(r'NOR_Eliteserien_2024/pv_all NOR_Eliteserien_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'NOR_Eliteserien_2024/xA_all NOR_Eliteserien_2024.csv')
    df_possession_xa = pd.read_csv(r'NOR_Eliteserien_2024/xA_all NOR_Eliteserien_2024.csv')
    df_matchstats = pd.read_csv(r'NOR_Eliteserien_2024/matchstats_all NOR_Eliteserien_2024.csv')
    df_xg = pd.read_csv(r'NOR_Eliteserien_2024/xg_all NOR_Eliteserien_2024.csv')
    squads = pd.read_csv(r'NOR_Eliteserien_2024/squads NOR_Eliteserien_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def ISL_Úrvalsdeild_2024_23_24():
    try:
        df_pv = pd.read_csv(r'ISL_Úrvalsdeild_2024/pv_all ISL_Úrvalsdeild_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'ISL_Úrvalsdeild_2024/xA_all ISL_Úrvalsdeild_2024.csv')    
    df_possession_xa = pd.read_csv(r'ISL_Úrvalsdeild_2024/xA_all ISL_Úrvalsdeild_2024.csv')
    df_matchstats = pd.read_csv(r'ISL_Úrvalsdeild_2024/matchstats_all ISL_Úrvalsdeild_2024.csv')
    df_xg = pd.read_csv(r'ISL_Úrvalsdeild_2024/xg_all ISL_Úrvalsdeild_2024.csv')
    squads = pd.read_csv(r'ISL_Úrvalsdeild_2024/squads ISL_Úrvalsdeild_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def NLD_Eredivisie_2023_2024_23_24():
    try:
        df_pv = pd.read_csv(r'NLD_Eredivisie_2023_2024/pv_all NLD_Eredivisie_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'NLD_Eredivisie_2023_2024/xA_all NLD_Eredivisie_2023_2024.csv')
  
    df_possession_xa = pd.read_csv(r'NLD_Eredivisie_2023_2024/xA_all NLD_Eredivisie_2023_2024.csv')
    df_matchstats = pd.read_csv(r'NLD_Eredivisie_2023_2024/matchstats_all NLD_Eredivisie_2023_2024.csv')
    df_xg = pd.read_csv(r'NLD_Eredivisie_2023_2024/xg_all NLD_Eredivisie_2023_2024.csv')
    squads = pd.read_csv(r'NLD_Eredivisie_2023_2024/squads NLD_Eredivisie_2023_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def USA_MLS_2024_23_24():
    try:
        df_pv = pd.read_csv(r'USA_MLS_2024/pv_all USA_MLS_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'USA_MLS_2024/xA_all USA_MLS_2024.csv')
     
    df_possession_xa = pd.read_csv(r'USA_MLS_2024/xA_all USA_MLS_2024.csv')
    df_matchstats = pd.read_csv(r'USA_MLS_2024/matchstats_all USA_MLS_2024.csv')
    df_xg = pd.read_csv(r'USA_MLS_2024/xg_all USA_MLS_2024.csv')
    squads = pd.read_csv(r'USA_MLS_2024/squads USA_MLS_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def USL_Championship_23_24():
    try:
        df_pv = pd.read_csv(r'USA_USL_Championship_2024/pv_all USA_USL_Championship_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'USA_USL_Championship_2024/xA_all USA_USL_Championship_2024.csv')
    df_possession_xa = pd.read_csv(r'USA_USL_Championship_2024/xA_all USA_USL_Championship_2024.csv')
    df_matchstats = pd.read_csv(r'USA_USL_Championship_2024/matchstats_all USA_USL_Championship_2024.csv')
    df_xg = pd.read_csv(r'USA_USL_Championship_2024/xg_all USA_USL_Championship_2024.csv')
    squads = pd.read_csv(r'USA_USL_Championship_2024/squads USA_USL_Championship_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def Super_liga_slovakia_23_24():
    try:
        df_pv = pd.read_csv(r'SVK_Super_Liga_2023_2024/pv_all SVK_Super_Liga_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'SVK_Super_Liga_2023_2024/xA_all SVK_Super_Liga_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'SVK_Super_Liga_2023_2024/xA_all SVK_Super_Liga_2023_2024.csv')
    df_matchstats = pd.read_csv(r'SVK_Super_Liga_2023_2024/matchstats_all SVK_Super_Liga_2023_2024.csv')
    df_xg = pd.read_csv(r'SVK_Super_Liga_2023_2024/xg_all SVK_Super_Liga_2023_2024.csv')
    squads = pd.read_csv(r'SVK_Super_Liga_2023_2024/squads SVK_Super_Liga_2023_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def Super_liga_serbia_23_24():
    try:
        df_pv = pd.read_csv(r'SRB_Super_Liga_2023_2024/pv_all SRB_Super_Liga_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'SRB_Super_Liga_2023_2024/xA_all SRB_Super_Liga_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'SRB_Super_Liga_2023_2024/xA_all SRB_Super_Liga_2023_2024.csv')
    df_matchstats = pd.read_csv(r'SRB_Super_Liga_2023_2024/matchstats_all SRB_Super_Liga_2023_2024.csv')
    df_xg = pd.read_csv(r'SRB_Super_Liga_2023_2024/xg_all SRB_Super_Liga_2023_2024.csv')
    squads = pd.read_csv(r'SRB_Super_Liga_2023_2024/squads SRB_Super_Liga_2023_2024.csv')   
   
    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def Challenger_pro_league_23_24():
    try:
        df_pv = pd.read_csv(r'BEL_Challenger_Pro_League_2023_2024/pv_all BEL_Challenger_Pro_League_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'BEL_Challenger_Pro_League_2023_2024/xA_all BEL_Challenger_Pro_League_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'BEL_Challenger_Pro_League_2023_2024/xA_all BEL_Challenger_Pro_League_2023_2024.csv')
    df_matchstats = pd.read_csv(r'BEL_Challenger_Pro_League_2023_2024/matchstats_all BEL_Challenger_Pro_League_2023_2024.csv')
    df_xg = pd.read_csv(r'BEL_Challenger_Pro_League_2023_2024/xg_all BEL_Challenger_Pro_League_2023_2024.csv')
    squads = pd.read_csv(r'BEL_Challenger_Pro_League_2023_2024/squads BEL_Challenger_Pro_League_2023_2024.csv')   

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def DNK_Superliga_2023_2024_23_24():
    try:
        df_pv = pd.read_csv(r'DNK_Superliga_2023_2024/pv_all DNK_Superliga_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'DNK_Superliga_2023_2024/xA_all DNK_Superliga_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'DNK_Superliga_2023_2024/xA_all DNK_Superliga_2023_2024.csv')
    df_matchstats = pd.read_csv(r'DNK_Superliga_2023_2024/matchstats_all DNK_Superliga_2023_2024.csv')
    df_xg = pd.read_csv(r'DNK_Superliga_2023_2024/xg_all DNK_Superliga_2023_2024.csv')
    squads = pd.read_csv(r'DNK_Superliga_2023_2024/squads DNK_Superliga_2023_2024.csv')

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def DNK_1_Division_2023_2024():
    try:
        df_pv = pd.read_csv(r'DNK_1_Division_2023_2024/pv_all DNK_1_Division_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'DNK_1_Division_2023_2024/xA_all DNK_1_Division_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'DNK_1_Division_2023_2024/xA_all DNK_1_Division_2023_2024.csv')
    df_matchstats = pd.read_csv(r'DNK_1_Division_2023_2024/matchstats_all DNK_1_Division_2023_2024.csv')
    df_xg = pd.read_csv(r'DNK_1_Division_2023_2024/xg_all DNK_1_Division_2023_2024.csv')
    squads = pd.read_csv(r'DNK_1_Division_2023_2024/squads DNK_1_Division_2023_2024.csv')

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
def DNK_1_Division_2024_2025():
    try:
        df_pv = pd.read_csv(r'DNK_1_Division_2024_2025/pv_all DNK_1_Division_2024_2025.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'DNK_1_Division_2024_2025/xA_all DNK_1_Division_2024_2025.csv')
    df_possession_xa = pd.read_csv(r'DNK_1_Division_2024_2025/xA_all DNK_1_Division_2024_2025.csv')
    df_matchstats = pd.read_csv(r'DNK_1_Division_2024_2025/matchstats_all DNK_1_Division_2024_2025.csv')
    df_xg = pd.read_csv(r'DNK_1_Division_2024_2025/xg_all DNK_1_Division_2024_2025.csv')
    squads = pd.read_csv(r'DNK_1_Division_2024_2025/squads DNK_1_Division_2024_2025.csv')

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)


@st.cache_data(experimental_allow_widgets=True)
def Eerste_Divisie_23_24():
    try:
        df_pv = pd.read_csv(r'NLD_Eerste_Divisie_2023_2024/pv_all NLD_Eerste_Divisie_2023_2024.csv')
    except FileNotFoundError:
        df_pv = pd.read_csv(r'NLD_Eerste_Divisie_2023_2024/xA_all NLD_Eerste_Divisie_2023_2024.csv')
    df_possession_xa = pd.read_csv(r'NLD_Eerste_Divisie_2023_2024/xA_all NLD_Eerste_Divisie_2023_2024.csv')
    df_matchstats = pd.read_csv(r'NLD_Eerste_Divisie_2023_2024/matchstats_all NLD_Eerste_Divisie_2023_2024.csv')
    df_xg = pd.read_csv(r'NLD_Eerste_Divisie_2023_2024/xg_all NLD_Eerste_Divisie_2023_2024.csv')
    squads = pd.read_csv(r'NLD_Eerste_Divisie_2023_2024/squads NLD_Eerste_Divisie_2023_2024.csv')

    Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads)

@st.cache_data(experimental_allow_widgets=True)
@st.cache_resource(experimental_allow_widgets=True)
def Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads):

    def calculate_score(df, column, score_column):
        df_unique = df.drop_duplicates(column).copy()
        df_unique.loc[:, score_column] = pd.qcut(df_unique[column], q=10, labels=False, duplicates='raise') + 1
        return df.merge(df_unique[[column, score_column]], on=column, how='left')
    
    col1,col2,col3 = st.columns(3)
    with col1:
        minutter_kamp = st.number_input('Minutes per match')
    with col2:
        minutter_total = st.number_input('Minutes total')
    with col3:
        alder = st.number_input('Max age',value=25)
        
    df_possession_xa = df_possession_xa.rename(columns={'318.0': 'xA'})
    df_possession_xa_summed = df_possession_xa.groupby(['playerName','label'])['xA'].sum().reset_index()

    try:
        df_pv = df_pv[['playerName', 'team_name', 'label', 'possessionValue.pvValue', 'possessionValue.pvAdded']]
        df_pv['possessionValue.pvValue'] = df_pv['possessionValue.pvValue'].astype(float)
        df_pv['possessionValue.pvAdded'] = df_pv['possessionValue.pvAdded'].astype(float)
        df_pv['possessionValue'] = df_pv['possessionValue.pvValue'] + df_pv['possessionValue.pvAdded']
        df_kamp = df_pv.groupby(['playerName', 'label', 'team_name']).sum()
    except KeyError:
        df_pv = df_possession_xa[['playerName', 'team_name', 'label', 'xA']]
        df_pv['possessionValue.pvValue'] = df_pv['xA'].astype(float)
        df_pv['possessionValue.pvAdded'] = df_pv['xA'].astype(float)
        df_pv['possessionValue'] = df_pv['xA'] + df_pv['xA']
        df_kamp = df_pv.groupby(['playerName', 'label', 'team_name']).sum()

    df_kamp = df_kamp.reset_index()
    df_matchstats = df_matchstats[['player_matchName','player_playerId','contestantId','duelLost','aerialLost','player_position','player_positionSide','successfulOpenPlayPass','totalContest','duelWon','penAreaEntries','accurateBackZonePass','possWonDef3rd','wonContest','accurateFwdZonePass','openPlayPass','totalBackZonePass','minsPlayed','fwdPass','finalThirdEntries','ballRecovery','totalFwdZonePass','successfulFinalThirdPasses','totalFinalThirdPasses','attAssistOpenplay','aerialWon','totalAttAssist','possWonMid3rd','interception','totalCrossNocorner','interceptionWon','attOpenplay','touchesInOppBox','attemptsIbox','totalThroughBall','possWonAtt3rd','accurateCrossNocorner','bigChanceCreated','accurateThroughBall','totalLayoffs','accurateLayoffs','totalFastbreak','shotFastbreak','formationUsed','label','match_id','date']]
    df_matchstats = df_matchstats.rename(columns={'player_matchName': 'playerName'})
    df_scouting = df_matchstats.merge(df_kamp)
    df_xg = df_xg[['contestantId','team_name','playerName','playerId','321','match_id','label','date']]
    df_xg = df_xg.rename(columns={'321': 'xg'})
    df_xg['xg'] = df_xg['xg'].astype(float)
    df_xg = df_xg.groupby(['playerName','playerId','match_id','contestantId','team_name','label','date']).sum()
    df_xg = df_xg.reset_index()
    df_scouting = df_scouting.rename(columns={'player_playerId': 'playerId'})
    df_scouting = df_scouting.merge(df_xg, how='left', on=['playerName', 'playerId', 'match_id', 'contestantId', 'team_name', 'label', 'date']).reset_index()
    df_scouting = df_scouting.merge(df_possession_xa_summed, how='left')
    df_scouting.fillna(0, inplace=True)
    squads['dateOfBirth'] = pd.to_datetime(squads['dateOfBirth'])
    today = datetime.today()
    squads['age_today'] = ((today - squads['dateOfBirth']).dt.days / 365.25).apply(np.floor)
    squads = squads[['id','matchName','nationality','dateOfBirth','age_today']]
    squads = squads.rename(columns={'id': 'playerId'})
    squads = squads.rename(columns={'matchName': 'playerName'})
    squads.fillna(0,inplace=True)

    df_scouting = df_scouting.merge(squads,how='outer')
    df_scouting['label'] = df_scouting['label'] +' ' + df_scouting['date']
    df_scouting = df_scouting.drop_duplicates(subset=['playerName', 'team_name', 'player_position', 'player_positionSide', 'label'])
    
    df_scouting['xg_per90'] = (df_scouting['xg'].astype(float) / df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['xA_per90'] = (df_scouting['xA'].astype(float) / df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['possessionValue.pvValue_per90'] = (df_scouting['possessionValue.pvValue'].astype(float) / df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['possessionValue.pvAdded_per90'] = (df_scouting['possessionValue.pvAdded'].astype(float) / df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['Possession value total per_90'] = df_scouting['possessionValue.pvAdded_per90'] + df_scouting['possessionValue.pvValue_per90']
    df_scouting['penAreaEntries_per90&crosses%shotassists'] = ((df_scouting['penAreaEntries'].astype(float)+df_scouting['totalCrossNocorner'].astype(float) + df_scouting['attAssistOpenplay'].astype(float))/ df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['penAreaEntries_per90'] = (df_scouting['penAreaEntries'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90    
    df_scouting['attAssistOpenplay_per90'] = (df_scouting['attAssistOpenplay'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['totalCrossNocorner_per90'] = (df_scouting['totalCrossNocorner'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['finalThird passes %'] = (df_scouting['successfulFinalThirdPasses'].astype(float) / df_scouting['totalFinalThirdPasses'].astype(float)) * 100
    df_scouting['finalThirdEntries_per90'] = (df_scouting['finalThirdEntries'].astype(float) / df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['interception_per90'] = (df_scouting['interception'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['possWonDef3rd_possWonMid3rd'] = (df_scouting['possWonDef3rd'].astype(float) + df_scouting['possWonMid3rd'].astype(float))
    df_scouting['possWonDef3rd_possWonMid3rd_per90'] =  (df_scouting['possWonDef3rd_possWonMid3rd'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['possWonDef3rd_possWonMid3rd_possWonAtt3rd'] = (df_scouting['possWonDef3rd'].astype(float) + df_scouting['possWonMid3rd'].astype(float) + df_scouting['possWonAtt3rd'].astype(float))
    df_scouting['possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90'] =  (df_scouting['possWonDef3rd_possWonMid3rd_possWonAtt3rd'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['possWonDef3rd_possWonMid3rd_per90&interceptions_per90'] = ((df_scouting['interception_per90'].astype(float) + df_scouting['possWonDef3rd_possWonMid3rd_per90'].astype(float))/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['duels won %'] = (df_scouting['duelWon'].astype(float) / (df_scouting['duelWon'].astype(float) + df_scouting['duelLost'].astype(float)))*100
    df_scouting['Forward zone pass %'] = (df_scouting['accurateFwdZonePass'].astype(float) / df_scouting['totalFwdZonePass'].astype(float)) * 100
    df_scouting['Back zone pass %'] = (df_scouting['accurateBackZonePass'].astype(float) / df_scouting['totalBackZonePass'].astype(float)) * 100
    df_scouting['Passing %'] = (df_scouting['successfulOpenPlayPass'].astype(float) / df_scouting['openPlayPass'].astype(float)) * 100
    df_scouting['Aerial duel %'] = (df_scouting['aerialWon'].astype(float) / (df_scouting['aerialWon'].astype(float) + df_scouting['aerialLost'].astype(float))) * 100
    df_scouting['Ballrecovery_per90'] = (df_scouting['ballRecovery'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['fwdPass_per90'] = (df_scouting['fwdPass'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['finalthirdpass_per90'] = (df_scouting['totalFinalThirdPasses'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['shotFastbreak_per90'] = (df_scouting['shotFastbreak'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['bigChanceCreated_per90'] = (df_scouting['bigChanceCreated'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['dribble %'] = (df_scouting['wonContest'].astype(float) / df_scouting['totalContest'].astype(float)) * 100
    df_scouting['touches_in_box_per90'] = (df_scouting['touchesInOppBox'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['totalThroughBall_per90'] = (df_scouting['totalThroughBall'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['attemptsIbox_per90'] = (df_scouting['attemptsIbox'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['aerialWon'] = (df_scouting['aerialWon'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90

    df_scouting.fillna(0, inplace=True)

    def ball_playing_central_defender():
        st.title('Ball playing central defender')
        df_spillende_stopper = df_scouting[(df_scouting['player_position'] == 'Defender') & (df_scouting['player_positionSide'].str.contains('Centre'))]
        df_spillende_stopper['minsPlayed'] = df_spillende_stopper['minsPlayed'].astype(int)
        df_spillende_stopper = df_spillende_stopper[df_spillende_stopper['minsPlayed'].astype(int) >= minutter_kamp]
        df_spillende_stopper = df_spillende_stopper[df_spillende_stopper['age_today'].astype(int) <= alder]
        df_spillende_stopper = calculate_score(df_spillende_stopper,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_spillende_stopper = calculate_score(df_spillende_stopper, 'duels won %', 'duels won % score')
        df_spillende_stopper = calculate_score(df_spillende_stopper, 'Forward zone pass %', 'Forward zone pass % score')
        df_spillende_stopper = calculate_score(df_spillende_stopper, 'Passing %', 'Open play passing % score')
        df_spillende_stopper = calculate_score(df_spillende_stopper, 'Back zone pass %', 'Back zone pass % score')
        df_spillende_stopper = calculate_score(df_spillende_stopper, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_spillende_stopper = calculate_score(df_spillende_stopper, 'Ballrecovery_per90', 'Ballrecovery_per90 score')

        
        df_spillende_stopper['Passing'] = df_spillende_stopper[['Open play passing % score', 'Back zone pass % score']].mean(axis=1)
        df_spillende_stopper['Forward passing'] = df_spillende_stopper[['Forward zone pass % score', 'Possession value added score', 'Possession value added score']].mean(axis=1)
        df_spillende_stopper['Defending'] = df_spillende_stopper[['duels won % score', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score', 'Ballrecovery_per90 score']].mean(axis=1)
        df_spillende_stopper['Possession value added'] = df_spillende_stopper['Possession value added score']
        
        df_spillende_stopper['Total score'] = df_spillende_stopper[['Passing','Passing','Forward passing','Forward passing','Forward passing','Defending','Defending','Possession value added','Possession value added','Possession value added']].mean(axis=1)
        df_spillende_stopper = df_spillende_stopper[['playerName','team_name','player_position','label','minsPlayed','age_today','Passing','Forward passing','Defending','Possession value added score','Total score']] 
        df_spillende_stoppertotal = df_spillende_stopper[['playerName','team_name','player_position','minsPlayed','age_today','Passing','Forward passing','Defending','Possession value added score','Total score']]
        df_spillende_stoppertotal = df_spillende_stoppertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_spillende_stopper.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_spillende_stoppertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_spillende_stopper = df_spillende_stopper.sort_values('Total score',ascending = False)
            st.dataframe(df_spillende_stopper,hide_index=True)
        with st.expander('Total'):
            df_spillende_stoppertotal = df_spillende_stoppertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Passing','Forward passing','Defending','Possession value added score','Total score']]
            df_spillende_stoppertotal = df_spillende_stoppertotal[df_spillende_stoppertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_spillende_stoppertotal = df_spillende_stoppertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_spillende_stoppertotal,hide_index=True)
    
    def defending_central_defender():
        st.title('Defending central defender')
        df_forsvarende_stopper = df_scouting[(df_scouting['player_position'] == 'Defender') & (df_scouting['player_positionSide'].str.contains('Centre'))]
        df_forsvarende_stopper['minsPlayed'] = df_forsvarende_stopper['minsPlayed'].astype(int)
        df_forsvarende_stopper = df_forsvarende_stopper[df_forsvarende_stopper['minsPlayed'].astype(int) >= minutter_kamp]
        df_forsvarende_stopper = df_forsvarende_stopper[df_forsvarende_stopper['age_today'].astype(int) <= alder]
        
        df_forsvarende_stopper = calculate_score(df_forsvarende_stopper, 'duels won %', 'duels won % score')
        df_forsvarende_stopper = calculate_score(df_forsvarende_stopper, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_forsvarende_stopper = calculate_score(df_forsvarende_stopper, 'Ballrecovery_per90', 'ballRecovery score')
        df_forsvarende_stopper = calculate_score(df_forsvarende_stopper,'Aerial duel %', 'Aerial duel score')
        df_forsvarende_stopper = calculate_score(df_forsvarende_stopper,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_forsvarende_stopper = calculate_score(df_forsvarende_stopper, 'Passing %', 'Open play passing % score')
        df_forsvarende_stopper = calculate_score(df_forsvarende_stopper, 'Back zone pass %', 'Back zone pass % score')


        df_forsvarende_stopper['Defending'] = df_forsvarende_stopper[['duels won % score','Aerial duel score', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score', 'ballRecovery score']].mean(axis=1)
        df_forsvarende_stopper['Duels'] = df_forsvarende_stopper[['duels won % score','duels won % score','Aerial duel score']].mean(axis=1)
        df_forsvarende_stopper['Intercepting'] = df_forsvarende_stopper[['possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','ballRecovery score']].mean(axis=1)
        df_forsvarende_stopper['Passing'] = df_forsvarende_stopper[['Open play passing % score', 'Back zone pass % score','Possession value added score','Possession value added score']].mean(axis=1)
        
        df_forsvarende_stopper['Total score'] = df_forsvarende_stopper[['Defending','Defending','Defending','Defending','Duels','Duels','Duels','Intercepting','Intercepting','Intercepting','Passing','Passing']].mean(axis=1)

        df_forsvarende_stopper = df_forsvarende_stopper[['playerName','team_name','player_position','label','minsPlayed','age_today','Defending','Duels','Intercepting','Passing','Total score']]
        df_forsvarende_stoppertotal = df_forsvarende_stopper[['playerName','team_name','player_position','minsPlayed','age_today','Defending','Duels','Intercepting','Passing','Total score']]
        df_forsvarende_stoppertotal = df_forsvarende_stoppertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_forsvarende_stopper.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_forsvarende_stoppertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_forsvarende_stopper = df_forsvarende_stopper.sort_values('Total score',ascending = False)
            st.dataframe(df_forsvarende_stopper,hide_index=True)
        with st.expander('Total'):
            df_forsvarende_stoppertotal = df_forsvarende_stoppertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Defending','Duels','Intercepting','Passing','Total score']]
            df_forsvarende_stoppertotal = df_forsvarende_stoppertotal[df_forsvarende_stoppertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_forsvarende_stoppertotal = df_forsvarende_stoppertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_forsvarende_stoppertotal,hide_index=True)

    def balanced_central_defender():
        st.title('Balanced central defender')
        df_balanced_central_defender = df_scouting[(df_scouting['player_position'] == 'Defender') & (df_scouting['player_positionSide'].str.contains('Centre'))]
        df_balanced_central_defender['minsPlayed'] = df_balanced_central_defender['minsPlayed'].astype(int)
        df_balanced_central_defender = df_balanced_central_defender[df_balanced_central_defender['minsPlayed'].astype(int) >= minutter_kamp]
        df_balanced_central_defender = df_balanced_central_defender[df_balanced_central_defender['age_today'].astype(int) <= alder]
        
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'duels won %', 'duels won % score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Ballrecovery_per90', 'ballRecovery score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender,'Aerial duel %', 'Aerial duel score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Passing %', 'Open play passing % score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Back zone pass %', 'Back zone pass % score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Forward zone pass %', 'Forward zone pass % score')


        df_balanced_central_defender['Defending'] = df_balanced_central_defender[['duels won % score','Aerial duel score', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score', 'ballRecovery score']].mean(axis=1)
        df_balanced_central_defender['Possession value added'] = df_balanced_central_defender['Possession value added score']
        df_balanced_central_defender['Passing'] = df_balanced_central_defender[['Open play passing % score', 'Back zone pass % score','Forward zone pass % score','Possession value added score','Possession value added score']].mean(axis=1)
        
        df_balanced_central_defender['Total score'] = df_balanced_central_defender[['Defending','Possession value added','Passing']].mean(axis=1)

        df_balanced_central_defender = df_balanced_central_defender[['playerName','team_name','player_position','label','minsPlayed','age_today','Defending','Possession value added','Passing','Total score']]
        
        df_balanced_central_defendertotal = df_balanced_central_defender[['playerName','team_name','player_position','minsPlayed','age_today','Defending','Possession value added','Passing','Total score']]
        df_balanced_central_defendertotal = df_balanced_central_defendertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_balanced_central_defender.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_balanced_central_defendertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_balanced_central_defender = df_balanced_central_defender.sort_values('Total score',ascending = False)
            st.dataframe(df_balanced_central_defender,hide_index=True)
        with st.expander('Total'):
            df_balanced_central_defendertotal = df_balanced_central_defendertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Defending','Possession value added','Passing','Total score']]
            df_balanced_central_defendertotal = df_balanced_central_defendertotal[df_balanced_central_defendertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_balanced_central_defendertotal = df_balanced_central_defendertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_balanced_central_defendertotal,hide_index=True)

    def fullbacks():
        st.title('Fullbacks')
        df_backs = df_scouting[((df_scouting['player_position'] == 'Defender') | (df_scouting['player_position'] == 'Wing Back')) & ((df_scouting['player_positionSide'] == 'Right') | (df_scouting['player_positionSide'] == 'Left'))]
        df_backs['minsPlayed'] = df_backs['minsPlayed'].astype(int)
        df_backs = df_backs[df_backs['minsPlayed'].astype(int) >= minutter_kamp]
        df_backs = df_backs[df_backs['age_today'].astype(int) <= alder]

        df_backs = calculate_score(df_backs,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_backs = calculate_score(df_backs, 'duels won %', 'duels won % score')
        df_backs = calculate_score(df_backs, 'Forward zone pass %', 'Forward zone pass % score')
        df_backs = calculate_score(df_backs, 'penAreaEntries_per90&crosses%shotassists', 'Penalty area entries & crosses & shot assists score')
        df_backs = calculate_score(df_backs, 'attAssistOpenplay_per90', 'attAssistOpenplay_per90 score')
        df_backs = calculate_score(df_backs, 'finalThird passes %', 'finalThird passes % score')
        df_backs = calculate_score(df_backs, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_backs = calculate_score(df_backs, 'interception_per90', 'interception_per90 score')
        df_backs = calculate_score(df_backs, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_backs = calculate_score(df_backs, 'Back zone pass %', 'Back zone pass % score')
        df_backs = calculate_score(df_backs, 'totalCrossNocorner_per90', 'totalCrossNocorner_per90 score')
        df_backs['Defending'] = (df_backs['duels won % score'] + df_backs['duels won % score'] + df_backs['possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score'])/3
        df_backs['Passing'] = (df_backs['Forward zone pass % score'] + df_backs['finalThird passes % score'] + df_backs['Back zone pass % score'] + df_backs['Possession value added score'])/4
        df_backs['Chance creation'] = (df_backs['Penalty area entries & crosses & shot assists score'] + df_backs['totalCrossNocorner_per90 score'] + df_backs['totalCrossNocorner_per90 score'] + df_backs['finalThirdEntries_per90 score']+ df_backs['finalThirdEntries_per90 score'] + df_backs['Forward zone pass % score']+ df_backs['Forward zone pass % score'] + df_backs['Possession value added score'] + df_backs['Possession value added score'])/9
        df_backs['Possession value added'] = df_backs['Possession value added score']
        
        df_backs = calculate_score(df_backs, 'Defending', 'Defending_')
        df_backs = calculate_score(df_backs, 'Passing', 'Passing_')
        df_backs = calculate_score(df_backs, 'Chance creation','Chance_creation')
        df_backs = calculate_score(df_backs, 'Possession value added', 'Possession_value_added')
        
        df_backs['Total score'] = (df_backs['Defending_'] + df_backs['Defending_'] + df_backs['Defending_'] + df_backs['Defending_'] + df_backs['Passing_']+ df_backs['Passing_'] + df_backs['Chance_creation'] + df_backs['Chance_creation'] + df_backs['Chance_creation'] + df_backs['Possession_value_added'] + df_backs['Possession_value_added'] + df_backs['Possession_value_added'] + df_backs['Possession_value_added']) / 13
        df_backs = df_backs[['playerName','team_name','player_position','player_positionSide','label','minsPlayed','age_today','Defending_','Passing_','Chance_creation','Possession_value_added','Total score']]
        df_backs = df_backs.dropna()
        df_backstotal = df_backs[['playerName','team_name','player_position','player_positionSide','minsPlayed','age_today','Defending_','Passing_','Chance_creation','Possession_value_added','Total score']]
        df_backstotal = df_backstotal.groupby(['playerName','team_name','player_position','player_positionSide','age_today']).mean().reset_index()
        minutter = df_backs.groupby(['playerName', 'team_name','player_position','player_positionSide','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_backstotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_backs = df_backs.sort_values('Total score',ascending = False)
            st.dataframe(df_backs,hide_index=True)
        with st.expander('Total'):
            df_backstotal = df_backstotal[['playerName','team_name','player_position','player_positionSide','age_today','minsPlayed total','Defending_','Passing_','Chance_creation','Possession_value_added','Total score']]
            df_backstotal = df_backstotal[df_backstotal['minsPlayed total'].astype(int) >= minutter_total]
            df_backstotal = df_backstotal.sort_values('Total score',ascending = False)
            st.dataframe(df_backstotal,hide_index=True)
    
    def number6():
        st.title('Number 6')
        df_sekser = df_scouting[((df_scouting['player_position'] == 'Defensive Midfielder') | (df_scouting['player_position'] == 'Midfielder')) & df_scouting['player_positionSide'].str.contains('Centre')]
        df_sekser['minsPlayed'] = df_sekser['minsPlayed'].astype(int)
        df_sekser = df_sekser[df_sekser['minsPlayed'].astype(int) >= minutter_kamp]
        df_sekser = df_sekser[df_sekser['age_today'].astype(int) <= alder]

        df_sekser = calculate_score(df_sekser,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_sekser = calculate_score(df_sekser, 'duels won %', 'duels won % score')
        df_sekser = calculate_score(df_sekser, 'Passing %', 'Passing % score')
        df_sekser = calculate_score(df_sekser, 'Back zone pass %', 'Back zone pass % score')
        df_sekser = calculate_score(df_sekser, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_sekser = calculate_score(df_sekser, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_sekser = calculate_score(df_sekser, 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90', 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90 score')
        df_sekser = calculate_score(df_sekser, 'Forward zone pass %', 'Forward zone pass % score')
        df_sekser = calculate_score(df_sekser, 'Ballrecovery_per90', 'ballRecovery score')

        
        df_sekser['Defending'] = df_sekser[['duels won % score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','ballRecovery score']].mean(axis=1)
        df_sekser['Passing'] = df_sekser[['Back zone pass % score','Passing % score']].mean(axis=1)
        df_sekser['Progressive ball movement'] = df_sekser[['Possession value added score','Possession value added score','Forward zone pass % score']].mean(axis=1)
        df_sekser['Possession value added'] = df_sekser['Possession value added score']
        
        df_sekser = calculate_score(df_sekser, 'Defending', 'Defending_')
        df_sekser = calculate_score(df_sekser, 'Passing', 'Passing_')
        df_sekser = calculate_score(df_sekser, 'Progressive ball movement','Progressive_ball_movement')
        df_sekser = calculate_score(df_sekser, 'Possession value added', 'Possession_value_added')
        
        df_sekser['Total score'] = df_sekser[['Defending_','Passing_','Progressive_ball_movement','Possession_value_added']].mean(axis=1)
        df_sekser = df_sekser[['playerName','team_name','player_position','label','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]
        df_sekser = df_sekser.dropna()
        df_seksertotal = df_sekser[['playerName','team_name','player_position','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]

        df_seksertotal = df_seksertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_sekser.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_seksertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_sekser = df_sekser.sort_values('Total score',ascending = False)
            st.dataframe(df_sekser,hide_index=True)
        with st.expander('Total'):
            df_seksertotal = df_seksertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]
            df_seksertotal= df_seksertotal[df_seksertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_seksertotal = df_seksertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_seksertotal,hide_index=True)

    def number6_destroyer():
        st.title('Number 6 (destroyer)')
        df_sekser = df_scouting[((df_scouting['player_position'] == 'Defensive Midfielder') | (df_scouting['player_position'] == 'Midfielder')) & df_scouting['player_positionSide'].str.contains('Centre')]
        df_sekser['minsPlayed'] = df_sekser['minsPlayed'].astype(int)
        df_sekser = df_sekser[df_sekser['minsPlayed'].astype(int) >= minutter_kamp]
        df_sekser = df_sekser[df_sekser['age_today'].astype(int) <= alder]

        df_sekser = calculate_score(df_sekser,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_sekser = calculate_score(df_sekser, 'duels won %', 'duels won % score')
        df_sekser = calculate_score(df_sekser, 'Passing %', 'Passing % score')
        df_sekser = calculate_score(df_sekser, 'Back zone pass %', 'Back zone pass % score')
        df_sekser = calculate_score(df_sekser, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_sekser = calculate_score(df_sekser, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_sekser = calculate_score(df_sekser, 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90', 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90 score')
        df_sekser = calculate_score(df_sekser, 'Forward zone pass %', 'Forward zone pass % score')
        df_sekser = calculate_score(df_sekser, 'Ballrecovery_per90', 'ballRecovery score')

        
        df_sekser['Defending'] = df_sekser[['duels won % score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','ballRecovery score']].mean(axis=1)
        df_sekser['Passing'] = df_sekser[['Back zone pass % score','Passing % score']].mean(axis=1)
        df_sekser['Progressive ball movement'] = df_sekser[['Possession value added score','Possession value added score','Forward zone pass % score']].mean(axis=1)
        df_sekser['Possession value added'] = df_sekser['Possession value added score']
        
        df_sekser = calculate_score(df_sekser, 'Defending', 'Defending_')
        df_sekser = calculate_score(df_sekser, 'Passing', 'Passing_')
        df_sekser = calculate_score(df_sekser, 'Progressive ball movement','Progressive_ball_movement')
        df_sekser = calculate_score(df_sekser, 'Possession value added', 'Possession_value_added')
        
        df_sekser['Total score'] = df_sekser[['Defending_','Defending_','Defending_','Passing_','Passing_','Progressive_ball_movement','Possession_value_added']].mean(axis=1)
        df_sekser = df_sekser[['playerName','team_name','player_position','label','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]
        df_sekser = df_sekser.dropna()

        df_seksertotal = df_sekser[['playerName','team_name','player_position','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]

        df_seksertotal = df_seksertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_sekser.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_seksertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_sekser = df_sekser.sort_values('Total score',ascending = False)
            st.dataframe(df_sekser,hide_index=True)
        with st.expander('Total'):
            df_seksertotal = df_seksertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]
            df_seksertotal= df_seksertotal[df_seksertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_seksertotal = df_seksertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_seksertotal,hide_index=True)

    def number6_double_6_forward():
        st.title('Number 6 (double 6 forward)')
        df_sekser = df_scouting[((df_scouting['player_position'] == 'Defensive Midfielder') | (df_scouting['player_position'] == 'Midfielder')) & df_scouting['player_positionSide'].str.contains('Centre')]
        df_sekser['minsPlayed'] = df_sekser['minsPlayed'].astype(int)
        df_sekser = df_sekser[df_sekser['minsPlayed'].astype(int) >= minutter_kamp]
        df_sekser = df_sekser[df_sekser['age_today'].astype(int) <= alder]

        df_sekser = calculate_score(df_sekser,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_sekser = calculate_score(df_sekser, 'duels won %', 'duels won % score')
        df_sekser = calculate_score(df_sekser, 'Passing %', 'Passing % score')
        df_sekser = calculate_score(df_sekser, 'Back zone pass %', 'Back zone pass % score')
        df_sekser = calculate_score(df_sekser, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_sekser = calculate_score(df_sekser, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_sekser = calculate_score(df_sekser, 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90', 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90 score')
        df_sekser = calculate_score(df_sekser, 'Forward zone pass %', 'Forward zone pass % score')
        df_sekser = calculate_score(df_sekser, 'Ballrecovery_per90', 'ballRecovery score')

        
        df_sekser['Defending'] = df_sekser[['duels won % score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','ballRecovery score']].mean(axis=1)
        df_sekser['Passing'] = df_sekser[['Back zone pass % score','Passing % score']].mean(axis=1)
        df_sekser['Progressive ball movement'] = df_sekser[['Possession value added score','Possession value added score','Forward zone pass % score']].mean(axis=1)
        df_sekser['Possession value added'] = df_sekser['Possession value added score']
        
        df_sekser = calculate_score(df_sekser, 'Defending', 'Defending_')
        df_sekser = calculate_score(df_sekser, 'Passing', 'Passing_')
        df_sekser = calculate_score(df_sekser, 'Progressive ball movement','Progressive_ball_movement')
        df_sekser = calculate_score(df_sekser, 'Possession value added', 'Possession_value_added')
        
        df_sekser['Total score'] = df_sekser[['Defending_','Defending_','Passing_','Passing_','Progressive_ball_movement','Progressive_ball_movement','Possession_value_added','Possession_value_added']].mean(axis=1)
        df_sekser = df_sekser[['playerName','team_name','player_position','label','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]
        df_sekser = df_sekser.dropna()
        df_seksertotal = df_sekser[['playerName','team_name','player_position','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]

        df_seksertotal = df_seksertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_sekser.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_seksertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_sekser = df_sekser.sort_values('Total score',ascending = False)
            st.dataframe(df_sekser,hide_index=True)
        with st.expander('Total'):
            df_seksertotal = df_seksertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]
            df_seksertotal= df_seksertotal[df_seksertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_seksertotal = df_seksertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_seksertotal,hide_index=True)

    def number8():
        st.title('Number 8')
        df_otter = df_scouting[(df_scouting['player_position'] == 'Midfielder') & df_scouting['player_positionSide'].str.contains('Centre')]
        df_otter['minsPlayed'] = df_otter['minsPlayed'].astype(int)
        df_otter = df_otter[df_otter['minsPlayed'].astype(int) >= minutter_kamp]
        df_otter = df_otter[df_otter['age_today'].astype(int) <= alder]

        df_otter = calculate_score(df_otter,'Possession value total per_90','Possession value total score')
        df_otter = calculate_score(df_otter,'possessionValue.pvValue_per90', 'Possession value score')
        df_otter = calculate_score(df_otter,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_otter = calculate_score(df_otter, 'duels won %', 'duels won % score')
        df_otter = calculate_score(df_otter, 'Passing %', 'Passing % score')
        df_otter = calculate_score(df_otter, 'Back zone pass %', 'Back zone pass % score')
        df_otter = calculate_score(df_otter, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_otter = calculate_score(df_otter, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_otter = calculate_score(df_otter, 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90', 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90 score')
        df_otter = calculate_score(df_otter, 'Forward zone pass %', 'Forward zone pass % score')
        df_otter = calculate_score(df_otter, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_otter = calculate_score(df_otter, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_otter = calculate_score(df_otter, 'penAreaEntries_per90','penAreaEntries_per90 score')

        df_otter['Defending'] = df_otter[['duels won % score','possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90 score']].mean(axis=1)
        df_otter['Passing'] = df_otter[['Forward zone pass % score','Passing % score']].mean(axis=1)
        df_otter['Progressive ball movement'] = df_otter[['attAssistOpenplay_per90 score','fwd_Pass_per90 score','penAreaEntries_per90 score','Forward zone pass % score','finalThirdEntries_per90 score','Possession value total score']].mean(axis=1)
        df_otter['Possession value'] = df_otter[['Possession value added score','Possession value total score']].mean(axis=1)
        
        df_otter = calculate_score(df_otter, 'Defending', 'Defending_')
        df_otter = calculate_score(df_otter, 'Passing', 'Passing_')
        df_otter = calculate_score(df_otter, 'Progressive ball movement','Progressive_ball_movement')
        df_otter = calculate_score(df_otter, 'Possession value', 'Possession_value')
        
        df_otter['Total score'] = df_otter[['Defending_','Passing_','Passing_','Progressive_ball_movement','Progressive_ball_movement','Possession_value','Possession_value','Possession_value']].mean(axis=1)
        df_otter = df_otter[['playerName','team_name','player_position','label','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value','Total score']]
        df_otter = df_otter.dropna()

        df_ottertotal = df_otter[['playerName','team_name','player_position','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value','Total score']]

        df_ottertotal = df_ottertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_otter.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_ottertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_otter = df_otter.sort_values('Total score',ascending = False)
            st.dataframe(df_otter,hide_index=True)
        with st.expander('Total'):
            df_ottertotal = df_ottertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Defending_','Passing_','Progressive_ball_movement','Possession_value','Total score']]
            df_ottertotal= df_ottertotal[df_ottertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_ottertotal = df_ottertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_ottertotal,hide_index=True)

    def number10():
        st.title('Number 10')
        df_10 = df_scouting[((df_scouting['player_position'] == 'Midfielder') | (df_scouting['player_position'] == 'Attacking Midfielder')) & (df_scouting['player_positionSide'] == 'Centre')]
        df_10['minsPlayed'] = df_10['minsPlayed'].astype(int)
        df_10 = df_10[df_10['minsPlayed'].astype(int) >= minutter_kamp]
        df_10 = df_10[df_10['age_today'].astype(int) <= alder]

        df_10 = calculate_score(df_10,'Possession value total per_90','Possession value total score')
        df_10 = calculate_score(df_10,'possessionValue.pvValue_per90', 'Possession value score')
        df_10 = calculate_score(df_10,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_10 = calculate_score(df_10, 'Passing %', 'Passing % score')
        df_10 = calculate_score(df_10, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_10 = calculate_score(df_10, 'Forward zone pass %', 'Forward zone pass % score')
        df_10 = calculate_score(df_10, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_10 = calculate_score(df_10, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_10 = calculate_score(df_10, 'penAreaEntries_per90','penAreaEntries_per90 score')
        df_10 = calculate_score(df_10, 'finalThird passes %','finalThird passes % score')
        df_10 = calculate_score(df_10, 'bigChanceCreated_per90','bigChanceCreated_per90 score')
        df_10 = calculate_score(df_10, 'dribble %','dribble % score')
        df_10 = calculate_score(df_10, 'touches_in_box_per90','touches_in_box_per90 score')
        df_10 = calculate_score(df_10, 'totalThroughBall_per90','totalThroughBall_per90 score')
        df_10 = calculate_score(df_10, 'xA_per90','xA_per90 score')
        df_10 = calculate_score(df_10, 'attemptsIbox_per90','attemptsIbox_per90 score')
        df_10 = calculate_score(df_10, 'xg_per90','xg_per90 score')


        df_10['Passing'] = df_10[['Forward zone pass % score','Passing % score']].mean(axis=1)
        df_10['Chance creation'] = df_10[['attAssistOpenplay_per90 score','penAreaEntries_per90 score','Forward zone pass % score','finalThird passes % score','Possession value total score','Possession value score','bigChanceCreated_per90 score','dribble % score','touches_in_box_per90 score','totalThroughBall_per90 score','xA_per90 score']].mean(axis=1)
        df_10['Goalscoring'] = df_10[['attemptsIbox_per90 score','xg_per90 score','xg_per90 score']].mean(axis=1)
        df_10['Possession value'] = df_10[['Possession value total score','Possession value total score','Possession value added score','Possession value score','Possession value score','Possession value score']].mean(axis=1)
                
        df_10 = calculate_score(df_10, 'Passing', 'Passing_')
        df_10 = calculate_score(df_10, 'Chance creation','Chance_creation')
        df_10 = calculate_score(df_10, 'Goalscoring','Goalscoring_')        
        df_10 = calculate_score(df_10, 'Possession value', 'Possession_value')
        
        df_10['Total score'] = df_10[['Passing_','Chance_creation','Chance_creation','Chance_creation','Chance_creation','Goalscoring_','Goalscoring_','Goalscoring_','Possession_value','Possession_value','Possession_value']].mean(axis=1)
        df_10 = df_10[['playerName','team_name','label','minsPlayed','age_today','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]
        df_10 = df_10.dropna()
        df_10total = df_10[['playerName','team_name','minsPlayed','age_today','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]

        df_10total = df_10total.groupby(['playerName','team_name','age_today']).mean().reset_index()
        minutter = df_10.groupby(['playerName', 'team_name','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_10total['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_10 = df_10.sort_values('Total score',ascending = False)
            st.dataframe(df_10,hide_index=True)
        with st.expander('Total'):
            df_10total = df_10total[['playerName','team_name','age_today','minsPlayed total','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]
            df_10total= df_10total[df_10total['minsPlayed total'].astype(int) >= minutter_total]
            df_10total = df_10total.sort_values('Total score',ascending = False)
            st.dataframe(df_10total,hide_index=True)

    def winger():
        st.title('Winger')
        df_10 = df_scouting[
            ((df_scouting['player_position'] == 'Midfielder') & 
            (df_scouting['player_positionSide'].isin(['Right', 'Left']))) |
            (((df_scouting['player_position'] == 'Attacking Midfielder') | 
            (df_scouting['player_position'] == 'Striker')) & 
            (df_scouting['player_positionSide'].str.contains('Right|Left')))
        ]        
        df_10['minsPlayed'] = df_10['minsPlayed'].astype(int)
        df_10 = df_10[df_10['minsPlayed'].astype(int) >= minutter_kamp]
        df_10 = df_10[df_10['age_today'].astype(int) <= alder]

        df_10 = calculate_score(df_10,'Possession value total per_90','Possession value total score')
        df_10 = calculate_score(df_10,'possessionValue.pvValue_per90', 'Possession value score')
        df_10 = calculate_score(df_10,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_10 = calculate_score(df_10, 'Passing %', 'Passing % score')
        df_10 = calculate_score(df_10, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_10 = calculate_score(df_10, 'Forward zone pass %', 'Forward zone pass % score')
        df_10 = calculate_score(df_10, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_10 = calculate_score(df_10, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_10 = calculate_score(df_10, 'penAreaEntries_per90','penAreaEntries_per90 score')
        df_10 = calculate_score(df_10, 'finalThird passes %','finalThird passes % score')
        df_10 = calculate_score(df_10, 'shotFastbreak_per90','shotFastbreak_per90 score')
        df_10 = calculate_score(df_10, 'bigChanceCreated_per90','bigChanceCreated_per90 score')
        df_10 = calculate_score(df_10, 'dribble %','dribble % score')
        df_10 = calculate_score(df_10, 'touches_in_box_per90','touches_in_box_per90 score')
        df_10 = calculate_score(df_10, 'totalThroughBall_per90','totalThroughBall_per90 score')
        df_10 = calculate_score(df_10, 'xA_per90','xA_per90 score')
        df_10 = calculate_score(df_10, 'attemptsIbox_per90','attemptsIbox_per90 score')
        df_10 = calculate_score(df_10, 'xg_per90','xg_per90 score')


        df_10['Passing'] = df_10[['Forward zone pass % score','Passing % score']].mean(axis=1)
        df_10['Chance creation'] = df_10[['attAssistOpenplay_per90 score','penAreaEntries_per90 score','Forward zone pass % score','finalThird passes % score','Possession value total score','Possession value score','shotFastbreak_per90 score','bigChanceCreated_per90 score','dribble % score','dribble % score','dribble % score','touches_in_box_per90 score','totalThroughBall_per90 score','xA_per90 score','xA_per90 score','xA_per90 score']].mean(axis=1)
        df_10['Goalscoring'] = df_10[['attemptsIbox_per90 score','xg_per90 score','xg_per90 score']].mean(axis=1)
        df_10['Possession value'] = df_10[['Possession value total score','Possession value total score','Possession value added score','Possession value score','Possession value score','Possession value score']].mean(axis=1)
                
        df_10 = calculate_score(df_10, 'Passing', 'Passing_')
        df_10 = calculate_score(df_10, 'Chance creation','Chance_creation')
        df_10 = calculate_score(df_10, 'Goalscoring','Goalscoring_')        
        df_10 = calculate_score(df_10, 'Possession value', 'Possession_value')
        
        df_10['Total score'] = df_10[['Passing_','Chance_creation','Chance_creation','Chance_creation','Chance_creation','Goalscoring_','Goalscoring_','Goalscoring_','Goalscoring_','Possession_value','Possession_value','Possession_value','Possession_value']].mean(axis=1)
        df_10 = df_10[['playerName','team_name','label','minsPlayed','age_today','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]
        df_10 = df_10.dropna()
        df_10total = df_10[['playerName','team_name','minsPlayed','age_today','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]

        df_10total = df_10total.groupby(['playerName','team_name','age_today']).mean().reset_index()
        minutter = df_10.groupby(['playerName', 'team_name','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_10total['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_10 = df_10.sort_values('Total score',ascending = False)
            st.dataframe(df_10,hide_index=True)
        with st.expander('Total'):
            df_10total = df_10total[['playerName','team_name','age_today','minsPlayed total','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]
            df_10total= df_10total[df_10total['minsPlayed total'].astype(int) >= minutter_total]
            df_10total = df_10total.sort_values('Total score',ascending = False)
            st.dataframe(df_10total,hide_index=True)

    def Classic_striker():
        st.title('Classic striker')
        df_striker = df_scouting[(df_scouting['player_position'] == 'Striker') & (df_scouting['player_positionSide'].str.contains('Centre'))]
        df_striker['minsPlayed'] = df_striker['minsPlayed'].astype(int)
        df_striker = df_striker[df_striker['minsPlayed'].astype(int) >= minutter_kamp]
        df_striker = df_striker[df_striker['age_today'].astype(int) <= alder]

        df_striker = calculate_score(df_striker,'Possession value total per_90','Possession value total score')
        df_striker = calculate_score(df_striker,'possessionValue.pvValue_per90', 'Possession value score')
        df_striker = calculate_score(df_striker,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_striker = calculate_score(df_striker, 'Passing %', 'Passing % score')
        df_striker = calculate_score(df_striker, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_striker = calculate_score(df_striker, 'Forward zone pass %', 'Forward zone pass % score')
        df_striker = calculate_score(df_striker, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_striker = calculate_score(df_striker, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_striker = calculate_score(df_striker, 'penAreaEntries_per90','penAreaEntries_per90 score')
        df_striker = calculate_score(df_striker, 'finalThird passes %','finalThird passes % score')
        df_striker = calculate_score(df_striker, 'shotFastbreak_per90','shotFastbreak_per90 score')
        df_striker = calculate_score(df_striker, 'bigChanceCreated_per90','bigChanceCreated_per90 score')
        df_striker = calculate_score(df_striker, 'dribble %','dribble % score')
        df_striker = calculate_score(df_striker, 'touches_in_box_per90','touches_in_box_per90 score')
        df_striker = calculate_score(df_striker, 'xA_per90','xA_per90 score')
        df_striker = calculate_score(df_striker, 'attemptsIbox_per90','attemptsIbox_per90 score')
        df_striker = calculate_score(df_striker, 'xg_per90','xg_per90 score')


        df_striker['Linkup_play'] = df_striker[['Forward zone pass % score','Passing % score','Possession value score','penAreaEntries_per90 score','finalThirdEntries_per90 score']].mean(axis=1)
        df_striker['Chance_creation'] = df_striker[['penAreaEntries_per90 score','Possession value total score','bigChanceCreated_per90 score','touches_in_box_per90 score','finalThirdEntries_per90 score']].mean(axis=1)
        df_striker['Goalscoring_'] = df_striker[['attemptsIbox_per90 score','xg_per90 score','xg_per90 score','xg_per90 score','xg_per90 score']].mean(axis=1)
        df_striker['Possession_value'] = df_striker[['Possession value total score','Possession value score','Possession value score','Possession value score']].mean(axis=1)

        df_striker = calculate_score(df_striker, 'Linkup_play', 'Linkup play')
        df_striker = calculate_score(df_striker, 'Chance_creation','Chance creation')
        df_striker = calculate_score(df_striker, 'Goalscoring_','Goalscoring')        
        df_striker = calculate_score(df_striker, 'Possession_value', 'Possession value')

        
        df_striker['Total score'] = df_striker[['Linkup play','Chance creation','Goalscoring','Possession value']].mean(axis=1)
        df_striker = df_striker[['playerName','team_name','label','minsPlayed','age_today','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]
        df_striker = df_striker.dropna()

        df_strikertotal = df_striker[['playerName','team_name','minsPlayed','age_today','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]

        df_strikertotal = df_strikertotal.groupby(['playerName','team_name','age_today']).mean().reset_index()
        minutter = df_striker.groupby(['playerName', 'team_name','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_strikertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_striker = df_striker.sort_values('Total score',ascending = False)
            st.dataframe(df_striker,hide_index=True)
        with st.expander('Total'):
            df_strikertotal = df_strikertotal[['playerName','team_name','age_today','minsPlayed total','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]
            df_strikertotal= df_strikertotal[df_strikertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_strikertotal = df_strikertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_strikertotal,hide_index=True)

    def Targetman():
        st.title('Targetman')
        df_striker = df_scouting[(df_scouting['player_position'] == 'Striker') & (df_scouting['player_positionSide'].str.contains('Centre'))]
        df_striker['minsPlayed'] = df_striker['minsPlayed'].astype(int)
        df_striker = df_striker[df_striker['minsPlayed'].astype(int) >= minutter_kamp]
        df_striker = df_striker[df_striker['age_today'].astype(int) <= alder]

        df_striker = calculate_score(df_striker,'Possession value total per_90','Possession value total score')
        df_striker = calculate_score(df_striker,'possessionValue.pvValue_per90', 'Possession value score')
        df_striker = calculate_score(df_striker,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_striker = calculate_score(df_striker, 'Passing %', 'Passing % score')
        df_striker = calculate_score(df_striker, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_striker = calculate_score(df_striker, 'Forward zone pass %', 'Forward zone pass % score')
        df_striker = calculate_score(df_striker, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_striker = calculate_score(df_striker, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_striker = calculate_score(df_striker, 'penAreaEntries_per90','penAreaEntries_per90 score')
        df_striker = calculate_score(df_striker, 'finalThird passes %','finalThird passes % score')
        df_striker = calculate_score(df_striker, 'shotFastbreak_per90','shotFastbreak_per90 score')
        df_striker = calculate_score(df_striker, 'bigChanceCreated_per90','bigChanceCreated_per90 score')
        df_striker = calculate_score(df_striker, 'dribble %','dribble % score')
        df_striker = calculate_score(df_striker, 'touches_in_box_per90','touches_in_box_per90 score')
        df_striker = calculate_score(df_striker, 'xA_per90','xA_per90 score')
        df_striker = calculate_score(df_striker, 'attemptsIbox_per90','attemptsIbox_per90 score')
        df_striker = calculate_score(df_striker, 'xg_per90','xg_per90 score')
        df_striker = calculate_score(df_striker, 'aerialWon','aerialWon score')


        df_striker['Linkup_play'] = df_striker[['Forward zone pass % score','Passing % score','Possession value score','penAreaEntries_per90 score','finalThirdEntries_per90 score','aerialWon score']].mean(axis=1)
        df_striker['Chance_creation'] = df_striker[['penAreaEntries_per90 score','Possession value total score','bigChanceCreated_per90 score','touches_in_box_per90 score','finalThirdEntries_per90 score']].mean(axis=1)
        df_striker['Goalscoring_'] = df_striker[['attemptsIbox_per90 score','xg_per90 score','xg_per90 score','xg_per90 score','xg_per90 score']].mean(axis=1)
        df_striker['Possession_value'] = df_striker[['Possession value total score','Possession value score','Possession value score','Possession value score']].mean(axis=1)

        df_striker = calculate_score(df_striker, 'Linkup_play', 'Linkup play')
        df_striker = calculate_score(df_striker, 'Chance_creation','Chance creation')
        df_striker = calculate_score(df_striker, 'Goalscoring_','Goalscoring')        
        df_striker = calculate_score(df_striker, 'Possession_value', 'Possession value')

        
        df_striker['Total score'] = df_striker[['Linkup play','Linkup play','Linkup play','Chance creation','Goalscoring','Goalscoring','Possession value','Possession value']].mean(axis=1)
        df_striker = df_striker[['playerName','team_name','label','minsPlayed','age_today','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]
        df_striker = df_striker.dropna()
        df_strikertotal = df_striker[['playerName','team_name','minsPlayed','age_today','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]

        df_strikertotal = df_strikertotal.groupby(['playerName','team_name','age_today']).mean().reset_index()
        minutter = df_striker.groupby(['playerName', 'team_name','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_strikertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_striker = df_striker.sort_values('Total score',ascending = False)
            st.dataframe(df_striker,hide_index=True)
        with st.expander('Total'):
            df_strikertotal = df_strikertotal[['playerName','team_name','age_today','minsPlayed total','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]
            df_strikertotal= df_strikertotal[df_strikertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_strikertotal = df_strikertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_strikertotal,hide_index=True)

    def Boxstriker():
        st.title('Boxstriker')
        df_striker = df_scouting[(df_scouting['player_position'] == 'Striker') & (df_scouting['player_positionSide'].str.contains('Centre'))]
        df_striker['minsPlayed'] = df_striker['minsPlayed'].astype(int)
        df_striker = df_striker[df_striker['minsPlayed'].astype(int) >= minutter_kamp]
        df_striker = df_striker[df_striker['age_today'].astype(int) <= alder]

        df_striker = calculate_score(df_striker,'Possession value total per_90','Possession value total score')
        df_striker = calculate_score(df_striker,'possessionValue.pvValue_per90', 'Possession value score')
        df_striker = calculate_score(df_striker,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_striker = calculate_score(df_striker, 'Passing %', 'Passing % score')
        df_striker = calculate_score(df_striker, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_striker = calculate_score(df_striker, 'Forward zone pass %', 'Forward zone pass % score')
        df_striker = calculate_score(df_striker, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_striker = calculate_score(df_striker, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_striker = calculate_score(df_striker, 'penAreaEntries_per90','penAreaEntries_per90 score')
        df_striker = calculate_score(df_striker, 'finalThird passes %','finalThird passes % score')
        df_striker = calculate_score(df_striker, 'shotFastbreak_per90','shotFastbreak_per90 score')
        df_striker = calculate_score(df_striker, 'bigChanceCreated_per90','bigChanceCreated_per90 score')
        df_striker = calculate_score(df_striker, 'dribble %','dribble % score')
        df_striker = calculate_score(df_striker, 'touches_in_box_per90','touches_in_box_per90 score')
        df_striker = calculate_score(df_striker, 'xA_per90','xA_per90 score')
        df_striker = calculate_score(df_striker, 'attemptsIbox_per90','attemptsIbox_per90 score')
        df_striker = calculate_score(df_striker, 'xg_per90','xg_per90 score')


        df_striker['Linkup_play'] = df_striker[['Forward zone pass % score','Passing % score','Possession value score','penAreaEntries_per90 score','finalThirdEntries_per90 score']].mean(axis=1)
        df_striker['Chance_creation'] = df_striker[['penAreaEntries_per90 score','Possession value total score','bigChanceCreated_per90 score','touches_in_box_per90 score','finalThirdEntries_per90 score']].mean(axis=1)
        df_striker['Goalscoring_'] = df_striker[['attemptsIbox_per90 score','xg_per90 score','xg_per90 score','xg_per90 score','xg_per90 score']].mean(axis=1)
        df_striker['Possession_value'] = df_striker[['Possession value total score','Possession value score','Possession value score','Possession value score']].mean(axis=1)

        df_striker = calculate_score(df_striker, 'Linkup_play', 'Linkup play')
        df_striker = calculate_score(df_striker, 'Chance_creation','Chance creation')
        df_striker = calculate_score(df_striker, 'Goalscoring_','Goalscoring')        
        df_striker = calculate_score(df_striker, 'Possession_value', 'Possession value')

        
        df_striker['Total score'] = df_striker[['Linkup play','Chance creation','Goalscoring','Goalscoring','Goalscoring','Goalscoring','Possession value','Possession value','Possession value']].mean(axis=1)
        df_striker = df_striker[['playerName','team_name','label','minsPlayed','age_today','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]
        df_striker = df_striker.dropna()
        df_strikertotal = df_striker[['playerName','team_name','minsPlayed','age_today','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]

        df_strikertotal = df_strikertotal.groupby(['playerName','team_name','age_today']).mean().reset_index()
        minutter = df_striker.groupby(['playerName', 'team_name','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_strikertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_striker = df_striker.sort_values('Total score',ascending = False)
            st.dataframe(df_striker,hide_index=True)
        with st.expander('Total'):
            df_strikertotal = df_strikertotal[['playerName','team_name','age_today','minsPlayed total','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]
            df_strikertotal= df_strikertotal[df_strikertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_strikertotal = df_strikertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_strikertotal,hide_index=True)

    overskrifter_til_menu = {
        'Ball playing central defender': ball_playing_central_defender,
        'Defending central defender': defending_central_defender,
        'Balanced central defender': balanced_central_defender,
        'Fullbacks': fullbacks,
        'Number 6': number6,
        'Number 6 (destroyer)': number6_destroyer,
        'Number 6 (double 6 forward)':number6_double_6_forward,
        'Number 8': number8,
        'Number 10': number10,
        'Winger' : winger,
        'Classic striker' : Classic_striker,
        'Targetman' : Targetman,
        'Boxstriker' : Boxstriker
        
    }

    selected_tabs = st.multiselect("Choose position profile", list(overskrifter_til_menu.keys()))

    for selected_tab in selected_tabs:
        overskrifter_til_menu[selected_tab]()

ligaer = {
    'BEL_First_Division_A_2023_2024': BEL_First_Division_A_2023_2024,
    'BEL_Challenger_Pro_League_2023_2024': Challenger_pro_league_23_24,
    'CZE_Czech_Liga_2023_2024' : Czech_liga_23_24,
    'DEU_3_Liga_2023_2024' : DEU_3_Liga_2023_2024,
    'DNK_Superliga_2023_2024' : DNK_Superliga_2023_2024_23_24,
    'DNK_1_Division_2023_2024' : DNK_1_Division_2023_2024,
    'DNK_1_Division_2024_2025' : DNK_1_Division_2024_2025,
    'FIN_Veikkausliiga_2024' : FIN_Veikkausliiga_2024_23_24,
    'FRA_Ligue_2_2023_2024' : Ligue_2_23_24,
    'HRV_HNL_2023_2024' : HRV_HNL_2023_2024_23_24,
    'ISL_Úrvalsdeild_2024' : ISL_Úrvalsdeild_2024_23_24,
    'ITA_Serie_B_2023_2024' : ITA_Serie_B_2023_2024,
    'ITA_Serie_B_2024_2025' : ITA_Serie_B_2024_2025,
    'NOR_Eliteserien_2024' : NOR_Eliteserien_2024_23_24,
    'NLD_Eredivisie_2023_2024' : NLD_Eredivisie_2023_2024_23_24,
    'NLD_Eerste_Divisie_2023_2024': Eerste_Divisie_23_24,
    'POL_Ekstraklasa_2023_2024' : POL_Ekstraklasa_2023_2024,
    'ROU_Liga_I_2023_2024': ROU_Liga_I_2023_2024,
    'SVK_Super_Liga_2023_2024': Super_liga_slovakia_23_24,
    'SRB_Super_Liga_2023_2024' : Super_liga_serbia_23_24,
    'SWE_Allsvenskan_2024' : SWE_Allsvenskan_2024,
    'USA_MLS_2024' : USA_MLS_2024_23_24,
    'USA_USL_Championship_2024' : USL_Championship_23_24,
}
selected_league = st.sidebar.radio('Choose league',list(ligaer.keys()))

ligaer[selected_league]()

if st.sidebar.button("Clear All"):
    # Clears all st.cache_resource caches:
    st.cache_resource.clear()
    st.cache_data.clear()
