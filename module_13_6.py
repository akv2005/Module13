from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

api = 'XXX'
bot = Bot(token= api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ]
    ]
)
inline_kb = InlineKeyboardMarkup()
inline_butt1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_butt2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(inline_butt1, inline_butt2)


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = 'start')
async def start(message):
    print('Мы получили /start.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.Нажмите на кнопку "Рассчитать"', reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    print(f'Сообщение от {message.from_user.first_name}')
    await message.answer('Выберите опцию:', reply_markup=inline_kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    txt = ('Упрощенный вариант формулы Миффлина-Сан Жеора:\n\n'
           'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
           'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161\n\n'
           'Формула расчета индекса массы тела (ИМТ):\n\n'
           'ИМТ = вес (кг) / рост (м) ^ 2')
    await call.message.answer(txt)
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_gender(call: types.CallbackQuery):
    await call.message.answer('Введите свой пол (М/Ж):')
    await UserState.gender.set()
    await call.answer()

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

@dp.message_handler(text='Информация')
async def info(message: types.Message):
    await message.answer('Я -помогу Вам скинуть лишний "жирок"!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)