FROM python:3.11-slim-bullseye


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


COPY ./src ./src

ENTRYPOINT env && python src/manage.py runserver 0.0.0.0:80