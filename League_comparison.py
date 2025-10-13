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
# DATA LOADING (lazy, cached)
# ------------------------------------------------------------
@st.cache_data(show_spinner="Fetching league data from GitHub...")
def load_league_data(selected_leagues):
    """Download matchstats files for selected leagues from GitHub."""
    base_url = "https://raw.githubusercontent.com/AC-Horsens/AC-Horsens-scouting/main/"
    dfs = []

    for league in selected_leagues:
        file_url = f"{base_url}{league}/matchstats_all%20{league}.csv"
        try:
            df_temp = pd.read_csv(file_url)
            df_temp["source_folder"] = league
            dfs.append(df_temp)
        except Exception as e:
            st.warning(f"⚠️ Could not load data for {league}: {e}")

    if not dfs:
        st.error("❌ No data could be loaded for the selected leagues.")
        st.stop()

    df = pd.concat(dfs, ignore_index=True)
    return df


def get_league_folders():
    """Fetch all league folders dynamically from GitHub API."""
    api_url = "https://api.github.com/repos/AC-Horsens/AC-Horsens-scouting/contents"
    response = requests.get(api_url)
    if response.status_code != 200:
        st.error(f"Failed to fetch repo contents: {response.status_code}")
        return []
    contents = response.json()
    return [item["name"] for item in contents if item["type"] == "dir"]


# ------------------------------------------------------------
# USER INPUT — select leagues
# ------------------------------------------------------------
with st.expander("⚙️ Select leagues to include"):
    all_leagues = get_league_folders()
    selected_leagues = st.multiselect(
        "Select one or more leagues to analyze:",
        options=all_leagues,
        default=all_leagues[:3] if all_leagues else [],
    )

load_button = st.button("🚀 Load League Data")

# ------------------------------------------------------------
# LOAD DATA only after button click
# ------------------------------------------------------------
if load_button and selected_leagues:
    df_leagues = load_league_data(selected_leagues)

    # --- Clean + Aggregate ---
    if "league_name" in df_leagues.columns:
        df_leagues = df_leagues[~df_leagues["league_name"].str.contains("DBU", na=False)]
    if "successfulOpenPlayPass" in df_leagues.columns:
        df_leagues = df_leagues[df_leagues["successfulOpenPlayPass"].notna()]

    df_leagues = (
        df_leagues.groupby(["league_name", "label", "date"])
        .sum(numeric_only=True)
        .round(2)
    )
    df_leagues = df_leagues.groupby("league_name").mean(numeric_only=True).round(2)

    # --------------------------------------------------------
    # DISPLAY LEAGUE TABLE
    # --------------------------------------------------------
    st.subheader("📊 League Averages")
    st.dataframe(df_leagues, use_container_width=True)

    # --------------------------------------------------------
    # SIMILARITY ANALYSIS
    # --------------------------------------------------------
    st.subheader("🤝 Find Similar Leagues")

    metric_choice = st.radio(
        "Choose similarity metric:", ["euclidean", "manhattan", "cosine"]
    )
    selected_league = st.selectbox("Select a league:", df_leagues.index)

    if selected_league:
        X = df_leagues.fillna(0)
        nn = NearestNeighbors(n_neighbors=6, metric=metric_choice)
        nn.fit(X)

        selected_idx = df_leagues.index.get_loc(selected_league)
        distances, indices = nn.kneighbors([X.iloc[selected_idx].values])

        similar_leagues = df_leagues.iloc[indices[0]].copy()
        similar_leagues["similarity_score"] = distances[0]
        similar_leagues = similar_leagues.drop(selected_league, errors="ignore")

        st.write(
            f"Leagues similar to **{selected_league}** ({metric_choice} distance):"
        )
        st.dataframe(similar_leagues, use_container_width=True)

    # --------------------------------------------------------
    # PCA VISUALIZATION
    # --------------------------------------------------------
    st.subheader("🧭 League Visualization (PCA Projection)")

    X = df_leagues.fillna(0)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    df_plot = pd.DataFrame(
        {"PC1": X_pca[:, 0], "PC2": X_pca[:, 1], "league_name": df_leagues.index}
    )

    # --- Matplotlib ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df_plot["PC1"], df_plot["PC2"], s=80, alpha=0.7)
    for i, txt in enumerate(df_plot["league_name"]):
        ax.annotate(txt, (df_plot["PC1"][i], df_plot["PC2"][i]), fontsize=8)
    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")
    ax.set_title("League Similarity Visualization (PCA Projection)")
    st.pyplot(fig)

    # --- Plotly ---
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

else:
    st.info("👆 Select leagues and press **Load League Data** to begin.")
