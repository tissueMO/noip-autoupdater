FROM python:3.7

# WSGI Webアプリケーションをホストから丸ごとコピー
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# 依存パッケージをインストール
RUN pip install -r requirements.txt

# Chromedriver のパスを通す
ENV PATH $PATH:/app/chromedriver-81.0.4044.20

# Gunicorn 起動
CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 app:app
