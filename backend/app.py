import os
import flask
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import chromedriver_binary

# Flask アプリケーション
app = Flask(__name__)


@app.route("/selenium_demo", methods=["GET"])
def selenium_demo():
    # このリクエストで使用するユーザーエージェントをランダムに決定
    user_agent = UserAgent().random
    print(user_agent)

    # Chromeドライバーの起動設定
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.binary_location = "/app/chromedriver-81.0.4044.20"

    # Chromeドライバー起動
    # print(f"binary_location exists: {os.path.exists('/app/chromedriver-81.0.4044.20')}")
    driver = webdriver.Chrome("/app/chromedriver-81.0.4044.20", options=chrome_options)

    # Wikipediaのランダムな記事を取得
    driver.get("https://en.wikipedia.org/wiki/Special:Random")
    line = driver.find_element_by_class_name("firstHeading").text
    print(line)

    # Chromeドライバークローズ
    driver.quit()
    return jsonify({
      "result": line
    })


@app.route("/noip_auto_update", methods=["GET"])
def noip_auto_update():
    request_json = request.get_json()
    if request_json and "message" in request_json:
        print(request_json["message"])
        return jsonify({ "result": "OK. Accepted." })
    else:
        return jsonify({ "result": "NG. Includes 'message' in a request." })
