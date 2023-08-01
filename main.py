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


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    bot.reply_to(message=message, text='Привет!')


@bot.message_handler(commands=['search'])
def search_command(message: Message):
    bot.send_message(message.chat.id, "Пожалуйста, укажите название книги или автора для поиска.")


@bot.message_handler(content_types=['text'])
def get_books(message: Message):
    if message.text:
        book_name = message.text.strip()
        book_data = parser(book_name)
        if book_data:
            response_text = ""
            for i, (title, url) in enumerate(book_data, start=1):
                response_text += f"{i}. {title} - {url}\n"
                if len(response_text) <= 405:
                    bot.send_message(message.chat.id, response_text)
                    response_text = ""
            if response_text:
                bot.send_message(message.chat.id, response_text)
        else:
            bot.send_message(message.chat.id, f"Книги с названием '{book_name}' не найдено.")


if __name__ == '__main__':
    bot.polling()
