import datetime

import redis

from order_table import OrderTable
from redis_helper import RedisHelper
from table import Table

# table = Table()
# print(table.create_header())
# print(table.create_html())

# rh = RedisHelper()
# for product_link in rh.test_products_link_list:
#     rh.add_to_links_list(rh.site_index_link + product_link)
# print(f'{product_link} is {rh.is_link_exist(rh.site_index_link + product_link)}')
# rh.add_product()
# rh.load_prices()

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
date_yesterday = datetime.date.today() - datetime.timedelta(days=1)
print(date_yesterday.strftime("%Y-%m-%d"))

# red = RedisHelper()
conn = redis.Redis(db=1)
# red.load_prices(conn)
conn.hdel('Processors (CPUs)','https://www.computeruniverse.net/en/intel-core-i7-9700k-tray')
conn.close()
