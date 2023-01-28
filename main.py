from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher, Bot, executor
import wikipedia
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

bot = Bot('5566865465:AAHqpak45wYiU9bfcAXkptaZL04mc6xIiVQ', parse_mode='HTML')  # TOKEN
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Введите слово которое хотите найти')


@dp.message_handler(content_types='text')
async def search_form_wikipedia(message: Message):
    chat_id = message.chat.id
    res = f'https://ru.m.wikipedia.org/w/index.php?search=' + message.text
    print(res)
    response = requests.get(res).text
    soup = BeautifulSoup(response, 'html.parser')
    try:
        h1 = soup.find('span', class_='mw-page-title-main').get_text(strip=True)
        par = soup.find('section', class_='mf-section-0')
        par1 = str(par.text).split('\n')[0]
        await bot.send_message(chat_id, f'''{h1} \n
{par1} \n
{res}''')
    except Exception as e:
        await bot.send_message(chat_id, f'Не смогли обработать ваш запрос {message.text}')



executor.start_polling(dp, skip_updates=True)
