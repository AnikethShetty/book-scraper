import requests
from bs4 import BeautifulSoup
import csv
import logging
from urllib.parse import urljoin

logging.basicConfig(
    filename="scraper.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "http://books.toscrape.com/"
START_URL = BASE_URL + "catalogue/page-1.html"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_books():
    books = []
    current_url = START_URL

    while current_url:
        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"HTTP error: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        book_items = soup.find_all("article", class_="product_pod")

        for book in book_items:
            try:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text.replace("£", "")
                availability = book.find("p", class_="instock availability").text.strip()
                rating_class = book.find("p", class_="star-rating")["class"][1]
                rating = RATING_MAP.get(rating_class)
                relative_url = book.h3.a["href"]
                product_url = urljoin(BASE_URL + "catalogue/", relative_url)

                books.append([title, price, rating, availability, product_url])

            except Exception as e:
                logging.error(f"Extraction error: {e}")
                continue

        next_page = soup.find("li", class_="next")
        if next_page:
            current_url = urljoin(current_url, next_page.a["href"])
        else:
            current_url = None

    save_to_csv(books)

def save_to_csv(data):
    with open("books_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Rating", "Availability", "URL"])
        writer.writerows(data)

    print("Data saved successfully!")

if __name__ == "__main__":
    scrape_books()
