import requests_
from bs4 import BeautifulSoup as BS

r = requests.get("http://stopgame.ru/review/new/izumitelno/p1")
html = BS (r.content, 'html.parser')
