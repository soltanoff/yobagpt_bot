from typing import List

import openai


class AIWrapper:
    model: str = 'text-davinci-003'
    temperature: float = 0.4
    max_tokens: int = 2048
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: List[str] = ['#', ';']

    def __init__(self, token: str):
        openai.api_key = token

    @classmethod
    async def get_answer(cls, message_history: str) -> str:
        response = await openai.Completion.acreate(
            model=cls.model,
            prompt=message_history,
            temperature=cls.temperature,
            max_tokens=cls.max_tokens,
            top_p=cls.top_p,
            frequency_penalty=cls.frequency_penalty,
            presence_penalty=cls.presence_penalty,
            stop=cls.stop,
        )
        return response['choices'][0]['text']
