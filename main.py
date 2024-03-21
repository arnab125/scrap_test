import time
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# Function to generate random sleep time
def random_sleep(minimum, maximum):
    time.sleep(random.uniform(minimum, maximum))
"""
proxy_list = []
with open("http_proxies.txt", "r") as file:
    for line in file:
        proxy_list.append(line)
print(proxy_list)

proxies = {
    "http": random.choice(proxy_list).strip(),
}



print(proxies)
"""
categories = []

proxies = {}


def scrap_categories_links():
    try:
        url = "https://www.amazon.com/Best-Sellers-Audible-Books-Originals/zgbs/audible/ref=zg_bs_unv_audible_1_18571910011_1"
        headers = {'User-Agent': UserAgent().random, 'Accept-Language': 'en-US,en'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        random_sleep(2, 4)  # Add a random delay to simulate human behavior
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all("div",
                              class_="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8",
                              role="treeitem")
        for item in items:
            a_tag = item.find("a")
            if a_tag:
                href = a_tag.get("href")
                categories.append(f"https://www.amazon.com{href}")
    except Exception as e:
        print("Error:", e)
    return categories


def scrape_category(url):
    try:
        headers = {'User-Agent': UserAgent().random, 'Accept-Language': 'en-US,en'}
        random_sleep(2, 4)  # Add a random delay to simulate human behavior
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
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

        df = pd.DataFrame(data)
        df.to_csv(f"{url.split('/')[-5]}.csv", index=False)
        print(f"Saved {len(data)} products to {url.split('/')[-5]}.csv")


    except Exception as e:
        print("Error:", e)


links = scrap_categories_links()
print(links)

if len(links) > 0 or links is not None:
    for link in links:
        scrape_category(link)
