import config
import message_texts
import json
import random
import ast
from aiogram import Dispatcher, Bot, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from sqlite import create_profile, add_word_to_vocab, get_random_word_from_vocab, get_word_translaition, add_vocab, add_word_to_knowledge_base
from misc.util import get_translated_word_list
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

storage = MemoryStorage()
TOKEN = config.token
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
crossIcon = u"\u274C"


class ProfileStatesGroup(StatesGroup):
    youtube_url = State()

# Handle '/start' and '/help'
@dp.message_handler(commands=['help', 'start'])
async def start(message: types.Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}! {message_texts.GREETINGS}")
    await create_profile(message.from_user.id, message.from_user.username)


@dp.message_handler(commands='word')
async def next_word(message: types.Message) -> None:
    await get_word(message.chat.id, message.from_user.username)


@dp.message_handler(commands='youtube_add')
async def youtube_vocab(message: types.Message) -> None:
    await message.answer("Отправьте в чат ссылку на ютуб видео")
    await ProfileStatesGroup.youtube_url.set()


@dp.message_handler(content_types='text', state=ProfileStatesGroup.youtube_url)
async def add_youtube_vocab(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if "youtu" in message.text:
            data["yotube_url"] = message.text

            await message.answer("video starts parsing...")
            yt_videoname, youtube_id, yt_word_list = get_translated_word_list(message.text)
            await message.answer("parsing end, you can learn new words...")
            await add_vocab(youtube_id, yt_videoname, "youtube")
            for word, translation in yt_word_list.items():
                await add_word_to_vocab(word, translation, youtube_id)

            await state.finish()


async def get_word(chat_id, username):
    word, translation = await get_random_word_from_vocab()
    if not word:
        await bot.send_message(
            chat_id=chat_id,
            text="Ваш словарь пуст, загрузите видео..",
            parse_mode='HTML')

    await bot.send_message(
        chat_id=chat_id,
        text=word + " переводится как: " + translation,
        reply_markup=get_inline_keyboard(word, translation),
        parse_mode='HTML')


def get_inline_keyboard(word, translation) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    ikb.add(
        InlineKeyboardButton(
            text=word,
            callback_data="btn_show_translation"),
        InlineKeyboardButton(
            text=crossIcon,
            callback_data="btn_add_word_to_vocab"),
    )
    ikb.add(
        InlineKeyboardButton(
            text=f'Вперёд --->',
            callback_data='btn_next_word'))
    return ikb


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("btn"))
async def handle_query(call: types.callback_query) -> None:
    username = call.from_user.username
    word = call["message"]["reply_markup"]["inline_keyboard"][0][0]["text"]
    translation = await get_word_translaition(word)

    if call.data == "btn_show_translation":
        await bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text=word + " переводится как: " + translation)

    if call.data == "btn_next_word":
        await get_word(chat_id=call.message.chat.id, username=username)
