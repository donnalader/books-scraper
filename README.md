Books to Scrape Web Scraper

This is a Python web scraping application that extracts book data from the website https:books.toscrape.com/.
The scraper collects data for all book categories, handles pagination and extracts detailed product information for each book on the website. The results have been saved into separate .csv files for each category of books. 

The features of this application are:
extracts all book categories from the home page
handles pagination automatically
scrapes detailed information, such as:
    product page url
    UPC
    book title
    price (including and excluding tax)
    quantity available
    product description
    category
    review rating
    image url
and then saves each category of books to its own .csv file.

The Installation would be as follows:
1. clone the Git repository: https://github.com/donnalader/books-scraper.git
2. go to the project directory: cd books-scraper
3. create a virtual environment: python -m venv env
4. activate the virtual environment: env\Scripts\Activate
5. install required packages listed in requirements.txt

To run the scraper using the terminal: python allbooks.py
    This script will extract all categories, scrape all books across all pages and save each category's data into a separate .csv file. 

Donna Lader - author