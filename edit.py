# file_id='AgACAgIAAxkBAAIDyGX4Z72CNF1shKwrt-COdcqSLXmEAAIf2DEbhNTAS4LcfUYcORqdAQADAgADbQADNAQ'
# file_id='AgACAgIAAxkBAAIDyWX4Z_fXusUjnqeyiGt122npshEhAAIi2DEbhNTAS5y6Yez_aIotAQADAgADbQADNAQ
from aiogram.types import (Message,CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup,
                           InputMediaDocument,InputMediaPhoto,InputMediaVideo)
from aiogram import Dispatcher,Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter,Command,CommandStart
from aiogram import F
from aiogram.fsm.storage.redis import RedisStorage,Redis
from aiogram.fsm.state import State,StatesGroup,default_state
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

BOT_TOKEN = '6770547708:AAESTRQgbjl1lPqv4DPZXxeYOUVbb7OPyk4'
redis = Redis(host='localhost')
storage=RedisStorage(redis=redis)
dp =Dispatcher(storage=storage)
bot = Bot(token=BOT_TOKEN)

user_dict:dict[str,str] = {'photo_1':'AgACAgIAAxkBAAIDyGX4Z72CNF1shKwrt-COdcqSLXmEAAIf2DEbhNTAS4LcfUYcORqdAQADAgADbQADNAQ',
                           'photo_2':'AgACAgIAAxkBAAIDyWX4Z_fXusUjnqeyiGt122npshEhAAIi2DEbhNTAS5y6Yez_aIotAQADAgADbQADNAQ'} 

def get_keyb()->InlineKeyboardMarkup:
    button = InlineKeyboardButton(text='Next',callback_data='Next')
    keyboard = InlineKeyboardMarkup(inline_keyboard= [[button]])
    return keyboard

@dp.message(CommandStart())
async def strt(message:Message):
    markup=get_keyb()
    await message.answer_photo(photo=user_dict['photo_1'],reply_markup=markup,caption='')

@dp.callback_query(F.data.in_(
    ['text', 'audio', 'video', 'document', 'photo', 'voice'] ))
async def process(callback:CallbackQuery):
    markup=get_keyb()
    try:
        await bot.edit_message_media(chat_id=callback.message.chat.id,
                           message_id=callback.message.message_id,media=InputMediaPhoto(
                           media=user_dict['photo_1'],
                           caption='It\'s me'
                           ),reply_markup=markup)
    except TelegramBadRequest:
        await bot.edit_message_media(chat_id=callback.message.chat.id,
                           message_id=callback.message.message_id,media=InputMediaPhoto(
                           media=user_dict['photo_2'],
                           caption='It\'s me also'
                           ),reply_markup=markup)
if __name__== "__main__":
    dp.run_polling(bot)