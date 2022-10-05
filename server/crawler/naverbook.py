from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd

barcodes = ['9791188331796', '9788956601021', '9791185428673','9780553509977','9788934975137','9791161571379']

lst = []
url = 'https://search.shopping.naver.com/book/search?query={barcode}'
for barcode in barcodes:
    doc = bs(req.get(url.format(barcode=barcode)).content)
    item = doc.find('ul', {'class':'list_book'}).find('li')
    image = item.find('img')['src']
    title = item.find('span', {'class':'bookListItem_text__bglOw'}).text.strip().replace('\xa0','')
    try:
        category2 = item.find('div', {'class':'bookListItem_feature__txTlp'}).text.strip().split(' ')[0]
    except:
        pass
    author = item.find('span',{'class':'bookListItem_define_data__kKD8t'}).text.strip()
    publish = item.find('span', {'class':'bookListItem_define_data__kKD8t'}).text.strip()
    try:
        published_date = item.find('div', {'class':'bookListItem_detail_date___byvG'}).text.strip()
    except:
        pass
    price=''
    lst.append(dict(barcode=barcode, image=image, category2=category2, title=title, author=author, publish=publish, published_date=published_date, price=price))

df = pd.DataFrame(lst)
