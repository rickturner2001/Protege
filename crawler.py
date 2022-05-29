from sqlite3 import dbapi2
import requests
import concurrent.futures
from scraper import ph_scraper
from bs4 import BeautifulSoup as bs
import sqlite3
from pathlib import Path

current_path = Path(__file__).resolve().parent
db_path = current_path / "database" / "videos_info.sqlite"

if __name__ == "__main__":
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS videos (id INT PRIMARY KEY, link TEXT NOT NULL ,title TEXT NOT NULL, actors, categories)
        """)

    # Phub crawler
    base_url = "http://www.pornhub.com"
    url = "https://www.pornhub.com/video?o=mv"

    def get_page_data(url):
        response = requests.get(url)
        if response.ok:
            soup = bs(response.content, "html.parser")
            videos = soup.find_all("a", {"class": "videoPreviewBg"})
            urls = []
            for video in videos:
                urls.append(base_url + str(video['href']))
    
        return urls

    urls = []
    for i in range(40):
        if i == 0:
            urls.append(get_page_data(url))
        else:
            urls.append(get_page_data(url + f"&page={i + 1}"))

    url = [u for url in urls for u in url ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(ph_scraper, urls))

    print(results)



    
    