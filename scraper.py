# Used to send HTTP requests to the website
import requests

# Used to parse and extract HTML content
from bs4 import BeautifulSoup

# Used to write scraped data into CSV files
import csv

# Used to log information and errors during execution
import logging

# Used to safely create full URLs from relative links
from urllib.parse import urljoin

# Logging configuration
# All INFO and ERROR messages are stored in scraper.log
# This helps in debugging and tracking scraper execution

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Base URL of the website to scrape
# START_URL points to the first page of the catalogue
BASE_URL = "http://books.toscrape.com/"
START_URL = BASE_URL + "catalogue/page-1.html"

# Mapping textual star ratings to numeric values
# Example: "Three" → 3
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_books():
    """
    Scrapes all book data from the website by iterating through
    all pages and collecting required book information.
    """
    books = []
    current_url = START_URL

    while current_url:
        # Log the URL of the page currently being scraped
        logging.info(f"Fetching page: {current_url}")
        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"HTTP error: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
                # Find all book entries on the page
        book_items = soup.find_all("article", class_="product_pod")

        # Loop through each book and extract details
        for book in book_items:
            try:
                title = book.h3.a["title"]
                price_text = book.find("p", class_="price_color").text
                price = price_text.encode("ascii", "ignore").decode().replace("£", "").strip()
                availability = book.find("p", class_="instock availability").text.strip()
                rating_class = book.find("p", class_="star-rating")["class"][1]
                rating = RATING_MAP.get(rating_class)
                relative_url = book.h3.a["href"]
                product_url = urljoin(BASE_URL + "catalogue/", relative_url)

                books.append([title, price, rating, availability, product_url])

            except Exception as e:
                logging.error(f"Extraction error: {e}")
                continue

        # Check if a next page exists and update the URL
        next_page = soup.find("li", class_="next")
        if next_page:
            current_url = urljoin(current_url, next_page.a["href"])
        else:
            current_url = None

# This function saves the scraped book data into a CSV file
# It ensures proper formatting and logs success or failure
    save_to_csv(books)

def save_to_csv(data):
    """
    Saves the extracted book data into a CSV file.
    """
    with open("books_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Rating", "Availability", "URL"])
        writer.writerows(data)

    logging.info("CSV file saved successfully")
    print("Data saved successfully!")

if __name__ == "__main__":
    scrape_books()
