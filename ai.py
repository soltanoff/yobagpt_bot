import openai


class AIWrapper:
    model: str = 'text-davinci-003'
    temperature: float = 0.25
    max_tokens: int = 2048
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    image_size: str = '512x512'  # '1024x1024'

    def __init__(self, token: str):
        openai.api_key = token

    @classmethod
    async def get_answer(cls, message: str) -> str:
        if not message.endswith('.'):
            message += '.'

        response = await openai.Completion.acreate(
            model=cls.model,
            prompt=message,
            temperature=cls.temperature,
            max_tokens=cls.max_tokens,
            top_p=cls.top_p,
            frequency_penalty=cls.frequency_penalty,
            presence_penalty=cls.presence_penalty,
        )
        answer = response['choices'][0]['text'].strip()
        if not answer:
            answer = 'Мне нечего ответить :('

        return answer

    @classmethod
    async def get_image(cls, message: str) -> str:
        response = await openai.Image.acreate(
            prompt=message,
            n=1,
            size=cls.image_size,
        )
        return f'Готово<a href="{response["data"][0]["url"]}">.</a>'
