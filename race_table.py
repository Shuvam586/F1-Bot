from bs4.element import TemplateString
import requests
import json
from bs4 import BeautifulSoup

def race_table_updater(year):
    URL = f"https://www.formula1.com/en/results.html/{year}/races.html"
    html_text = requests.get(URL).text

    soup = BeautifulSoup(html_text , "lxml")

    results_table = soup.find("table" , class_ = "resultsarchive-table")
    results_body = results_table.find("tbody")
    result = results_body.find_all("tr")

    i = 0

    race_dict = {}

    while i < len(result):
        race = result[i].find_all("td")

        venue = race[1].text.replace(" " , "").replace("\n" , "")
        date = race[2].text 

        winner = race[3].text
        not_req_1 , name , surname , short , not_req_2 = winner.split("\n")
        winner_driver = f"{name} {surname}"

        winner_team = race[4].text 
        laps = race[5].text  
        time = race[6].text  

        temp_race_dict = {
            "venue" : venue , "date" : date , "race_winner" : [winner_driver , winner_team] , "laps" : laps , "time" : time
        }

        race_dict[str(i+1)] = temp_race_dict

        i += 1

    with open("race_table.json" , "r") as f:
        data = json.load(f)

    data = race_dict

    with open("race_table.json", "w") as f:
        json.dump(data , f , indent = 4) 
