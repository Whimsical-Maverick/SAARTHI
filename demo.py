from bs4 import BeautifulSoup
import requests
import re

url="https://quotes.toscrape.com/"

header={
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response=requests.get(url,headers=header)

soup = BeautifulSoup(response.text,"html.parser")

quote=[sp.get_text() for sp in soup.find_all("span",class_="text")]
author = [ath.get_text() for ath in soup.find_all("small",class_="author")]

for i in range(10):
    print(quote[i]+"-"+author[i])