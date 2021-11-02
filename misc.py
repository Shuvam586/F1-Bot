from bs4.element import TemplateString
import requests
from bs4 import BeautifulSoup

def race_result_page_url_getter(year , race_no):
    URL = f"https://www.formula1.com/en/results.html/{year}/races.html"
    html_text = requests.get(URL).text

    soup = BeautifulSoup(html_text , "lxml")

    body = soup.find("tbody")
    rows = body.find_all("tr")

    req_race = rows[race_no - 1]
    data_levels = req_race.find_all("td")

    req_level = data_levels[1]
    url_tag = req_level.find("a")

    url = url_tag['href']

    return f"https://www.formula1.com{url}"

def team_page_url_getter(team):
    if team == "MER":
        URL = "https://www.formula1.com/en/teams/Mercedes.html"
        return URL
    elif team == "RBR":
        URL = "https://www.formula1.com/en/teams/Red-Bull-Racing.html"
        return URL
    elif team == "MCL":
        URL = "https://www.formula1.com/en/teams/McLaren.html"
        return URL
    elif team == "FER":
        URL = "https://www.formula1.com/en/teams/Ferrari.html"
        return URL
    elif team == "ALP":
        URL = "https://www.formula1.com/en/teams/Alpine.html"
        return URL
    elif team == "ALT":
        URL = "https://www.formula1.com/en/teams/AlphaTauri.html"
        return URL
    elif team == "ASM":
        URL = "https://www.formula1.com/en/teams/Aston-Martin.html"
        return URL
    elif team == "WIL":
        URL = "https://www.formula1.com/en/teams/Williams.html"
        return URL
    elif team == "ALF":
        URL = "https://www.formula1.com/en/teams/Alfa-Romeo-Racing.html"
        return URL
    elif team == "HAS":
        URL = "https://www.formula1.com/en/teams/Haas-F1-Team.html"
        return URL

def driver_page_url_getter(driver):
    if driver == "HAM":
        URL = "https://www.formula1.com/en/drivers/lewis-hamilton.html"
        return URL
    elif driver == "BOT":
        URL = "https://www.formula1.com/en/drivers/valtteri-bottas.html"
        return URL
    elif driver == "VER":
        URL = "https://www.formula1.com/en/drivers/max-verstappen.html"
        return URL
    elif driver == "PER":
        URL = "https://www.formula1.com/en/drivers/sergio-perez.html"
        return URL
    elif driver == "NOR":
        URL = "https://www.formula1.com/en/drivers/lando-norris.html"
        return URL
    elif driver == "RIC":
        URL = "https://www.formula1.com/en/drivers/daniel-ricciardo.html"
        return URL
    elif driver == "SAI":
        URL = "https://www.formula1.com/en/drivers/carlos-sainz.html"
        return URL
    elif driver == "LEC":
        URL = "https://www.formula1.com/en/drivers/charles-leclerc.html"
        return URL
    elif driver == "ALO":
        URL = "https://www.formula1.com/en/drivers/fernando-alonso.html"
        return URL
    elif driver == "OCO":
        URL = "https://www.formula1.com/en/drivers/esteban-ocon.html"
        return URL
    elif driver == "GAS":
        URL = "https://www.formula1.com/en/drivers/pierre-gasly.html"
        return URL
    elif driver == "TSU":
        URL = "https://www.formula1.com/en/drivers/yuki-tsunoda.html"
        return URL
    elif driver == "VET":
        URL = "https://www.formula1.com/en/drivers/sebastian-vettel.html"
        return URL
    elif driver == "STR":
        URL = "https://www.formula1.com/en/drivers/lance-stroll.html"
        return URL
    elif driver == "RUS":
        URL = "https://www.formula1.com/en/drivers/george-russell.html"
        return URL
    elif driver == "LAT":
        URL = "https://www.formula1.com/en/drivers/nicholas-latifi.html"
        return URL
    elif driver == "RAI":
        URL = "https://www.formula1.com/en/drivers/kimi-raikkonen.html"
        return URL
    elif driver == "GIO":
        URL = "https://www.formula1.com/en/drivers/antonio-giovinazzi.html"
        return URL
    elif driver == "MSC":
        URL = "https://www.formula1.com/en/drivers/mick-schumacher.html"
        return URL
    elif driver == "MAZ":
        URL = "https://www.formula1.com/en/drivers/nikita-mazepin.html"
        return URL