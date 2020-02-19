# https://hub.docker.com/_/python
FROM python:3.7

# WSGI Webアプリケーションをホストから丸ごとコピー
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./backend/* ./
RUN chmod +x /app/chromedriver-81.0.4044.20

# 依存パッケージをインストール
RUN apt-get update && apt-get install -y \
    gconf-gsettings-backend \
    libnss3-dev \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# Gunicorn 起動
CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 app:app
