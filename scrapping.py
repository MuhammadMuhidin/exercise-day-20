import re
import requests
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup


# Connect to the database
conn = sqlite3.connect("books.db")

# Create variable to store data
names = []
prices = []
ratings = []

# Method to get rating, with concept of mapper
def get_rating(txt):
    mapper = {"one" : 1, "two" : 2, "three" : 3, "four" : 4, "five" : 5}
    return mapper[txt]

# Enumerate the pages
for page_number in range(1, 10):
    if page_number == 1:
        uri = 'https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html'
    else:
        uri = f'https://books.toscrape.com/catalogue/category/books/nonfiction_13/page-{page_number}.html'
    response = requests.get(uri)

    # Check the response if it is 200
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("article", class_="product_pod")
        rating_pattern = re.compile("star-rating.*")

        # Enumerate the products in the page
        # Get the name, price and rating
        # Append the data
        for product in products:
            product_name_tag = product.find("h3").text
            names.append(product_name_tag)

            product_price_tag = product.find("div", "product_price")
            product_price_txt = product_price_tag.find("p", "price_color").text
            prices.append(product_price_txt)

            rating_tag = product.find("p", class_=rating_pattern)
            rating_num = get_rating(rating_tag["class"][1].lower())
            ratings.append(rating_num)

# Create a dataframe
df = pd.DataFrame({
  "Name" : names,
  "Price" : prices,
  "Rating" : ratings
})

# Save the dataframe as a sqlite database
df.to_sql("books", conn, index=False, if_exists="replace")
print("Scapping success, file saved as books.db")