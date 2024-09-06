FROM python:3.9 -slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /social_network/app

COPY requirements.txt /social_network/app

RUN apt-get update \
    && apt-get install -y gcc python3-dev default-libmysqlclient-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY . /social_network/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
