FROM python:3.6

ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /usr/src/app

ADD . /usr/src/app

RUN pip install -r requirements.txt
