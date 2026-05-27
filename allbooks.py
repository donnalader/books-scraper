import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import re

url = "http://books.toscrape.com/"

response = requests.get(url, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')

category_links = soup.find("ul", class_="nav nav-list").find_all("a")

categories = []
for link in category_links:
    name = link.text.strip()
    href = link['href']

    if name != "Books":
        full_url = urljoin(url, href)
        categories.append((name, full_url))

for category_name, category_url in categories:
    print(f"\nScraping category: {category_name}")

    url = category_url
    category_books = []

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Page: {url}")


        books = soup.find_all("article", class_="product_pod")

        for book in books:
            relative_url = book.find("h3").find("a")['href']
            product_url = urljoin(url, relative_url)

            print(f"Processing book: {product_url}")

            try:
                book_response = requests.get(product_url, timeout=10)
                book_soup = BeautifulSoup(book_response.text, 'html.parser')

                import time
                time.sleep(0.5)

            except Exception as e:
                print(f"Error loading {product_url}: {e}")
                continue
          

            title = book_soup.find("h1").text

            table = book_soup.find("table")
            product_info = {}
            for row in table.find_all("tr"):
                key = row.find("th").text
                value = row.find("td").text
                product_info[key] = value

            upc = product_info.get("UPC")
            price_incl = product_info.get("Price (incl. tax)")
            price_excl = product_info.get("Price (excl. tax)")
            quantity_available = product_info.get("Availability")

            description_tag = book_soup.find("div", id="product_description")
            description = (
                description_tag.find_next_sibling("p").text
                if description_tag else""
            )

            rating_tag = book_soup.find("p", class_="star-rating")
            rating = rating_tag['class'][1] 
            
            image_relative = book_soup.find("img")['src']
            image_url = urljoin(product_url, image_relative)

            description = description.replace('\n', ' ').strip()

            match = re.search(r"\d+", quantity_available)
            quantity = match.group() if match else "0"

            rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            rating = rating_map.get(rating, rating)

            price_incl = price_incl.replace('£', '')
            price_excl = price_excl.replace('£', '')

            category_books.append({
                "product_page_url": product_url,
                "upc": upc,
                "book_title": title,
                "price_including_tax": price_incl,
                "price_excl": price_excl,
                "quantity_available": quantity,
                "product_description": description,
                "category_name": category_name,
                "review_rating": rating,        
                "image_url": image_url
            })

        next_button = soup.find("li", class_="next")
        if next_button:
            next_page = next_button.find("a")['href']
            url = urljoin(url, next_page)
                              
        else:
            break
    filename = f"{category_name.lower().replace(' ', '_')}.csv"

    with open(filename,"w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=category_books[0].keys())
        writer.writeheader()
        writer.writerows(category_books)

    print(f"{filename} ({len(category_books)} books)")