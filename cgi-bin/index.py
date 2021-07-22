import requests
import bs4
import cgi # CGIモジュールのインポート
import cgitb
import sys
import json
import datetime as dt
import calendar
import os
from googletrans import Translator

today = dt.date.today()
dayName = calendar.day_name[today.weekday()]

if today.month < 10:
    month = f'0{today.month}'
else:
    month = today.month

if today.day < 10:
    day = f'0{today.day}'
else:
    day = today.day

todayString = str(today.year) + '-' + str(month) + '-' + str(day) + 'T'

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

jsonList = []

sections = soup.find_all(class_="section-container")
sections = soup.find_all('section', class_='section-container bg-white')
for section in sections:
    title = section.select_one('h5.js-title-film')
    print(title.text)

    titleEng = ''
    tr = Translator(service_urls=['translate.googleapis.com'])
    while True:
        try:
            titleEng = tr.translate(title.text, dest="en").text
            break
        except Exception as e:
            tr = Translator(service_urls=['translate.googleapis.com'])
    
    times = section.select('p.schedule-time')
    
    for time in times:
        timeString = time.text
        target = '～'
        idx = timeString.find(target)
        end = timeString[idx+1:].replace( '\n' , '' ).replace(' ', '')
        start = timeString[:idx].replace( '\n' , '' ).replace(' ', '')
        
        print(start)
        print('～')
        print(end)
        print(' ')
        item = {
            'service': titleEng,
            'service_title': titleEng,
            'start':  todayString + start + ':00',
            'end': todayString + end + ':00',
            'emp_title': titleEng + ' ' + start + '-' + end
        }
        jsonList.append(item)
    print('\n')
    
os.remove(f'./data/{today.year}{month}{day}.json')
with open(f'./data/{today.year}{month}{day}.json', 'w') as f:
    json.dump(jsonList, f, ensure_ascii=False, indent=4)
