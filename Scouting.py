import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import requests
import urllib.parse
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import linregress
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import plotly.express as px

st.set_page_config(layout='wide')

repo_url = "https://api.github.com/repos/AC-Horsens/AC-Horsens-scouting/contents/"

# Get list of folders (leagues)

response = requests.get(repo_url)
repo_content = response.json()
@st.cache_data(ttl=3600)
def get_leagues():
    repo_url = "https://api.github.com/repos/AC-Horsens/AC-Horsens-scouting/contents"
    headers = {"Authorization": f"token {st.secrets['github_token']}"}

    response = requests.get(repo_url, headers=headers)

    if response.status_code != 200:
        st.error(f"GitHub API error: {response.status_code}")
        return []

    try:
        repo_content = response.json()
    except Exception as e:
        st.error(f"Could not parse GitHub JSON: {e}")
        return []

    if not isinstance(repo_content, list):
        st.error("GitHub response was not a list — possibly rate-limited or malformed.")
        st.write(repo_content)
        return []

    return [item['name'] for item in repo_content if item.get('type') == 'dir']


leagues = get_leagues()

# Define base URL for loading CSV files
base_url = "https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/"
def Process_data(df_possession_xa,df_pv,df_matchstats,df_xg,squads):
    if df_pv is df_possession_xa:
        required_cols = ['playerName', 'team_name', 'label']
        for col in required_cols:
            if col not in df_pv.columns:
                df_pv[col] = 'UNKNOWN'
        if '318.0' not in df_pv.columns:
            raise ValueError("No xA column in fallback possession_xa data")
        df_pv['possessionValue.pvValue'] = df_pv['xA'].astype(float)
        df_pv['possessionValue.pvAdded'] = df_pv['xA'].astype(float)


    def weighted_mean(scores, weights):
        expanded_scores = []
        for score, weight in zip(scores, weights):
            expanded_scores.extend([score] * weight)
        return np.mean(expanded_scores)

    def calculate_score(df, column, score_column):
        df_unique = df.drop_duplicates(column).copy()
        df_unique.loc[:, score_column] = pd.qcut(df_unique[column], q=10, labels=False, duplicates='drop') + 1
        return df.merge(df_unique[[column, score_column]], on=column, how='left')

    def calculate_opposite_score(df, column, score_column):
        df_unique = df.drop_duplicates(column).copy()
        df_unique.loc[:, score_column] = pd.qcut(-df_unique[column], q=10, labels=False, duplicates='drop') + 1
        return df.merge(df_unique[[column, score_column]], on=column, how='left')

    def player_performance_profile(df_position, position_title='Player'):
        """Display individual player performance chart and table for a specific position."""
        with st.expander('Choose player'):
            players = sorted(df_position['playerName'].unique())
            selected_player = st.selectbox('Choose player', players)
            df = df_position[df_position['playerName'] == selected_player]
            df = df.sort_values('date',ascending = True)

            exclude_cols = ['playerName', 'team_name', 'player_position', 'player_positionSide',
                            'minsPlayed', 'label', 'date', 'age_today']

            metrics_df = df.drop(columns=exclude_cols, errors='ignore')
            metrics_df['label'] = df['label']

            melted_df = metrics_df.melt(id_vars='label', var_name='Metric', value_name='Value')

            fig = px.line(
                melted_df,
                x='label',
                y='Value',
                color='Metric',
                markers=True,
                title=f'Performance profile as {position_title}'
            )

            # Highlight "Total score"
            fig.for_each_trace(
                lambda trace: trace.update(line=dict(width=5, color='yellow')) if trace.name == 'Total score'
                else trace.update(line=dict(width=1))
            )

            # Background performance zones
            fig.update_layout(
                yaxis=dict(range=[0, 10]),
                shapes=[
                    dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=0, y1=4,
                        fillcolor="rgba(255, 0, 0, 0.1)", line=dict(width=0)),
                    dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=4, y1=6,
                        fillcolor="rgba(255, 255, 0, 0.15)", line=dict(width=0)),
                    dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=6, y1=10,
                        fillcolor="rgba(0, 255, 0, 0.1)", line=dict(width=0)),
                ]
            )

            # 3-game rolling average + regression for Total score
            total_df = melted_df[melted_df['Metric'] == 'Total score'].copy().reset_index(drop=True)
            total_df['rolling_avg'] = total_df['Value'].rolling(window=3, min_periods=1).mean()
            total_df['index'] = total_df.index

            regression_df = total_df.dropna(subset=['rolling_avg'])

            if not regression_df.empty and len(regression_df) >= 2:
                slope, intercept, *_ = linregress(regression_df['index'], regression_df['rolling_avg'])
                regression_df['regression_line'] = intercept + slope * regression_df['index']

                fig.add_trace(
                    go.Scatter(
                        x=regression_df['label'],
                        y=regression_df['rolling_avg'],
                        mode='lines+markers',
                        name='3-game rolling avg (Total score)',
                        line=dict(color='blue', width=3, dash='dot')
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=regression_df['label'],
                        y=regression_df['regression_line'],
                        mode='lines',
                        name='Regression on rolling avg',
                        line=dict(color='black', width=2)
                    )
                )

            st.plotly_chart(fig, use_container_width=True)            
            df = df.sort_values('date',ascending = False)
            st.dataframe(df,use_container_width=True,hide_index=True)

    col1,col2,col3 = st.columns(3)
    with col1:
        minutter_kamp = st.number_input('Minutes per match')
    with col2:
        minutter_total = st.number_input('Minutes total')
    with col3:
        alder = st.number_input('Max age',value=25)

    df_possession_xa = df_possession_xa.rename(columns={'318.0': 'xA'})
    df_possession_xa_summed = df_possession_xa.groupby(['playerName','label'])['xA'].sum().reset_index()

    df_pv = df_pv[['playerName', 'team_name', 'label', 'possessionValue.pvValue', 'possessionValue.pvAdded']]
    df_pv.loc[:, 'possessionValue.pvValue'] = df_pv['possessionValue.pvValue'].astype(float)
    df_pv.loc[:, 'possessionValue.pvAdded'] = df_pv['possessionValue.pvAdded'].astype(float)
    df_pv['possessionValue'] = df_pv['possessionValue.pvValue'] + df_pv['possessionValue.pvAdded']
    df_kamp = df_pv.groupby(['playerName', 'label', 'team_name']).sum()

    df_kamp = df_kamp.reset_index()
    df_matchstats = df_matchstats[['player_matchName','player_playerId','contestantId','duelLost','aerialLost','player_position','player_positionSide','successfulOpenPlayPass','totalContest','duelWon','penAreaEntries','accurateBackZonePass','possWonDef3rd','wonContest','accurateFwdZonePass','openPlayPass','totalBackZonePass','minsPlayed','fwdPass','finalThirdEntries','ballRecovery','totalFwdZonePass','successfulFinalThirdPasses','totalFinalThirdPasses','attAssistOpenplay','aerialWon','totalAttAssist','possWonMid3rd','interception','totalCrossNocorner','interceptionWon','attOpenplay','touchesInOppBox','attemptsIbox','totalThroughBall','possWonAtt3rd','accurateCrossNocorner','bigChanceCreated','accurateThroughBall','totalLayoffs','accurateLayoffs','totalFastbreak','shotFastbreak','formationUsed','goals','label','match_id','date','possLostAll']]
    df_matchstats = df_matchstats.rename(columns={'player_matchName': 'playerName'})
    df_scouting = df_matchstats.merge(df_kamp)
    def calculate_match_pv(df_scouting):
        # Calculate the total match_xg for each match_id
        df_scouting['match_pv'] = df_scouting.groupby('match_id')['possessionValue.pvValue'].transform('sum')
        
        # Calculate the total team_xg for each team in each match
        df_scouting['team_pv'] = df_scouting.groupby(['contestantId', 'match_id'])['possessionValue.pvValue'].transform('sum')
        
        # Calculate opponents_xg as match_xg - team_xg
        df_scouting['opponents_pv'] = df_scouting['match_pv'] - df_scouting['team_pv']
        df_scouting['opponents_pv'] = pd.to_numeric(df_scouting['opponents_pv'], errors='coerce')
        return df_scouting
    df_scouting = calculate_match_pv(df_scouting)
    
    df_xg = df_xg[['contestantId','team_name','playerName','playerId','321','322','9','match_id','label','date']]
    df_xg = df_xg[df_xg['9']!= True]
    df_xg = df_xg.rename(columns={'321': 'xg'})
    df_xg = df_xg.rename(columns={'322': 'post shot xg'})
    df_xg['xg'] = df_xg['xg'].astype(float)
    df_xg['post shot xg'] = df_xg['post shot xg'].astype(float)
    df_xg = df_xg.fillna(0)
    df_xg = df_xg.groupby(['playerName','playerId','match_id','contestantId','team_name','label','date']).sum()
    df_xg = df_xg.reset_index()

    df_scouting = df_scouting.rename(columns={'player_playerId': 'playerId'})
    df_scouting = df_scouting.merge(df_xg, how='left', on=['playerName', 'playerId', 'match_id', 'contestantId', 'team_name', 'label', 'date']).reset_index()
    df_scouting['label'] = df_scouting['label'] + ' ' + df_scouting['date']
    def calculate_match_goals(df_scouting):
        # Calculate the total match_xg for each match_id
        df_scouting['match_goals'] = df_scouting.groupby('match_id')['goals'].transform('sum')
        
        # Calculate the total team_xg for each team in each match
        df_scouting['team_goals'] = df_scouting.groupby(['contestantId', 'match_id'])['goals'].transform('sum')
        
        # Calculate opponents_xg as match_xg - team_xg
        df_scouting['opponents_goals'] = df_scouting['match_goals'] - df_scouting['team_goals']
        df_scouting['opponents_goals'] = pd.to_numeric(df_scouting['opponents_goals'], errors='coerce')
       
        return df_scouting

    def calculate_match_xg(df_scouting):
        # Calculate the total match_xg for each match_id
        df_scouting['match_xg'] = df_scouting.groupby('match_id')['xg'].transform('sum')
        
        # Calculate the total team_xg for each team in each match
        df_scouting['team_xg'] = df_scouting.groupby(['contestantId', 'match_id'])['xg'].transform('sum')
        
        # Calculate opponents_xg as match_xg - team_xg
        df_scouting['opponents_xg'] = df_scouting['match_xg'] - df_scouting['team_xg']
        df_scouting['opponents_xg'] = pd.to_numeric(df_scouting['opponents_xg'], errors='coerce')
       
        return df_scouting

    def calculate_match_post_shot_xg(df_scouting):
        # Calculate the total match_xg for each match_id
        df_scouting['match_post_shot_xg'] = df_scouting.groupby('match_id')['post shot xg'].transform('sum')
        
        # Calculate the total team_xg for each team in each match
        df_scouting['team_post_shot_xg'] = df_scouting.groupby(['contestantId', 'match_id'])['post shot xg'].transform('sum')
        
        # Calculate opponents_xg as match_xg - team_xg
        df_scouting['opponents_post_shot_xg'] = df_scouting['match_post_shot_xg'] - df_scouting['team_post_shot_xg']
        df_scouting['opponents_post_shot_xg'] = pd.to_numeric(df_scouting['opponents_post_shot_xg'], errors='coerce')
       
        return df_scouting


    df_scouting = calculate_match_xg(df_scouting)
    df_scouting = calculate_match_goals(df_scouting)
    df_scouting = calculate_match_post_shot_xg(df_scouting)

    df_scouting = df_scouting.merge(df_possession_xa_summed, how='left')
    def calculate_match_xa(df_scouting):
        # Calculate the total match_xg for each match_id
        df_scouting['match_xA'] = df_scouting.groupby('match_id')['xA'].transform('sum')
        
        # Calculate the total team_xg for each team in each match
        df_scouting['team_xA'] = df_scouting.groupby(['contestantId', 'match_id'])['xA'].transform('sum')
        
        # Calculate opponents_xg as match_xg - team_xg
        df_scouting['opponents_xA'] = df_scouting['match_xA'] - df_scouting['team_xA']
        df_scouting['opponents_xA'] = pd.to_numeric(df_scouting['opponents_xA'], errors='coerce')
        
        return df_scouting
    df_scouting = calculate_match_xa(df_scouting)
    
    df_scouting.fillna(0, inplace=True)
    squads['dateOfBirth'] = pd.to_datetime(squads['dateOfBirth'])
    today = datetime.today()
    squads['age_today'] = ((today - squads['dateOfBirth']).dt.days / 365.25).apply(np.floor)
    squads = squads[['id','matchName','nationality','dateOfBirth','age_today']]
    squads = squads.rename(columns={'id': 'playerId'})
    squads = squads.rename(columns={'matchName': 'playerName'})
    squads.fillna(0,inplace=True)

    df_scouting = df_scouting.merge(squads,how='outer')
    df_scouting = df_scouting.drop_duplicates(subset=['playerName', 'team_name', 'player_position', 'player_positionSide', 'label'])
    df_scouting['post_shot_xg_per90'] = (df_scouting['post shot xg'].astype(float) / df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['xg_per90'] = (df_scouting['xg'].astype(float) / df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['xA_per90'] = (df_scouting['xA'].astype(float) / df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['Pv_added_stoppere'] = df_scouting['possessionValue.pvValue'].astype(float).loc[df_scouting['possessionValue.pvValue'].astype(float) < 0.1]
    df_scouting['Pv_added_stoppere_per90'] = (df_scouting['Pv_added_stoppere'].astype(float) / df_scouting['minsPlayed'].astype(float)) * 90
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
    df_scouting['Forward zone pass_per90'] = (df_scouting['accurateFwdZonePass'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['Back zone pass %'] = (df_scouting['accurateBackZonePass'].astype(float) / df_scouting['totalBackZonePass'].astype(float)) * 100
    df_scouting['Back zone pass_per90'] = (df_scouting['accurateBackZonePass'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['Passing %'] = (df_scouting['successfulOpenPlayPass'].astype(float) / df_scouting['openPlayPass'].astype(float)) * 100
    df_scouting['Passes_per90'] = (df_scouting['successfulOpenPlayPass'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['Duels_per90'] = (df_scouting['duelWon'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['Aerial duel %'] = (df_scouting['aerialWon'].astype(float) / (df_scouting['aerialWon'].astype(float) + df_scouting['aerialLost'].astype(float))) * 100
    df_scouting['Ballrecovery_per90'] = (df_scouting['ballRecovery'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['fwdPass_per90'] = (df_scouting['fwdPass'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['finalthirdpass_per90'] = (df_scouting['successfulFinalThirdPasses'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['shotFastbreak_per90'] = (df_scouting['shotFastbreak'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['bigChanceCreated_per90'] = (df_scouting['bigChanceCreated'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['dribble %'] = (df_scouting['wonContest'].astype(float) / df_scouting['totalContest'].astype(float)) * 100
    df_scouting['dribble_per90'] = (df_scouting['wonContest'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['touches_in_box_per90'] = (df_scouting['touchesInOppBox'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['totalThroughBall_per90'] = (df_scouting['totalThroughBall'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['attemptsIbox_per90'] = (df_scouting['attemptsIbox'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['aerialWon_per90'] = (df_scouting['aerialWon'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['possLost_per90'] = (df_scouting['possLostAll'].astype(float)/df_scouting['minsPlayed'].astype(float)) * 90
    df_scouting['Goals saved'] = (df_scouting['opponents_post_shot_xg'].astype(float) - df_scouting['opponents_goals'].astype(float))
    df_scouting.fillna(0, inplace=True)

    def Goalkeeper():
        st.title('Goalkeeper')
        Goalkeeper = df_scouting[(df_scouting['player_position'] == 'Goalkeeper')]
        Goalkeeper = Goalkeeper[['playerName','team_name','minsPlayed','age_today','Back zone pass %','Goals saved']]
        Goalkeeper['minsPlayed'] = Goalkeeper['minsPlayed'].astype(int)
        Goalkeeper = Goalkeeper[Goalkeeper['minsPlayed'].astype(int) >= minutter_kamp]
        Goalkeeper = Goalkeeper[Goalkeeper['age_today'].astype(int) >= alder]
        Goalkeeper = Goalkeeper.groupby(
            ['playerName','team_name', 'age_today']
        ).agg({
            'minsPlayed':'sum',
            'Back zone pass %': 'mean',
            'Goals saved': 'sum'
        }).reset_index()
        Goalkeeper = Goalkeeper[Goalkeeper['minsPlayed'].astype(int) >= minutter_total]
        st.dataframe(Goalkeeper,hide_index=True)

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
        df_spillende_stopper = df_spillende_stopper[['playerName','team_name','player_position','label','date','minsPlayed','age_today','Passing','Forward passing','Defending','Possession value added score','Total score']] 
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

        df_balanced_central_defender = df_balanced_central_defender[df_balanced_central_defender['minsPlayed'].astype(int) >= minutter_kamp]
        df_balanced_central_defender = calculate_opposite_score(df_balanced_central_defender,'opponents_pv', 'opponents pv score')
        df_balanced_central_defender = calculate_opposite_score(df_balanced_central_defender,'opponents_xg', 'opponents xg score')
        df_balanced_central_defender = calculate_opposite_score(df_balanced_central_defender,'opponents_xA', 'opponents xA score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'duels won %', 'duels won % score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Duels_per90', 'duelWon score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Ballrecovery_per90', 'ballRecovery score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Aerial duel %', 'Aerial duel % score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'aerialWon_per90', 'Aerial duel score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender,'Pv_added_stoppere_per90', 'Possession value added score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Passing %', 'Open play passing % score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Passes_per90', 'Passing score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Back zone pass %', 'Back zone pass % score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Back zone pass_per90', 'Back zone pass score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Forward zone pass %', 'Forward zone pass % score')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Forward zone pass_per90', 'Forward zone pass score')
        df_balanced_central_defender = calculate_opposite_score(df_balanced_central_defender,'possLost_per90','possLost per90 score')

        df_balanced_central_defender['Defending'] = df_balanced_central_defender[['duels won % score','duels won % score','duelWon score','opponents pv score','opponents xg score','opponents xA score','opponents pv score','opponents xg score','opponents xA score','Aerial duel % score','Aerial duel % score','Aerial duel score', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score', 'ballRecovery score']].mean(axis=1)
        df_balanced_central_defender['Possession value added'] = df_balanced_central_defender[['Possession value added score','possLost per90 score']].mean(axis=1)
        df_balanced_central_defender['Passing'] = df_balanced_central_defender[['Open play passing % score','Passing score', 'Back zone pass % score','Back zone pass score','Back zone pass % score','Back zone pass score','Back zone pass % score','Back zone pass score','possLost per90 score','possLost per90 score']].mean(axis=1)
        
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Defending', 'Defending_')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Passing', 'Passing_')
        df_balanced_central_defender = calculate_score(df_balanced_central_defender, 'Possession value added', 'Possession_value_added')

        df_balanced_central_defender['Total score'] = df_balanced_central_defender.apply(
            lambda row: weighted_mean(
                [row['Defending_'], row['Passing_'], row['Possession_value_added']],
                [
                    7 if row['Defending_'] < 3 else 5,
                    4 if row['Passing_'] < 3 else 3,
                    1 if row['Possession_value_added'] < 3 else 1
                ]
            ),
            axis=1
        )
        df_balanced_central_defender = df_balanced_central_defender[['playerName','team_name','player_position','label','date','minsPlayed','age_today','Defending_','Possession_value_added','Passing_','Total score']]
        
        df_balanced_central_defendertotal = df_balanced_central_defender[['playerName','team_name','player_position','minsPlayed','age_today','Defending_','Possession_value_added','Passing_','Total score']]
        df_balanced_central_defendertotal = df_balanced_central_defendertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_balanced_central_defender.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_balanced_central_defendertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_balanced_central_defender = df_balanced_central_defender.sort_values('date',ascending = False)
            st.dataframe(df_balanced_central_defender,hide_index=True)
        with st.expander('Total'):
            df_balanced_central_defendertotal = df_balanced_central_defendertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Defending_','Possession_value_added','Passing_','Total score']]
            df_balanced_central_defendertotal = df_balanced_central_defendertotal[df_balanced_central_defendertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_balanced_central_defendertotal = df_balanced_central_defendertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_balanced_central_defendertotal,hide_index=True)
        player_performance_profile(df_balanced_central_defender, position_title='Central defender')

    def fullbacks():
        st.title('Fullbacks')
        mask = (
        (df_scouting['player_position'] == 'Defender') &
        (df_scouting['player_positionSide'].isin(['Right', 'Left'])))
        
        df_backs = df_scouting[mask].copy()
        df_backs['minsPlayed'] = df_backs['minsPlayed'].astype(int)
        df_backs = df_backs[df_backs['minsPlayed'].astype(int) >= minutter_kamp]
        df_backs = df_backs[df_backs['age_today'].astype(int) <= alder]

        df_backs = calculate_opposite_score(df_backs,'opponents_pv', 'opponents pv score')
        df_backs = calculate_opposite_score(df_backs,'opponents_xg', 'opponents xg score')
        df_backs = calculate_opposite_score(df_backs,'opponents_xA', 'opponents xA score')

        df_backs = calculate_score(df_backs,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_backs = calculate_score(df_backs, 'duels won %', 'duels won % score')
        df_backs = calculate_score(df_backs, 'Duels_per90', 'Duels per 90 score')
        df_backs = calculate_score(df_backs, 'Forward zone pass %', 'Forward zone pass % score')
        df_backs = calculate_score(df_backs, 'Forward zone pass_per90', 'Forward zone pass per 90 score')
        df_backs = calculate_score(df_backs, 'penAreaEntries_per90&crosses%shotassists', 'Penalty area entries & crosses & shot assists score')
        df_backs = calculate_score(df_backs, 'attAssistOpenplay_per90', 'attAssistOpenplay_per90 score')
        df_backs = calculate_score(df_backs, 'finalThird passes %', 'finalThird passes % score')
        df_backs = calculate_score(df_backs, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_backs = calculate_score(df_backs, 'interception_per90', 'interception_per90 score')
        df_backs = calculate_score(df_backs, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_backs = calculate_score(df_backs, 'Back zone pass %', 'Back zone pass % score')
        df_backs = calculate_score(df_backs, 'Back zone pass_per90', 'Back zone pass_per90 score')
        df_backs = calculate_score(df_backs, 'totalCrossNocorner_per90', 'totalCrossNocorner_per90 score')
        df_backs = calculate_score(df_backs, 'xA_per90', 'xA per90 score')
        df_backs = calculate_opposite_score(df_backs,'possLost_per90', 'possLost_per90 score')
        
        df_backs['Defending'] = df_backs[['opponents pv score','opponents xg score','opponents xA score','duels won % score','Duels per 90 score','Duels per 90 score','duels won % score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score']].mean(axis=1)
        df_backs['Passing'] = df_backs[['Forward zone pass % score','Forward zone pass per 90 score','finalThird passes % score','finalThirdEntries_per90 score','Back zone pass % score','Back zone pass_per90 score','Possession value added score','possLost_per90 score','possLost_per90 score']].mean(axis=1)
        df_backs['Chance creation'] = df_backs[['Penalty area entries & crosses & shot assists score','totalCrossNocorner_per90 score','xA per90 score','xA per90 score','finalThirdEntries_per90 score','finalThirdEntries_per90 score','Forward zone pass % score','Forward zone pass per 90 score','Forward zone pass per 90 score','Forward zone pass % score','Possession value added score','Possession value added score']].mean(axis=1)
        df_backs['Possession value added'] = df_backs[['Possession value added score','possLost_per90 score']].mean(axis=1)
        
        df_backs = calculate_score(df_backs, 'Defending', 'Defending_')
        df_backs = calculate_score(df_backs, 'Passing', 'Passing_')
        df_backs = calculate_score(df_backs, 'Chance creation','Chance_creation')
        df_backs = calculate_score(df_backs, 'Possession value added', 'Possession_value_added')
        
        df_backs['Total score'] = df_backs.apply(
            lambda row: weighted_mean(
                [row['Defending_'], row['Passing_'], row['Chance_creation'], row['Possession_value_added']],
                [3 if row['Defending_'] < 3 else 3, 3 if row['Passing_'] < 2 else 1, 6 if row['Chance_creation'] > 3 else 2, 3 if row['Possession_value_added'] < 3 else 2]
            ), axis=1
        )        
        df_backs = df_backs[['playerName','team_name','player_position','player_positionSide','label','date','minsPlayed','age_today','Defending_','Passing_','Chance_creation','Possession_value_added','Total score']]
        df_backs = df_backs.dropna()
        df_backstotal = df_backs[['playerName','team_name','player_position','player_positionSide','minsPlayed','age_today','Defending_','Passing_','Chance_creation','Possession_value_added','Total score']]
        df_backstotal = df_backstotal.groupby(['playerName','team_name','player_position','player_positionSide','age_today']).mean().reset_index()
        minutter = df_backs.groupby(['playerName', 'team_name','player_position','player_positionSide','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_backstotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_backs = df_backs.sort_values('date',ascending = False)
            st.dataframe(df_backs,hide_index=True)
        with st.expander('Total'):
            df_backstotal = df_backstotal[['playerName','team_name','player_position','player_positionSide','age_today','minsPlayed total','Defending_','Passing_','Chance_creation','Possession_value_added','Total score']]
            df_backstotal = df_backstotal[df_backstotal['minsPlayed total'].astype(int) >= minutter_total]
            df_backstotal = df_backstotal.sort_values('Total score',ascending = False)
            st.dataframe(df_backstotal,hide_index=True)
        player_performance_profile(df_backs, position_title='Fullback')

    def wingbacks():
        st.title('Wingbacks')
        mask = (
        ((df_scouting['formationUsed'].isin([532, 541])) &
        (df_scouting['player_position'] == 'Defender') &
        (df_scouting['player_positionSide'].isin(['Right', 'Left'])))
        |
        ((df_scouting['formationUsed'].isin([352, 343,3421])) &
        (df_scouting['player_position'] == 'Midfielder') &
        (df_scouting['player_positionSide'].isin(['Right', 'Left'])))
        |
        (df_scouting['player_position'] == 'Wing Back') &
        (df_scouting['player_positionSide'].isin(['Right', 'Left'])))
        

        df_backs = df_scouting[mask].copy()
        df_backs['minsPlayed'] = df_backs['minsPlayed'].astype(int)
        df_backs = df_backs[df_backs['minsPlayed'].astype(int) >= minutter_kamp]
        df_backs = df_backs[df_backs['age_today'].astype(int) <= alder]

        df_backs = calculate_opposite_score(df_backs,'opponents_pv', 'opponents pv score')
        df_backs = calculate_opposite_score(df_backs,'opponents_xg', 'opponents xg score')
        df_backs = calculate_opposite_score(df_backs,'opponents_xA', 'opponents xA score')

        df_backs = calculate_score(df_backs,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_backs = calculate_score(df_backs, 'duels won %', 'duels won % score')
        df_backs = calculate_score(df_backs, 'Duels_per90', 'Duels per 90 score')
        df_backs = calculate_score(df_backs, 'Forward zone pass %', 'Forward zone pass % score')
        df_backs = calculate_score(df_backs, 'Forward zone pass_per90', 'Forward zone pass per 90 score')
        df_backs = calculate_score(df_backs, 'penAreaEntries_per90&crosses%shotassists', 'Penalty area entries & crosses & shot assists score')
        df_backs = calculate_score(df_backs, 'attAssistOpenplay_per90', 'attAssistOpenplay_per90 score')
        df_backs = calculate_score(df_backs, 'finalThird passes %', 'finalThird passes % score')
        df_backs = calculate_score(df_backs, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_backs = calculate_score(df_backs, 'interception_per90', 'interception_per90 score')
        df_backs = calculate_score(df_backs, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_backs = calculate_score(df_backs, 'Back zone pass %', 'Back zone pass % score')
        df_backs = calculate_score(df_backs, 'Back zone pass_per90', 'Back zone pass_per90 score')
        df_backs = calculate_score(df_backs, 'totalCrossNocorner_per90', 'totalCrossNocorner_per90 score')
        df_backs = calculate_score(df_backs, 'xA_per90', 'xA per90 score')
        df_backs = calculate_opposite_score(df_backs,'possLost_per90', 'possLost_per90 score')
        
        df_backs['Defending'] = df_backs[['opponents pv score','opponents xg score','opponents xA score','duels won % score','Duels per 90 score','Duels per 90 score','duels won % score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score']].mean(axis=1)
        df_backs['Passing'] = df_backs[['Forward zone pass % score','Forward zone pass per 90 score','finalThird passes % score','finalThirdEntries_per90 score','Back zone pass % score','Back zone pass_per90 score','Possession value added score','possLost_per90 score','possLost_per90 score']].mean(axis=1)
        df_backs['Chance creation'] = df_backs[['Penalty area entries & crosses & shot assists score','totalCrossNocorner_per90 score','xA per90 score','xA per90 score','finalThirdEntries_per90 score','finalThirdEntries_per90 score','Forward zone pass % score','Forward zone pass per 90 score','Forward zone pass per 90 score','Forward zone pass % score','Possession value added score','Possession value added score']].mean(axis=1)
        df_backs['Possession value added'] = df_backs[['Possession value added score','possLost_per90 score']].mean(axis=1)
        
        df_backs = calculate_score(df_backs, 'Defending', 'Defending_')
        df_backs = calculate_score(df_backs, 'Passing', 'Passing_')
        df_backs = calculate_score(df_backs, 'Chance creation','Chance_creation')
        df_backs = calculate_score(df_backs, 'Possession value added', 'Possession_value_added')
        
        df_backs['Total score'] = df_backs.apply(
            lambda row: weighted_mean(
                [row['Defending_'], row['Passing_'], row['Chance_creation'], row['Possession_value_added']],
                [3 if row['Defending_'] < 3 else 5, 1 if row['Passing_'] < 2 else 1, 6 if row['Chance_creation'] > 3 else 2, 3 if row['Possession_value_added'] < 3 else 2]
            ), axis=1
        )

        df_backs = df_backs[['playerName','team_name','player_position','player_positionSide','label','date','minsPlayed','age_today','Defending_','Passing_','Chance_creation','Possession_value_added','Total score']]
        df_backs = df_backs.dropna()
        df_backstotal = df_backs[['playerName','team_name','player_position','player_positionSide','minsPlayed','age_today','Defending_','Passing_','Chance_creation','Possession_value_added','Total score']]
        df_backstotal = df_backstotal.groupby(['playerName','team_name','player_position','player_positionSide','age_today']).mean().reset_index()
        minutter = df_backs.groupby(['playerName', 'team_name','player_position','player_positionSide','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_backstotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_backs = df_backs.sort_values('date',ascending = False)
            st.dataframe(df_backs,hide_index=True)
        with st.expander('Total'):
            df_backstotal = df_backstotal[['playerName','team_name','player_position','player_positionSide','age_today','minsPlayed total','Defending_','Passing_','Chance_creation','Possession_value_added','Total score']]
            df_backstotal = df_backstotal[df_backstotal['minsPlayed total'].astype(int) >= minutter_total]
            df_backstotal = df_backstotal.sort_values('Total score',ascending = False)
            st.dataframe(df_backstotal,hide_index=True)
        player_performance_profile(df_backs, position_title='Fullback')

    def number6():
        st.title('Number 6')
        df_sekser = df_scouting[((df_scouting['player_position'] == 'Defensive Midfielder') | (df_scouting['player_position'] == 'Midfielder')) & df_scouting['player_positionSide'].str.contains('Centre')]
        df_sekser['minsPlayed'] = df_sekser['minsPlayed'].astype(int)
        df_sekser = df_sekser[df_sekser['minsPlayed'].astype(int) >= minutter_kamp]
        df_sekser = df_sekser[df_sekser['age_today'].astype(int) <= alder]

        df_sekser = calculate_score(df_sekser,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_sekser = calculate_score(df_sekser, 'duels won %', 'duels won % score')
        df_sekser = calculate_score(df_sekser, 'Duels_per90', 'Duels per 90 score')
        df_sekser = calculate_score(df_sekser, 'Passing %', 'Passing % score')
        df_sekser = calculate_score(df_sekser, 'Passes_per90', 'Passing score')
        df_sekser = calculate_score(df_sekser, 'Back zone pass %', 'Back zone pass % score')
        df_sekser = calculate_score(df_sekser, 'Back zone pass_per90', 'Back zone pass_per90 score')
        df_sekser = calculate_score(df_sekser, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_sekser = calculate_score(df_sekser, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_sekser = calculate_score(df_sekser, 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90', 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90 score')
        df_sekser = calculate_score(df_sekser, 'Forward zone pass %', 'Forward zone pass % score')
        df_sekser = calculate_score(df_sekser, 'Forward zone pass_per90', 'Forward zone pass_per90 score')
        df_sekser = calculate_score(df_sekser, 'Ballrecovery_per90', 'ballRecovery score')
        df_sekser = calculate_opposite_score(df_sekser, 'possLost_per90', 'possLost_per90 score')

        
        df_sekser['Defending'] = df_sekser[['duels won % score','Duels per 90 score','Duels per 90 score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score','ballRecovery score']].mean(axis=1)
        df_sekser['Passing'] = df_sekser[['Back zone pass % score','Back zone pass_per90 score','Passing % score','Passing score','possLost_per90 score','possLost_per90 score']].mean(axis=1)
        df_sekser['Progressive ball movement'] = df_sekser[['Possession value added score','Possession value added score','Forward zone pass % score','Forward zone pass_per90 score','finalThirdEntries_per90 score']].mean(axis=1)
        df_sekser['Possession value added'] = df_sekser[['Possession value added score','possLost_per90 score']].mean(axis=1)
        
        df_sekser = calculate_score(df_sekser, 'Defending', 'Defending_')
        df_sekser = calculate_score(df_sekser, 'Passing', 'Passing_')
        df_sekser = calculate_score(df_sekser, 'Progressive ball movement','Progressive_ball_movement')
        df_sekser = calculate_score(df_sekser, 'Possession value added', 'Possession_value_added')
        
        df_sekser['Total score'] = df_sekser.apply(
        lambda row: weighted_mean(
            [row['Defending_'], row['Passing_'],row['Progressive_ball_movement'],row['Possession_value_added']],
            [3 if row['Defending_'] < 5 else 5, 3 if row['Passing_'] < 5 else 4, 3 if row['Progressive_ball_movement'] < 5 else 2, 1 if row['Possession_value_added'] < 5 else 1]
        ), axis=1
        )

        df_sekser = df_sekser[['playerName','team_name','player_position','label','date','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]
        df_sekser = df_sekser.dropna()
        df_seksertotal = df_sekser[['playerName','team_name','player_position','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]

        df_seksertotal = df_seksertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_sekser.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_seksertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_sekser = df_sekser.sort_values('date',ascending = False)
            st.dataframe(df_sekser,hide_index=True)
        with st.expander('Total'):
            df_seksertotal = df_seksertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Defending_','Passing_','Progressive_ball_movement','Possession_value_added','Total score']]
            df_seksertotal= df_seksertotal[df_seksertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_seksertotal = df_seksertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_seksertotal,hide_index=True)
        player_performance_profile(df_sekser, position_title='Number 6')

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
        player_performance_profile(df_sekser, position_title='Number 6 (destroyer)')

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
        df_otter = calculate_score(df_otter,'Duels_per90', 'Duels per 90 score')
        df_otter = calculate_score(df_otter, 'Passing %', 'Passing % score')
        df_otter = calculate_score(df_otter, 'Passes_per90', 'Passing score')
        df_otter = calculate_score(df_otter, 'Back zone pass %', 'Back zone pass % score')
        df_otter = calculate_score(df_otter, 'Back zone pass_per90', 'Back zone pass score')
        df_otter = calculate_score(df_otter, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_otter = calculate_score(df_otter, 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90', 'possWonDef3rd_possWonMid3rd_per90&interceptions_per90 score')
        df_otter = calculate_score(df_otter, 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90', 'possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90 score')
        df_otter = calculate_score(df_otter, 'Forward zone pass %', 'Forward zone pass % score')
        df_otter = calculate_score(df_otter, 'Forward zone pass_per90', 'Forward zone pass score')
        df_otter = calculate_score(df_otter, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_otter = calculate_score(df_otter, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_otter = calculate_score(df_otter, 'penAreaEntries_per90','penAreaEntries_per90 score')
        df_otter = calculate_opposite_score(df_otter, 'possLost_per90', 'possLost_per90 score')
        df_otter = calculate_score(df_otter, 'xA_per90','xA_per90 score')

        df_otter['Defending'] = df_otter[['duels won % score','Duels per 90 score','possWonDef3rd_possWonMid3rd_possWonAtt3rd_per90 score']].mean(axis=1)
        df_otter['Passing'] = df_otter[['Forward zone pass % score','Forward zone pass score','Passing % score','Passing score','possLost_per90 score']].mean(axis=1)
        df_otter['Progressive ball movement'] = df_otter[['xA_per90 score','fwd_Pass_per90 score','penAreaEntries_per90 score','Forward zone pass % score','Forward zone pass score','finalThirdEntries_per90 score','Possession value total score','possLost_per90 score']].mean(axis=1)
        df_otter['Possession value'] = df_otter[['Possession value added score','Possession value total score','possLost_per90 score']].mean(axis=1)
        
        df_otter = calculate_score(df_otter, 'Defending', 'Defending_')
        df_otter = calculate_score(df_otter, 'Passing', 'Passing_')
        df_otter = calculate_score(df_otter, 'Progressive ball movement','Progressive_ball_movement')
        df_otter = calculate_score(df_otter, 'Possession value', 'Possession_value')
        
        df_otter['Total score'] = df_otter.apply(
            lambda row: weighted_mean(
                [row['Defending_'], row['Passing_'], row['Progressive_ball_movement'], row['Possession_value']],
                [5 if row['Defending_'] > 5 else 1, 5 if row['Passing_'] > 5 else 1, 
                1 if row['Progressive_ball_movement'] < 5 else 3, 1 if row['Possession_value'] < 5 else 3]
            ), axis=1
        )
        df_otter = df_otter[['playerName','team_name','player_position','label','date','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value','Total score']]
        df_otter = df_otter.dropna()

        df_ottertotal = df_otter[['playerName','team_name','player_position','minsPlayed','age_today','Defending_','Passing_','Progressive_ball_movement','Possession_value','Total score']]

        df_ottertotal = df_ottertotal.groupby(['playerName','team_name','player_position','age_today']).mean().reset_index()
        minutter = df_otter.groupby(['playerName', 'team_name','player_position','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_ottertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_otter = df_otter.sort_values('date',ascending = False)
            st.dataframe(df_otter,hide_index=True)
        with st.expander('Total'):
            df_ottertotal = df_ottertotal[['playerName','team_name','player_position','age_today','minsPlayed total','Defending_','Passing_','Progressive_ball_movement','Possession_value','Total score']]
            df_ottertotal= df_ottertotal[df_ottertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_ottertotal = df_ottertotal.sort_values('Total score',ascending = False)
            st.dataframe(df_ottertotal,hide_index=True)

        player_performance_profile(df_otter, position_title='Number 8')

    def number10():
        st.title('Number 10')
        mask = (
            (
                (df_scouting['formationUsed'].isin([343, 3421, 541, 4231, 4321])) &
                (df_scouting['player_position'].isin(['Attacking Midfielder', 'Striker'])) &
                (df_scouting['player_positionSide'].isin(['Centre/Right', 'Left/Centre']))
            )
            |
            (
                (df_scouting['player_position'] == 'Attacking Midfielder') &
                (df_scouting['player_positionSide'].isin(['Centre','Centre/Right','Left/Centre']))
            )
        )

        df_10 = df_scouting[mask].copy()


        df_10['minsPlayed'] = df_10['minsPlayed'].astype(int)
        df_10 = df_10[df_10['minsPlayed'].astype(int) >= minutter_kamp]
        df_10 = df_10[df_10['age_today'].astype(int) <= alder]

        df_10 = calculate_score(df_10,'Possession value total per_90','Possession value total score')
        df_10 = calculate_score(df_10,'possessionValue.pvValue_per90', 'Possession value score')
        df_10 = calculate_score(df_10,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_10 = calculate_score(df_10, 'Passing %', 'Passing % score')
        df_10 = calculate_score(df_10, 'Passes_per90', 'Passing score')
        df_10 = calculate_score(df_10, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_10 = calculate_score(df_10, 'Forward zone pass %', 'Forward zone pass % score')
        df_10 = calculate_score(df_10, 'Forward zone pass_per90', 'Forward zone pass score')
        df_10 = calculate_score(df_10, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_10 = calculate_score(df_10, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_10 = calculate_score(df_10, 'penAreaEntries_per90','penAreaEntries_per90 score')
        df_10 = calculate_score(df_10, 'finalThird passes %','finalThird passes % score')
        df_10 = calculate_score(df_10, 'finalthirdpass_per90', 'finalthirdpass per 90 score')
        df_10 = calculate_score(df_10, 'dribble %','dribble % score')
        df_10 = calculate_score(df_10, 'dribble_per90','dribble score')
        df_10 = calculate_score(df_10, 'touches_in_box_per90','touches_in_box_per90 score')
        df_10 = calculate_score(df_10, 'xA_per90','xA_per90 score')
        df_10 = calculate_score(df_10, 'xg_per90','xg_per90 score')
        df_10 = calculate_opposite_score(df_10,'possLost_per90', 'possLost_per90 score')
        df_10 = calculate_score(df_10, 'post_shot_xg_per90','post_shot_xg_per90 score')


        df_10['Passing'] = df_10[['Forward zone pass % score','Forward zone pass score','Passing % score','Passing score']].mean(axis=1)
        df_10['Chance creation'] = df_10[['attAssistOpenplay_per90 score','penAreaEntries_per90 score','Forward zone pass % score','Forward zone pass score','finalThird passes % score','finalthirdpass per 90 score','Possession value total score','Possession value score','dribble % score','touches_in_box_per90 score','xA_per90 score']].mean(axis=1)
        df_10['Goalscoring'] = df_10[['xg_per90 score','xg_per90 score','xg_per90 score','post_shot_xg_per90 score','touches_in_box_per90 score']].mean(axis=1)
        df_10['Possession value'] = df_10[['Possession value total score','Possession value total score','Possession value added score','Possession value score','possLost_per90 score']].mean(axis=1)
                
        df_10 = calculate_score(df_10, 'Passing', 'Passing_')
        df_10 = calculate_score(df_10, 'Chance creation','Chance_creation')
        df_10 = calculate_score(df_10, 'Goalscoring','Goalscoring_')        
        df_10 = calculate_score(df_10, 'Possession value', 'Possession_value')
        
        df_10['Total score'] = df_10.apply(
            lambda row: weighted_mean(
                [row['Passing_'], row['Chance_creation'], row['Goalscoring_'], row['Possession_value']],
                [3 if row['Passing_'] > 5 else 1, 5 if row['Chance_creation'] > 5 else 1, 
                5 if row['Goalscoring_'] > 5 else 1, 3 if row['Possession_value'] < 5 else 1]
            ), axis=1
        )

        # Prepare final output
        df_10 = df_10[['playerName','team_name','label','date','minsPlayed','age_today','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]
        df_10 = df_10.fillna(1)
        df_10total = df_10[['playerName','team_name','minsPlayed','age_today','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]

        df_10total = df_10total.groupby(['playerName','team_name','age_today']).mean().reset_index()
        minutter = df_10.groupby(['playerName', 'team_name','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_10total['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_10 = df_10.sort_values('date',ascending = False)
            st.dataframe(df_10,hide_index=True)
        with st.expander('Total'):
            df_10total = df_10total[['playerName','team_name','age_today','minsPlayed total','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]
            df_10total= df_10total[df_10total['minsPlayed total'].astype(int) >= minutter_total]
            df_10total = df_10total.sort_values('Total score',ascending = False)
            st.dataframe(df_10total,hide_index=True)
        player_performance_profile(df_10, position_title='Number 10')

    def winger():
        st.title('Winger')
        mask = (
            ((df_scouting['formationUsed'].isin([442,541,451,4141])) &
            (df_scouting['player_position'] == 'Midfielder') &
            (df_scouting['player_positionSide'].isin(['Right', 'Left'])))
            |
            ((df_scouting['formationUsed'].isin([433])) &
            (df_scouting['player_position'] == 'Striker') &
            (df_scouting['player_positionSide'].isin(['Left/Centre', 'Centre/Right'])))
            |
            (df_scouting['player_position'].isin(['Attacking Midfielder', 'Striker'])) &
            (df_scouting['player_positionSide'].isin(['Right', 'Left'])))        

        df_10 = df_scouting[mask].copy()

        df_10['minsPlayed'] = df_10['minsPlayed'].astype(int)
        df_10 = df_10[df_10['minsPlayed'].astype(int) >= minutter_kamp]
        df_10 = df_10[df_10['age_today'].astype(int) <= alder]

        df_10 = calculate_score(df_10,'Possession value total per_90','Possession value total score')
        df_10 = calculate_score(df_10,'possessionValue.pvValue_per90', 'Possession value score')
        df_10 = calculate_score(df_10,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_10 = calculate_score(df_10, 'Passing %', 'Passing % score')
        df_10 = calculate_score(df_10, 'Passes_per90', 'Passing score')
        df_10 = calculate_score(df_10, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_10 = calculate_score(df_10, 'Forward zone pass %', 'Forward zone pass % score')
        df_10 = calculate_score(df_10, 'Forward zone pass_per90', 'Forward zone pass score')
        df_10 = calculate_score(df_10, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_10 = calculate_score(df_10, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_10 = calculate_score(df_10, 'penAreaEntries_per90','penAreaEntries_per90 score')
        df_10 = calculate_score(df_10, 'finalThird passes %','finalThird passes % score')
        df_10 = calculate_score(df_10, 'finalthirdpass_per90', 'finalthirdpass per 90 score')
        df_10 = calculate_score(df_10, 'dribble %','dribble % score')
        df_10 = calculate_score(df_10, 'dribble_per90', 'dribble score')
        df_10 = calculate_score(df_10, 'touches_in_box_per90','touches_in_box_per90 score')
        df_10 = calculate_score(df_10, 'xA_per90','xA_per90 score')
        df_10 = calculate_score(df_10, 'attemptsIbox_per90','attemptsIbox_per90 score')
        df_10 = calculate_score(df_10, 'xg_per90','xg_per90 score')
        df_10 = calculate_score(df_10, 'post_shot_xg_per90','post_shot_xg_per90 score')


        df_10['Passing'] = df_10[['Forward zone pass % score','Forward zone pass score','Passing % score','Passing score']].mean(axis=1)
        df_10['Chance creation'] = df_10[['attAssistOpenplay_per90 score','penAreaEntries_per90 score','Forward zone pass % score','Forward zone pass score','finalThird passes % score','finalthirdpass per 90 score','Possession value total score','Possession value score','dribble % score','dribble score','touches_in_box_per90 score','xA_per90 score']].mean(axis=1)
        df_10['Goalscoring'] = df_10[['xg_per90 score','xg_per90 score','xg_per90 score','touches_in_box_per90 score','post_shot_xg_per90 score']].mean(axis=1)
        df_10['Possession value'] = df_10[['Possession value total score','Possession value total score','Possession value added score','Possession value score','Possession value score','Possession value score']].mean(axis=1)
                
        df_10 = calculate_score(df_10, 'Passing', 'Passing_')
        df_10 = calculate_score(df_10, 'Chance creation','Chance_creation')
        df_10 = calculate_score(df_10, 'Goalscoring','Goalscoring_')        
        df_10 = calculate_score(df_10, 'Possession value', 'Possession_value')
        
        df_10['Total score'] = df_10.apply(
            lambda row: weighted_mean(
                [row['Passing_'], row['Chance_creation'], row['Goalscoring_'], row['Possession_value']],
                [3 if row['Passing_'] > 5 else 1, 5 if row['Chance_creation'] > 5 else 1, 
                5 if row['Goalscoring_'] > 5 else 1, 3 if row['Possession_value'] > 5 else 1]
            ), axis=1
        )
        df_10 = df_10[['playerName','team_name','label','date','minsPlayed','age_today','Passing_','Chance_creation','Goalscoring_','Possession_value','Total score']]
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
        player_performance_profile(df_10, position_title='Winger')

    def Classic_striker():
        st.title('Classic striker')
        mask = (
        ((df_scouting['formationUsed'].isin([532,442,352,3142,3412])) &
        (df_scouting['player_position'] == 'Striker') &
        (df_scouting['player_positionSide'].str.contains('Centre')))
        |
        (df_scouting['player_position'] == 'Striker') &
        (df_scouting['player_positionSide'] == 'Centre'))

        df_striker = df_scouting[mask].copy()
        df_striker['minsPlayed'] = df_striker['minsPlayed'].astype(int)
        df_striker = df_striker[df_striker['minsPlayed'].astype(int) >= minutter_kamp]
        df_striker = df_striker[df_striker['age_today'].astype(int) <= alder]

        df_striker = calculate_score(df_striker,'Possession value total per_90','Possession value total score')
        df_striker = calculate_score(df_striker,'possessionValue.pvValue_per90', 'Possession value score')
        df_striker = calculate_score(df_striker,'possessionValue.pvAdded_per90', 'Possession value added score')
        df_striker = calculate_score(df_striker, 'Passing %', 'Passing % score')
        df_striker = calculate_score(df_striker, 'Passes_per90', 'Passing score')
        df_striker = calculate_score(df_striker, 'finalThirdEntries_per90', 'finalThirdEntries_per90 score')
        df_striker = calculate_score(df_striker, 'Forward zone pass %', 'Forward zone pass % score')
        df_striker = calculate_score(df_striker, 'Forward zone pass_per90', 'Forward zone pass score')
        df_striker = calculate_score(df_striker, 'fwdPass_per90', 'fwd_Pass_per90 score')
        df_striker = calculate_score(df_striker, 'attAssistOpenplay_per90','attAssistOpenplay_per90 score')
        df_striker = calculate_score(df_striker, 'penAreaEntries_per90','penAreaEntries_per90 score')
        df_striker = calculate_score(df_striker, 'finalThird passes %','finalThird passes % score')
        df_striker = calculate_score(df_striker, 'finalthirdpass_per90','finalThird passes per90 score')
        df_striker = calculate_score(df_striker, 'shotFastbreak_per90','shotFastbreak_per90 score')
        df_striker = calculate_score(df_striker, 'dribble %','dribble % score')
        df_striker = calculate_score(df_striker, 'dribble_per90', 'dribble_per90 score')
        df_striker = calculate_score(df_striker, 'touches_in_box_per90','touches_in_box_per90 score')
        df_striker = calculate_score(df_striker, 'xA_per90','xA_per90 score')
        df_striker = calculate_score(df_striker, 'attemptsIbox_per90','attemptsIbox_per90 score')
        df_striker = calculate_score(df_striker, 'xg_per90','xg_per90 score')
        df_striker = calculate_score(df_striker, 'post_shot_xg_per90','post_shot_xg_per90 score')

        df_striker['Linkup_play'] = df_striker[['Forward zone pass % score','Forward zone pass score','Passing % score','Passing score','Possession value score','penAreaEntries_per90 score','finalThirdEntries_per90 score']].mean(axis=1)
        df_striker['Chance_creation'] = df_striker[['penAreaEntries_per90 score','Possession value total score','touches_in_box_per90 score','finalThirdEntries_per90 score']].mean(axis=1)
        df_striker['Goalscoring_'] = df_striker[['post_shot_xg_per90','xg_per90 score','xg_per90 score','xg_per90 score']].mean(axis=1)
        df_striker['Possession_value'] = df_striker[['Possession value total score','Possession value score','Possession value score','Possession value score']].mean(axis=1)

        df_striker = calculate_score(df_striker, 'Linkup_play', 'Linkup play')
        df_striker = calculate_score(df_striker, 'Chance_creation','Chance creation')
        df_striker = calculate_score(df_striker, 'Goalscoring_','Goalscoring')        
        df_striker = calculate_score(df_striker, 'Possession_value', 'Possession value')

        df_striker['Total score'] = df_striker.apply(
            lambda row: weighted_mean(
                [row['Linkup play'], row['Chance creation'], row['Goalscoring'], row['Possession value']],
                [3 if row['Linkup play'] > 5 else 1, 3 if row['Chance creation'] > 5 else 1, 
                5 if row['Goalscoring'] > 5 else 2, 3 if row['Possession value'] < 5 else 1]
            ), axis=1
        )        
        df_striker = df_striker[['playerName','team_name','label','date','minsPlayed','age_today','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]
        df_striker = df_striker.fillna(1)

        df_strikertotal = df_striker[['playerName','team_name','minsPlayed','age_today','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]

        df_strikertotal = df_strikertotal.groupby(['playerName','team_name','age_today']).mean().reset_index()
        minutter = df_striker.groupby(['playerName', 'team_name','age_today'])['minsPlayed'].sum().astype(float).reset_index()
        df_strikertotal['minsPlayed total'] = minutter['minsPlayed']
        with st.expander('Game by game'):
            df_striker = df_striker.sort_values('date',ascending = False)
            df_striker = df_striker.round(2)
            st.dataframe(df_striker,hide_index=True)
        with st.expander('Total'):
            df_strikertotal = df_strikertotal[['playerName','team_name','age_today','minsPlayed total','Linkup play','Chance creation','Goalscoring','Possession value','Total score']]
            df_strikertotal= df_strikertotal[df_strikertotal['minsPlayed total'].astype(int) >= minutter_total]
            df_strikertotal = df_strikertotal.sort_values('Total score',ascending = False)
            df_strikertotal = df_strikertotal.round(2)
            st.dataframe(df_strikertotal,hide_index=True)
        player_performance_profile(df_striker, position_title='Striker')


    overskrifter_til_menu = {
        'Goalkeeper':Goalkeeper,
        'Balanced central defender': balanced_central_defender,
        'Fullbacks': fullbacks,
        'Wingbacks': wingbacks,
        'Number 6': number6,
        'Number 6 (destroyer)': number6_destroyer,
        'Number 8': number8,
        'Number 10': number10,
        'Winger' : winger,
        'Classic striker' : Classic_striker,
        
    }


    selected_tabs = st.multiselect("Choose position profile", list(overskrifter_til_menu.keys()))

    for selected_tab in selected_tabs:
        overskrifter_til_menu[selected_tab]()

def process_league_data(league_name):
    folder = f"{base_url}{league_name}/"

    def build_url(file_type):
        # Handles space in filename by encoding it
        file_name = f"{file_type} {league_name}.csv"
        encoded_file_name = urllib.parse.quote(file_name)
        return f"{folder}{encoded_file_name}"

    try:
        try:
            df_pv = pd.read_csv(build_url('pv_all'))
        except Exception:
            df_pv = None

        df_possession_xa = pd.read_csv(build_url('xA_all'))
        df_matchstats = pd.read_csv(build_url('matchstats_all'))
        df_xg = pd.read_csv(build_url('xg_all'))
        squads = pd.read_csv(build_url('squads'))
    except Exception as e:
        st.error(f"❌ Failed to load data files for {league_name}: {e}")
        return

    # Fallback: Use df_possession_xa if df_pv is None
    if df_pv is None:
        required_cols = ['playerName', 'team_name', 'label']
        for col in required_cols:
            if col not in df_possession_xa.columns:
                df_possession_xa[col] = 'UNKNOWN'
        if '318.0' not in df_possession_xa.columns:
            st.error("No xA column in xA_all, cannot fallback to possession value data.")
            return
        df_pv = df_possession_xa[required_cols + ['318.0']].copy()
        df_pv['possessionValue.pvValue'] = df_pv['318.0'].astype(float)
        df_pv['possessionValue.pvAdded'] = df_pv['318.0'].astype(float)
        df_pv = df_pv.drop(columns=['318.0'])

    Process_data(df_possession_xa, df_pv, df_matchstats, df_xg, squads)


    
    # Process the data (assuming Process_data is defined)


selected_league = st.sidebar.radio('Choose league', leagues)

process_league_data(selected_league)

position_metrics = {
    "Goalkeeper": ["Back zone pass %", "Goals saved"],
    "Balanced central defender": ["duels won %","Aerial duel %","Ballrecovery_per90",
                                  "interception_per90","Passing %","Forward zone pass %"],
    "Fullbacks": ["duels won %","Duels_per90","Forward zone pass %","Forward zone pass_per90",
                  "penAreaEntries_per90","xA_per90","totalCrossNocorner_per90"],
    "Wingbacks": ["duels won %","Forward zone pass %","penAreaEntries_per90",
                  "xA_per90","totalCrossNocorner_per90","finalThirdEntries_per90"],
    "Number 6": ["Passing %","Passes_per90","Forward zone pass %","Forward zone pass_per90",
                 "finalThirdEntries_per90","Ballrecovery_per90",
                 "possWonDef3rd_possWonMid3rd_per90&interceptions_per90"],
    "Number 6 (destroyer)": ["duels won %","Ballrecovery_per90","Forward zone pass %",
                             "Passing %","Back zone pass %"],
    "Number 8": ["Passing %","Passes_per90","Forward zone pass %","fwdPass_per90",
                 "finalThirdEntries_per90","Ballrecovery_per90","xA_per90"],
    "Number 10": ["xg_per90","post_shot_xg_per90","xA_per90","dribble_per90",
                  "touches_in_box_per90","finalthirdpass_per90","penAreaEntries_per90"],
    "Winger": ["dribble_per90","touches_in_box_per90","xA_per90","xg_per90",
               "finalThirdEntries_per90","penAreaEntries_per90"],
    "Classic striker": ["xg_per90","post_shot_xg_per90","touches_in_box_per90",
                        "attemptsIbox_per90","Passing %","Forward zone pass %"]
}

def player_similarity_across_leagues():
    st.title("Player similarity across leagues")

    # 1. Vælg position
    pos_choice = st.selectbox("Choose position profile", list(position_metrics.keys()))
    metrics = position_metrics[pos_choice]

    # 2. Saml data på tværs af ligaer
    all_leagues_data = []
    for league in leagues:
        folder = f"{base_url}{league}/"
        try:
            df = pd.read_csv(f"{folder}matchstats_all%20{league}.csv")
            df["league"] = league
            all_leagues_data.append(df)
        except Exception as e:
            st.warning(f"Kunne ikke loade {league}: {e}")
    
    if not all_leagues_data:
        st.error("Ingen ligaer kunne indlæses")
        return

    df_all = pd.concat(all_leagues_data, ignore_index=True)

    # 3. Filtrér på spillere med nok minutter
    df_all = df_all[df_all["minsPlayed"] > 300]

    # 4. Brug kun de valgte metrics
    df_all = df_all.dropna(subset=metrics)
    if df_all.empty:
        st.warning("Ingen spillere matcher disse metrics.")
        return

    # 5. Vælg reference spiller
    players = sorted(df_all["playerName"].unique())
    selected_player = st.selectbox("Choose reference player", players)

    # 6. Kør similarity-model
    if st.button("Find similar players"):
        ref_idx = df_all[df_all["playerName"] == selected_player].index[0]
        X = df_all[metrics].fillna(0)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        nn = NearestNeighbors(n_neighbors=6, metric="euclidean")
        nn.fit(X_scaled)

        distances, indices = nn.kneighbors([X_scaled[ref_idx]])
        similar_players = df_all.iloc[indices[0]][["playerName","team_name","league","player_position"] + metrics]

        # 7. Output tabel
        st.subheader(f"Players most similar to {selected_player} ({pos_choice})")
        st.dataframe(similar_players, use_container_width=True, hide_index=True)

        # 8. Radarplot
        melted = similar_players.melt(id_vars=["playerName"], value_vars=metrics,
                                      var_name="Metric", value_name="Value")
        fig = px.line_polar(melted, r="Value", theta="Metric", color="playerName", line_close=True)
        st.plotly_chart(fig, use_container_width=True)

# --- Sidebar integration ---
if st.sidebar.button("Player similarity (ML)"):
    player_similarity_across_leagues()

if st.sidebar.button("Clear All"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()
