# https://hub.docker.com/_/python
FROM python:3.7

# WSGI Webアプリケーションをホストから丸ごとコピー
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./backend/* ./
RUN chmod +x /app/chromedriver-81.0.4044.20

# 依存パッケージをインストール
RUN apt-get update && apt-get install -y \
    gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 \
    libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 \
    libpango-1.0-0 libxss1 fonts-liberation \
    libappindicator1 libappindicator3-1 \
    libnss3 lsb-release xdg-utils \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

# Chromeをインストール
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb \
 && apt-get install -fy \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*
RUN google-chrome --version

RUN pip install -r requirements.txt

# Gunicorn 起動
CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 app:app
