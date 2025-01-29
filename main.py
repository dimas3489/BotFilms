import logging
import random
import requests
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram import types

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TMDB_API_KEY = 'YOUR API KEY"'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

user_history = {}

bot = Bot(token="YOUR API KEY")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def get_random_movie(genre):
    url = f"{TMDB_BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre}&sort_by=popularity.desc"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        return random.choice(data['results'])
    return None

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привет! Я Ваш кино-бот. Введите "показать фильм", чтобы начать.')

@dp.message_handler(lambda message: "показать фильм" in message.text.lower())
async def show_movie(message: types.Message):
    await message.reply('Какой жанр Вас интересует? (например, комедия, драма)')

@dp.message_handler(lambda message: True)
async def handle_message(message: types.Message):
    user_input = message.text.lower()
    
    if "комедия" in user_input:
        movie = get_random_movie(35)
        if movie:
            user_history[message.from_user.id] = movie
            await message.reply(f"Рекомендую Вам посмотреть '{movie['title']}' ({movie['release_date']}). Описание: {movie['overview']}. [Ссылка на трейлер](https://www.youtube.com/watch?v={movie['id']})", parse_mode='Markdown')
        else:
            await message.reply('Извините, не удалось найти фильм.')
    else:
        await message.reply('Пожалуйста, уточните жанр.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
