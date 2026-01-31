import unittest
import csv
import os

class TestBookScraper(unittest.TestCase):

    def test_csv_file_exists(self):
        self.assertTrue(os.path.exists("books_data.csv"))

    def test_csv_not_empty(self):
        with open("books_data.csv", "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
            self.assertGreater(len(rows), 1)

    def test_csv_headers(self):
        with open("books_data.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(header, ["Title", "Price", "Rating", "Availability", "URL"])

    def test_data_structure(self):
        with open("books_data.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.assertEqual(len(row), 5)

    def test_missing_data(self):
        with open("books_data.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                for value in row:
                    self.assertNotEqual(value.strip(), "")

if __name__ == "__main__":
    unittest.main()
