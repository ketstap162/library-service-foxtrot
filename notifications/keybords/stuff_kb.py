from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("/Users")
b2 = KeyboardButton("/Books")
b3 = KeyboardButton("/Borrowing")

kb_stuff = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
)

kb_stuff.row(b1, b2, b3)
