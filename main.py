# empty/main.py

import pandas as pd
from bs4 import BeautifulSoup as bs

from fake_useragent import UserAgent

import duckdb
import requests
from pathlib import Path

data_path = Path("data/results.csv")
database_path = "data/results.db"


def check_db(database_path_: Path) -> str:
    con = duckdb.connect(database_path_)
    q2 = """
        SELECT * FROM states;
    """
    df2 = con.sql(q2).to_df()
    con.close()
    if len(df2) > 3:
        message = "All is ok with the database"
    else:
        message = "Problem with the database"
    return message


url = "https://en.wikipedia.org/wiki/U.S._state"
ua = UserAgent()
headers = {"user-agent": ua.random}
base = "https://en.wikipedia.org"
page = requests.get(url, headers=headers)
soup = bs(page.content, "html.parser")

states = soup.find("div", class_="div-col").find_all("li")

results = []
for state in states:
    result = {
        "Name": state.find("a")["title"],
        "flag_img": "https:" + state.find("img")["src"],
        "state_link": base + state.find("a")["href"],
    }
    results.append(result)

df = pd.DataFrame(results)

df.to_csv(data_path, index=False)


conn = duckdb.connect(database_path)
q1 = """
    CREATE TABLE IF NOT EXISTS states AS SELECT * FROM df;
"""
conn.sql(q1)

print(check_db(database_path))
