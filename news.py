import json
import requests
from bs4 import BeautifulSoup

def news_page_refresher():
    URL = f"https://www.formula1.com/en/latest.html"
    html_text = requests.get(URL).text

    soup = BeautifulSoup(html_text , "lxml")

    news_mains = soup.find_all("div" , class_ = "col-lg-6 col-md-12")
    latest_article = news_mains[0]

    article_url = latest_article.find("a")
    article_url =  f"https://www.formula1.com{article_url['href']}"

    thumbnail = latest_article.find(class_ = "f1-cc--photo")
    thumbnail = thumbnail.find("img")
    thumbnail_url = thumbnail['data-src']

    caption_box = latest_article.find("div" , class_ = "f1-cc--caption")
    tags = caption_box.find(class_ = "misc--tag").text.replace("\n" , "").replace("  " , "")
    heading = caption_box.find(class_ = "f1--s no-margin").text.replace("\n" , "")

    sub_articles = news_mains[1]
    sub_article_divs = sub_articles.find_all(class_ = "col-md-6 col-sm-12")
    sub_article_1 = sub_article_divs[0]
    sub_article_2 = sub_article_divs[1]

    sub_article_1_article_url = sub_article_1.find("a")
    sub_article_1_article_url = sub_article_1_article_url['href']
    sub_article_1_article_url =  f"https://www.formula1.com{sub_article_1_article_url}"

    sub_article_2_article_url = sub_article_2.find("a")
    sub_article_2_article_url = sub_article_2_article_url['href']
    sub_article_2_article_url =  f"https://www.formula1.com{sub_article_2_article_url}"

    sub_article_1_thumbnail = sub_article_1.find("div" , class_ = "d-none d-md-block f1-cc--image")
    sub_article_1_thumbnail = sub_article_1_thumbnail.find("img")['data-src']

    sub_article_2_thumbnail = sub_article_2.find("div" , class_ = "d-none d-md-block f1-cc--image")
    sub_article_2_thumbnail = sub_article_2_thumbnail.find("img")['data-src']

    sub_article_1_caption_box = sub_article_1.find("div" , class_ = "f1-cc--caption")
    sub_article_1_tags = sub_article_1_caption_box.find(class_ = "misc--tag").text.replace("\n" , "").replace("  " , "")
    sub_article_1_heading = sub_article_1_caption_box.find(class_ = "no-margin").text.replace("\n" , "").replace("  " , "")

    sub_article_2_caption_box = sub_article_2.find("div" , class_ = "f1-cc--caption")
    sub_article_2_tags = sub_article_2_caption_box.find(class_ = "misc--tag").text.replace("\n" , "").replace("  " , "")
    sub_article_2_heading = sub_article_2_caption_box.find(class_ = "no-margin").text.replace("\n" , "").replace("  " , "")

    with open("news.json" , "r") as f:
        data = json.load(f)

    temp_dict_p = {
        "heading": heading, 
        "tags": tags,
        "thumbnail": thumbnail_url,
        "article url": article_url
    }

    temp_dict_s_1 = {
        "heading": sub_article_1_heading, 
        "tags": sub_article_1_tags,
        "thumbnail": sub_article_1_thumbnail,
        "article url": sub_article_1_article_url
    }

    temp_dict_s_2 = {
        "heading": sub_article_2_heading, 
        "tags": sub_article_2_tags,
        "thumbnail": sub_article_2_thumbnail,
        "article url": sub_article_2_article_url
    }

    data['primary'] = temp_dict_p
    data['secondary']['first'] = temp_dict_s_1
    data['secondary']['second'] = temp_dict_s_2

    with open("news.json" , "w") as f:
        json.dump(data , f , indent = 4)
