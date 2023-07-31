from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
help_button = KeyboardButton('/help')
keyboard.add(help_button)



