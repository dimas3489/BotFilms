import logging
import random
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

with open('movies.json', 'r', encoding='utf-8') as file:
    movies_data = json.load(file)

def get_random_movie(genre):
    movies_list = movies_data['docs']
    filtered_movies = [
        movie for movie in movies_list
        if any(g['name'].lower() == genre.lower() for g in movie['genres'])
    ]
    if filtered_movies:
        return random.choice(filtered_movies)
    return None

with open('series.json', 'r', encoding='utf-8') as file:
    series_data = json.load(file)

def get_random_series(genre):
    series_list = series_data['docs']
    filtered_series = [
        series for series in series_list
        if any(g['name'].lower() == genre.lower() for g in series['genres'])
    ]
    if filtered_series:
        return random.choice(filtered_series)
    return None

def save_favorites_to_file(user_id, favorites):
    with open(f'favorites_{user_id}.json', 'w', encoding='utf-8') as file:
        json.dump(favorites, file, ensure_ascii=False, indent=4)

def load_favorites_from_file(user_id):
    try:
        with open(f'favorites_{user_id}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

user_history = {}
user_favorites = {}

bot = Bot(token="")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button_menu = InlineKeyboardButton("Меню", callback_data="menu")
    keyboard.add(button_menu)
    await message.reply('Привет! Я ваш бот для поиска фильмов и сериалов. Нажмите кнопку ниже, чтобы начать.', reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "menu")
async def show_genre_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_poisk = InlineKeyboardButton("Поиск", callback_data="poisk")
    button_historyk = InlineKeyboardButton("История и избранное", callback_data="historyk")
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
    button_detektiv = InlineKeyboardButton("Детектив", callback_data="detektiv")
    button_voennyy = InlineKeyboardButton("Военный", callback_data="voennyy")
    button_istorya = InlineKeyboardButton("История", callback_data="istoriya")
    button_komediya = InlineKeyboardButton("Комедия", callback_data="komediya")
    button_triller = InlineKeyboardButton("Триллер", callback_data="triller")
    button_uzhasy = InlineKeyboardButton("Ужасы", callback_data="uzhasy")
    button_fantastika = InlineKeyboardButton("Фантастика", callback_data="fantastika")
    button_fentezi = InlineKeyboardButton("Фэнтези", callback_data="fentezi")
    button_drama = InlineKeyboardButton("Драма", callback_data="drama")
    button_menu = InlineKeyboardButton("Вернутся в меню", callback_data="menu")
    keyboard.add(button_detektiv, button_voennyy, button_istorya, button_komediya, button_triller, button_uzhasy, button_fantastika, button_fentezi, button_drama, button_menu)
    
    await bot.send_message(callback_query.from_user.id, 'Какой жанр сериала вас интересует?', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "films")
async def show_genre_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_detektiv = InlineKeyboardButton("Детектив", callback_data="detektiv")
    button_voennyy = InlineKeyboardButton("Военный", callback_data="voennyy")
    button_istorya = InlineKeyboardButton("История", callback_data="istoriya")
    button_komediya = InlineKeyboardButton("Комедия", callback_data="komediya")
    button_triller = InlineKeyboardButton("Триллер", callback_data="triller")
    button_uzhasy = InlineKeyboardButton("Ужасы", callback_data="uzhasy")
    button_fantastika = InlineKeyboardButton("Фантастика", callback_data="fantastika")
    button_fentezi = InlineKeyboardButton("Фэнтези", callback_data="fentezi")
    button_drama = InlineKeyboardButton("Драма", callback_data="drama")
    button_menu = InlineKeyboardButton("Вернутся в меню", callback_data="menu")
    keyboard.add(button_detektiv, button_voennyy, button_istorya, button_komediya, button_triller, button_uzhasy, button_fantastika, button_fentezi, button_drama, button_menu)
    
    await bot.send_message(callback_query.from_user.id, 'Какой жанр Вас интересует?', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data in [
    "komediya", "drama", "melodram", "detectiv", "war", "history", "fantasy",
    "detektiv", "voennyy", "istoriya", "triller", "uzhasy", "fantastika", "fentezi"
])
async def handle_genre_selection(callback_query: types.CallbackQuery):
    genre = callback_query.data
    
    if callback_query.message.text == 'Какой жанр сериала вас интересует?':
        series = get_random_series(genre)
        if series:
            user_history[callback_query.from_user.id] = series
            keyboard = InlineKeyboardMarkup()
            button_search_again = InlineKeyboardButton("Искать дальше", callback_data=f"search_again_{genre}")
            button_add_to_favorites = InlineKeyboardButton(
                "Сохранить", 
                callback_data=f"add_to_favorites_{series['id']}"  
            )
            button_back_to_menu = InlineKeyboardButton("Вернуться в меню", callback_data="menu")
            keyboard.add(button_search_again, button_add_to_favorites, button_back_to_menu)
            
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть сериал '{series['name']}' ({series['year']}). Описание: {series['description']}",
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти сериал.')
    else:
        movie = get_random_movie(genre)
        if movie:
            user_history[callback_query.from_user.id] = movie
            keyboard = InlineKeyboardMarkup()
            button_search_again = InlineKeyboardButton("Искать дальше", callback_data=f"search_again_{genre}")
            button_add_to_favorites = InlineKeyboardButton(
                "Сохранить", 
                callback_data=f"add_to_favorites_{movie['id']}" 
            )
            button_back_to_menu = InlineKeyboardButton("Вернуться в меню", callback_data="menu")
            keyboard.add(button_search_again, button_add_to_favorites, button_back_to_menu)
            
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть фильм '{movie['name']}' ({movie['year']}). Описание: {movie['description']}", 
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти фильм.')
    
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("search_again_"))
async def search_again(callback_query: types.CallbackQuery):
    genre = callback_query.data.split("_")[2]
    
    if callback_query.message.text.startswith("Рекомендую Вам посмотреть сериал"):
        series = get_random_series(genre)
        if series:
            user_history[callback_query.from_user.id] = series
            keyboard = InlineKeyboardMarkup()
            button_search_again = InlineKeyboardButton("Искать дальше", callback_data=f"search_again_{genre}")
            button_add_to_favorites = InlineKeyboardButton(
                "Сохранить", 
                callback_data=f"add_to_favorites_{series['id']}"
            )
            button_back_to_menu = InlineKeyboardButton("Вернуться в меню", callback_data="menu")
            keyboard.add(button_search_again, button_add_to_favorites, button_back_to_menu)
            
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть сериал '{series['name']}' ({series['year']}). Описание: {series['description']}", 
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти сериал.')
    else:
        movie = get_random_movie(genre)
        if movie:
            user_history[callback_query.from_user.id] = movie
            keyboard = InlineKeyboardMarkup()
            button_search_again = InlineKeyboardButton("Искать дальше", callback_data=f"search_again_{genre}")
            button_add_to_favorites = InlineKeyboardButton(
                "Сохранить", 
                callback_data=f"add_to_favorites_{movie['id']}" 
            )
            button_back_to_menu = InlineKeyboardButton("Вернуться в меню", callback_data="menu")
            keyboard.add(button_search_again, button_add_to_favorites, button_back_to_menu)
            
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть фильм '{movie['name']}' ({movie['year']}). Описание: {movie['description']}", 
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти фильм.')
    
    await callback_query.answer()      

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("add_to_favorites_"))
async def add_to_favorites(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    item_id = int(callback_query.data.split("_")[-1])

    item = None
    if callback_query.message.text.startswith("Рекомендую Вам посмотреть сериал"):
        item = next((s for s in series_data['docs'] if s['id'] == item_id), None)
    else:
        item = next((m for m in movies_data['docs'] if m['id'] == item_id), None)

    if item:
        if user_id not in user_favorites:
            user_favorites[user_id] = []
        user_favorites[user_id].append(item)
        save_favorites_to_file(user_id, user_favorites[user_id])
        await bot.answer_callback_query(callback_query.id, "Фильм/сериал добавлен в избранное!")
    else:
        await bot.answer_callback_query(callback_query.id, "Ошибка: не удалось добавить в избранное.")

@dp.callback_query_handler(lambda callback_query: callback_query.data == "historyk")
async def show_favorites(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    favorites = load_favorites_from_file(user_id)
    
    if favorites:
        message_text = "Ваше избранное:\n\n"
        for idx, item in enumerate(favorites, start=1):
            message_text += f"{idx}. {item['name']} ({item['year']})\nОписание: {item['description']}\n\n"
        
        await bot.send_message(user_id, message_text, parse_mode='Markdown')
    else:
        await bot.send_message(user_id, "Ваше избранное пусто.")
    
    await callback_query.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
