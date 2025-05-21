import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

### Load the DataFrames from CSV files ###
data_dir = r"C:\Users\sathy\OneDrive\Desktop\Project\Cric-MatchsheetDataAnalysis" 
try:
    test_df = pd.read_csv(os.path.join(data_dir, "test.csv"))
    odi_df = pd.read_csv(os.path.join(data_dir, "ODI.csv"))
    t20_df = pd.read_csv(os.path.join(data_dir, "T20.csv"))
    ipl_df = pd.read_csv(os.path.join(data_dir, "IPL.csv"))
except FileNotFoundError:
    print("Error: One or more CSV files not found. Please ensure they are in the specified directory.")
    exit()

# Data Cleaning and pre-processing ###
# Converting season to numeric for better data representation
for df in [test_df, odi_df, t20_df, ipl_df]:
    if 'season' in df.columns:
        df['season'] = pd.to_numeric(df['season'], errors='coerce')

# --- 1. Number of Matches Played per Season (All Matches) --- #
plt.figure(figsize=(12, 6))
all_seasons = pd.concat([test_df['season'], odi_df['season'], t20_df['season'], ipl_df['season']]).dropna().astype(int)
sns.countplot(x=all_seasons, palette='viridis')
plt.title('Number of Matches Played per Season (All Matches)')
plt.xlabel('Season')
plt.ylabel('Number of Matches')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(data_dir, "matches_per_season.png"))
plt.close()
print("Visualization 1 created: matches_per_season.png")

# --- 2. Top 10 Most Frequent Venues (All Matches) --- #
plt.figure(figsize=(10, 8))
all_venues = pd.concat([test_df['venue'], odi_df['venue'], t20_df['venue'], ipl_df['venue']]).value_counts().nlargest(10)
sns.barplot(x=all_venues.values, y=all_venues.index, palette='magma')
plt.title('Top 10 Most Frequent Venues (All Matches)')
plt.xlabel('Number of Matches')
plt.ylabel('Venue')
plt.tight_layout()
plt.savefig(os.path.join(data_dir, "top_venues.png"))
plt.close()
print("Visualization 2 created: top_venues.png")

# --- 3. Toss Decision Distribution (ODI Matches) --- #
plt.figure(figsize=(8, 6))
odi_df['toss_decision'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Toss Decision Distribution in ODI Matches')
plt.ylabel('')
plt.tight_layout()
plt.savefig(os.path.join(data_dir, "odi_toss_decision.png"))
plt.close()
print("Visualization 3 created: odi_toss_decision.png")

# --- 4. Distribution of Winners (Test Matches) --- #
plt.figure(figsize=(12, 7))
test_df['winner'].value_counts().nlargest(15).plot(kind='bar', color=sns.color_palette('cividis'))
plt.title('Distribution of Winners in Test Matches (Top 15)')
plt.xlabel('Team')
plt.ylabel('Number of Wins')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(data_dir, "test_winners.png"))
plt.close()
print("Visualization 4 created: test_winners.png")

# --- 5. Runs Scored per Over (IPL Matches - Line Plot) --- #
if 'over' in ipl_df.columns and 'runs_total' in ipl_df.columns:
    runs_per_over_ipl = ipl_df.groupby('over')['runs_total'].mean()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=runs_per_over_ipl.index, y=runs_per_over_ipl.values, marker='o', color='coral')
    plt.title('Average Runs Scored per Over in IPL Matches')
    plt.xlabel('Over')
    plt.ylabel('Average Runs')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, "ipl_runs_per_over.png"))
    plt.close()
    print("Visualization 5 created: ipl_runs_per_over.png")
else:
    print("Warning: 'over' or 'runs_total' column not found in IPL DataFrame for visualization 5.")

# --- 6. Wickets Taken Distribution (T20 Matches) --- #
if 'wicket' in t20_df.columns:
    wickets_taken_t20 = t20_df['wicket'].apply(lambda x: 1 if pd.notna(x) and x != 'None' else 0)
    plt.figure(figsize=(8, 5))
    sns.histplot(wickets_taken_t20, bins=2, discrete=True, palette='Set2')
    plt.xticks([0, 1], ['No Wicket', 'Wicket Taken'])
    plt.title('Distribution of Wickets Taken per Delivery in T20 Matches')
    plt.xlabel('Wicket Status')
    plt.ylabel('Number of Deliveries')
    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, "t20_wicket_distribution.png"))
    plt.close()
    print("Visualization 6 created: t20_wicket_distribution.png")
else:
    print("Warning: 'wicket' column not found in T20 DataFrame for visualization 6.")

# --- 7. Top 10 Toss Winners (All Matches) --- #
plt.figure(figsize=(10, 6))
all_toss_winners = pd.concat([test_df['toss_winner'], odi_df['toss_winner'], t20_df['toss_winner'], ipl_df['toss_winner']]).value_counts().nlargest(10)
sns.barplot(x=all_toss_winners.index, y=all_toss_winners.values, palette='viridis')
plt.title('Top 10 Toss Winners (All Matches)')
plt.xlabel('Team')
plt.ylabel('Number of Tosses Won')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(data_dir, "top_toss_winners.png"))
plt.close()
print("Visualization 7 created: top_toss_winners.png")

# --- 8. City vs Number of Matches Played (Scatter Plot - Plotly for Interactivity) --- #
all_cities_df = pd.concat([test_df['city'], odi_df['city'], t20_df['city'], ipl_df['city']]).dropna().value_counts().reset_index()
all_cities_df.columns = ['city', 'match_count']
fig_city_matches = px.scatter(all_cities_df, x='city', y='match_count', size='match_count', color='match_count',
                             hover_name='city', size_max=60, title='City vs Number of Matches Played')
fig_city_matches.write_html(os.path.join(data_dir, "city_vs_matches.html"))
print("Visualization 8 created: city_vs_matches.html")

# --- 9. Season vs Runs Scored (Box Plot - IPL) --- #
if 'season' in ipl_df.columns and 'runs_total' in ipl_df.columns:
    plt.figure(figsize=(12, 7))
    sns.boxplot(x='season', y='runs_total', data=ipl_df, palette='Set3')
    plt.title('Runs Scored per Delivery by Season (IPL)')
    plt.xlabel('Season')
    plt.ylabel('Runs Total')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, "ipl_season_runs.png"))
    plt.close()
    print("Visualization 9 created: ipl_season_runs.png")
else:
    print("Warning: 'season' or 'runs_total' column not found in IPL DataFrame for visualization 9.")

# --- 10. Top 10 Player of the Match Winners (All Matches) --- #
plt.figure(figsize=(10, 8))
all_pom = pd.concat([test_df['player_of_match'].dropna(), odi_df['player_of_match'].dropna(),
                      t20_df['player_of_match'].dropna(), ipl_df['player_of_match'].dropna()]).value_counts().nlargest(10)
sns.barplot(x=all_pom.values, y=all_pom.index, palette='plasma')
plt.title('Top 10 Player of the Match Winners (All Matches)')
plt.xlabel('Number of Player of the Match Awards')
plt.ylabel('Player')
plt.tight_layout()
plt.savefig(os.path.join(data_dir, "top_pom_winners.png"))
plt.close()
print("Visualization 10 created: top_pom_winners.png")

print("All 10 visualizations created and saved as image/HTML files in your data directory.")