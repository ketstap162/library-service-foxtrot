from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from notifications.keybords.stuff_kb import kb_stuff

bot = Bot(token="5940358054:AAEFRx8od9PwXF1aSRet74wy4eh1Lre0wMM")
db = Dispatcher(bot)


async def on_startup(_):
    print("Bot is online")


@db.message_handler(commands=["start", "help"])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "start", reply_markup=kb_stuff)
        await message.delete()
    except Exception:
        await message.reply(
            "Contact with bot, write him:\nhttps://t.me/library_project_bot "
        )


@db.message_handler(commands=["users"])
async def commands_users(message: types.Message):
    await bot.send_message(message.from_user.id, "all_users")


@db.message_handler(commands=["books"])
async def commands_books(message: types.Message):
    await bot.send_message(message.from_user.id, "all_books")


@db.message_handler()
async def echo_send(message: types.Message):
    if message.text == "hi":
        await message.answer("Hello")


executor.start_polling(db, skip_updates=True, on_startup=on_startup)
