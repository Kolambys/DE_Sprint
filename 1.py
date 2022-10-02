import json

import requests as req
from bs4 import BeautifulSoup
import fake_user_agent


data = []
ua = fake_user_agent.user_agent()
resp = req.get(
    url= f'https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=python+разработчик&from=suggest_post&page=1',
    headers={"user-agent":ua}
)
soup = BeautifulSoup(resp.content, "lxml")
page_count = int(soup.find("div", attrs={"class" : "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)

for page in range(page_count):
    resp = req.get(
        url=f'https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=python+разработчик&from=suggest_post&page={page}',
        headers={"user-agent": ua}
    )
    soup = BeautifulSoup(resp.content, "lxml")
    for a in soup.find_all("a", attrs={"class" : "serp-item__title"}):
        resp = req.get(
            url=f"{a.attrs['href']}",
            headers={"user-agent": ua}
        )
        soup = BeautifulSoup(resp.content, "lxml")
        try:
            name = soup.find(attrs={"class" : "bloko-header-section-1"}).text
        except:
            continue
        try:
            work_exp = soup.find(attrs={"class" : "vacancy-description-list-item"}).text.split(":")[-1]
        except:
            work_exp = "не указан"
        try:
            salary = soup.find(attrs={"class" : "bloko-header-section-2"}).text.replace("\xa0", "")
        except:
            salary = "з/п не указана"
        try:
            region = soup.find("span", attrs={"data-qa": "vacancy-view-raw-address"}).text.split(",")[0]
        except:
            region = "не указан"

        resume = {
            "title" : name,
            "work_experience" : work_exp,
            "salary" : salary,
            "region" : region
        }

        data.append(resume)
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4,ensure_ascii=False)
