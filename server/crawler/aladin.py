from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd


barcodes = ['9791188331796', '9788956601021', '9791185428673','9780553509977','9788934975137','9791161571379']
url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord={barcode}&x=0&y=0'
lst = []
for barcode in barcodes:
    doc = bs(req.get(url.format(barcode=barcode)).content)
    item = doc.find('div',{'id':'Search3_Result'}).find('tr')
    image = item.find('img')['src']
    title = item.find('a', {'class':'bo3'}).text.strip()
    try:
        [author, publish, published_date] = [x.text.strip() for x in doc.find('div',{'id':'Search3_Result'}).find('div', {'class':'ss_book_list'}).find('ul').find_all('li')][2].split('|')
    except:
        [author, publish, published_date] = [x.text.strip() for x in doc.find('div',{'id':'Search3_Result'}).find('div', {'class':'ss_book_list'}).find('ul').find_all('li')][1].split('|')
    [author, publish, published_date] = [author.strip(), publish.strip(), published_date.strip()]
    price = [x.text.strip() for x in doc.find('div',{'id':'Search3_Result'}).find('div', {'class':'ss_book_list'}).find('ul').find_all('li')][3].split(' ')[0]
    dtl_doc = bs(req.get(item.find('a')['href']).content,'lxml')
    category2 = dtl_doc.find('div',{'class':'conts_info_list2'}).text.strip().replace('\xa0',' ')
    lst.append(dict(barcode=barcode, image=image, category2=category2, title=title, author=author, publish=publish, published_date=published_date, price=price))

df = pd.DataFrame(lst)
