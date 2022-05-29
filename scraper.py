from ast import Pass
from urllib import response
import requests 
from bs4 import BeautifulSoup as bs
import sqlite3
from pathlib import Path
import datetime


BASE_DIR = Path(__file__).resolve().parent
VIDEOS_DB = BASE_DIR / 'protege' / 'data.sqlite'
CURRENT_DATE = str(datetime.datetime.now())


def ph_scraper(url):
    response = requests.get(url)
    if response.ok:
        print(f"Fetching data for: {url}")
        soup = bs(response.content, "html.parser")
        thumbnail = soup.find("img", {'id': 'videoElementPoster'})
        if not thumbnail:
            return

        thumbnail = thumbnail['src']

        categories = soup.find('div', {'class': 'categoriesWrapper'})
        categories_data = []
        for category in categories:
            categories_data.append(category.get_text().strip())

        # TODO
        actors = soup.find_all("a", {'class': 'pstar-list-btn'})

        actors_data = []
        for actor in actors:
            actors_data.append(actor.get_text().strip())

        categories_data = [
            c for c in categories_data if c and c != 'Categories']

        title = soup.find("span", {"class": "inlineFree"}).get_text().strip()

        if len(categories_data):
            categories_data = categories_data[0]
        else:
            categories_data = None

        if len(actors_data):
            actors_data = actors_data[0]
        else:
            actors_data = None

        print(f"actors: {actors_data} -> Category: {categories_data}")

        return {"thumbnail": thumbnail, "actors": actors_data, "categories": categories_data, "title": title}

    else:
        raise ConnectionError(f"Error: {response.status_code}")


def xvid_scraper(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla 5/0"})
    if response.ok:
        soup = bs(response.content, "html.parser")
        thumbnail = soup.find_all("img")[0]

        actors = soup.find_all("a", {"class": "hover-name"})[1:]
        actors_data = []
        for actor in actors:
            actors_data.append(actor.span.get_text())

        categories = soup.find("div", {"class": "video-metadata"})
        categories_data = []
        for i in categories.ul:
            if i.a['href'][:5] == "/tags":
                categories_data.append(i.get_text())

        return {"thumbnail": thumbnail, "actors": actors_data, "categories": categories_data}


def xham_scraper(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla 5/0"})
    if response.ok:
        print(response)
        soup = bs(response.content, "html.parser")
        thumbnail = soup.find('div', {"class": "xp-preload-image"})
        thumbnail = thumbnail['style'][22:-2]

        categories = soup.find("ul", {"class": "categories-container"})
        categories_data = []
        for category in categories:
            try:
                categories_data.append(category.a.get_text().strip())

            except AttributeError:
                pass

        return {"thumbnail": thumbnail, "actors": [], "categories": categories_data}


def spank_scraper(url):
    print(f"Fetching data for {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla 5/0"})
    if response.ok:
        soup = bs(response.content, "html.parser")
        thumbnail = soup.find("div", {"class": "play_cover"})
        thumbnail = thumbnail.img['src']

        if not thumbnail:
            return

        bottom = soup.find("div", {"class": "bottom"})
        bottom_parts = bottom.find_all("div", {"class": "cat"})

        categories = bottom_parts[0]
        actors = bottom_parts[1]

        def parse_bottom(bottom_part, name):
            if not bottom_part.span.get_text().lower()[:-1] == name:
                return
            elements = bottom_part.find_all("div", {"class": "ent"})
            elements_data = []
            for element in elements:
                elements_data.append(element.a.get_text())
            return elements_data

        actors_data = parse_bottom(actors, "pornstar")
        categories_data = parse_bottom(categories, 'category')

        if len(categories_data):
            categories_data = categories_data[0]
        else:
            categories_data = None
        if actors_data is not None:
            actors_data = actors_data[0]
        else:
            actors_data = None

        title = soup.find("div", {"class": "left"})
        title = title.find("h1")
        title = title['title'].strip()

        return {"thumbnail": thumbnail, "actors": actors_data, "categories": categories_data, "title": title}

# Leaks


def leak_xxx_fetch_data(url):
    response = requests.get(url)
    if response.ok:
        soup = bs(response.content, 'html.parser')
        info = soup.find("div", {"class": "info"})
        info_items = info.find_all("div", {"class": "item"})

        try:
            category = info_items[1].a.get_text().strip()
        except:
            category = None
        try:
            model = info_items[2].a.get_text().strip()
        except:
            model = None
        return {"actors": model, "categories": category}


def leak_xxx_page_scraper(url):
    links = []
    thumbnails = []
    titles = []

    response = requests.get(url)
    if response.ok:
        soup = bs(response.content, "html.parser")
        items = soup.find_all("div", {"class": "item"})
        for item in items:
            links.append(item.a['href'])
            thumbnails.append(item.a.div.img['data-original'])
            titles.append(item.a['title'].strip())

    for link in links:
        video_data = leak_xxx_fetch_data(link)


def the_leak_bay_fetch_data(url):
    response = requests.get(url)
    if response.ok:
        soup = bs(response.content, "html.parser")


def the_leak_bay_page_scraper(url):
    connection = sqlite3.connect(VIDEOS_DB)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    links = []
    titles = []
    thumbnails = []

    response = requests.get(url)
    if response.ok:
        print(response.status_code)
        soup = bs(response.content, "html.parser")
        videos = soup.find_all("article", {"class": "entry-tpl-grid"})
        for video in videos:
            links.append(video.div.a['href'])
            titles.append(video.div.a['title'])
            thumbnails.append(video.div.a.img['data-src'])

        for i, _ in enumerate(links):
            print(f"Inserting into db: {links[i]} -> {thumbnails[i]}")
            cursor.execute(
                """
                INSERT INTO post
                (user_id, post_video, post_video_url, date, title, category, thumbnail, actors, is_leak)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", (1, None, links[i], CURRENT_DATE, titles[i], "Leak", thumbnails[i], None, True))

        connection.commit()
        connection.close()
    else:
        print(response.status_code)


