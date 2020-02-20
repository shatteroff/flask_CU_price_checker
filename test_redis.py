import redis


def get_unique_fields(conn, keys_list):
    product_names_list = []
    product_names_set = set()
    for key in keys_list:
        # print((conn.hgetall(key)))
        product_names_list = product_names_list + list(conn.hgetall(key).keys())
    for name in product_names_list:
        product = bytes(name).decode("utf-8")
        product_names_set.add(product)
    return list(product_names_set)


lines = ''
product_price_html = ''
table_header = ''
table_sub_header = '<th style="text-align:center"></th>\n<th style="text-align:center"></th>\n'
currency_eurrub = 70.0
conn = redis.Redis()
keys_list = conn.keys()
keys_list.sort()
print(keys_list)
fields_list = get_unique_fields(conn, keys_list)
print(fields_list)
for i, key in enumerate(keys_list):
    # print(bytes(key).decode("utf-8"))
    if i == 0:
        table_header = table_header + '<th style="text-align:center">Date</th>\n<th style="text-align:center">Currency</th>\n'
    for field in fields_list:
        if field == 'currency':
            currency_eurrub = float(bytes(conn.hget(key, field)).decode("utf-8"))
        else:
            if i == 0:
                table_header = table_header + f'\t\t<th colspan="2" style="text-align:center">{field}</th>\n'
                table_sub_header = table_sub_header + '\t\t<th style="text-align:center">EUR</th>\n' \
                                                      '\t\t<th style="text-align:center">RUB</th>\n'
            redis_price = conn.hget(key, field)
            if redis_price is None:
                product_price_html = product_price_html + \
                                     f'\t\t<td style="text-align:center"></td>\n' \
                                     f'\t\t<td style="text-align:center;background-color:#f0f0f0"></td>\n'
            else:
                product_price_html = product_price_html + \
                                     f'\t\t<td style="text-align:center">{bytes(redis_price).decode("utf-8")}</td>\n' \
                                     f'\t\t<td style="text-align:center;background-color:#f0f0f0">{round(float(bytes(redis_price).decode("utf-8")) * currency_eurrub, 2)}</td>\n'
    line = f'\t<tr>\n' \
           f'\t\t<td style="text-align:center">{bytes(key).decode("utf-8")}</td>\n' \
           f'\t\t<td style="text-align:center">{currency_eurrub}</td>' \
           f'\n{product_price_html}' \
           f'\t</tr>\n'
    lines = lines + line
    product_price_html = ''
    # print(line)
# print(table_header)
# print(table_sub_header)
table = f'<tbody>\n\t<tr>\n{table_header}\t</tr>\n\t<tr>\n{table_sub_header}\t</tr>\n{lines}</tbody>'
print(table)


