from bs4.element import TemplateString
import requests
import json
from bs4 import BeautifulSoup

def race_result_page_updater(URL):
    html_text = requests.get(URL).text

    soup = BeautifulSoup(html_text , "lxml")

    race_title = soup.find("h1" , class_ = "ResultsArchiveTitle").text.replace("\n" , "").replace("  " , "").title()

    race_details = soup.find("p" , class_ = "date")
    date = race_details.find("span" , class_ = "full-date").text

    circuit_info = race_details.find("span" , class_ = "circuit-info").text

    image_div = soup.find("figure" , class_ = "race-header-sponsor")
    try:
        image = image_div.find("img")
        image_url = image['src']
        image_url = f"https://www.formula1.com/{image_url}"
    except:
        image = None
        image_url = None

    if image_url == None:
        image_url = "https://www.racecar-engineering.com/wp-content/uploads/2018/03/F1-LOGO.png"

    drivers = {}

    drivers_body = soup.find("tbody")

    drivers_table = drivers_body.find_all("tr")

    i = 0
    while i < len(drivers_table):
        req_level = drivers_table[i]
        req_fields = req_level.find_all("td")

        position = req_fields[1].text
        driver_no = req_fields[2].text

        driver = req_fields[3].text
        not_req_1 , name , surname , short , not_req_2 = driver.split("\n")
        driver = f"{name} {surname}"

        team = req_fields[4].text
        laps = req_fields[5].text
        time = req_fields[6].text
        points = req_fields[7].text

        temp_driver_dict = {
            "position" : position,
            "driver_no" : driver_no,
            "driver" : driver,
            "team" : team,
            "laps" : laps,
            "time" : time,
            "points" : points
        }

        drivers[i + 1] = temp_driver_dict

        i += 1

    with open("race_result_page_getter.json" , "r") as f:
        data = json.load(f)

    data = {
        "title": race_title,
        "date": date,
        "circuit": circuit_info,
        "sponsor": image_url,
        "drivers": drivers
    }

    with open("race_result_page_getter.json" , "w") as f:
        json.dump(data , f , indent=4)