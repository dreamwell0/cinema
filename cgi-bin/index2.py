import requests
import bs4
import cgi # CGIモジュールのインポート
import cgitb
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time

form = cgi.FieldStorage() 

print("Content-Type: text/html; charset=Shift_JIS") # HTMLを記述するためのヘッダ
print("")

if "text" not in form:
    print("<h1>Error!</h1>")
    print("<br>")
    print("テキストを入力してください！")
    print("<a href='/'><button type='submit'>戻る</button></a>")
    sys.exit()

text = form.getvalue("text") # データの値を取得する

# 取得結果
current_value = ''

options = Options()
# ヘッドレスモードで実行する場合
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

try:
	# 取得先URLにアクセス
	driver.get(text)
	
	# コンテンツが描画されるまで待機
	time.sleep(10)
	
    bc_value = browser.find_element_by_id("schedule-body-title").text
    print(bc_value)
	
finally:
# プラウザを閉じる
driver.quit()