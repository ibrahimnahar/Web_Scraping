import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data from a book's individual URL
def scrape_book_details(book_url):
    response = session.get(book_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        table_rows = soup.select('table tr')
        
        # Extract the image URL and convert it from relative to absolute
        relative_image_url = soup.select_one('.item.active img')['src']
        # Remove '../' and prepend with base URL
        base_url = "https://books.toscrape.com"
        image_url = relative_image_url.replace('../.../', '/')  # Adjusting the path
        full_image_url = base_url + image_url

        # Extract additional data as needed
        return {
            'title': soup.select_one('.product_main h1').text.strip(),
            'product_type': table_rows[1].select_one('td').text.strip(),
            'price_excl_tax': table_rows[2].select_one('td').text.strip(),
            'price_incl_tax': table_rows[3].select_one('td').text.strip(),
            'tax': table_rows[4].select_one('td').text.strip(),
            'availability': table_rows[5].select_one('td').text.strip(),
            'num_reviews': table_rows[6].select_one('td').text.strip(),
            'description': soup.select_one('article.product_page p').text.strip(),
            'stars': soup.select_one('.product_main p.star-rating')['class'][1],
            'category': soup.select_one('ul.breadcrumb li:nth-child(3) a').text.strip(),
            'image_url': full_image_url  # Corrected field for image URL
        }
    else:
        print(f"Error fetching details for {book_url}: {response.status_code}")
        return None


# Function to scrape books from a page and iterate through pagination
def scrape_books(url):
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.find_all('article', class_='product_pod')
        for book in books:
            relative_url = book.find('h3').find('a')['href']
            book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield scrape_book_details(book_url)

        # Check for next page
        next_page = soup.find('li', class_='next')
        if next_page:
            next_url = 'https://books.toscrape.com/catalogue/' + next_page.find('a')['href']
            yield from scrape_books(next_url)
    else:
        print(f"Error loading page {url}: {response.status_code}")

# Main function to initiate scraping and save data to CSV
def main():
    url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    books_info = list(scrape_books(url))
    df = pd.DataFrame(books_info)
    df.to_csv('books.csv', index=False)
    print('Data written to bookss.csv')

# Use a session for requests
session = requests.Session()
main()
