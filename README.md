🏏 CricMatchSheet Data Analysis - Transforming Raw Data into Strategic Insights.
This repository aims to analyze the cricket match data across 4 matches(ODI, TEST, IPL, T20).
Thus, this project is built on a robust pipeline where it extracts, transforms, and loads extensive match statistics helping us to dwelve into actionable insights such as player performance, team dynamics, and game trends across various formats.

✨ Project Highlights
From Data acquisiton using we b scraping to analysing the data in visual formats using EDA, Power BI this project encapsulates a dynamic variety of python tools.
The step-by-step are as follows:

1) Data Acquisition:
Using selenium we scrape the web Cricsheet.org and download comprehensive JSON data stored in zipfiles for Test, One-Day International (ODI), Twenty20 International (T20), and Indian Premier League (IPL) matches.

2) Robust Data Engineering:
   i) Parses complex JSON structures into clean, normalized tabular DataFrames using Python's pandas library.
   ii) Converts the DataFrame into CSV file formats and populates a structured SQL database (using MySQL Database Connector) with distinct tables for each match format (test_matches, odi_matches, t20_matches).

3) Data Querying:
SQL queries to filter the top player of matches, top bowlers, team's strategies on toss decisions, teams' winning percentage, most common venues and many such informations.

4) Exploratory Data Analysis (EDA):
Generates 10 diverse and informative visualizations using Python's matplotlib, seaborn, and plotly libraries, providing dynamic graphical representations of key data patterns.

5) Interactive Business Intelligence Dashboard:
Develops a compelling Power BI dashboard connected to the SQL database, offering intuitive and interactive visualizations for in-depth exploration of:
Player performance trends (batting & bowling).
Match outcomes and comparative team analyses.
Win/loss ratios across different cricket formats.
Team statistics and players acheivements.

🛠 Technology Stack
Data Scraping: Python (Selenium, requests, BeautifulSoup)
Data Processing: Python (pandas, json, zipfile)
Database Management: SQL (MySQL)
Data Analysis: MySQL
Data Visualization: Python (matplotlib, seaborn, plotly)
Business Intelligence: Power BI

🚀 Getting Started
To explore this project or replicate its functionality, follow these steps:

Environment Setup:
Ensure Python 3.x is installed.
Install required libraries using pip:
Bash
pip install -r requirements
(requirements include selenium, mysql database connector, pandas)
(Applications - VISUAL CODE studio, MYSQL workbench and MYSQL msi(for Power BI), Power BI desktop(for easy access))

Execute Data Pipeline:
Refer to the scripts/ directory for the sequential execution order:

1)Webscraping and data loading.ipynb : 
  Initiates data download from Cricsheet.
  Processes raw JSONs into structured DataFrames.
  Creates tables and loads data into MYSQL database.
2)cricmatchanalysis.py: 
Contains the analytical SQL queries executed by streamlit environment.
Type the following command - streamlit run cricmatchanalysis.py, a new browser with an interactive page will be opened. Select each topic to get the results.)
Note: Streamlit secrets has been used here for security reasons to hold the database credentials.(To use this py file, create a .streamlit folder in your project folder then, Create a "secrets.toml" file and enter your credentails)
3)eda_visuals.py: 
Generates Python-based visualizations and saves them in .png format and .html(for interactive purpose) formats.
Type python eda_visuals.py in your terminal and the file gets executed.
4)eda_visuals_present.py:
An interactive presentation of the data visuals generated in step 3 using streamlit.
Type streamlit run eda_visuals_present.py in your terrminal and the file gets executed. A web page with distinct visuals generated in step 3 with proper navigational instructions will open.
5)Power BI Dashboard:
Open CricMatchDashboard.pbix using Power BI Desktop to interact with the comprehensive dashboard.

📞 Support & Contribution
For any inquiries, suggestions, or potential collaborations, please feel free to reach out.
Sathya P/Sathya Pichandi
(Professional Name across all social media platforms)

© Data Attribution
Match data sourced from Cricsheet.org under their respective licenses.
