import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import requests
import urllib.parse

def load_league_comparison():
    url = "https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/league%20comparison%20data.csv"
    encoded_url = urllib.parse.quote(url, safe=":/")
    df_leagues = pd.read_csv(encoded_url)
    return df_leagues

df_leagues = load_league_comparison()

st.dataframe(df_leagues)
