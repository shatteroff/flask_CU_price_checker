import requests
from bs4 import BeautifulSoup

links_list_name = 'new_link'

url = 'https://www.computeruniverse.net/en/'
products_list = ['intel-core-i5-9600kf-6-core-hexa-core-cpu-with-370-ghz', 'msi-z390-a-pro',
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
                 ]
for product in products_list:
    resp = requests.get(url + product)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    tags_name = soup('h1', 'at__productheadline')
    product_name = tags_name[0].text.replace('\n', '').strip()
    tags_category = soup.find('a', {'data-breadcrumblevel': "2"})
    print(list(tags_category.children)[1].string)