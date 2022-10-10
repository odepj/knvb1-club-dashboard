# importeren van de benodigde python libaries(bibliotheken)
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import plotly.express as px

# Het onderstaande get request haalt de eridivisie statistieken pagina op
statistieken_url = "https://fbref.com/en/comps/23/Eredivisie-Stats"
data = requests.get(statistieken_url)

# De onderstaande pandas read html zet de statistieken html pagina om naar een pandas dataframe
statistieken_df = pd.read_html('https://fbref.com/en/comps/23/Eredivisie-Stats')

# De for loop loopt door Eredivisie stand lijst en de enumerate zorgt voor een geindexte lijst
for idx,table in enumerate(statistieken_df):
    (idx)
    (table)
print(statistieken_df[0]) # Print de Eredivisie stand lijst

# De BeautifulSoup bibliotheek parst(ontleedt) de text van de opgevraagde HTML/XML pagina
soup = BeautifulSoup(data.text,'lxml')

# In de onderstaande code word eerste de stats_table van de website geselecteerd vervolgens word de squids(teams) urls in links gestopt    
stand_tabel = soup.select("table.stats_table")[0]
links  = stand_tabel.find_all("a")
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]

# Het eerste team van de gescrapte squads(teams) word opgevraagd 
team_urls = [f"https://fbref.com{l}" for l in links]
team_url = team_urls[0]
data = requests.get(team_url)

# De wedstrijd uitslagen etc. van de 1ste club in de ranglijst word in een dataframe gestopt 
wedstrijden = pd.read_html(data.text, match = "Scores & Fixtures")

# De text word geparst en de schoten per team urls worden in links opgeslagen 
soup = BeautifulSoup(data.text,'lxml')
links = soup.find_all("a")
links = [l.get("href") for l in links]
links = [l for l in links if l and "all_comps/shooting/" in l]

# De link data van het eerste team in de shoten(shooting) tabel word opgevraagd en in een dataframe gezet en vervolgens geprint
data = requests.get(f"https://fbref.com{links[0]}")
shoten = pd.read_html(data.text, match = "Shooting")[0]
shoten.columns = shoten.columns.droplevel()
print(shoten.head())

# De wedstrijd tabel en de schoten tabel worden samen gevoegd
team_data = wedstrijden[0].merge(shoten[["Date", "Sh", "SoT", "PK", "PKatt"]], on = "Date")


# Instellen list range dit is van 2022 t/m 2022
jaren = list(range(2022,2020, -1))

alle_wedstrijden = []
statistieken_url = "https://fbref.com/en/comps/23/Eredivisie-Stats"

# for loop door de competitie jaren 2020 t/m 2022 statistieken, stand tabel en de vorige voetbal seizoenen
for jaar in jaren:
    data = requests.get(statistieken_url)
    soup = BeautifulSoup(data.text,'lxml')
    stand_tabel = soup.select("table.stats_table")[0]
    
    links = stand_tabel.find_all("a")
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]
    
    vorig_seizoen = soup.select("a.prev")[0].get("href")
    statistieken_url = f"https://fbref.com/{vorig_seizoen}"

# for loop door team data, opgschonen data, wedstrijden en schoten tabel word samengevoegt en alleen de geslecterde kollomen worden getoond  
    for team_url in team_urls:
        team_naam = team_url.split("/")[-1].replace("-Stats","").replace("-"," ")
        
        data = requests.get(team_url)
        wedstrijden = pd.read_html(data.text, match = "Scores & Fixtures")[0]
        
        soup = BeautifulSoup(data.text,'lxml')
        links = soup.find_all("a")
        links = [l.get("href") for l in links]
        links = [l for l in links if l and "all_comps/shooting/" in l]
        data = requests.get(f"https://fbref.com{links[0]}")
        shoten = pd.read_html(data.text, match = "Shooting")[0]
        shoten.columns = shoten.columns.droplevel()
        
        try:
            team_data = wedstrijden.merge(shoten[["Date", "Sh", "SoT", "PK", "PKatt"]], on = "Date")
        except ValueError:
            continue
            
        team_data = team_data[team_data["Comp"] == "Eredivisie"]
        team_data["Season"] = jaar
        team_data["Team"] = team_naam
        alle_wedstrijden.append(team_data)
        time.sleep(1)

# team url word gesplit en Stats word vervangen door "" en - door " " 
# wedstrijd_df datafram word samengevoegd met alle_wedstrijden
team_url.split("/")[-1].replace("-Stats","").replace("-"," ")
wedstrijd_df = pd.concat(alle_wedstrijden)

# Tekst word naar lowercase(kleine letters) veranderd
wedstrijd_df.columns = [c.lower() for c in wedstrijd_df.columns]

# De eeste 5 regels van het wedstrijd dataframe word geprint
print(wedstrijd_df.head())

# Gebruikte dataframes worden als csv opgeslagen
wedstrijd_df.to_csv("wedstrijden.csv", encoding='utf-8', index=False)
statistieken_df[0].to_csv("statistieken.csv", encoding='utf-8', index=False)
shoten.to_csv("shoten.csv", encoding='utf-8', index=False)
team_data.to_csv("team-data.csv", encoding='utf-8', index=False)
