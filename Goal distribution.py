import pandas as pd
from pathlib import Path

# Define base path
base_path = Path(r'C:\Users\Seamus-admin\Documents\GitHub\AC-Horsens-scouting')

# Formations to include
filtered_formations = ['343', '3421', '541', '3241']

# Final dictionary to store grouped results
results = {}

# Loop through each league folder
for league_folder in base_path.iterdir():
    if league_folder.is_dir():
        league_name = league_folder.name
        file_name = f'matchstats_all {league_name}.csv'
        file_path = league_folder / file_name

        if not file_path.exists():
            continue

        # Load data
        matchstats_df = pd.read_csv(file_path)

        # Normalize relevant columns
        matchstats_df['formationUsed'] = matchstats_df['formationUsed'].astype(str).str.strip().str.lower()
        matchstats_df['player_position'] = matchstats_df['player_position'].astype(str).str.strip().str.lower()
        matchstats_df['player_positionSide'] = matchstats_df['player_positionSide'].astype(str).str.strip().str.lower()

        # Filter for relevant formations
        df_filtered = matchstats_df[matchstats_df['formationUsed'].isin(filtered_formations)].copy()
        if df_filtered.empty:
            continue

        # Role mapping function
        def map_position(row):
            pos = row['player_position']
            side = row['player_positionSide']
            formation = row['formationUsed']
            if pos == 'striker':
                return 'striker' if side == 'centre' else 'attacking midfielder'
            elif pos == 'defender':
                return 'wing back' if side in ['left', 'right'] else 'defender'
            elif pos == 'midfielder':
                if formation == '541' and side in ['left', 'right']:
                    return 'attacking midfielder'
                return 'wing back' if side in ['left', 'right'] else 'midfielder'
            elif pos == 'defensive midfielder':
                return 'midfielder'
            else:
                return pos

        # Apply role mapping
        df_filtered['position_grouped'] = df_filtered.apply(map_position, axis=1)
        df_filtered['goals'] = pd.to_numeric(df_filtered['goals'], errors='coerce')

        # Group and aggregate goals
        grouped_goals = df_filtered.groupby('position_grouped')['goals'].sum().fillna(0)
        total_goals = grouped_goals.sum()
        grouped_pct = (grouped_goals / total_goals * 100).round(1)

        # Store in results dict
        for pos in grouped_goals.index:
            if pos not in results:
                results[pos] = {}
            results[pos][f'{league_name}_goals'] = int(grouped_goals[pos])
            results[pos][f'{league_name}_pct'] = grouped_pct[pos]

# Convert to DataFrame
final_df = pd.DataFrame.from_dict(results, orient='index').fillna(0)
final_df = final_df.sort_index()
final_df = final_df[sorted(final_df.columns)]

# ----------- Add Total Columns -----------

# Extract only the *_goals columns
goals_cols = [col for col in final_df.columns if col.endswith('_goals')]

# Sum goals across all leagues
final_df['Total_goals'] = final_df[goals_cols].sum(axis=1).astype(int)

# Compute Total percentage relative to grand total
grand_total = final_df['Total_goals'].sum()
final_df['Total_pct'] = (final_df['Total_goals'] / grand_total * 100).round(1)

# Reorder: put Total columns at the end
cols = [col for col in final_df.columns if col not in ['Total_goals', 'Total_pct']]
final_df = final_df[cols + ['Total_goals', 'Total_pct']]

# Save to CSV
output_path = base_path / 'goals_by_position_and_league.csv'
final_df.to_csv(output_path)

print(f"\n✅ Saved final DataFrame with goals, percentages, and total columns to: {output_path}")
