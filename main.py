from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

HELP_COMMAND = '''
/help - список команд
/start - начать работу с ботом'''


async def on_startup(_):
    print('Бот запущен!')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text="Привет! Этот бот скачивает книги с сайте 'flibusta.club'. Для скачивания"
                              " напиши имя книги или интересующего автора ")
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND)
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

