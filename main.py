import logging
import os
import time
from datetime import timedelta

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from ai import AIWrapper

load_dotenv()

# Initialize bot and dispatcher
ai = AIWrapper(token=os.getenv('OPEANAI_API_KEY'))
bot = Bot(token=os.getenv('TELEGRAM_API_KEY'))
dp = Dispatcher(bot)
SLEEP_AFTER_EXCEPTION = timedelta(minutes=1).seconds


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer_chat_action('typing')
    await message.reply('Штош, ну привет!')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer_chat_action('typing')
    answer = await ai.get_answer(message.text)
    await message.answer_chat_action('typing')
    await message.answer(answer)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.getLevelName(os.getenv('LOG_LEVEL')),
        format='%(levelname)9s | %(asctime)s | %(name)30s | %(filename)20s | %(lineno)6s | %(message)s',
    )

    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as ex:
            logging.error(f'Error found: {repr(ex)}. Restarting')
            time.sleep(SLEEP_AFTER_EXCEPTION)
