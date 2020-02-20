import os
import flask
from flask import Flask, Response, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import chromedriver_binary
from pyquery import PyQuery as pq

# Flask アプリケーション
app = Flask(__name__)


@app.route("/noip-autoupdate", methods=["POST"])
def noip_auto_update() -> Response:
    """No-IP の自動更新を実行します。

    Returns:
        Response -- JSONレスポンス
    """
    driver = create_chrome_driver()
    additional_results = {}

    try:
        request_json = request.get_json()
        if request_json is None or "message" not in request_json:
            return jsonify({
                "result": "NG",
                "message": "Includes 'message' in a request."
            })

        # print(f'message: {request_json["message"]}')

        # 渡されてきたHTMLをDOMとして認識させて解析
        dom = pq(request_json["message"])
        # target_anchors = dom("a:contains('Confirm Hostname')")
        target_anchors = dom("a[href^='https://www.noip.com/confirm-host?']")
        # print(f":target_anchors({target_anchors.size()})={target_anchors.html()}")

        if target_anchors.size() != 1:
            return jsonify({
                "result": "NG",
                "message": "Doesn't include an 'Confirm Hostname' anchor element."
            })

        for target_anchor in target_anchors:
            # SeleniumでアクセスするURLを抽出
            target_url = dom(target_anchor).attr["href"]
            # print(f":target_url={target_url}")
            break

        # Seleniumで [Confirm Hostname] のページにアクセス
        # driver.get(target_url)
        # line = driver.find_element_by_link_text("No thanks, just renew my free hostname").text

        # 追加情報
        additional_results["target_anchors_length"] = target_anchors.size()
        additional_results["target_url"] = target_url

    finally:
        # Chromeドライバークローズ
        driver.quit()

    # 成功: 正常終了のレスポンスを返す
    result = { "result": "OK" }
    result.update(additional_results)
    return jsonify(result)


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
