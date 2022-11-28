from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd



def crawling(barcodes):
    barcodes = barcodes
    #print(barcodes)
    url = 'http://www.yes24.com/Product/Search?domain=ALL&query={barcode}'
    lst = []
    for barcode in barcodes:
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

    df = pd.DataFrame(lst)
    #df.set_index('barcode', inplace=True)
    return df

