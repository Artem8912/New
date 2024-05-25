from aiogram.types import Message,CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram import Dispatcher,Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter,Command,CommandStart
from aiogram import F
from aiogram.fsm.storage.redis import RedisStorage,Redis
from aiogram.fsm.state import State,StatesGroup,default_state
from aiogram.utils.keyboard import InlineKeyboardBuilder


BOT_TOKEN = '6770547708:AAESTRQgbjl1lPqv4DPZXxeYOUVbb7OPyk4'
redis = Redis(host='localhost')
storage=RedisStorage(redis=redis)
dp =Dispatcher(storage=storage)
bot = Bot(token=BOT_TOKEN)

user_data:dict[int,dict[str,str |int|bool]] = {}

class FSMfillform(StatesGroup):
    fill_name = State()
    fill_gender = State()
    fill_age = State()

@dp.message(Command(commands='cancel'),~StateFilter(default_state))
async def process_cancel(message:Message,state:FSMContext):
    
    await message.answer("""Вы отменили заполнение формы \n
Для заполнение новой - введите команду: /start""")
    await state.clear()
    
@dp.message(Command(commands='cancel'),StateFilter(default_state))
async def process_cancel(message:Message,state:FSMContext):
        await message.answer('Отменять нечего')
        await state.clear()
@dp.message(CommandStart())
async def process_start(message:Message,state:FSMContext):
    await message.answer(text='добро пожаловать, введите ваше имя: ')
    await state.set_state(FSMfillform.fill_name)
@dp.message(StateFilter(FSMfillform.fill_name),F.text.isalpha(),lambda x:len(x.text)<15)
async def start_fill(message:Message,state:FSMContext):
    await state.update_data(name = message.text)
    
    await message.answer('Введите ваш пол:')
    kb_builder = InlineKeyboardBuilder()
    buttons:list[InlineKeyboardButton] = [InlineKeyboardButton(text='Женский',callback_data='women'),
                                          InlineKeyboardButton(text='Мужской',callback_data='man'),
                                          InlineKeyboardButton(text='Трансгендер',callback_data='transgender')]
    kb_builder.add(*buttons)
    kb_builder.adjust(2,1)
    keyboard:InlineKeyboardMarkup = kb_builder.as_markup()
    await message.answer(text='Варианты ',reply_markup=keyboard)
    await state.set_state(FSMfillform.fill_gender)
    
@dp.message(StateFilter(FSMfillform.fill_name))
async def start_fill_name(message:Message):
    await message.answer('Это не похоже на имя')

@dp.callback_query(StateFilter(FSMfillform.fill_gender),F.data.in_(['women','man','transgender']))
async def start_fill_gender(callback:CallbackQuery,state:FSMContext):
    await state.update_data(gender=callback.data)
    # print(state.get_data())
    await state.set_state(FSMfillform.fill_age)
    await callback.message.answer(text='Введите ваш возраст:')

@dp.message(StateFilter(FSMfillform.fill_age),lambda x:4<int(x.text)<125)
async def start_fill_age(message:Message,state:FSMContext):
    await state.update_data(age=message.text)
    user_data[message.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer(text = f"{user_data[message.from_user.id]['name']}\n"
                                f"{user_data[message.from_user.id]['gender']}\n" 
                                f"{user_data[message.from_user.id]['age']}\n")
if __name__== "__main__":
    dp.run_polling(bot)