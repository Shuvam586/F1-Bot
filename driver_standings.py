import requests
import json
from bs4 import BeautifulSoup

def driver_standings_updater(year):
    URL = f"https://www.formula1.com/en/results.html/{year}/drivers.html"
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
        driver = level[2].text
        not_req_3 , not_req_1 , name , surname , short , not_req_2 , not_req_4 = driver.split("\n")
        driver = f"{name} {surname}" 
        team = level[4].text.replace("\n" , "")
        points = level[5].text 

        temp_stand_dict = {
            "number" : number , "driver" : driver , "team" : team , "points" : points
        }

        standings_dict[str(i+1)] = temp_stand_dict

        i += 1

    with open("driver_standings.json" , "r") as f:
        data = json.load(f)

    data = standings_dict

    with open("driver_standings.json", "w") as f:
        json.dump(data , f , indent = 4) 