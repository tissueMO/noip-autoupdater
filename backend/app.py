import os
import flask
from flask import Flask, Response, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import chromedriver_binary

# Flask アプリケーション
app = Flask(__name__)


@app.route("/selenium-test", methods=["GET"])
def selenium_test() -> Response:
    """Seleniumの動作テストを行います。

    Returns:
        Response -- JSONレスポンス
    """
    driver = create_chrome_driver()

    # Wikipediaのランダムな記事を取得
    driver.get("https://en.wikipedia.org/wiki/Special:Random")
    line = driver.find_element_by_class_name("firstHeading").text

    # Chromeドライバークローズ
    driver.quit()
    return jsonify({ "result": line })


@app.route("/noip-autoupdate", methods=["POST"])
def noip_auto_update() -> Response:
    """No-IP の自動更新を実行します。

    Returns:
        Response -- JSONレスポンス
    """
    driver = create_chrome_driver()
    request_json = request.get_json()
    if request_json and "message" in request_json:
        print(request_json["message"])
        return jsonify({ "result": "OK. Accepted." })
    else:
        return jsonify({ "result": "NG. Includes 'message' in a request." })


def create_chrome_driver(user_agent: str = None) -> webdriver.Chrome:
    """Chromeドライバーを生成します。
    使用後は必ず quit() を呼び出してクローズして下さい。

    Keyword Arguments:
        user_agent {str} -- 使用するユーザーエージェント (default: {None})

    Returns:
        webdriver.Chrome -- 生成したChromeドライバー
    """
    if user_agent is None:
      # このリクエストで使用するユーザーエージェントをランダムに決定
      user_agent = UserAgent().random
    # print(user_agent)

    # Chromeドライバーの起動設定
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(f"user-agent={user_agent}")

    # Chromeドライバー起動
    driver = webdriver.Chrome(options=chrome_options)
    return driver
