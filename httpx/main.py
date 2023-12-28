import httpx
from selectolax.parser import HTMLParser
import csv
import time


def html_gether(url, headers):
    resp = httpx.get(url, headers=headers)
    html = HTMLParser(resp.text)
    return html


def to_csv(data):
    for element in data:
        fields = [field for field, value in element.items()]
    with open("info.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        for info in data:
            writer.writerow(info)
    print("saved to csv")


def data_stracter(html):
    games = html.css("div.tabcontent div.m_block")
    for game in games:
        data = {
            "الفريق الاول": game.css_first("div.alba_sports_events-team_title").text(),
            "وقت المباراة": game.css_first(".match-data h3").text(),
            "الفريق الثاني": game.css_first(".h2").text(),
            "البطولة": game.css_first("span.cup").text(),
        }
        yield data


def main():
    url = "https://kooora4life.com/"
    headers = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    }
    html = html_gether(url, headers)
    data = data_stracter(html)
    data = [info for info in data]
    to_csv(data)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
