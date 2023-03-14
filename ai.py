import asyncio
import logging
from functools import partial
from time import time
from typing import Optional

import openai
from revChatGPT import V1

from utils import api_exception_safe, api_background_call


class AIWrapper:
    model: str = 'text-davinci-003'
    temperature: float = 0.0
    max_tokens: int = 3000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    image_size: str = '512x512'  # '1024x1024'

    def __init__(
        self,
        openai_token: str,
        chat_access_token: str,
        chatgpt_proxy_url: Optional[str],
        use_v2: str,
    ):
        openai.api_key = openai_token
        chatgpt_proxy_url and setattr(V1, 'BASE_URL', chatgpt_proxy_url)
        self._chatbot = V1.AsyncChatbot(config={'access_token': chat_access_token})
        self._lock = asyncio.Lock()
        self._use_v2 = use_v2 == '1'

    async def _get_answer_v1(
        self,
        message: str,
        typing_event: partial,
    ) -> str:
        answer = ''
        start_time = time()
        while self._lock.locked():
            if time() - start_time > 3:
                start_time = time()
                await typing_event()
            await asyncio.sleep(1)

        if time() - start_time > 3:
            await typing_event()

        try:
            await self._lock.acquire()
            start_time = time()
            async for data in self._chatbot.ask(message):
                if time() - start_time > 3:
                    start_time = time()
                    await typing_event()

                answer = data['message']
        except Exception as ex:
            if 'Something went wrong, please try reloading the conversation' in str(ex):
                self._chatbot.reset_chat()
                self._lock.locked() and self._lock.release()
                return await self.get_answer(message, typing_event=typing_event)

            logging.error('V1 API error: %r. Try to use V2 for emergency case...', ex)
            answer = await self._get_answer_v2(message, typing_event, start_time)
        finally:
            self._lock.locked() and self._lock.release()

        if not answer:
            answer = 'Мне нечего ответить :('

        return answer

    @classmethod
    async def _get_answer_v2(
        cls,
        message: str,
        typing_event: partial,
        start_time: Optional[float] = None,
    ) -> str:
        response = await api_background_call(
            openai.Completion.acreate(
                model=cls.model,
                prompt=message,
                temperature=cls.temperature,
                max_tokens=cls.max_tokens,
                top_p=cls.top_p,
                frequency_penalty=cls.frequency_penalty,
                presence_penalty=cls.presence_penalty,
            ),
            typing_event=typing_event,
            start_time=start_time,
        )
        answer = response['choices'][0]['text'].strip()
        if not answer:
            answer = 'Мне нечего ответить :('

        return answer

    @api_exception_safe
    async def get_answer(self, message: str, typing_event: partial) -> str:
        if not message.endswith('.'):
            message += '.'

        if self._use_v2:
            return await self._get_answer_v2(message, typing_event)
        return await self._get_answer_v1(message, typing_event)

    @api_exception_safe
    async def get_image(self, message: str, typing_event: partial) -> str:
        response = await api_background_call(
            openai.Image.acreate(
                prompt=message,
                n=1,
                size=self.image_size,
            ),
            typing_event=typing_event,
        )
        return f'Готово<a href="{response["data"][0]["url"]}">.</a>'
