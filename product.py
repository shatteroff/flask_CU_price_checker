import re

import requests
from bs4 import BeautifulSoup


class Product(object):

    def __init__(self, link, name):
        self.vat = 11931.93 / 14199.0
        self.link = link
        self.soup = None
        self.name = name
        self.category = ''
        # self.is_new = is_new
        self.price = 3.5
        self.set_product_soup()
        self.set_product()

    def set_product_soup(self):
        print(f'Downloading data from {self.link}')
        resp = requests.get(self.link)
        html = resp.text
        self.soup = BeautifulSoup(html, 'lxml')

    def set_product(self):
        tags_price = self.soup('div', 'product-price')
        if tags_price:
            price = float([tag['data-productpricevalue'] for tag in tags_price][0].replace(',', ''))
            self.price = round(price * self.vat, 2)
            if self.name is None:
                tags_name = self.soup('h1', 'at__productheadline')
                if tags_name:
                    product_name = tags_name[0].text.replace('\n', '').strip()
                    tags_category = self.soup.find('a', {'data-breadcrumblevel': "2"})
                    self.category = list(tags_category.children)[1].string
                    if self.category.lower().find('processors') != -1:
                        result_amd = re.findall(r"AMD\sRyzen\s\d\s\S*", product_name)
                        result_intel = re.findall(r"Intel\s\S*\si\d.\S*", product_name)
                        if result_amd or result_intel:
                            self.name = (result_amd + result_intel)[0]
                        else:
                            self.name = product_name
                    else:
                        self.name = product_name
                else:
                    self.name = "There is no product"
            print(f'Product name is {self.name.upper()} and price is {self.price}')
        else:
            self.name = "There is no product"

