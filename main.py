from pydoc import html

import telebot
import requests
from bs4 import BeautifulSoup
from telebot.types import Message
from config import TOKEN_API

bot = telebot.TeleBot(TOKEN_API)


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


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    bot.reply_to(message=message, text='Привет!')


@bot.message_handler(commands=['search'])
def search_command(message: Message):
    bot.send_message(message.chat.id, "Пожалуйста, укажите название книги или автора для поиска.")


@bot.message_handler(content_types=['text'])
def handle_text_message(message: Message):
    if message.text.startswith("https://flibusta.club"):
        # Если это ссылка на сайт, тогда вызываем функцию link_parser
        links = link_parser(message.text)
        # Отправляем результат работы функции в ответ пользователю
        bot.send_message(message.chat.id, str(links))
    else:
        # Если это не ссылка на сайт, тогда обрабатываем как текст и выполняем поиск книги
        book_name = message.text.strip()
        book_data = parser(book_name)
        if book_data:
            response_text = ""
            for i, (title, url) in enumerate(book_data, start=0):
                if title == 'Главная' and url == '//':
                    continue
                else:
                    current_text = f"{i}. {html.escape(title)} - <a href='https://flibusta.club{url}'>{html.escape(url)}</a>\n"
                    if len(response_text) + len(current_text) <= 4096:
                        response_text += current_text
                    else:
                        bot.send_message(message.chat.id, response_text, parse_mode='HTML')
                        response_text = current_text
            if response_text:
                bot.send_message(message.chat.id, response_text, parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, f"Книги с названием '{book_name}' не найдено")


if __name__ == '__main__':
    bot.polling()
