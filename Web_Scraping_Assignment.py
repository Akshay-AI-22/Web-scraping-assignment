import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
import sqlite3
import csv


class BookItem(Item):
    """Template for book data."""
    title = Field()
    price = Field() 
    availability = Field()
    rating = Field()


class BooksScraper:
    """
    This class handles all the data processing:
    - Cleans the data
    - Saves to SQLite database
    - Exports to CSV file
    """
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.csv_file = None
        self.csv_writer = None

    def open_spider(self, spider):
        """Initialize database and CSV file when scraping starts."""
        # Setup SQLite database
        self.connection = sqlite3.connect('books.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL,
                availability TEXT,
                rating INTEGER
            )
        ''')
        self.connection.commit()

        # Setup CSV file
        self.csv_file = open('books.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(
            self.csv_file,
            fieldnames=['Title', 'Price', 'Availability', 'Rating']
        )
        self.csv_writer.writeheader()

    def close_spider(self, spider):
        """Close database connection and CSV file when scraping finishes."""
        if self.connection:
            self.connection.close()
        if self.csv_file:
            self.csv_file.close()

    def process_item(self, item, spider):
        """Clean data, save to database, and export to CSV."""
        # Clean price data
        if item.get('price'):
            orignalPrice = item['price'].replace('£', '').strip()
            item['price'] = float(orignalPrice)

        # Validate rating
        rating = item.get('rating', 0)
        if rating < 0 or rating > 5:
            item['rating'] = 0

        # Save to database
        try:
            self.cursor.execute('''
                INSERT INTO books (title, price, availability, rating)
                VALUES (?, ?, ?, ?)
            ''', (
                item['title'],
                item['price'],
                item['availability'],
                item['rating'],
            ))
            self.connection.commit()
        except Exception as e:
            print(f"Error saving to database: {e}")

        # Save to CSV
        self.csv_writer.writerow({
            'Title': item['title'],
            'Price': item['price'],
            'Availability': item['availability'],
            'Rating': item['rating']
        })

        return item

class BooksSpider(scrapy.Spider):
    """Main scraper that visits the website and extracts book data."""

    name = 'booksSpider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/catalogue/page-1.html']

    def __init__(self):
        super().__init__()
        self.MAX_PAGES = 5
        self.current_page = 1
        self.books_count = 0

    def parse(self, response):
        """Extract data from each page."""
        books = response.css('article.product_pod')

        for book in books:
            item = BookItem()
            item['title'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('p.price_color::text').get()

            availability = book.css('p.instock.availability::text').getall()
            item['availability'] = ''.join(availability).strip()

            rating = book.css('p.star-rating::attr(class)').get()
            item['rating'] = self.convert_rating_to_number(rating)

            self.books_count += 1
            yield item

        # Move to next page
        if self.current_page < self.MAX_PAGES:
            self.current_page += 1
            next_page_url = f'http://books.toscrape.com/catalogue/page-{self.current_page}.html'
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            print(f"\nScraping complete! Total books found: {self.books_count}")

    def convert_rating_to_number(self, rating):
        """Convert rating from text to number."""
        ratingMap = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

        if rating:
            for word in rating.split():
                if word in ratingMap:
                    return ratingMap[word]
        return 0


def main():
    """Main function to configure and run the scraper."""
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0',
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 8,
        'ITEM_PIPELINES': {
            '__main__.BooksScraper': 100,
        },
        'LOG_LEVEL': 'WARNING',
    }

    process = CrawlerProcess(settings)
    process.crawl(BooksSpider)
    process.start()


if __name__ == '__main__':
    try:
        print("Starting book scraper...")
        main()
    except Exception as e:
        print(f"\nError: {e}")
