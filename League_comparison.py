import pandas as pd
from pathlib import Path
import streamlit as st
# Base folder
st.set_page_config(layout="wide")

base_path = Path(r"C:\Users\Seamus-admin\Documents\GitHub\AC-Horsens-scouting")

# Find alle _matchstats-filer i undermapper
matchstats_files = list(base_path.rglob("matchstats_all*"))

# Læs og kombiner
dfs = []
for f in matchstats_files:
    df_temp = pd.read_csv(f)
    df_temp["source_file"] = f.name                 # bare filnavnet
    df_temp["source_folder"] = f.parent.name        # navnet på mappen, hvor filen ligger
    dfs.append(df_temp)

# Slå alt sammen
df_leagues = pd.concat(dfs, ignore_index=True)

print("Antal filer fundet:", len(matchstats_files))
print("Kombineret DataFrame shape:", df_leagues.shape)

df_leagues['league'] = df_leagues
df_leagues = df_leagues[~df_leagues['league_name'].str.contains('DBU', na=False)]
df_leagues = df_leagues[df_leagues['successfulOpenPlayPass'].notna()]
df_leagues = df_leagues.groupby(['league_name','label','date']).sum(numeric_only=True).round(2)

df_leagues = df_leagues.groupby("league_name").mean(numeric_only=True).round(2)
df_leagues = df_leagues.round(2)

st.dataframe(df_leagues)
