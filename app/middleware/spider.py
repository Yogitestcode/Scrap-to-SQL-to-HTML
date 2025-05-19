import requests
from bs4 import BeautifulSoup
import mysql.connector


def scrap_product_on_page(page):
    url = 'https://books.toscrape.com/catalogue/page-{}.html'.format(page)
    books = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('article', class_='product_pod')
        for article in articles:
            title = article.h3.a['title']
            price = article.find('p', class_='price_color').text
            availability = article.find('p', class_='instock availability').text.strip()
            books.append((title, price, availability))

        next_button = soup.find('li', class_='next')
        if next_button:
            next_url = next_button.a['href']
            url = 'http://books.toscrape.com/catalogue/' + next_url
        else:
            url = None
    print(books)
    return books

def get_pages_number():
    url = 'https://books.toscrape.com/catalogue/page-1 .html'
    books = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        pages = soup.find('ul', class_='pager').find('li', class_='current').text.strip().split()

        pages = max(int(page) for page in pages if page.isdigit())
        return pages
    
def get_product_details(url):
    headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#'accept-encoding' : 'gzip, deflate, br, zstd',
'accept-language' : 'en-US,en;q=0.6',
'cache-control' : 'max-age=0' ,
'if-modified-since' : 'Wed, 08 Feb 2023 21:02:32 GMT' ,
'if-none-match' : 'W/"63e40de8-476e"' ,
'priority' : 'u=0, i' ,
'referer' : 'https://books.toscrape.com/catalogue/page-1.html' ,
'sec-ch-ua' : '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
'sec-ch-ua-mobile' : '?0',
'sec-ch-ua-platform' : '"Windows"',
'sec-fetch-dest' : 'document',
'sec-fetch-mode' : 'navigate',
'sec-fetch-site' : 'same-origin',
'sec-fetch-user' : '?1',
'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_details = {}



    # Product Description
    product_description = soup.find('div', attrs={"id": 'product_description'}).find_next('p').text
    product_details['description'] = product_description

    
    # Product Price
    price = soup.find('p', class_='price_color').text.strip()
    product_details['price'] = price

    # Availability
    availability = soup.find('p', class_='instock availability').text.strip()
    product_details['availability'] = availability

    # UPC, Product Type, etc.
    product_info_table = soup.find('table', class_='table table-striped')
    rows = product_info_table.find_all('tr')
    for row in rows:
        header = row.find('th').text.strip()
        value = row.find('td').text.strip()
        product_details[header] = value

    return product_details

    #FOR MAKING DUMMY HTML
    #f = open('test.html' , 'w', encoding = 'utf-8')
   # f.write(response.text)
  #  f.close()