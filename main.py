from aiogram import Bot, Dispatcher, executor, types
import requests
import logging
from config import TOKEN_API
from keyboard import keyboard


logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

HELP_COMMAND = '''
/help - список команд
/start - начать работу с ботом'''


async def on_startup(_):
    print('Бот запущен!')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user = message.from_user
    await message.answer(text=f"Привет, {user.first_name}! Этот бот скачивает книги с сайте 'flibusta.club'. Для скачивания"
                              " напиши имя книги или интересующего автора ")
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND, reply_markup=keyboard)
    await message.delete()


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def search_book(message: types.Message):
    pass


async def search_book_on_flibusta(book_name: str, page: int):
    if requests.status_codes == 200:
        params = {'ask': book_name}
        response = requests.get("https://flibusta.club/booksearch", params=params)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

