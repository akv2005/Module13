from aiogram import Bot, executor, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = 'XXX'
bot = Bot(token= api)
dp = Dispatcher(bot, storage = MemoryStorage())

@dp.message_handler(text = 'Hi')
async def Hi_messages(messages):
    print('Мы получили Hi')

@dp.message_handler(commands = 'start')
async def start(messages):
    print('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler()
async def all_messages(messages):
    print('Введите команду /start, чтобы начать общение. ')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)