import requests
from bs4 import BeautifulSoup


def parser(book_name):
    params = {'ask': book_name}
    response = requests.get('https://flibusta.club/booksearch/', params=params).text
    soup = BeautifulSoup(response, 'html.parser')
    items = soup.find('div', {'id': 'main', 'class': 'clear-block'})
    books = []

    if items:
        book_links = items.find_all('a', href=True)
        for link in book_links:
            title = link.get_text().strip()
            url = link['href']
            books.append((title, url))
    return books


def link_parser(link):
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'html.parser')
    links = []
    link_elements = soup.find_all('span', class_='link')

    for link in link_elements:
        links.append(
            {
                link.text: link.get('onclick').split("'")[1]
            }
        )
    return links