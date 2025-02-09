import logging
import random
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

try:
 with open('movies.json', 'r', encoding='utf-8') as f:
        movies_data = json.load(f)
except Exception as e:
    logger.error(f"Ошибка при загрузке movies.json: {e}")
    movies_data = []

try:
 with open('series.json', 'r', encoding='utf-8') as f:
        series_data = json.load(f)
except Exception as e:
    logger.error(f"Ошибка при загрузке series.json: {e}")
    series_data = []

user_history = {}

bot = Bot(token="")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def get_random_movie(genres):
    filtered_movies = [movie for movie in movies_data if movie['genres'] == genres]
    if filtered_movies:
        return random.choice(filtered_movies)
    return None

def get_random_series(genres):
    filtered_series = [series for series in series_data if series['genres'] == genres]
    if filtered_series:
        return random.choice(filtered_series)
    return None

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button_menu = InlineKeyboardButton("Меню", callback_data="menu")
    keyboard.add(button_menu)
    await message.reply('Привет! Я ваш бот для поиска фильмов и сериалов. Нажмите кнопку ниже, чтобы начать.', reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "menu")
async def show_genres_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_poisk = InlineKeyboardButton("Поиск фильма или сериала на вечер", callback_data="poisk")
    button_historyk = InlineKeyboardButton("История просмотра и избранное", callback_data="historyk")
    keyboard.add(button_poisk, button_historyk)
    
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Я имею несколько функций, которые представленны ниже', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "poisk")
async def show_genres_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_serials = InlineKeyboardButton("Cериалы", callback_data="serials")
    button_films = InlineKeyboardButton("Фильмы", callback_data="films")
    keyboard.add(button_serials, button_films)
    
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Что будем искать?', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "serials")
async def show_genres_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_melodram = InlineKeyboardButton("Мелодрама", callback_data="melodram")
    button_comedy = InlineKeyboardButton("Комедия", callback_data="comedy")
    button_detectiv = InlineKeyboardButton("Детективные", callback_data="detectiv")
    button_war = InlineKeyboardButton("Военные", callback_data="war")
    button_history = InlineKeyboardButton("Исторические", callback_data="history")
    button_fantasy = InlineKeyboardButton("Фантастика", callback_data="fantasy")
    button_menu = InlineKeyboardButton("Вернутся в меню", callback_data="menu")
    keyboard.add(button_comedy, button_melodram, button_detectiv, button_war, button_history, button_fantasy, button_menu)
    
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Какой жанр сериала вас интересует?', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "films")
async def show_genres_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_detektiv = InlineKeyboardButton("Детектив", callback_data="detektiv")
    button_voennyy = InlineKeyboardButton("Военный", callback_data="voennyy")
    button_istorya = InlineKeyboardButton("История", callback_data="istorya")
    button_comedy = InlineKeyboardButton("Комедия", callback_data="comedy")
    button_triller = InlineKeyboardButton("Триллер", callback_data="triller")
    button_uzhasy = InlineKeyboardButton("Ужасы", callback_data="uzhasy")
    button_fantastika = InlineKeyboardButton("Фантастика", callback_data="fantastika")
    button_fentezi = InlineKeyboardButton("Фэнтези", callback_data="fentezi")
    button_drama = InlineKeyboardButton("Драма", callback_data="drama")
    button_menu = InlineKeyboardButton("Вернутся в меню", callback_data="menu")
    keyboard.add(button_detektiv, button_voennyy, button_istorya, button_comedy, button_triller, button_uzhasy, button_fantastika, button_fentezi, button_drama, button_menu)
    
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Какой жанр Вас интересует?', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data in [
    "comedy", "drama", "melodram", "detectiv", "war", "history", "fantasy",  # Сериалы
    "detektiv", "voennyy", "istorya", "triller", "uzhasy", "fantastika", "fentezi"  # Фильмы
])
async def handle_genres_selection(callback_query: types.CallbackQuery):
    genres = callback_query.data
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    
    if callback_query.message.text == 'Какой жанр сериала вас интересует?':
        series = get_random_series(genres)
        if series:
            user_history[callback_query.from_user.id] = series
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть сериал '{series['name']}' ({series['year']}). Описание: {series['description']}. [Ссылка на Кинопоиск](https://www.kinopoisk.ru/series/{series['id']})", 
                                   parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти сериал.')
    else:
        movie = get_random_movie(genres)
        if movie:
            user_history[callback_query.from_user.id] = movie
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть фильм '{movie['name']}' ({movie['year']}). Описание: {movie['description']}", 
                                   parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти фильм.')
    
    await callback_query.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
