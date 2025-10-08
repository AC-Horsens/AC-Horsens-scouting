import pandas as pd
from pathlib import Path
import streamlit as st
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import plotly.express as px


st.set_page_config(layout="wide")

# --- Load and prepare data ---
base_path = Path(r"C:\Users\Seamus-admin\Documents\GitHub\AC-Horsens-scouting")
matchstats_files = list(base_path.rglob("matchstats_all*"))

dfs = []
for f in matchstats_files:
    df_temp = pd.read_csv(f)
    df_temp["source_file"] = f.name
    df_temp["source_folder"] = f.parent.name
    dfs.append(df_temp)

df_leagues = pd.concat(dfs, ignore_index=True)

# Filter out DBU and missing values
df_leagues = df_leagues[~df_leagues['league_name'].str.contains('DBU', na=False)]
df_leagues = df_leagues[df_leagues['successfulOpenPlayPass'].notna()]

# Aggregate
df_leagues = df_leagues.groupby(['league_name','label','date']).sum(numeric_only=True).round(2)
df_leagues = df_leagues.groupby("league_name").mean(numeric_only=True).round(2)

# --- Step 1: Show all leagues ---
st.subheader("League averages")
st.dataframe(df_leagues, use_container_width=True)

# --- Step 2: Similarity analysis ---
st.subheader("Find similar leagues")

# Choose a metric
metric_choice = st.radio("Choose similarity metric:", ["euclidean", "manhattan", "cosine"])

# Select a league
selected_league = st.selectbox("Select a league:", df_leagues.index)

if selected_league:
    # Prepare feature matrix
    X = df_leagues.fillna(0)

    # Fit nearest neighbors
    nn = NearestNeighbors(n_neighbors=6, metric=metric_choice)
    nn.fit(X)

    # Get neighbors
    selected_idx = df_leagues.index.get_loc(selected_league)
    distances, indices = nn.kneighbors([X.iloc[selected_idx].values])

    # Collect similar leagues
    similar_leagues = df_leagues.iloc[indices[0]].copy()
    similar_leagues["similarity_score"] = distances[0]

    # Drop the league itself
    similar_leagues = similar_leagues.drop(selected_league)

    st.write(f"Leagues similar to **{selected_league}** ({metric_choice} distance):")
    st.dataframe(similar_leagues, use_container_width=True)

st.subheader("League visualization")

# Reduce to 2 dimensions with PCA
X = df_leagues.fillna(0)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Build DataFrame for plotting
df_plot = pd.DataFrame({
    "PC1": X_pca[:, 0],
    "PC2": X_pca[:, 1],
    "league_name": df_leagues.index
})

# Matplotlib scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_plot["PC1"], df_plot["PC2"], s=80, alpha=0.7)

# Annotate points
for i, txt in enumerate(df_plot["league_name"]):
    ax.annotate(txt, (df_plot["PC1"][i], df_plot["PC2"][i]), fontsize=8)

ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")
ax.set_title("League similarity visualization (PCA projection)")

st.pyplot(fig)

fig = px.scatter(
    df_plot, x="PC1", y="PC2", text="league_name",
    title="League similarity visualization (PCA projection)",
    width=900, height=600
)
fig.update_traces(textposition="top center")
st.plotly_chart(fig, use_container_width=True)