import requests
from bs4 import BeautifulSoup

def get_data():
    data = requests.get('https://www.gismeteo.ru/diary/4368/2021/9/').text
    print(data)
get_data()