import logging
import os
import time
from functools import partial
from typing import Optional

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from dotenv import load_dotenv

from ai import AIWrapper
from utils import special_command_handler, SLEEP_AFTER_EXCEPTION

load_dotenv()

ai = AIWrapper(
    openai_token=os.getenv('OPEANAI_API_KEY'),
    chat_access_token=os.getenv('CHAT_ACCESS_TOKEN'),
    chatgpt_proxy_url=os.getenv('CHATGPT_PROXY_URL', default=None),
    use_v2=os.getenv('USE_V2', default='0'),
)
bot = Bot(token=os.getenv('TELEGRAM_API_KEY'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username

    await message.answer_chat_action('typing')
    logging.info('>>> User[%s|%s:@%s]: %r', chat_id, user_id, username, message.text)
    await message.reply('Штош, ну привет!')


@special_command_handler(dp, command='report')
async def send_report(message: types.Message, request_message: str) -> None:
    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username

    await message.answer_chat_action('typing')
    logging.warning('[REPORT] User[%s|%s:@%s]: %r', chat_id, user_id, username, request_message)
    await message.reply('✅ Отчет отправлен, спасибо!')


@special_command_handler(dp, command='img')
async def send_image(message: types.Message, request_message: str) -> None:
    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username

    await message.answer_chat_action('typing')
    logging.info('>>> User[%s|%s:@%s]: %r', chat_id, user_id, username, request_message)
    answer = await ai.get_image(request_message, typing_event=partial(message.answer_chat_action, 'typing'))
    logging.info('<<< User[%s|%s:@%s]: %r', chat_id, user_id, username, answer)
    await message.reply(answer, parse_mode=ParseMode.HTML)


@dp.message_handler(lambda message: message.chat.id > 0)
@special_command_handler(dp, command='cat')
async def send_ai_answer(message: types.Message, request_message: Optional[str] = None) -> None:
    chat_id: int = message.chat.id
    user_id: str = message.from_user.id
    username: str = message.from_user.username
    request_message: str = request_message or message.text.strip()

    await message.answer_chat_action('typing')
    logging.info('>>> User[%s|%s:@%s]: %r', chat_id, user_id, username, request_message)
    answer = await ai.get_answer(request_message, typing_event=partial(message.answer_chat_action, 'typing'))
    logging.info('<<< User[%s|%s:@%s]: %r', chat_id, user_id, username, answer)
    await message.reply(answer, parse_mode=ParseMode.MARKDOWN if '```' in answer else None)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.getLevelName(os.getenv('LOG_LEVEL', default=logging.INFO)),
        format='%(levelname)9s | %(asctime)s | %(name)30s | %(filename)20s | %(lineno)6s | %(message)s',
        force=True,
    )

    while True:
        try:
            executor.start_polling(dp, skip_updates=False)
        except Exception as ex:
            logging.error('Error found: %r. Restarting...', ex)
            time.sleep(SLEEP_AFTER_EXCEPTION)
