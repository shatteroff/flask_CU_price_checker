import datetime
import re

import redis
import requests
from bs4 import BeautifulSoup

import config
from config import Config
from product import Product


class RedisHelper(object):
    links_list_name = 'new_link'
    currency_str = 'Currency'
    wrong_result = 'There is no product'

    site_index_link = 'https://www.computeruniverse.net/en/'
    test_products_link_list = ['intel-core-i5-9600kf-6-core-hexa-core-cpu-with-370-ghz', 'amd-ryzen-5-3600-tray',
                               'msi-b450-a-pro-max', 'msi-z390-a-pro',
                               'asrock-z390-phantom-gaming-6',
                               'asrock-z390-phantom-gaming-7',
                               'ballistix-sport-lt-rot-16gb-ddr4-kit-2x8gb-ram',
                               'crucial-ballistix-sport-lt-rot-16gb-ddr4-kit-ram',
                               'ballistix-sport-lt-rot-16gb-ddr4-ram-4',
                               'gskill-ripjaws-v-16gb-ddr4-k2-16gvk-ram',
                               'gskill-ripjaws-v-16gb-ddr4-16gvk-kit-ram-4',
                               'be-quiet-pure-power-11-80-gold-600-watt',
                               'seasonic-core-gc-650-80-gold-650-watt',
                               'be-quiet-pure-power-11-80-gold-700-watt',
                               'adata-xpg-sx8200-pro-m2-nvme-pcie-gen3x4-512gb',
                               'adata-xpg-sx8200-pro-m2-nvme-pcie-gen3x4-1tb'
                               ]

    def __init__(self):
        # self.today_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.today_str = datetime.date.today().isoformat()

    def get_currency(self):
        resp = requests.get('http://www.cbr.ru/scripts/xml_daily.asp')
        soup = BeautifulSoup(resp.content, 'xml')
        currency_eur = float(soup.find('CharCode', text='EUR').find_next_sibling('Value').string.replace(',', '.'))
        return currency_eur

    def get_price_table_name_list(self, conn):
        table_name_list = list(bytes(x).decode('utf-8') for x in conn.keys())
        days_list = []
        for table_name in table_name_list:
            result = re.findall(r'^\d+-\d+-\d+', table_name)
            if result:
                days_list.append(table_name)
        days_list.sort()
        return days_list

    def add_to_links_list(self, link, conn):
        # conn = redis.Redis(db=1)
        conn.rpush(self.links_list_name, link)
        print(f'{link} added as new link')
        # conn.close()

    def add_product(self, conn):
        # conn = redis.Redis(db=1)
        links_list = conn.lrange(self.links_list_name, 0, -1)
        with conn.pipeline() as pipe:
            for link in links_list:
                link_str = bytes(link).decode("utf-8")
                product_ = Product(link_str, None)
                if product_.name != self.wrong_result:
                    pipe.hset(product_.category, link, product_.name)
                    pipe.hset(self.today_str, product_.name, product_.price)
                else:
                    print(f'There was not name tag on {link_str}')
                pipe.lrem(self.links_list_name, 0, link)
            # pipe.bgsave()
            pipe.execute()
        # conn.bgsave()
        # conn.close()

    def load_prices(self, conn):
        # conn = redis.Redis(db=1)
        is_robot_block = True
        keys_list = conn.keys()
        today_price_dict = {}
        with conn.pipeline() as pipe:
            today_price_dict.update({self.currency_str: self.get_currency()})
            # pipe.hset(self.today_str, self.currency_str, self.get_currency())
            for key in keys_list:
                key_str = bytes(key).decode("utf-8")
                result = re.findall(r"^\D+", key_str)
                if result and key_str != self.links_list_name:
                    key_dict = conn.hgetall(key)
                    for field, value in key_dict.items():
                        name = bytes(value).decode("utf-8")
                        link = bytes(field).decode("utf-8")
                        product_ = Product(link, name)
                        if product_.price != 3.5:
                            today_price_dict.update({product_.name: product_.price})
                            is_robot_block = False
                        # pipe.hset(self.today_str, product_.name, product_.price)
            if not is_robot_block:
                for name, price in today_price_dict.items():
                    pipe.hset(self.today_str, name, price)
                # pipe.bgsave()
                pipe.execute()
        # conn.bgsave()
        # conn.close()

    def is_link_exist(self, link, conn):
        # conn = redis.Redis(db=1)
        keys_list = conn.keys()
        for key in keys_list:
            key_str = bytes(key).decode("utf-8")
            result = re.findall(r"^\D+", key_str)
            if result and key_str != self.links_list_name:
                value = conn.hget(key_str, link)
                if value:
                    # conn.close()
                    return True
        # conn.close()
        return False

    def get_fresh_prices_dict(self, conn):
        fresh_date = self.get_price_table_name_list(conn)[-1]
        prices_dict_bytes = conn.hgetall(fresh_date)
        prices_dict = {bytes(key).decode('utf-8'): bytes(value).decode('utf-8') for key, value in
                       prices_dict_bytes.items()}
        return prices_dict

    def get_products_dict(self, conn):
        products_dict = {}
        keys_list = conn.keys()
        for key in keys_list:
            key_str = bytes(key).decode("utf-8")
            result = re.findall(r"^\D+", key_str)
            if result and key_str != self.links_list_name:
                products_list = list(bytes(x).decode('utf-8') for x in conn.hgetall(key_str).values())
                products_dict[key_str] = products_list
        return products_dict

    def update_date(self):
        self.today_str = datetime.date.today().isoformat()
        # self.today_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
