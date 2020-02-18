import os
import flask
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# Flask アプリケーション
app = Flask(__name__)


@app.route("/selenium_demo", methods=["GET"])
def selenium_demo():
    # このリクエストで使用するユーザーエージェントをランダムに決定
    user_agent = UserAgent().random
    print(user_agent)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--hide-scrollbars")
    # chrome_options.add_argument("--enable-logging")
    # chrome_options.add_argument("--log-level=0")
    # chrome_options.add_argument("--v=99")
    # chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(f"user-agent={user_agent}")

    # Chromeドライバー起動
    driver = webdriver.Chrome(
        executable_path=os.path.join(os.getcwd(), "./chromedriver"),
        options=chrome_options
    )

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
