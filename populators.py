

# -------------------------------------------
# Leak Bat 

# for i in range(2, 12):
#     print(i)
#     the_leak_bay_page_scraper(f"https://theleakbay.com/onlyfans-leaks-sextapes-and-pictures/page/{i}/")
#
# --------------------------------------------

# P-hub Categories Populator 

import requests
from bs4 import BeautifulSoup as bs
import sqlite3
from pathlib import Path
import datetime
from scraper import ph_scraper

DB_PATH = Path(__file__).resolve().parent / 'protege' / 'data.sqlite'
CURRENT_DATE = str(datetime.datetime.now())

def ph_populator():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    sources =  []
    categories = []

    base_url = "https://www.pornhub.com"
    response = requests.get("https://www.pornhub.com/categories")
    if response.ok:
        soup = bs(response.content, "html.parser")
        categories_data = soup.find_all("div", {"class": "category-wrapper"})
        for category in categories_data:
            categories.append(category.div.a['alt'].strip())
            sources.append(category.div.a['href'])

        for i, source in enumerate(sources):
            print(categories[i])
            response = requests.get(base_url  + source)
            if response.ok:
                soup = bs(response.content, "html.parser")
                videos = soup.find_all('a', {"class": "linkVideoThumb"})
                for video in videos:
                    url = base_url + video['href']
                    title = video['title'].strip()
                    data = ph_scraper(url)
                    cursor.execute(
                        """
                        INSERT INTO post (user_id, post_video, post_video_url, date, title, category, thumbnail, actors, is_leak)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (1, None, url, CURRENT_DATE, title, categories[i], data['thumbnail'], data['actors'], False))
                    
                    print(f"Correctly added {title}")

        connection.commit()
        connection.close()

def spank_populator(url, pages):
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    base_url = "http://spankbang.com"
    def scrape_page(url):
        response = requests.get(url)
        soup = bs(response.content, "html.parser")
        videos = soup.find_all("a", {"class": "thumb"})
        titles = []
        sources = []
        thumbnails = []
        for video in videos:
            sources.append(base_url + video['href'])
            thumbnails.append(video.img['data-src'])
            titles.append(video.img['alt'])
        return (titles, sources, thumbnails)

    for i in range (1, pages + 1):
        if i == 1:
            print("scraping: ", url)
            titles, sources, thumbnails = scrape_page(url)
        else: 
            print("scraping: ", url + f"{i}/")
            titles, sources, thumbnails = scrape_page(url + f"{i}/")
            
        
        for i in range(len(titles)):
            cursor.execute(
                        """
                        INSERT INTO post (user_id, post_video, post_video_url, date, title, category, thumbnail, actors, is_leak)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (1, None, sources[i], CURRENT_DATE, titles[i], "OnlyFans", thumbnails[i], None, True))
        
    connection.commit()

# spank_populator("https://spankbang.com/s/onlyfans+leaks/", 40)



def thot_tok_scraper(url, pages):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    def scrape_page(url):
        response = requests.get(url)
        soup = bs(response.content, "html.parser")
        videos = soup.findAll("article", {"class" : ["loop-video", "thumb-block"]})
        titles = []
        thumbnails = []
        sources = []
        for video in videos:
            sources.append(video.a['href'])
            thumbnails.append(video.a.div.div.img['data-src'])
            titles.append(video.a.div.div.img['alt'].strip())
        return (titles, thumbnails, sources)

    for i in range(1, pages + 1):
        if i == 1:
            print("fetching: ", url)
            titles, thumbnails, sources = scrape_page(url)
        else:
            print("fetching: ", url + f"page/{i}/")
            titles, thumbnails, sources = scrape_page(url + f"page/{i}/")


        for i in range(len(titles)):
            cursor.execute(
                        """
                        INSERT INTO post (user_id, post_video, post_video_url, date, title, category, thumbnail, actors, is_leak)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (1, None, sources[i], CURRENT_DATE, titles[i], "OnlyFans", thumbnails[i], None, True))

    connection.commit()

