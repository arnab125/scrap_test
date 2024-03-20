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
# options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

# Use a random user agent to mimic different devices
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")

proxy_server = "http://35.185.196.38:3128"

# Set up proxy if necessary
options.add_argument(f'--proxy-server={proxy_server}')


# Function to generate random sleep time
def random_sleep(minimum, maximum):
    time.sleep(random.uniform(minimum, maximum))


categories = []


def scrap_categories_links():
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(
            "https://www.amazon.com/Best-Sellers-Audible-Books-Originals/zgbs/audible/ref=zg_bs_unv_audible_1_18571910011_1")
        random_sleep(2, 4)  # Add a random delay to simulate human behavior
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print(soup.prettify())
        items = soup.find_all("div",
                              class_="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8",
                              role="treeitem")
        # Iterate over each div element
        for item in items:
            # Find the <a> tag within the div element
            a_tag = item.find("a")
            if a_tag:
                # Extract and print the href attribute of the <a> tag
                href = a_tag.get("href")
                categories.append(f"https://www.amazon.com{href}")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()
        return categories


# Function to scrape product details from a category page
def scrape_category(url):
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "_cDEzb_iveVideoWrapper_JJ34T")))

        random_sleep(2, 4)  # Add a random delay to simulate human behavior

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract product details
        products = soup.find_all("div", class_="_cDEzb_iveVideoWrapper_JJ34T")
        data = []
        for product in products:
            book_name = product.find("div", class_="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y").text.strip()
            author = product.find("span", class_="a-size-small a-color-base").find("div",
                                                                                   class_="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y").text.strip()
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

        # Save the data to a CSV file
        df = pd.DataFrame(data)
        df.to_csv(f"{url.split('/')[-1]}.csv", index=False)
        print(f"Saved {len(data)} products to {url.split('/')[-1]}.csv")

    except Exception as e:
        print("Error:", e)
        return []
    finally:
        driver.quit()


links = scrap_categories_links()

if len(links) > 0 or links is not None:
    # Iterate over each category link
    for link in links:
        scrape_category(link)
