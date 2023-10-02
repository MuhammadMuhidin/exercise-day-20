from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import sqlite3
import time

# Create variables to initialize
conn = sqlite3.connect('gmaps.db')
driver = webdriver.Chrome()
driver.get('https://www.google.com/maps')
keyword = 'Indomaret near Cinere Depok'

# Create variables to store result
location_names = []
location_address = []

# Initialize searchbox
# Input keyword into searchbox
search_box_xpath = '//*[@id="searchboxinput"]'
search_element = driver.find_element(By.XPATH, search_box_xpath)
search_element.click()
search_element.send_keys(keyword)
search_element.send_keys(Keys.ENTER)
time.sleep(5)

# Initialize to prepare infinite scroll
scroll_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
scroll_element = driver.find_element(By.XPATH, scroll_xpath)
init_wait = WebDriverWait(driver, 30)
print('wait initial text displayed before infinity scroll')
init_wait.until(lambda _: scroll_element.is_displayed())

# Do Infinite scroll
while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", driver.find_element(By.XPATH, scroll_xpath))

        # If the last element is reached, break
        most_bottom_el = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[last()]')
        if most_bottom_el.text.strip().lower() == 'anda telah mencapai akhir daftar.':
            break

# Get all locations
locations_el = driver.find_elements(By.XPATH, '//*[@class="Nv2PK tH5CWc THOPZb "]')
print(f"There are {len(locations_el)} locations found with '{keyword}' keyword")

# Loop through each location
for loc_element in locations_el:
    name_el = loc_element.find_element(By.XPATH, ".//a[contains(@href, 'google.com')]")
    name = name_el.get_attribute('aria-label')
    address_el = loc_element.find_element(By.XPATH, './/div[@class="bfdHYd Ppzolf OFBs3e "]//div[contains(@class, "fontBodyMedium")]/div[4]/div[1]')

    # Store result
    location_names.append(name)
    location_address.append(address_el.text)

# Create dataframe
df = pd.DataFrame({
    'name': location_names,
    'address': location_address,
    'keyword' : keyword
})

# Save dataframe to sqlite database
df.to_sql('locations', conn, index=False, if_exists='replace')
print("Scapping success, file saved as gmaps.db")