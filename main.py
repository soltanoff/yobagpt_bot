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
    logging.info('>>> User[%s:@%s]: %r', message.chat.id, message.chat.username, message.text)
    await message.reply('Штош, ну привет!')


@dp.message_handler()
async def send_ai_answer(message: types.Message):
    chat_id: int = message.chat.id
    username: str = message.chat.username
    request_message: str = message.text

    await message.answer_chat_action('typing')
    logging.info('>>> User[%s:@%s]: %r', chat_id, username, request_message)
    answer = await ai.get_answer(message.text)
    logging.info('<<< User[%s:@%s]: %r', chat_id, username, answer)
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
            logging.error(f'Error found: %r. Restarting...', ex)
            time.sleep(SLEEP_AFTER_EXCEPTION)
