FROM python:3.11-alpine
#FROM joyzoursky/python-chromedriver:3.11-alpine

WORKDIR /app

#RUN apk add --no-cache \
#    wget \
#    unzip \
#    chromium \
#    chromium-chromedriver

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "main.py"]


#RUN apk add postgresql-client build-base postgresql-dev
#
#
#RUN mkdir /code
#COPY . /code
#
#RUN adduser --disabled-password src-user
#
#USER src-user

