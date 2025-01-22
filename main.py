import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.utils import executor
from aiogram.dispatcher import FSMRule, State

API_TOKEN = 'Your API'


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    genre = State()
    year = State()
    rating = State()


movies_db = [
    {"title": "Inception", "genre": "Sci-Fi", "year": 2010, "rating": 8.8},
    {"title": "The Godfather", "genre": "Crime", "year": 1972, "rating": 9.2},
    {"title": "The Dark Knight", "genre": "Action", "year": 2008, "rating": 9.0},
    {"title": "Breaking Bad", "genre": "Drama", "year": 2008, "rating": 9.5},

]

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я помогу тебе выбрать фильм или сериал. Какой жанр тебя интересует?")
    await Form.genre.set()

@dp.message_handler(state=Form.genre)
async def process_genre(message: types.Message, state: FSMContext):
    genre = message.text
    await state.update_data(genre=genre)
    await message.reply("Отлично! Укажи год выпуска (например, 2020) или напиши 'любой'.")
    await Form.year.set()

@dp.message_handler(state=Form.year)
async def process_year(message: types.Message, state: FSMContext):
    year = message.text
    await state.update_data(year=year)
    await message.reply("Какой минимальный рейтинг тебя устраивает? (например, 7.0)")
    await Form.rating.set()

@dp.message_handler(state=Form.rating)
async def process_rating(message: types.Message, state: FSMContext):
    rating = float(message.text)
    user_data = await state.get_data()
    genre = user_data.get('genre')
    year = user_data.get('year')


    filtered_movies = [
        movie for movie in movies_db
        if (genre.lower() in movie['genre'].lower()) and
           (year == 'любой' or movie['year'] == int(year)) and
           (movie['rating'] >= rating)
    ]

    if filtered_movies:
        selected_movie = random.choice(filtered_movies)
        await message.reply(f"Я рекомендую тебе: {selected_movie['title']} ({selected_movie['year']}) - Жанр: {selected_movie['genre']}, Рейтинг: {selected_movie['rating']}")
    else:
        await message.reply("Извини, я не нашел подходящих фильмов или сериалов.")

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

