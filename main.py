import time
import random
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure headless browser options
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

# Use a random user agent to mimic different devices
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")


# Function to generate random sleep time
def random_sleep(minimum=1, maximum=3):
    time.sleep(random.uniform(minimum, maximum))


# Function to scrape product details from a category page
def scrape_category(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "a-cardui")))

    random_sleep(2, 4)  # Add a random delay to simulate human behavior

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Extract product details
    products = soup.find_all("div", class_="a-cardui _cDEzb_grid-cell_1uMOS expandableGrid p13n-grid-content")
    data = []
    for product in products:
        book_name = product.find("div", class_="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y").text.strip()
        author = product.find("span", class_="a-size-small a-color-base").find("div", class_="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y").text.strip()
        rating = product.find("i").find("span", class_="a-icon-alt").text.strip()
        num_ratings = product.find("div", class_="a-icon-row").find("span", class_="a-size-small").text.strip()
        price = product.find("span", class_="p13n-sc-price").text.strip()
        img_link = product.find("img")["src"]
        data.append({
            "book_name": book_name,
            "author": author,
            "rating": rating,
            "num_ratings": num_ratings,
            "price": price,
            "img_link": img_link
        })

    return data


# URL of Amazon Audible Best Sellers
url_link = "https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Arts-Entertainment/zgbs/audible/18571910011/ref=zg_bs_nav_audible_1"

# Scrape data from the main page
main_page_data = scrape_category(url_link)
print(main_page_data)

# Save the data to a CSV file
df = pd.DataFrame(main_page_data)
df.to_csv("audible_books_new.csv", index=False)
print("Data saved to CSV file")


