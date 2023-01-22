import asyncio
import config
import message_texts
from telebot.async_telebot import AsyncTeleBot


bot = AsyncTeleBot(config.token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, message_texts.GREETINGS)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)


asyncio.run(bot.polling())
