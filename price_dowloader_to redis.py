import redis
import requests
from bs4 import BeautifulSoup
import datetime


def get_currency():
    resp = requests.get('http://www.cbr.ru/scripts/xml_daily.asp')
    soup = BeautifulSoup(resp.content, 'xml')
    currency_eur = float(soup.find('CharCode', text='EUR').find_next_sibling('Value').string.replace(',', '.'))
    return currency_eur


def get_prices_dict(product_list):
    prices_dict = {}
    vat = 11931.93 / 14199.0
    site_url = 'https://www.computeruniverse.net/en/'
    for product in product_list:
        resp = requests.get(site_url + product)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        tags_name = soup('h1', 'at__productheadline')
        product_name = tags_name[0].text.replace('\n', '').strip()
        tags_price = soup('div', 'product-price')
        price = float([tag['data-productpricevalue'] for tag in tags_price][0].replace(',', ''))
        price_without_vat = round(price * vat, 2)
        prices_dict[product_name] = price_without_vat
    return prices_dict


def check_customs_tax(prices_sum):
    tax_rate = 0.15
    untaxed_value = 200
    if prices_sum <= untaxed_value:
        return 0
    else:
        tax = (prices_sum - untaxed_value) * tax_rate
        return tax


def save_to_redis(product_list):
    today_str = datetime.date.today().isoformat()
    # today_str = '2020-02-03'
    conn = redis.Redis()
    products_price_dict = {"currency": get_currency()}
    products_price_dict.update(get_prices_dict(product_list))
    prices = {f"{today_str}": products_price_dict}
    print(prices)
    with conn.pipeline() as pipe:
        for h_id, product in prices.items():
            pipe.hmset(h_id, product)
        pipe.execute()
    conn.bgsave()


def get_from_redis():
    conn = redis.Redis()
    keys_list = conn.keys()
    print(keys_list)
    for key in keys_list:
        for key1 in conn.hgetall(key).keys():
            print(key1)


def get_full_prices(product_list):
    paypal_tax_rate = 0.028
    price_delivery = 35
    products_price_dict = get_prices_dict(product_list)
    prices_sum = sum(products_price_dict.values())
    customs_tax = check_customs_tax(prices_sum)
    paypal_tax = prices_sum * paypal_tax_rate


currency_eurrub = get_currency()
print('current currency EURRUB is {}'.format(currency_eurrub))
save_to_redis(['intel-core-i5-9600kf-6-core-hexa-core-cpu-with-370-ghz', 'msi-z390-a-pro',
               'amd-ryzen-5-3600-tray', 'msi-b450-a-pro-max',
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
               ])
get_from_redis()
