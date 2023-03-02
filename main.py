import logging
import os
import time
from datetime import timedelta
from functools import partial
from typing import Optional, Tuple

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from dotenv import load_dotenv

from ai import AIWrapper

load_dotenv()

ai = AIWrapper(openai_token=os.getenv('OPEANAI_API_KEY'), chat_access_token=os.getenv('CHAT_ACCESS_TOKEN'))
bot = Bot(token=os.getenv('TELEGRAM_API_KEY'))
dp = Dispatcher(bot)
SLEEP_AFTER_EXCEPTION = timedelta(minutes=1).seconds


async def get_ai_answer(message: types.Message, request_message: Optional[str] = None) -> Tuple[str, Optional[str]]:
    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username
    request_message: str = request_message or message.text.strip()

    await message.answer_chat_action('typing')
    logging.info('>>> User[%s|%s:@%s]: %r', chat_id, user_id, username, request_message)
    answer = await ai.get_answer(request_message, typing_event=partial(message.answer_chat_action, 'typing'))
    logging.info('<<< User[%s|%s:@%s]: %r', chat_id, user_id, username, answer)
    return answer, ParseMode.MARKDOWN if '```' in answer else None


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username
    request_message: str = message.text

    await message.answer_chat_action('typing')
    logging.info('>>> User[%s|%s:@%s]: %r', chat_id, user_id, username, request_message)
    await message.reply('Штош, ну привет!')


@dp.message_handler(commands=['report'])
async def send_report(message: types.Message):
    request_message: str = message.text[7:].strip()
    if len(request_message) < 10:
        await message.reply('Краткость - сестра таланта, да?')
        return

    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username

    await message.answer_chat_action('typing')
    logging.warning('[REPORT] User[%s|%s:@%s]: %r', chat_id, user_id, username, request_message)
    await message.reply('✅ Отчет отправлен, спасибо!', parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['img'])
async def send_image(message: types.Message):
    request_message: str = message.text[4:].strip()
    if len(request_message) < 3:
        await message.reply('Краткость - сестра таланта, да?')
        return

    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username

    await message.answer_chat_action('typing')
    logging.info('>>> User[%s|%s:@%s]: %r', chat_id, user_id, username, request_message)
    answer = await ai.get_image(request_message)
    logging.info('<<< User[%s|%s:@%s]: %r', chat_id, user_id, username, answer)
    await message.reply(answer, parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['cat'])
async def send_ai_answer_from_group(message: types.Message):
    request_message: str = message.text[4:].strip()
    if len(request_message) < 3:
        await message.reply('Краткость - сестра таланта, да?')
        return

    answer, parse_mode = await get_ai_answer(message, request_message)
    await message.reply(answer, parse_mode=parse_mode)


@dp.message_handler(lambda message: message.chat.id > 0)
async def send_ai_answer_from_dm(message: types.Message):
    answer, parse_mode = await get_ai_answer(message)
    await message.reply(answer, parse_mode=parse_mode)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.getLevelName(os.getenv('LOG_LEVEL')),
        format='%(levelname)9s | %(asctime)s | %(name)30s | %(filename)20s | %(lineno)6s | %(message)s',
        force=True,
    )

    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as ex:
            logging.error('Error found: %r. Restarting...', ex)
            time.sleep(SLEEP_AFTER_EXCEPTION)
