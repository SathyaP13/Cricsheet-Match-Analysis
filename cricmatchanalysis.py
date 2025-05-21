import streamlit as st
import pandas as pd
import mysql.connector

# --- Database Credentials (Using Streamlit Secrets for security reasons)

DB_HOST = st.secrets["DB_HOST"]
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_NAME = st.secrets["DB_NAME"]

# 20 insightful queries that gets executed when streamlit runs #
sql_queries = {
    "Top 10 batsmen by total runs in ODI matches": """
        SELECT batter, SUM(runs_batter) AS total_runs
        FROM odi_matches
        GROUP BY batter
        ORDER BY total_runs DESC
        LIMIT 10;
    """,
    "Leading wicket-takers in T20 matches": """
        SELECT bowler, COUNT(wicket) AS total_wickets
        FROM t20_matches
        WHERE wicket IS NOT NULL AND wicket <> 'None'
        GROUP BY bowler
        ORDER BY total_wickets DESC
        LIMIT 10;
    """,
    "Team with the highest win percentage in Test cricket": """
        WITH TestResults AS (
            SELECT winner, COUNT(*) AS wins
            FROM test_matches
            WHERE winner IS NOT NULL AND winner <> 'draw'
            GROUP BY winner
        ),
        TotalTestMatches AS (
            SELECT team, COUNT(*) AS total_matches
            FROM (
                SELECT SUBSTRING_INDEX(teams, ', ', 1) AS team FROM test_matches
                UNION ALL
                SELECT SUBSTRING_INDEX(teams, ', ', -1) AS team FROM test_matches
            ) AS all_teams
            GROUP BY team
        )
        SELECT
            tr.winner AS team,
            (CAST(tr.wins AS DECIMAL) / tm.total_matches) * 100 AS win_percentage
        FROM TestResults tr
        JOIN TotalTestMatches tm ON tr.winner = tm.team
        ORDER BY win_percentage DESC
        LIMIT 1;
    """,
    "Total number of centuries across all match types (Simplified)": """
        SELECT match_type, batter, COUNT(*) AS centuries
        FROM (
            SELECT match_type, batter, SUM(runs_batter) AS inning_runs
            FROM (
                SELECT 'test' AS match_type, batter, SUM(runs_batter) AS runs_batter FROM test_matches GROUP BY match_type, batter
                UNION ALL
                SELECT 'odi' AS match_type, batter, SUM(runs_batter) AS runs_batter FROM odi_matches GROUP BY match_type, batter
                UNION ALL
                SELECT 't20' AS match_type, batter, SUM(runs_batter) AS runs_batter FROM t20_matches GROUP BY match_type, batter
                UNION ALL
                SELECT 'ipl' AS match_type, batter, SUM(runs_batter) AS runs_batter FROM ipl_matches GROUP BY match_type, batter
            ) AS all_runs_by_batter
            GROUP BY match_type, batter
            HAVING SUM(runs_batter) >= 100
        ) AS centuries_table
        GROUP BY match_type, batter
        ORDER BY centuries DESC;
    """,
    "Most frequent player of the match across all formats": """
        SELECT player_of_match, COUNT(*) AS count
        FROM (
            SELECT player_of_match FROM test_matches WHERE player_of_match IS NOT NULL AND player_of_match <> ''
            UNION ALL
            SELECT player_of_match FROM odi_matches WHERE player_of_match IS NOT NULL AND player_of_match <> ''
            UNION ALL
            SELECT player_of_match FROM t20_matches WHERE player_of_match IS NOT NULL AND player_of_match <> ''
            UNION ALL
            SELECT player_of_match FROM ipl_matches WHERE player_of_match IS NOT NULL AND player_of_match <> ''
        ) AS all_pom
        GROUP BY player_of_match
        ORDER BY count DESC
        LIMIT 1;
    """,
    "Bowlers with the best average in ODI (min 50 wickets)": """
        SELECT
            bowler,
            SUM(runs_total) AS runs_conceded,
            COUNT(CASE WHEN wicket IS NOT NULL AND wicket <> 'None' THEN 1 END) AS wickets_taken,
            CAST(SUM(runs_total) AS DECIMAL) / COUNT(CASE WHEN wicket IS NOT NULL AND wicket <> 'None' THEN 1 END) AS bowling_average
        FROM odi_matches
        GROUP BY bowler
        HAVING COUNT(CASE WHEN wicket IS NOT NULL AND wicket <> 'None' THEN 1 END) >= 50
        ORDER BY bowling_average ASC
        LIMIT 10;
    """,
    "Most common venue for IPL matches": """
        SELECT venue, COUNT(*) AS match_count
        FROM ipl_matches
        GROUP BY venue
        ORDER BY match_count DESC
        LIMIT 1;
    """,
    "Teams that have won the most tosses in Test matches": """
        SELECT toss_winner, COUNT(*) AS tosses_won
        FROM test_matches
        GROUP BY toss_winner
        ORDER BY tosses_won DESC
        LIMIT 5;
    """,
    "Most frequent toss decision in ODI matches": """
        SELECT toss_decision, COUNT(*) AS decision_count
        FROM odi_matches
        GROUP BY toss_decision
        ORDER BY decision_count DESC
        LIMIT 1;
    """,
    "Number of matches played in each season across all formats": """
        SELECT season, match_type, COUNT(*) AS matches_played
        FROM (
            SELECT season, 'test' AS match_type FROM test_matches
            UNION ALL
            SELECT season, 'odi' AS match_type FROM odi_matches
            UNION ALL
            SELECT season, 't20' AS match_type FROM t20_matches
            UNION ALL
            SELECT season, 'ipl' AS match_type FROM ipl_matches
        ) AS all_matches
        GROUP BY season, match_type
        ORDER BY season, match_type;
    """,
    "City with the most number of cricket matches": """
        SELECT city, COUNT(*) AS match_count
        FROM (
            SELECT city FROM test_matches WHERE city IS NOT NULL
            UNION ALL
            SELECT city FROM odi_matches WHERE city IS NOT NULL
            UNION ALL
            SELECT city FROM t20_matches WHERE city IS NOT NULL
            UNION ALL
            SELECT city FROM ipl_matches WHERE city IS NOT NULL
        ) AS all_matches
        GROUP BY city
        ORDER BY match_count DESC
        LIMIT 1;
    """,
    "Teams that have won after losing the toss in T20 matches": """
        SELECT winner, COUNT(*) AS wins_after_losing_toss
        FROM t20_matches
        WHERE toss_winner <> winner
        GROUP BY winner
        ORDER BY wins_after_losing_toss DESC;
    """,
    "Average runs scored per over in IPL matches": """
        SELECT
            CAST(SUM(runs_total) AS DECIMAL) / SUM(over + 1) AS average_runs_per_over
        FROM ipl_matches;
    """,
    "Players who have been player of the match in the most number of seasons": """
        SELECT player_of_match, COUNT(DISTINCT season) AS seasons_as_pom
        FROM (
            SELECT season, player_of_match FROM test_matches WHERE player_of_match IS NOT NULL AND player_of_match <> ''
            UNION ALL
            SELECT season, player_of_match FROM odi_matches WHERE player_of_match IS NOT NULL AND player_of_match <> ''
            UNION ALL
            SELECT season, player_of_match FROM t20_matches WHERE player_of_match IS NOT NULL AND player_of_match <> ''
            UNION ALL
            SELECT season, player_of_match FROM ipl_matches WHERE player_of_match IS NOT NULL AND player_of_match <> ''
        ) AS all_pom_seasons
        GROUP BY player_of_match
        ORDER BY seasons_as_pom DESC
        LIMIT 10;
    """,
    "Number of drawn matches in Test cricket": """
        SELECT COUNT(*) AS drawn_matches
        FROM test_matches
        WHERE winner = 'draw';
    """,
    "Top 5 batsmen with most runs in IPL": """
        SELECT batter, SUM(runs_batter) AS total_runs
        FROM ipl_matches
        GROUP BY batter
        ORDER BY total_runs DESC
        LIMIT 5;
    """,
    "Top 5 bowlers with most wickets in IPL": """
        SELECT bowler, COUNT(wicket) AS total_wickets
        FROM ipl_matches
        WHERE wicket IS NOT NULL AND wicket <> 'None'
        GROUP BY bowler
        ORDER BY total_wickets DESC
        LIMIT 5;
    """,
    "Match with the highest total runs scored (across all formats)": """
        SELECT
            match_type,
            GROUP_CONCAT(DISTINCT season) AS seasons,
            GROUP_CONCAT(DISTINCT teams) AS teams,
            SUM(runs_total) AS total_runs
        FROM (
            SELECT 'test' AS match_type, season, teams, runs_total FROM test_matches
            UNION ALL
            SELECT 'odi' AS match_type, season, teams, runs_total FROM odi_matches
            UNION ALL
            SELECT 't20' AS match_type, season, teams, runs_total FROM t20_matches
            UNION ALL
            SELECT 'ipl' AS match_type, season, teams, runs_total FROM ipl_matches
        ) AS all_match_runs
        GROUP BY match_type, season, teams
        ORDER BY total_runs DESC
        LIMIT 1;
    """,
    "Venue with the most number of Test matches": """
        SELECT venue, COUNT(*) AS match_count
        FROM test_matches
        GROUP BY venue
        ORDER BY match_count DESC
        LIMIT 1;
    """,
    "Batsman with the highest individual score in ODI (This requires more specific data about individual match scores)": """
        -- This query is a simplification and assumes 'runs_batter' in a row might represent a significant portion of an individual score in a match.
        -- A more accurate approach would require data at the innings/player level per match.
        SELECT batter, MAX(runs_batter) AS highest_score
        FROM odi_matches
        GROUP BY batter
        ORDER BY highest_score DESC
        LIMIT 1;
    """,
}

### MYSQL database connection
def connect_db():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except mysql.connector.Error as err:
        st.error(f"Error connecting to MySQL: {err}")
        return None

### Executes the SQL query and returns the result as a pandas DataFrame.
def run_query(conn, query):
    if conn:
        try:
            df = pd.read_sql(query, conn)
            return df
        except mysql.connector.Error as err:
            st.error(f"Error executing query: {err}")
            return None
    return None

def main():
    st.title("Cricket Match Data Level Insights")

    conn = connect_db()
    if not conn:
        return

    query_name = st.selectbox("Select an Insight to Extract:", list(sql_queries.keys()))
    selected_query = sql_queries[query_name]

    st.subheader("SQL Query:")
    st.code(selected_query, language="sql")

    if st.button("Execute Query"):
        result_df = run_query(conn, selected_query)
        if result_df is not None and not result_df.empty:
            st.subheader("Query Result:")
            st.dataframe(result_df)
        elif result_df is not None and result_df.empty:
            st.info("No results found for this query.")

    if conn.is_connected():
        conn.close()

if __name__ == "__main__":
    main()