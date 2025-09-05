# empty/main.py

# import pandas as pd
from bs4 import BeautifulSoup as bs

from fake_useragent import UserAgent

# import duckdb
import requests

url = "https://en.wikipedia.org/wiki/U.S._state"
ua = UserAgent()
headers = {"user-agent": ua.random}

page = requests.get(url, headers=headers)
soup = bs(page.content, "html.parser")
title = soup.find("title")
print(title)
