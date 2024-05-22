import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data from a book's individual URL
def scrape_book_details(book_url):
    response = session.get(book_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        table_raws = soup.css.select('table tr')
        # Extract additional data as needed
        relative_image_url = soup.select_one('.item.active img')['src']
        base_url = "https://books.toscrape.com"
        image_url = relative_image_url.replace('../.../', '/')  # Adjusting the path
        full_image_url = base_url + image_url
        return {'title': soup.css.select_one('.product_main h1').text.strip(),
               'product_type': table_raws[1].css.select_one('td').text.strip(),
               'price_excl_tax' : table_raws[2].css.select_one('td').text.strip(),
               'price_incl_tax' : table_raws[3].css.select_one('td').text.strip(),
               'tax' : table_raws[4].css.select_one('td').text.strip(),
               'availability' : table_raws[5].css.select_one('td').text.strip(),
               'num_reviws' : table_raws[6].css.select_one('td').text.strip(),
               'description': soup.css.select_one('.sub-header').next_sibling.next_sibling.text.strip(),
               'stars': soup.css.select_one('.product_main p.star-rating')['class'][1],
               'category': soup.css.select_one('li.active').previous_sibling.previous_sibling.a.text.strip(),
               'image_url': full_image_url,
               }
    else:
        print(f"Error fetching details for {book_url}: {response.status_code}")
        return None

# Make a request to the URL
def scrape_books(url):
    response = session.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        # Work with the BeautifulSoup object
        books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
        for book in books:
            relative_url = book.h3.a['href']
            # Scrape additional data from each book's URL
            if 'catalogue' in relative_url:
                book_url = 'https://books.toscrape.com/'+relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/'+relative_url

            yield scrape_book_details(book_url)

        next_page = soup.find('li', class_='next')
        print('*'*40)
        if next_page is not None:
            next_page = next_page.a['href']
            if 'catalogue' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield from scrape_books(next_page_url)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")

# Starting URL
def main():
    url = "https://books.toscrape.com/"
    books_info = scrape_books(url)
    info = [book for book in books_info]
    df = pd.DataFrame(info)
    df.to_csv('books.csv', index=False)
    print(f'Data written to books.csv')
# Use a session for requests
session = requests.Session()
main()
