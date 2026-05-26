import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

url = "https://books.toscrape.com/catalogue/category/books/romance_8/index.html"

product_urls = []

while True:
    print("Scraping:", url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        relative_url = book.find("h3").find("a")["href"]
        full_url = urljoin(url, relative_url)
        product_urls.append(full_url)
    next_button = soup.find("li", class_="next")
    if next_button:
        next_page = next_button.find("a")["href"]
        url = urljoin(url, next_page)
    else:
        break 

with open("all_romance_book_urls.csv", "w", newline="",encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["product_page_url"])
    for url in product_urls:
        writer.writerow([url])
print("Saved to all_romance_book_urls.csv")
