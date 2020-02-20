import requests
from bs4 import BeautifulSoup


def get_currency():
    resp = requests.get('http://www.cbr.ru/scripts/xml_daily.asp')
    soup = BeautifulSoup(resp.content, 'xml')
    currency_eur = float(soup.find('CharCode', text='EUR').find_next_sibling('Value').string.replace(',', '.'))
    return currency_eur


def get_prices_dict(product_list):
    prices_dict = {}
    vat = 11931.93 / 14199.0
    site_url = 'https://www.computeruniverse.net/ru/'
    for product in product_list:
        resp = requests.get(site_url + product)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        tags_name = soup('h1', 'at__productheadline')
        product_name = tags_name[0].text.replace('\n','')
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


def format_print(product_name, price_eur, max_str):
    line_str = "%-{}s | %-12s | %-12s".format(max_str) % (
        product_name, round(price_eur, 2), round(price_eur * currency_eurrub, 2))
    print(line_str)


def get_full_prices(product_list):
    paypal_tax_rate = 0.028
    price_delivery = 35
    products_price_dict = get_prices_dict(product_list)
    prices_sum = sum(products_price_dict.values())
    customs_tax = check_customs_tax(prices_sum)
    paypal_tax = prices_sum * paypal_tax_rate
    products_price_dict.update({'summary before customs tax': prices_sum, 'customs tax': customs_tax,
                                'delivery': price_delivery, 'paypal_tax': paypal_tax,
                                'summary': prices_sum + customs_tax + price_delivery + prices_sum * paypal_tax_rate})
    max_str = 0
    for product in products_price_dict.keys():
        if max_str < len(product):
            max_str = len(product)
    print("%-{}s | %-6s | %-8s".format(max_str) % ('Product', 'Price in EUR', 'Price in RUB'))
    for product in products_price_dict.keys():
        format_print(product, products_price_dict[product], max_str)
    # format_print('summary before customs tax', prices_sum)
    # format_print('customs tax', customs_tax)
    # format_print('delivery', price_delivery)
    # format_print('paypal_tax', paypal_tax)
    # format_print('summary', prices_sum + customs_tax + price_delivery + prices_sum * paypal_tax_rate)


currency_eurrub = get_currency()
print('current currency EURRUB is {}'.format(currency_eurrub))
get_full_prices(['intel-core-i5-9600kf-6-core-hexa-core-cpu-with-370-ghz', 'msi-z390-a-pro',
                 'ballistix-sport-lt-rot-16gb-ddr4-ram-4',
                 'be-quiet-pure-power-11-80-gold-600-watt',])
get_full_prices(['amd-ryzen-5-3600-tray', 'msi-b450-a-pro-max',
                 'ballistix-sport-lt-rot-16gb-ddr4-ram-4',
                 'be-quiet-pure-power-11-80-gold-600-watt',
                 'adata-xpg-sx8200-pro-m2-nvme-pcie-gen3x4-1tb'])
