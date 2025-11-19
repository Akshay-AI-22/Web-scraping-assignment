## Web Scraper - Books.toscrape.com
A Python web scraper built with Scrapy framework to extract book information from books.toscrape.com and store it in both CSV and SQLite database formats.

📋 Overview
This project scrapes book data from the books.toscrape.com e-commerce website, extracting information such as titles, prices, availability, and ratings. 
The scraped data is saved to both a CSV file and a SQLite database for flexible data access.

✨ Features
- Multi-page scraping: Scrapes data from the first 5 pages of the website
- Book ratings included: Extracts and converts star ratings to numerical values (1-5)
- Dual storage: Saves data to both CSV file (books.csv) and SQLite database (books.db)
- Modular design: Well-structured code with separate classes for scraping and data processing
- Error handling: Includes validation and error handling for robust operation
- Data cleaning: Automatically cleans price data and validates ratings

🎯 Data Scraped
The scraper extracts the following information for each book:
FieldDescriptionTitleFull title of the bookPricePrice in pounds (£), converted to floatAvailabilityStock status (e.g., "In stock")RatingStar rating converted to number (1-5)

🛠️ Technologies Used
- Python 3.x
- Scrapy: Web scraping framework
- SQLite3: Database storage
- CSV: File-based data export

📦 Installation
Clone or download the repository
Install required dependencies:

> bashpip install scrapy

Verify Python version (Python 3.6+ recommended):

> bashpython --version

🚀 Usage
Run the scraper with:
bashpython Web_Scraping_Assignment.py

The script will:
- Start scraping from page 1 of books.toscrape.com
- Extract data from the first 5 pages
- Display progress messages
- Create books.csv and books.db files in the current directory
- Show total books scraped upon completion
