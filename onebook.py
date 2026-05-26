import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Send a GET request to the website
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Extract the desired information
product_page_url = url
book_title = soup.find("h1").text
table = soup.find("table", {"class": "table table-striped"} )
rows = table.find_all("tr")
product_info = {}
for row in rows:
    key = row.find("th").text
    value = row.find("td").text
    product_info[key] = value
upc = product_info.get("UPC", "N/A")
price_including_tax = product_info.get("Price (incl. tax)", "N/A")
price_excluding_tax = product_info.get("Price (excl. tax)", "N/A")
quantity_available = product_info.get("Availability", "N/A")
description_tag = soup.find("div", {"id": "product_description"})
if description_tag:
    product_description = description_tag.find_next_sibling("p").text   
else:
    product_description = "No description available."
category = soup.find("ul", {"class": "breadcrumb"}).find_all("li")[2].text.strip()
review_rating = soup.find("p", {"class": "star-rating"})["class"][1]
image_relative = soup.find("div", {"class": "item active"}).find("img")["src"]
image_url = "https://books.toscrape.com/" + image_relative.replace("../", "")


data = {
    "product_page_url": product_page_url,
    "upc": upc,
    "book_title": book_title,
    "price_including_tax": price_including_tax,
    "price_excluding_tax": price_excluding_tax,
    "quantity_available": quantity_available,
    "product_description": product_description,
    "category": category,
    "review_rating": review_rating,
    "image_url": image_url
}
with open("book_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)

    print("Data has been written to book_data.csv")
          
    