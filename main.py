import logging
import random
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

IMDB_API_KEY = 'ваш_ключ_здесь'
IMDB_BASE_URL = 'https://imdb-api.com/en/API'

user_history = {}

bot = Bot(token="")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def get_random_movie(genre):
    url = f"{IMDB_BASE_URL}/AdvancedSearch/{IMDB_API_KEY}?genres={genre}&sort=year,desc"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        return random.choice(data['results'])
    return None

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button_menu = InlineKeyboardButton("Меню", callback_data="menu")
    keyboard.add(button_menu)
    await message.reply('Привет! Я ваш бот для поиска фильмов и сериалов. Нажмите кнопку ниже, чтобы начать.', reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "menu")
async def show_genre_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_poisk = InlineKeyboardButton("Поиск фильма или сериала на вечер", callback_data="poisk")
    button_historyk = InlineKeyboardButton("История просмотра и избранное", callback_data="historyk")
    keyboard.add(button_poisk, button_historyk)
    
    await bot.send_message(callback_query.from_user.id, 'Я имею несколько функций, которые представленны ниже', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "poisk")
async def show_genre_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_serials = InlineKeyboardButton("Cериалы", callback_data="serials")
    button_films = InlineKeyboardButton("Фильмы", callback_data="films")
    keyboard.add(button_serials, button_films)
    
    await bot.send_message(callback_query.from_user.id, 'Что будем искать?', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "serials")
async def show_genre_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_melodram = InlineKeyboardButton("Мелодрама", callback_data="melodram")
    button_comedy = InlineKeyboardButton("Комедия", callback_data="comedy")
    button_detectiv = InlineKeyboardButton("Детективные", callback_data="detectiv")
    button_war = InlineKeyboardButton("Военные", callback_data="war")
    button_history = InlineKeyboardButton("Исторические", callback_data="history")
    button_fantasy = InlineKeyboardButton("Фантастика", callback_data="fantasy")
    button_menu = InlineKeyboardButton("Вернутся в меню", callback_data="menu")
    keyboard.add(button_comedy, button_melodram, button_detectiv, button_war, button_history, button_fantasy, button_menu)
    
    await bot.send_message(callback_query.from_user.id, 'Какой жанр сериала вас интересует?', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "films")
async def show_genre_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_comedy = InlineKeyboardButton("Комедия", callback_data="comedy")
    button_drama = InlineKeyboardButton("Драма", callback_data="drama")
    button_menu = InlineKeyboardButton("Вернутся в меню", callback_data="menu")
    keyboard.add(button_comedy, button_drama, button_menu)
    
    await bot.send_message(callback_query.from_user.id, 'Какой жанр Вас интересует?', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data in ["comedy", "drama"])
async def handle_genre_selection(callback_query: types.CallbackQuery):
    genre = callback_query.data
    movie = get_random_movie(genre)
    
    if movie:
        user_history[callback_query.from_user.id] = movie
        await bot.send_message(callback_query.from_user.id, 
                               f"Рекомендую Вам посмотреть '{movie['title']}' ({movie['year']}). Описание: {movie['description']}. [Ссылка на трейлер](https://www.imdb.com/title/{movie['id']})", 
                               parse_mode='Markdown')
    else:
        await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти фильм.')
    
    await callback_query.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)







