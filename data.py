# from ast import Store
# from cmath import pi
# from pydoc import html
# from importlib_metadata import re
import requests
from bs4 import BeautifulSoup
# import codecs
import random

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36' }

site = [
    'https://item.rakuten.co.jp/thegoldshopping/c/0000000443/?s=4&i=1#risFil',
    'https://item.rakuten.co.jp/thegoldshopping/c/0000000447/?s=4&i=1#risFil',
    'https://item.rakuten.co.jp/thegoldshopping/c/0000000444/?s=4&i=1#risFil',
    'https://item.rakuten.co.jp/thegoldshopping/c/0000000445/?s=4&i=1#risFil',
    'https://item.rakuten.co.jp/thegoldshopping/c/0000000446/?s=4&i=1#risFil'
]

title = [
    'watch',
    'jewelry',
    'bag',
    'wallet',
    'others'
]

class Crawler():
    def __init__(self, data):
        self.data = data  

    def get_urls(self, category_url):
        self.category_url = category_url
       
        r = requests.get(category_url,  headers = headers)
        soup = BeautifulSoup(r.text, "html.parser")
        
        a_tags = soup.select('#risFil .category_itemnamelink')
        a_tags_data = []
        for index, a_tag in enumerate(a_tags):
            # print(a_tag['href'])
            
            if not(a_tag['href'] in a_tags_data):
                a_tags_data.append(a_tag['href'])
            if( index == 0 ):
                continue
            # 拿到9個商品後break
            if(len(a_tags_data) == 9):
                break
        # print(a_tags_data)  
        return a_tags_data 
   
    def get_detail(self, urls):
        self.urls = urls
        detail_data = []
        detail = {}

        for index,url in enumerate(urls):
            detail = {}

            r = requests.get(url,  headers = headers)
            soup = BeautifulSoup(r.text, "html.parser")
            product = soup.find_all('td', bgcolor="#ffffff")

            # 取得店鋪名的tag
            store = soup.find_all('td', bgcolor="#fff6e4")
            store_name =store[len(store)-1].next_sibling
            # print(store_name)

            # 網址
            detail["url"] = url
            # 品牌
            brand = product[1].text.split('/')[1].lstrip()
            # print(brand)
            detail['brand'] = brand
            # 商品名
            product_name = product[2].text
            detail['product_name'] = product_name
            # 價錢
            price = soup.find(class_="price2").text.replace('\n','')
            detail['price'] = price
            detail['itemtype'] = ['Pick Up','新入荷','スタッフ一押し']
            detail['itemtypeclass'] = ['pickup','kaden','buyer']
            # 店名
            try:
                shop_name = store_name.text.split('GOLD')[1].split('T')[0].replace('（北海道札幌市）','').replace('お気軽にお問い合わせ下さい。','').replace(' 札幌','').replace(' ','').replace('\n','')
                detail['shop_name'] = shop_name
                
                if detail['shop_name'] == "銀座店":
                    # print("是銀座店")
                    detail["itemstore"] = "ginza"
                elif detail['shop_name'] == "狸小路3丁目店":
                    # print("是狸小路3丁目店")
                    detail["itemstore"] = "tanukikouji"
            except:
                print(f'第{index + 1}筆 店名資料有誤，請檢察')
                detail['shop_name'] =''
            detail_data.append(detail)
        print('爬蟲成功')
        # print(detail_data)

        return detail_data

    def get_imgs(self, url):
        self.url = url
        # print(url)
        imgs_data = []

        r = requests.get(url,  headers = headers)
        soup = BeautifulSoup(r.text, "html.parser")
        imgs = soup.find_all(class_='noImage')

        for index,img in enumerate(imgs):
            if(index == 9):
                break
            img = img['src'].split('?')[0]
            imgs_data.append(img)
        # print(imgs_data)
        return imgs_data

    def render_html(self, detail_data, imgs):
        html = '' 
        for index, item in enumerate(detail_data):
            num = random.randrange(0, 3)
            html += f"""
            <li class="box">
                <p class="img"><a href="{item["url"]}" class="ptn01" target="_top">
                    <img src="{imgs[index]}" width="264" height="264">
                    <span class="overlay"><span>Click</span></span>
                    </a></p>
                <p class="category {item['itemtypeclass'][num]}">{item['itemtype'][num]}</p>
                <p class="shop_name {item["itemstore"]}">{item['shop_name']}</p>
                <p class="price">税込 {item['price']}</p>
                <p class="txt">{item['brand']}<br>{item['product_name']}</p>
                <div class="inside_box"></div>
            </li> """
        return html
       
    def run(self, data):
        index = site.index(data)
        urls =  self.get_urls(data)
        imgs = self.get_imgs(data)
        detail_data = self.get_detail(urls)
        html = self.render_html(detail_data, imgs)

        # print(html)
       
        with open(f'{title[index]}.html','w', encoding="utf-8") as file:
            file.write(html)

c = Crawler(site)
for i in site :
    c.run(i)
    
