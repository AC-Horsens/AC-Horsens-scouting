import streamlit as st
import pandas as pd

def load_match_stats():
    url = 'https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/DNK_1_Division_2024_2025/matchstats_all%20DNK_1_Division_2024_2025.csv'
    match_stats = pd.read_csv(url)
    match_stats['label'] = (match_stats['label'] + ' ' + match_stats['date'])
    match_stats = match_stats[match_stats['team_name']]
    return match_stats

def load_match_stats1():
    url = 'https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/DNK_1_Division_2023_2024/matchstats_all%20DNK_1_Division_2023_2024.csv'
    match_stats = pd.read_csv(url)
    match_stats['label'] = (match_stats['label'] + ' ' + match_stats['date'])
    return match_stats

def load_match_stats2():
    url = 'https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/DNK_Superliga_2023_2024/matchstats_all%20DNK_Superliga_2023_2024.csv'
    match_stats = pd.read_csv(url)
    match_stats['label'] = (match_stats['label'] + ' ' + match_stats['date'])
    return match_stats

def load_match_stats3():
    url = 'https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/DNK_Superliga_2024_2025/matchstats_all%20DNK_Superliga_2024_2025.csv'
    match_stats = pd.read_csv(url)
    match_stats['label'] = (match_stats['label'] + ' ' + match_stats['date'])
    return match_stats


match_stats = load_match_stats()
match_stats1 = load_match_stats1()
match_stats2 = load_match_stats2()
match_stats3 = load_match_stats3()

match_stats = pd.concat([match_stats, match_stats1, match_stats2, match_stats3])

st.dataframe(match_stats)
