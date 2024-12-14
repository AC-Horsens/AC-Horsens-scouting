import streamlit as st
import pandas as pd


st.set_page_config(layout='wide')

def load_league_comparison():
    url = "https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/league%20comparison%20data.csv"
    df_leagues = pd.read_csv(url)
    return df_leagues

df_leagues = load_league_comparison()
df_leagues = df_leagues[~df_leagues['league_name'].str.contains('DBU', na=False)]
df_leagues = df_leagues[df_leagues['successfulOpenPlayPass'].notna()]

df_leagues = df_leagues.drop(columns=['label','date','league_name'])

df_country = df_leagues.drop(columns='schema')
df_country = df_country.groupby('country').mean()
df_country = df_country.round(2)

df_leagues = df_leagues.drop(columns='country')
df_leagues = df_leagues.groupby('schema').mean()
df_leagues = df_leagues.round(2)

st.dataframe(df_country)
st.dataframe(df_leagues)
