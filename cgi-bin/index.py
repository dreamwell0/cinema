import requests
import bs4
import cgi # CGIモジュールのインポート
import cgitb
import sys

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

res = requests.get(text)
#res = requests.get('https://tjoy.jp/tjoy-prince-shinagawa#schedule-content')
res.raise_for_status()
res.encoding = 'utf-8'
soup = bs4.BeautifulSoup(res.content, "html.parser",from_encoding='utf-8')
elems1 = soup.select('.schedule-body-title')
for elem1 in elems1:
    print(elem1)
elems2 = soup.select('.schedule-item.white')
for elem2 in elems2:
    print(elem2)

sections = soup.find_all(class_="section-container")
sections = soup.find_all('section', class_='section-container bg-white')
for section in sections:
    title = section.select('h5.js-title-film')
    print(title)
    times = section.select('p.schedule-time')
    
    for time in times:
        print(time.text)

#with open('template.html','r',encoding="utf-8") as file:
#    html = file.read()
#file.closed
#page_data = {}
#page_data['title'] = '魔進戦隊キラメイジャーVSリュウソウジャー'

#for key, value in page_data.items():
#    html = html.replace('{% ' + key + ' %}', value)

#print(html)