# Books to Scrape – Web Scraping Project

## Project Overview
This project is designed to scrape book information from the website
http://books.toscrape.com using Python. The extracted data is stored
in a CSV file for further analysis.

---

## Business Flow

1. The scraper sends an HTTP request to the website homepage.
2. The HTML content is parsed using BeautifulSoup.
3. Book details such as title, price, rating, availability,
   and product URL are extracted.
4. The scraper checks for pagination and navigates through
   all available pages.
5. The extracted data is stored in memory.
6. Once scraping is complete, the data is saved into a CSV file.
7. Logging is used to record page fetches, errors, and success messages.

---

## Error Handling
- Missing book fields are skipped without stopping execution.
- HTTP errors (404, 503, etc.) are logged.
- The scraper continues execution safely.

---

## Output
- CSV File: books_data.csv
- Log File: scraper.log

---

## Tools Used
- Python
- Requests
- BeautifulSoup
- CSV
- Logging
- Visual Studio Code
