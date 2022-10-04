from bs4 import BeautifulSoup as bas
import requests as req
import pandas as pd


barcodes = ['9791188331796', '9788956601021', '9791185428673','9780553509977','9788934975137','9791161571379']
url = 'https://search.kyobobook.co.kr/web/search?vPstrKeyWord={barcode}&orderClick=LAG'
lst = []
for barcode in barcodes:
    doc = bs(req.get(url.format(barcode=barcode)).content)
    tr = doc.find('tbody', {'id':'search_list'}).find('tr')
    image = tr.find('img')['src']
    category2 = tr.find('div',{'class':'title'}).find('span',{'class':'category2'}).text.strip()
    title = tr.find('div',{'class':'title'}).find('strong').text.strip()
    author = tr.find('div',{'class':'author'}).find('a').text.strip()
    publish = tr.find('div',{'class':'author'}).find_all('a')[1].text.strip()
    published_date = tr.find('div',{'class':'author'}).text.strip().split('\t')[-1]
    price = tr.find('div',{'class':'org_price'}).text.strip()
    lst.append(dict(image=image, category2=category2, title=title, author=author, publish=publish, published_date=published_date, price=price))

pd.DataFrame(lst)

