# Import of required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import plotly.express as px

# The get request below downloads the data from Eredivisie statistics page
statistics_url = "https://fbref.com/en/comps/23/Eredivisie-Stats"
data = requests.get(statistics_url)

# The pandas read html converts the statistics html page to a pandas dataframe
statistics_df = pd.read_html('https://fbref.com/en/comps/23/Eredivisie-Stats')

# The for loop loops through the Eredivisie standings list and the enumerate creates an indexed list
for idx,table in enumerate(statistics_df):
    (idx)
    (table)

# The BeautifulSoup library parst the text of the HTML/XML page
soup = BeautifulSoup(data.text,'lxml')

# In the code below soup.select selects the stats_table extracts the squads urls and places them in the links dataframe 
standing_table = soup.select("table.stats_table")[0]
links  = standing_table.find_all("a")
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]

# The data of the first index scraped team gets requested and placed in the data dataframe 
team_urls = [f"https://fbref.com{l}" for l in links]
team_url = team_urls[0]
data = requests.get(team_url)

# The game results etc. of the first club in the ranking gets placed in a dataframe 
matches = pd.read_html(data.text, match = "Scores & Fixtures")

# The text gets parsted and the shots per squad urls are placed in the links dataframe
soup = BeautifulSoup(data.text,'lxml')
links = soup.find_all("a")
links = [l.get("href") for l in links]
links = [l for l in links if l and "all_comps/shooting/" in l]

# The link data of the fist team in the shooting table gets requested and placed in the shooting dataframe
data = requests.get(f"https://fbref.com{links[0]}")
shooting = pd.read_html(data.text, match = "Shooting")[0]
shooting.columns = shooting.columns.droplevel()

# The matches table and shooting table are getting merged and placed in the team_data dataframe
team_data = matches[0].merge(shooting[["Date", "Sh", "SoT", "PK", "PKatt"]], on = "Date")

# List range setup, the range goes from Season 2020 to 2022
years = list(range(2022,2020, -1))

all_matches = []
statistics_url = "https://fbref.com/en/comps/23/Eredivisie-Stats"

# For loop through the competition season statistics from year 2020 to 2022, standing table and through the last soccer season
for year in years:
    data = requests.get(statistics_url)
    soup = BeautifulSoup(data.text,'lxml')
    standing_table = soup.select("table.stats_table")[0]
    
    links = standing_table.find_all("a")
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]
    
    last_season = soup.select("a.prev")[0].get("href")
    statistics_url = f"https://fbref.com/{last_season}"

# For loop through squad data, cleaning data, matches and shooting table are getting merged and only the selected columns are getting displayed
    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats","").replace("-"," ")
        
        data = requests.get(team_url)
        matches = pd.read_html(data.text, match = "Scores & Fixtures")[0]
        
        soup = BeautifulSoup(data.text,'lxml')
        links = soup.find_all("a")
        links = [l.get("href") for l in links]
        links = [l for l in links if l and "all_comps/shooting/" in l]
        data = requests.get(f"https://fbref.com{links[0]}")
        shooting = pd.read_html(data.text, match = "Shooting")[0]
        shooting.columns = shooting.columns.droplevel()
        
        try:
            team_data = matches.merge(shooting[["Date", "Sh", "SoT", "PK", "PKatt"]], on = "Date")
        except ValueError:
            continue
            
        team_data = team_data[team_data["Comp"] == "Eredivisie"]
        team_data["Season"] = year
        team_data["Team"] = team_name
        all_matches.append(team_data)
        time.sleep(1)

# Squad url gets splited and Stats are getting repalced to  and ""  -  " " 
# matches_df dataframe gets merged with the all_matches dataframe
team_url.split("/")[-1].replace("-Stats","").replace("-"," ")
matches_df = pd.concat(all_matches)

# The wedstrijd.df columns text is changed to lower case
matches_df.columns = [c.lower() for c in matches_df.columns]

# The used dataframes are getting exported as CSV files
matches_df.to_csv("matches.csv", encoding='utf-8', index=False)
statistics_df[0].to_csv("statistics.csv", encoding='utf-8', index=False)
shooting.to_csv("shooting.csv", encoding='utf-8', index=False)
team_data.to_csv("team-data.csv", encoding='utf-8', index=False)
