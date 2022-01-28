import requests
from bs4 import BeautifulSoup
import codecs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

data = [
    'https://item.rakuten.co.jp/thegoldshopping/c/0000000443/?s=4&i=1#risFil',
]

class Crawler():
    def __init__(self, data):
        self.data = data        

    def get_urls(self, category_url):
        self.category_url = category_url
        r = requests.get(category_url,  headers = headers)
        soup = BeautifulSoup(r.text, "html.parser")
        
        a_tags = soup.select('#risFil a')
        a_tags_data = []

        for index, a_tag in enumerate(a_tags):
            if( index == 0 ):
                continue
            # 拿到9個商品後break
            elif( len(a_tags_data) == 6):
                break
            if a_tag['href'] in a_tags_data:
                continue
            a_tags_data.append(a_tag['href'])

        return a_tags_data

    def get_detail(self, urls):
        self.urls = urls

        detail_data = []
        detail = {}

        for index,url in enumerate(urls):
            detail = {}

            r = requests.get(url,  headers = headers)
            soup = BeautifulSoup(r.text, "html.parser")
            product = soup.find_all('td',bgcolor="#ffffff")

            # 網址
            detail["url"] = url
            # 品牌
            brand = product[1].text.split('/')[1].replace(' ','')
            detail['brand'] = brand
            # 商品名
            product_name = product[2].text
            detail['product_name'] = product_name
            # 價錢
            price = soup.find(class_="price2").text.replace('\n','')
            detail['price'] = price
            # 店名
            try:
                shop_name = product[len(product) - 1].text.split('GOLD')[1].split('T')[0].replace('（北海道札幌市）','').replace('お気軽にお問い合わせ下さい。','').replace(' 札幌','').replace(' ','').replace('\n','')
                detail['shop_name'] = shop_name
            except:
                print(f'第{index + 1}筆 店名資料有誤，請檢察')
                detail['shop_name'] =''
            detail_data.append(detail)
        print('爬蟲成功')
        return detail_data

    def get_imgs(self,url):
        self.url = url
        imgs_data = []

        r = requests.get(url,  headers = headers)
        soup = BeautifulSoup(r.text, "html.parser")
        imgs = soup.find_all(class_='noImage')

        for index,img in enumerate(imgs):
            if(index == 9):
                break
            img = img['src'].split('?')[0]
            imgs_data.append(img)
        return imgs_data

    def render_html(self, detail_data, imgs):

        html = ''
        
        for index, item in enumerate(detail_data):
            html += f"""
                    <li class="newitem__list__item">
                        <a href="{item["url"]}">
                        <img class="newitem__list__item__image" src="{imgs[index]}" alt="" loading="lazy">
                        <p class="newitem__list__item__brandname">{item['brand']}</p>
                        <p class="newitem__list__item__name">{item['product_name']}</p>
                        <p class="newitem__list__item__price">{item['price']}(税込)</p>
                        </a>
                    </li>
                    """
        # print(html)

        with open("data_sp.html", "w", encoding='UTF-8') as file:
            file.write(html)

    def run(self, data):
        urls =  self.get_urls(data)
        imgs = self.get_imgs(data)
        detail_data = self.get_detail(urls)
        self.render_html(detail_data, imgs)


c = Crawler(data)
c.run(data[0])