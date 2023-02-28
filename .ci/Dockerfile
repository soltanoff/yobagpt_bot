FROM python:3.10-slim
ENV PYTHONUNBUFFERED 0

RUN apt-get update \
	&& apt-get install -y openssh-client --no-install-recommends \
	&& pip install --upgrade --no-cache-dir pip

COPY .. /src
WORKDIR /src

COPY ../.env.default ./.env

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]