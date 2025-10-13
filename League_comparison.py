import streamlit as st
import pandas as pd
import requests
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide", page_title="League Comparison")

# --- Load and prepare data ---
@st.cache_data(show_spinner="Loading league data from GitHub...")
def load_league_data():
    base_url = "https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/"
    api_url = "https://api.github.com/repos/AC-Horsens/AC-Horsens-scouting/contents"

    # Get all folders (leagues) from GitHub repo
    response = requests.get(api_url)
    if response.status_code != 200:
        st.error(f"Failed to fetch repo contents: {response.status_code}")
        st.stop()

    repo_contents = response.json()
    league_folders = [item["name"] for item in repo_contents if item["type"] == "dir"]

    dfs = []
    for league in league_folders:
        # Build URL to each matchstats file
        file_url = f"{base_url}{league}/matchstats_all%20{league}.csv"
        try:
            df_temp = pd.read_csv(file_url)
            df_temp["source_file"] = f"matchstats_all {league}.csv"
            df_temp["source_folder"] = league
            dfs.append(df_temp)
        except Exception as e:
            st.warning(f"⚠️ Could not load data for {league}: {e}")

    if not dfs:
        st.error("❌ No league data could be loaded. Check GitHub repo structure.")
        st.stop()

    df_leagues = pd.concat(dfs, ignore_index=True)
    return df_leagues


# Load and clean data
df_leagues = load_league_data()

# Filter out DBU and missing values
if "league_name" in df_leagues.columns:
    df_leagues = df_leagues[~df_leagues["league_name"].str.contains("DBU", na=False)]
if "successfulOpenPlayPass" in df_leagues.columns:
    df_leagues = df_leagues[df_leagues["successfulOpenPlayPass"].notna()]

# Aggregate data
df_leagues = (
    df_leagues.groupby(["league_name", "label", "date"])
    .sum(numeric_only=True)
    .round(2)
)
df_leagues = df_leagues.groupby("league_name").mean(numeric_only=True).round(2)

# --- Step 1: Show all leagues ---
st.subheader("🏆 League Averages")
st.dataframe(df_leagues, use_container_width=True)

# --- Step 2: Similarity analysis ---
st.subheader("🤝 Find Similar Leagues")

metric_choice = st.radio("Choose similarity metric:", ["euclidean", "manhattan", "cosine"])
selected_league = st.selectbox("Select a league:", df_leagues.index)

if selected_league:
    X = df_leagues.fillna(0)

    nn = NearestNeighbors(n_neighbors=6, metric=metric_choice)
    nn.fit(X)

    selected_idx = df_leagues.index.get_loc(selected_league)
    distances, indices = nn.kneighbors([X.iloc[selected_idx].values])

    similar_leagues = df_leagues.iloc[indices[0]].copy()
    similar_leagues["similarity_score"] = distances[0]

    # Drop the league itself
    similar_leagues = similar_leagues.drop(selected_league, errors="ignore")

    st.write(f"Leagues similar to **{selected_league}** ({metric_choice} distance):")
    st.dataframe(similar_leagues, use_container_width=True)

# --- Step 3: Visualization ---
st.subheader("📊 League Visualization (PCA Projection)")

X = df_leagues.fillna(0)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

df_plot = pd.DataFrame({
    "PC1": X_pca[:, 0],
    "PC2": X_pca[:, 1],
    "league_name": df_leagues.index
})

# Matplotlib scatter
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_plot["PC1"], df_plot["PC2"], s=80, alpha=0.7)
for i, txt in enumerate(df_plot["league_name"]):
    ax.annotate(txt, (df_plot["PC1"][i], df_plot["PC2"][i]), fontsize=8)
ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")
ax.set_title("League similarity visualization (PCA projection)")
st.pyplot(fig)

# Plotly scatter
fig2 = px.scatter(
    df_plot,
    x="PC1",
    y="PC2",
    text="league_name",
    title="League similarity visualization (PCA projection)",
    width=900,
    height=600,
)
fig2.update_traces(textposition="top center")
st.plotly_chart(fig2, use_container_width=True)
