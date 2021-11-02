import json
import requests
from bs4 import BeautifulSoup

def driver_page_getter_details(URL):
    html_text = requests.get(URL).text

    soup = BeautifulSoup(html_text , "lxml")
    
    driver_table = soup.find("table" , class_ = "stat-list")
    driver_body = driver_table.find("tbody")

    driver_rows = driver_body.find_all("tr")

    driver_keys = []
    driver_values = []

    i = 0

    while i < len(driver_rows):
        key = driver_rows[i].find("th").text.replace("\n" , "")
        value = driver_rows[i].find("td").text.replace("\n" , "")
        driver_keys.append(key)
        driver_values.append(value)
        i += 1

    driver_number = soup.find(class_ = "driver-number").text.replace("\n" , "")

    driver_name = soup.find(class_ = "driver-name").text.replace("\n" , "")

    j = 0
    temp_dict = {}

    temp_dict['Name'] = driver_name
    temp_dict['Number'] = driver_number

    while j < len(driver_rows):
        temp_dict[driver_keys[j]] = driver_values[j]
        j += 1

    with open("driver_page_getter.json" , "r") as f:
        data = json.load(f)

    data = temp_dict

    with open("driver_page_getter.json" , "w") as f:
        json.dump(data , f , indent = 4)