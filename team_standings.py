from bs4.element import TemplateString
import requests
import json
from bs4 import BeautifulSoup

def team_standings_updater(year):
    URL = f"https://www.formula1.com/en/results.html/{year}/team.html"
    html_text = requests.get(URL).text

    soup = BeautifulSoup(html_text , "lxml")

    standings_table = soup.find("table" , class_ = "resultsarchive-table")
    standings_body = standings_table.find("tbody")
    standings = standings_body.find_all("tr")

    i = 0

    standings_dict = {}

    while i < len(standings):

        level = standings[i].find_all("td")
        number = level[1].text  
        team = level[2].text.replace("\n" , "") 
        points = level[3].text 

        temp_stand_dict = {
            "number" : number , "team" : team , "points" : points
        }

        standings_dict[str(i+1)] = temp_stand_dict

        i += 1

    with open("team_standings.json" , "r") as f:
        data = json.load(f)

    data = standings_dict

    with open("team_standings.json", "w") as f:
        json.dump(data , f , indent = 4) 