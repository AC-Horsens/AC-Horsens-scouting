import streamlit as st
import pandas as pd
import requests
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.express as px

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(layout="wide", page_title="League Comparison")
st.title("🏆 League Comparison Dashboard")

# ------------------------------------------------------------
# LOAD ALL LEAGUES AUTOMATICALLY
# ------------------------------------------------------------
@st.cache_data(show_spinner="Loading all leagues from GitHub…")
def load_all_leagues():
    """Fetch all league folders and load their matchstats CSVs."""
    base_url = "https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/"
    api_url = "https://api.github.com/repos/AC-Horsens/AC-Horsens-scouting/contents"

    # get league folders
    resp = requests.get(api_url)
    if resp.status_code != 200:
        st.error(f"Failed to fetch repo contents: {resp.status_code}")
        st.stop()
    contents = resp.json()
    league_folders = [x["name"] for x in contents if x["type"] == "dir"]

    dfs = []
    for league in league_folders:
        file_url = f"{base_url}{league}/matchstats_all%20{league}.csv"
        try:
            df = pd.read_csv(file_url)
            df["source_folder"] = league
            df["source_file"] = f"matchstats_all {league}.csv"
            dfs.append(df)
        except Exception as e:
            st.warning(f"⚠️ Could not load {league}: {e}")

    if not dfs:
        st.error("No league data could be loaded from GitHub.")
        st.stop()

    return pd.concat(dfs, ignore_index=True)


# ------------------------------------------------------------
# LOAD + CLEAN DATA
# ------------------------------------------------------------
df_leagues = load_all_leagues()

# basic cleaning
if "league_name" in df_leagues.columns:
    df_leagues = df_leagues[~df_leagues["league_name"].str.contains("DBU", na=False)]
if "successfulOpenPlayPass" in df_leagues.columns:
    df_leagues = df_leagues[df_leagues["successfulOpenPlayPass"].notna()]

# aggregate by league
df_leagues = (
    df_leagues.groupby(["league_name", "label", "date"])
    .sum(numeric_only=True)
    .round(2)
)
df_leagues = df_leagues.groupby("league_name").mean(numeric_only=True).round(2)

# ------------------------------------------------------------
# DISPLAY TABLE
# ------------------------------------------------------------
st.subheader("📊 League Averages")
st.dataframe(df_leagues, use_container_width=True)

# ------------------------------------------------------------
# SIMILARITY ANALYSIS
# ------------------------------------------------------------
st.subheader("🤝 Find Similar Leagues")

metric_choice = st.radio(
    "Choose similarity metric:",
    ["euclidean", "manhattan", "cosine"],
    horizontal=True,
)

selected_league = st.selectbox("Select a league:", df_leagues.index)

if selected_league:
    X = df_leagues.fillna(0)
    nn = NearestNeighbors(n_neighbors=6, metric=metric_choice)
    nn.fit(X)

    idx = df_leagues.index.get_loc(selected_league)
    distances, indices = nn.kneighbors([X.iloc[idx].values])

    similar = df_leagues.iloc[indices[0]].copy()
    similar["similarity_score"] = distances[0]
    similar = similar.drop(selected_league, errors="ignore")

    st.write(f"Leagues similar to **{selected_league}** ({metric_choice} distance):")
    st.dataframe(similar, use_container_width=True)

# ------------------------------------------------------------
# PCA VISUALIZATION
# ------------------------------------------------------------
st.subheader("🧭 League Visualization (PCA Projection)")

X = df_leagues.fillna(0)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

df_plot = pd.DataFrame(
    {"PC1": X_pca[:, 0], "PC2": X_pca[:, 1], "league_name": df_leagues.index}
)

# Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_plot["PC1"], df_plot["PC2"], s=80, alpha=0.7)
for i, txt in enumerate(df_plot["league_name"]):
    ax.annotate(txt, (df_plot["PC1"][i], df_plot["PC2"][i]), fontsize=8)
ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")
ax.set_title("League Similarity Visualization (PCA Projection)")
st.pyplot(fig)

# Plotly
fig2 = px.scatter(
    df_plot,
    x="PC1",
    y="PC2",
    text="league_name",
    title="League Similarity Visualization (PCA Projection)",
    width=900,
    height=600,
)
fig2.update_traces(textposition="top center")
st.plotly_chart(fig2, use_container_width=True)
