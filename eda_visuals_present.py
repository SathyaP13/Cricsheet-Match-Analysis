import streamlit as st
import os
from PIL import Image # To open our visuals stored as PNG images
import streamlit.components.v1 as components # To embed HTML

### --- Configuration setting --- describing the data directory path --- ###
data_dir = r"C:\Users\sathy\OneDrive\Desktop\Project\Cric-MatchsheetDataAnalysis" 
app_title = "Cricket Match Sheet Insights : An Exploratory Data Analysis"

### --- Visualizations to be represented as an interactive Presentation using streamlit --- ###
### Each tuple is formatted as: (Title, file_name, file_type, description of the visual) ###
visualizations = [
    ("1. Matches Played per Season (All Matches)", "matches_per_season.png", "image",
     "This chart shows the total number of cricket matches played across all Matches (Test, ODI, T20, IPL) for each season. It helps us understand the activity level in different cricketing years."),

    ("2. Top 10 Most Frequent Venues (All Matches)", "top_venues.png", "image",
     "Discovering the most popular stadiums for cricket matches globally. This bar chart highlights the venues that have hosted the highest number of games across all Matches."),

    ("3. Toss Decision Distribution (ODI Matches)", "odi_toss_decision.png", "image",
     "An analysis of captains strategy on deciding to bat or bowl after winning the toss in One-Day International matches – Common strategies played well."),

    ("4. Distribution of Winners in Test Matches (Top 15)", "test_winners.png", "image",
     "Exploring which teams have been most successful in Test cricket. This chart displays the top 15 teams by their number of wins in the longest format of the game."),

    ("5. Average Runs Scored per Over in IPL Matches", "ipl_runs_per_over.png", "image",
     "A detailed look at scoring patterns in the Indian Premier League(IPL). This line graph illustrates the average runs scored in each over of an IPL innings, showcasing how scoring rates change throughout the game."),

    ("6. Distribution of Wickets Taken per Delivery in T20 Matches", "t20_wicket_distribution.png", "image",
     "Understanding the frequency of wickets falling in the fast-paced T20 format. This chart shows the deliveries that resulted in a wicket versus no wicket."),

    ("7. Top 10 Toss Winners (All Matches)", "top_toss_winners.png", "image",
     "Winning the toss can often be a crucial advantage. This chart shows the teams that have the highest success rate in winning the toss across all cricket Matches."),

    ("8. City vs Number of Matches Played (Interactive)", "city_vs_matches.html", "html",
     "This interactive scatter plot visualizes the number of cricket matches hosted by various cities around the world. Hover over the points to see specific city names and match counts."),

    ("9. Runs Scored per Delivery by Season (IPL)", "ipl_season_runs.png", "image",
     "A season-by-season breakdown of runs scored per delivery in the IPL. This box plot helps identify trends or variations in scoring intensity across different editions of the tournament."),

    ("10. Top 10 Player of the Match Winners (All Matches)", "top_pom_winners.png", "image",
     "Celebrating the most impactful players! This chart highlights the top 10 cricketers who have received the highest number of 'Player of the Match' awards across Test, ODI, T20, and IPL matches.")
]

### --- Building the Streamlit App Layout --- ###
st.set_page_config(layout="wide", page_title=app_title)

st.title(app_title)
st.write("Hello there! Presenting you the detailed analysis of the cricket matches(IPL,ODI,TEST,T20) held so far." \
"Kindly, navigate to the left side of the panel and hover over each title to visualize the data in different EDAs(ranging from Scatter Plot to Box Plot) ")

### Using Sidebar for navigation to select and view each visualization ###
st.sidebar.header("Navigation")
page_names = [viz[0] for viz in visualizations]
selected_page = st.sidebar.radio("Go to Slide:", page_names)

st.sidebar.write("!!! Note: Click Here !!! View the results as Visuals on the right side !!!")
st.sidebar.info(
    "Click on the radio buttons above to navigate through the visualizations. "
    "Each slide provides a visual insight into the cricket matches played so far."
)

### Display content based on selection ###
for viz_title, file_name, file_type, description in visualizations:
    if selected_page == viz_title:
        st.header(viz_title)
        st.write(description) 

        file_path = os.path.join(data_dir, file_name)

        if not os.path.exists(file_path):
            st.error(f"Error: Visualization file '{file_name}' not found at '{file_path}'. "
                     "Please ensure you've run 'eda_visualizations.py' to generate all files.")
            break

        if file_type == "image":
            try:
                image = Image.open(file_path)
                st.image(image, use_column_width=True)
            except Exception as e:
                st.error(f"Could not load image '{file_name}': {e}")
        elif file_type == "html":
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                components.html(html_content, height=600, scrolling=True)
            except Exception as e:
                st.error(f"Could not load HTML file '{file_name}': {e}")
        break # Exits the loop once the right page is found

st.write("Have a Great day!")
st.markdown("### Streamlit Signing Off until next time! ")