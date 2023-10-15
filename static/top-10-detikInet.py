import requests
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect("detik.db")
judul_list = []
link_list = []

for page_number in range(1, 10):
    if page_number == 1:
        uri = 'https://inet.detik.com/indeks'
    else:
        uri = f'https://inet.detik.com/indeks?page={page_number}'
    response = requests.get(uri)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find_all('article', class_='list-content__item')

        for a in article:
            judul = a.find('h3', 'media__title').text.strip()   
            link = a.find('a')['href']
            judul_list.append(judul)
            link_list.append(link)

df = pd.DataFrame({
    "Judul": judul_list,
    "Link": link_list
})
df = df.head(10)
df.to_sql("top_10_indeks", conn, index=False, if_exists="replace")
print("Scapping success, file saved as detik.db")





