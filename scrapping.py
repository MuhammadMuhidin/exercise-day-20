import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_rating(txt):
    mapper = {"one" : 1, "two" : 2, "three" : 3, "four" : 4, "five" : 5}
    return mapper[txt]
names = []
prices = []
ratings = []

for page_number in range(1, 10):
    if page_number == 1:
        uri = 'https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html'
    else:
        uri = f'https://books.toscrape.com/catalogue/category/books/nonfiction_13/page-{page_number}.html'
    response = requests.get(uri)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("article", class_="product_pod")
        rating_pattern = re.compile("star-rating.*")
 

        for product in products:
            product_name_tag = product.find("h3").text
            names.append(product_name_tag)

            product_price_tag = product.find("div", "product_price")
            product_price_txt = product_price_tag.find("p", "price_color").text
            prices.append(product_price_txt)

            rating_tag = product.find("p", class_=rating_pattern)
            rating_num = get_rating(rating_tag["class"][1].lower())
            ratings.append(rating_num)

df = pd.DataFrame({
  "Name" : names,
  "Price" : prices,
  "Rating" : ratings
})

df.to_csv("books.csv")