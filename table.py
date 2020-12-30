import re

import redis


class Table(object):
    links_list_name = 'new_link'

    # test_header = ['Intel Core i5-9600KF 6 core (Hexa Core) CPU with 3.70 GHz', 'MSI Z390-A PRO',
    #                'AMD Ryzen 5 3600 Tray', 'MSI B450-A PRO MAX', 'Ballistix Sport LT Rot 16GB DDR4 Kit (2x8GB) RAM',
    #                'Crucial Ballistix Sport LT Rot 16GB DDR4 Kit RAM', 'Ballistix Sport LT Rot 16GB DDR4 RAM',
    #                'G.Skill Ripjaws V 16GB DDR4 K2 16GVK RAM', 'G.Skill Ripjaws V 16GB DDR4 16GVK Kit RAM',
    #                'be quiet! Pure Power 11 80+ Gold 600 Watt', 'Seasonic Core GC-650 80+ Gold 650 Watt',
    #                'be quiet! Pure Power 11 80+ Gold 700 Watt', 'ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 512GB',
    #                'ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 1TB']

    def __init__(self):
        self.headers_list = ''
        self.lines_dict = ''
        self.table_html = ''
        # self.update()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Table, cls).__new__(cls)
        return cls.instance

    def create_headers_list(self, conn):
        # header_list = ['Date', 'currency']+self.test_header
        header_list = ['Date', 'Currency']
        # conn = redis.Redis(db=1)
        keys_list = conn.keys()
        for key in keys_list:
            key_str = bytes(key).decode("utf-8")
            result = re.findall(r"^\D+", key_str)
            if result and key_str != self.links_list_name:
                header_list = header_list + list(
                    bytes(value).decode('utf-8') for value in conn.hgetall(key_str).values())
        # conn.close()
        return header_list

    def create_lines_dict(self, conn):
        lines_dict = {}
        item_yesterday_dict = {}
        # conn = redis.Redis(db=1)
        keys_list = conn.keys()
        keys_list.sort()
        for key in keys_list:
            prices_list = ['']
            key_str = bytes(key).decode('utf-8')
            result = re.findall(r'^\d+-\d+-\d+', key_str)
            if result:
                items_today_dict = {bytes(key).decode('utf-8'): bytes(value).decode('utf-8') for key, value in
                                    conn.hgetall(key_str).items()}
                prices_list.append(items_today_dict.get(self.headers_list[1]))
                for product in self.headers_list[2:]:
                    # for product in self.test_header:
                    price_today = items_today_dict.get(product)
                    price_yesterday = item_yesterday_dict.get(product)
                    if price_yesterday is not None and price_today is not None:
                        if price_today > price_yesterday:
                            price_today = f'+{price_today}'
                        elif price_today < price_yesterday:
                            price_today = f'-{price_today}'
                        elif price_today == price_yesterday:
                            price_today = '—'
                    elif price_today is None:
                        price_today = ''
                    prices_list.append(price_today)
                item_yesterday_dict = items_today_dict
                lines_dict[key_str] = prices_list
        # conn.close()
        lines_dict = dict(sorted(lines_dict.items(), reverse=True))
        return lines_dict

    def create_html(self):
        # print(self.headers_list)
        header_html = ''
        lines_html = ''
        for i, header in enumerate(self.headers_list):
            if i < 2:
                header_html = header_html + f'\t\t<th style="text-align:center">{header}</th>\n'
            else:
                header_html = header_html + f'\t\t<th colspan="2" style="text-align:center">{header}</th>\n'
        header_html = f'\t<tr>\n{header_html}\t</tr>\n'
        for day, prices in self.lines_dict.items():
            line_table = ''
            line_table = line_table + f'\t\t<td style="text-align:center">{day}</td>\n'
            currency = float(prices[1])
            line_table = line_table + f'\t\t<td style="text-align:center">{round(currency, 2)}</td>\n'
            for price in prices[2:]:
                if price.find('+') == 0:
                    price = price.replace('+', '')
                    line_table = line_table + f'\t\t<td style="text-align:center;color:red">{price}</td>\n'
                elif price.find('-') == 0:
                    price = price.replace('-', '')
                    line_table = line_table + f'\t\t<td style="text-align:center;color:green">{price}</td>\n'
                else:
                    line_table = line_table + f'\t\t<td style="text-align:center">{price}</td>\n'
                if price == '' or price == '—':
                    line_table = line_table + f'\t\t<td style="text-align:center;background-color:#f0f0f0">{price}</td>\n'
                else:
                    price_rub = round(float(price) * currency, 2)
                    line_table = line_table + f'\t\t<td style="text-align:center;background-color:#f0f0f0">{price_rub}</td>\n'
            lines_html = lines_html + f'\t<tr>\n{line_table}\t</tr>\n'
        table_html = f'<tbody>\n{header_html}{lines_html}</tbody>'
        return table_html

    def update(self, conn):
        self.headers_list = self.create_headers_list(conn)
        self.lines_dict = self.create_lines_dict(conn)
        self.table_html = self.create_html()
        # print('Table were update')
        # print(self.table_html)
