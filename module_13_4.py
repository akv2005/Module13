from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = 'XXX'
bot = Bot(token= api)
dp = Dispatcher(bot, storage = MemoryStorage())

class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = 'start')
async def start(message):
    print('Мы получили /start.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.Отправьте слово "Калории"')

@dp.message_handler(text='Калории')
async def set_gender(message):
    print(f'Сообщение от {message["from"]["first_name"]}')
    await message.answer('Введите свой пол (М/Ж):')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    await state.update_data(gender=message.text)
    await message.answer('Введите свой возраст:')
    await UserState.age.set()
@dp.message_handler(state=UserState.age)
async  def set_growth(message, state):
    await  state.update_data(age= message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await state.finish()
    print(data)

    try:
        if data['gender'].upper() == 'Ж':
            calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
        elif data['gender'].upper() == 'М':
            calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
        else:
            raise ValueError
    except ValueError:
        txt = 'Вы ввели ошибочные данные'
    else:
        txt = f'Ваша норма калорий по формуле Миффлина-Сан Жеора: {calories}'



    await message.answer(f'Ваша норма калорий по формуле Миффлина-Сан Жеора: {txt}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
