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

with open('animes.json', 'r', encoding='utf-8') as file:
    animes_data = json.load(file)

def get_random_animes(genre):
    animes_list = animes_data['docs']
    filtered_animes = [
        animes for animes in animes_list
        if any(g['name'].lower() == genre.lower() for g in animes['genres'])
    ]
    if filtered_animes:
        return random.choice(filtered_animes)
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
    await message.reply('Привет, я бот для поиска фильма, сериала или аниме на вечер, помогу вам найти что нибудь интересное, основываясь на ваших пожеланиях. Нажмите кнопку ниже, чтобы начать.', reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "menu")
async def show_genre_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_poisk = InlineKeyboardButton("Поиск", callback_data="poisk")
    button_historyk = InlineKeyboardButton("Избранное", callback_data="historyk")
    keyboard.add(button_poisk, button_historyk)
    
    await bot.send_message(callback_query.from_user.id, 'Я имею несколько функций, которые представленны ниже', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == "poisk")
async def show_genre_selection(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button_serials = InlineKeyboardButton("Cериалы", callback_data="serials")
    button_films = InlineKeyboardButton("Фильмы", callback_data="films")
    button_anime = InlineKeyboardButton("Рандомное аниме", callback_data="anime")
    button_menu = InlineKeyboardButton("Вернутся в меню", callback_data="menu")
    keyboard.add(button_serials, button_films, button_anime, button_menu)
    
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
    button_back = InlineKeyboardButton("Вернуться назад", callback_data="poisk")
    keyboard.add(button_detektiv, button_voennyy, button_istorya, button_komediya, button_triller, button_uzhasy, button_fantastika, button_fentezi, button_drama, button_back)
    
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
    button_back = InlineKeyboardButton("Вернуться назад", callback_data="poisk")
    keyboard.add(button_detektiv, button_voennyy, button_istorya, button_komediya, button_triller, button_uzhasy, button_fantastika, button_fentezi, button_drama, button_back)
    
    await bot.send_message(callback_query.from_user.id, 'Какой жанр Вас интересует?', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data in [
    "komediya", "drama", "melodram", "detectiv", "war", "history", "fantasy",
    "detektiv", "voennyy", "istoriya", "triller", "uzhasy", "fantastika", "fentezi", "anime"
])
@dp.callback_query_handler(lambda callback_query: callback_query.data in [
    "komediya", "drama", "melodram", "detectiv", "war", "history", "fantasy",
    "detektiv", "voennyy", "istoriya", "triller", "uzhasy", "fantastika", "fentezi", "anime"
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
            button_back = InlineKeyboardButton("Вернуться назад", callback_data="serials")
            keyboard.add(button_search_again, button_add_to_favorites, button_back)
            
            countries = ", ".join([country['name'] for country in series.get('countries', [])])
            poster_url = series.get('poster', {}).get('url', '')
            
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть сериал: \n'{series['name']}'.\n"
                                   f"Год выпуска: {series['year']}\n"
                                   f"Страна: {countries}\n"
                                   f"Описание: {series['description']}\n"
                                   f"Постер: [ссылка]({poster_url})",
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти сериал.')
    elif callback_query.message.text == 'Какой жанр Вас интересует?':
        movie = get_random_movie(genre)
        if movie:
            user_history[callback_query.from_user.id] = movie
            keyboard = InlineKeyboardMarkup()
            button_search_again = InlineKeyboardButton("Искать дальше", callback_data=f"search_again_{genre}")
            button_add_to_favorites = InlineKeyboardButton(
                "Сохранить", 
                callback_data=f"add_to_favorites_{movie['id']}" 
            )
            button_back = InlineKeyboardButton("Вернуться назад", callback_data="films")
            keyboard.add(button_search_again, button_add_to_favorites, button_back)
            
            countries = ", ".join([country['name'] for country in movie.get('countries', [])])
            poster_url = movie.get('poster', {}).get('url', '')
            
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть фильм: \n'{movie['name']}'.\n"
                                   f"Год выпуска: {movie['year']}\n"
                                   f"Страна: {countries}\n"
                                   f"Описание: {movie['description']}\n"
                                   f"Постер: [ссылка]({poster_url})",  
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти фильм.')
    else:
        animes = get_random_animes(genre)
        if animes:
            user_history[callback_query.from_user.id] = animes
            keyboard = InlineKeyboardMarkup()
            button_search_again = InlineKeyboardButton("Искать дальше", callback_data=f"search_again_{genre}")
            button_add_to_favorites = InlineKeyboardButton(
                "Сохранить",
                callback_data=f"add_to_favorites_{animes['id']}"
            )
            button_menu = InlineKeyboardButton("Вернуться в меню", callback_data="menu")
            keyboard.add(button_search_again, button_add_to_favorites, button_menu)
            
            countries = ", ".join([country['name'] for country in animes.get('countries', [])])
            trailers = animes.get('videos', {}).get('trailers', [])
            trailer_url = trailers[0]['url'] if trailers else ''
            poster_url = animes.get('poster', {}).get('url', '')
            
            await bot.send_message(callback_query.from_user.id,
                                   f"Рекомендую Вам посмотреть аниме: \n'{animes['name']}'.\n"
                                   f"Год выпуска: {animes['year']}\n"
                                   f"Страна: {countries}\n"
                                   f"Описание: {animes['description']}\n"
                                   f"Постер: [ссылка]({poster_url})", 
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти аниме.')
           
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
            button_back = InlineKeyboardButton("Вернуться назад", callback_data="serials")
            keyboard.add(button_search_again, button_add_to_favorites, button_back)
            
            countries = ", ".join([country['name'] for country in series.get('countries', [])])
            poster_url = series.get('poster', {}).get('url', '')
            
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть сериал: \n'{series['name']}'.\n"
                                   f"Год выпуска: {series['year']}\n"
                                   f"Страна: {countries}\n"
                                   f"Описание: {series['description']}\n"
                                   f"Постер: [ссылка]({poster_url})",  
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти сериал.')
    elif callback_query.message.text.startswith("Рекомендую Вам посмотреть фильм"):
        movie = get_random_movie(genre)
        if movie:
            user_history[callback_query.from_user.id] = movie
            keyboard = InlineKeyboardMarkup()
            button_search_again = InlineKeyboardButton("Искать дальше", callback_data=f"search_again_{genre}")
            button_add_to_favorites = InlineKeyboardButton(
                "Сохранить", 
                callback_data=f"add_to_favorites_{movie['id']}" 
            )
            button_back = InlineKeyboardButton("Вернуться назад", callback_data="films")
            keyboard.add(button_search_again, button_add_to_favorites, button_back)
            
            countries = ", ".join([country['name'] for country in movie.get('countries', [])])
            poster_url = movie.get('poster', {}).get('url', '')
            
            await bot.send_message(callback_query.from_user.id, 
                                   f"Рекомендую Вам посмотреть фильм: \n'{movie['name']}'.\n"
                                   f"Год выпуска: {movie['year']}\n"
                                   f"Страна: {countries}\n"
                                   f"Описание: {movie['description']}\n"
                                   f"Постер: [ссылка]({poster_url})", 
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти фильм.')
    else:
        animes = get_random_animes(genre)
        if animes:
            user_history[callback_query.from_user.id] = animes
            keyboard = InlineKeyboardMarkup()
            button_search_again = InlineKeyboardButton("Искать дальше", callback_data=f"search_again_{genre}")
            button_add_to_favorites = InlineKeyboardButton(
                "Сохранить",
                callback_data=f"add_to_favorites_{animes['id']}"
            )
            button_menu = InlineKeyboardButton("Вернуться в меню", callback_data="menu")
            keyboard.add(button_search_again, button_add_to_favorites, button_menu)
            
            countries = ", ".join([country['name'] for country in animes.get('countries', [])])
            trailers = animes.get('videos', {}).get('trailers', [])
            trailer_url = trailers[0]['url'] if trailers else ''
            poster_url = animes.get('poster', {}).get('url', '')
            
            await bot.send_message(callback_query.from_user.id,
                                   f"Рекомендую Вам посмотреть аниме: \n'{animes['name']}'.\n"
                                   f"Год выпуска: {animes['year']}\n"
                                   f"Страна: {countries}\n"
                                   f"Описание: {animes['description']}\n"
                                   f"Постер: [ссылка]({poster_url})",
                                   reply_markup=keyboard, parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.from_user.id, 'Извините, не удалось найти аниме.')
    
    await callback_query.answer()      

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("add_to_favorites_"))
async def add_to_favorites(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    item_id = int(callback_query.data.split("_")[-1])

    item = None
    if callback_query.message.text.startswith("Рекомендую Вам посмотреть сериал"):
        item = next((s for s in series_data['docs'] if s['id'] == item_id), None)
    elif callback_query.message.text.startswith("Рекомендую Вам посмотреть фильм"):
        item = next((m for m in movies_data['docs'] if m['id'] == item_id), None)
    elif callback_query.message.text.startswith("Рекомендую Вам посмотреть аниме"):
        item = next((a for a in animes_data['docs'] if a['id'] == item_id), None)

    if item:
        if user_id not in user_favorites:
            user_favorites[user_id] = []
        user_favorites[user_id].append(item)
        save_favorites_to_file(user_id, user_favorites[user_id])
        await bot.answer_callback_query(callback_query.id, "Фильм/сериал/аниме добавлен в избранное!")
    else:
        await bot.answer_callback_query(callback_query.id, "Ошибка: не удалось добавить в избранное.")

@dp.callback_query_handler(lambda callback_query: callback_query.data == "historyk")
async def show_favorites(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    favorites = load_favorites_from_file(user_id)
    
    if favorites:
        message_text = "Ваше избранное:\n\n"
        for idx, item in enumerate(favorites, start=1):
            message_text += f"{idx}. {item['name']} ({item['year']})\n"
            message_text += f"Описание: {item['description']}\n"
            if 'countries' in item:
                countries = ", ".join([country['name'] for country in item['countries']])
                message_text += f"Страны: {countries}\n"
                if 'poster' in item and 'url' in item['poster']:
                     message_text += f"Постер: [ссылка]({item['poster']['url']})\n"
                         
        await bot.send_message(user_id, message_text, parse_mode='Markdown')
    else:
        await bot.send_message(user_id, "Ваше избранное пусто.")
    
    await callback_query.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
