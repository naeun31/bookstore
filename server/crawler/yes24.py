from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import Elasticsearch

es = Elasticsearch('http://localhost:9200')
barcodes = ['9791188331796', '9788956601021', '9791185428673','9780553509977','9788934975137','9791161571379']
url = 'http://www.yes24.com/Product/Search?domain=ALL&query={barcode}'
lst = []
for barcode in barcodes:
    doc = bs(req.get(url.format(barcode=barcode)).content)
    tr = doc.find('div',{'class':'itemUnit'})
    id = tr.find('a', {'class':'lnk_img'})['href'].split('/')[-1]
    image = f'https://image.yes24.com/goods/{id}/L'
    title = tr.find('div', {'class':'item_info'}).find('a', {'class':'gd_name'}).text.strip()
    author = tr.find('span', {'class':'authPub info_auth'}).text.strip()
    publish = tr.find('span', {'class':'authPub info_pub'}).text.strip()
    published_date = tr.find('span', {'class':'authPub info_date'}).text.strip()
    dtl_url = f'http://www.yes24.com/Product/Goods/{id}'
    dtl_doc = bs(req.get(dtl_url).content)
    for r in dtl_doc.find('div', {'class':'gd_infoTb'}).find_all('tr'):
        if r.find('th').text.strip() == '정가':
            price = r.find('td').text.strip()
    category2 = dtl_doc.find('div', {'id':'infoset_goodsCate'}).find('ul', {'class':'yesAlertLi'}).find_all('a')[1].text.strip()
    lst.append(dict(image=image, category2=category2, title=title, author=author, publish=publish, published_date=published_date, price=price))

print(pd.DataFrame(lst))

for i, row in df.iterrows():
    es.index(
     index='bookstore',
     document={'id':row['barcode'], 'barcode':row['barcode'], 'image':row['image']
         , 'category2':row['category2'], 'title':row['title'], 'author':row['author']
         , 'publish':row['publish'], 'published_date':row['published_date'], 'price':row['price']}
    )

