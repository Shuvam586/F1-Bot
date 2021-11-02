import json
import requests
from bs4 import BeautifulSoup

def team_page_getter_details(URL):
    html_text = requests.get(URL).text

    soup = BeautifulSoup(html_text , "lxml")
    team_table = soup.find("table" , class_ = "stat-list")
    team_body = team_table.find("tbody")
    team_rows = team_body.find_all("tr")

    team_keys = []
    team_values = []

    i = 0

    while i < len(team_rows):
        key = team_rows[i].find("th").text.replace("\n" , "")
        value = team_rows[i].find("td").text.replace("\n" , "")
        team_keys.append(key)
        team_values.append(value)
        i += 1

    j = 0
    temp_dict = {}

    while j < len(team_rows):
        temp_dict[team_keys[j]] = team_values[j]
        j += 1

    driver_list = soup.find("ul" , class_ = "drivers")
    drivers_details = driver_list.find_all("li")

    first_driver = drivers_details[0].find("figcaption" , class_ = "driver-details")
    first_driver_number = first_driver.find(class_ = "driver-number").text.replace("\n" , "")
    first_driver_name = first_driver.find(class_ = "driver-name").text.replace("\n" , "")
    first_driver_team = first_driver.find(class_ = "driver-team").text.replace("\n" , "")

    second_driver = drivers_details[1].find("figcaption" , class_ = "driver-details")
    second_driver_number = second_driver.find(class_ = "driver-number").text.replace("\n" , "")
    second_driver_name = second_driver.find(class_ = "driver-name").text.replace("\n" , "")
    second_driver_team = second_driver.find(class_ = "driver-team").text.replace("\n" , "")

    first_driver_details = {
        "number" : first_driver_number , 
        "name" : first_driver_name , 
        "team" : first_driver_team
    }
    second_driver_details = {
        "number" : second_driver_number , 
        "name" : second_driver_name , 
        "team" : second_driver_team
    }

    drivers = {
        "1" : first_driver_details , 
        "2" : second_driver_details
    }

    temp_dict['drivers'] = drivers

    with open("team_page_getter.json" , "r") as f:
        data = json.load(f)

    data = temp_dict

    with open("team_page_getter.json" , "w") as f:
        json.dump(data , f , indent = 4)