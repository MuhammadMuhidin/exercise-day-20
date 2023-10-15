import requests
import pandas as pd
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Initialize PyMongo client
with open('mongodb_uri.txt', 'r') as file:
    uri = file.read().strip()
client = MongoClient(uri, server_api=ServerApi('1'))

# Value to be inserted
judul_list = []
link_list = []

# Enumerate pages
for page_number in range(1, 10):
    if page_number == 1:
        uri = 'https://inet.detik.com/indeks'
    else:
        uri = f'https://inet.detik.com/indeks?page={page_number}'
    response = requests.get(uri)

    # If status code is 200 then proceed
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find_all('article', class_='list-content__item')

        for a in article:
            judul = a.find('h3', 'media__title').text.strip()   
            link = a.find('a')['href']

            # Append to list
            judul_list.append(judul)
            link_list.append(link)

# Dataframe to be inserted
df = pd.DataFrame({
    "Judul": judul_list,
    "Link": link_list
})

# Insert to MongoDB by filter head 10 in Dataframe
df = df.head(10)
db = client["detik"]
collection = db["top_10_indeks"]
collection.insert_many(df.to_dict(orient="records"))
client.close()









