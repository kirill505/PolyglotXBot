import config
import message_texts
from aiogram import Dispatcher, Bot, types

TOKEN = config.token
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Handle '/start' and '/help'
@dp.message_handler(commands=['help', 'start'])
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! {message_texts.GREETINGS}")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply("hello")

