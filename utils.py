import asyncio
import logging
from datetime import timedelta
from functools import wraps, partial
from time import time
from typing import Callable, Coroutine, Optional, Any

from aiogram import Dispatcher, types

SLEEP_AFTER_EXCEPTION = timedelta(minutes=1).seconds
MESSAGE_SIZE_LIMIT = 10


def special_command_handler(dispatcher: Dispatcher, command: str) -> Callable:
    def decorator(callback: Callable) -> Callable:
        @wraps(callback)
        async def wrapper(message: types.Message) -> None:
            request_message: str = message.text[len(command) + 1:].strip()
            if len(request_message) < MESSAGE_SIZE_LIMIT:
                await message.reply('Краткость - сестра таланта, да?')
                return

            await callback(message, request_message)

        dispatcher.message_handler(commands=[command])(wrapper)
        return callback

    return decorator


def api_exception_safe(func) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> str:
        try:
            return await func(*args, **kwargs)
        except Exception as ex:
            logging.exception('Unexpected error: %r', ex, exc_info=ex)
            return 'Мне нечего ответить :('

    return wrapper


async def api_background_call(
    coro: Coroutine,
    typing_event: partial,
    start_time: Optional[float] = None,
) -> Any:
    response_future = asyncio.create_task(coro)
    start_time = start_time or time()
    while not response_future.done():
        if time() - start_time > 3:
            start_time = time()
            await typing_event()
        await asyncio.sleep(1)

    return response_future.result()
