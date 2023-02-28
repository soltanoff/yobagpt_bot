import logging
import os
import time
from datetime import timedelta

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from ai import AIWrapper

load_dotenv()

ai = AIWrapper(token=os.getenv('OPEANAI_API_KEY'))
bot = Bot(token=os.getenv('TELEGRAM_API_KEY'))
dp = Dispatcher(bot)
SLEEP_AFTER_EXCEPTION = timedelta(minutes=1).seconds


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username
    request_message: str = message.text

    await message.answer_chat_action('typing')
    logging.info('>>> User[%s|%s:@%s]: %r', chat_id, user_id, username, request_message)
    await message.reply('Штош, ну привет!')


async def get_ai_answer(message: types.Message, request_message: str | None = None) -> str:
    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username
    request_message: str = request_message or message.text.strip()

    await message.answer_chat_action('typing')
    logging.info('>>> User[%s|%s:@%s]: %r', chat_id, user_id, username, request_message)
    answer = await ai.get_answer(request_message)
    logging.info('<<< User[%s|%s:@%s]: %r', chat_id, user_id, username, answer)
    return answer


@dp.message_handler(commands=['cat'])
async def send_ai_answer_from_group(message: types.Message):
    request_message: str = message.text[4:].strip()
    if len(request_message) < 3:
        await message.reply('Краткость - сестра таланта, да?')
        return

    answer = await get_ai_answer(message, request_message)
    await message.reply(answer)


@dp.message_handler(lambda message: message.chat.id > 0)
async def send_ai_answer_from_dm(message: types.Message):
    answer = await get_ai_answer(message)
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
            logging.error('Error found: %r. Restarting...', ex)
            time.sleep(SLEEP_AFTER_EXCEPTION)
