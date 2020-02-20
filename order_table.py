from redis_helper import RedisHelper


class OrderTable(object):

    def __init__(self, prices_dict, products_list):
        self.prices_dict = prices_dict
        self.products_list = products_list
        self.paypal_tax_rate = 0.028
        self.price_delivery = 35.0

    def check_customs_tax(self, prices_sum):
        tax_rate = 0.15
        untaxed_value = 200
        if prices_sum <= untaxed_value:
            return 0
        else:
            tax = (prices_sum - untaxed_value) * tax_rate
            return tax

    def create_html(self):
        # rh = RedisHelper()
        currency = float(self.prices_dict.get('Currency'))
        header_html = f'\t<tr>\n' \
                      f'\t\t<th style="text-align:center">Product</th>\n' \
                      f'\t\t<th style="text-align:center">Price in EUR</th>\n' \
                      f'\t\t<th style="text-align:center">Price in RUB</th>\n' \
                      f'\t</tr>\n'
        lines_html = ''
        price_full = 0.0
        for product in self.products_list:
            price = float(self.prices_dict.get(product))
            price_full = price_full + price
            lines_html = lines_html + f'\t<tr>\n' \
                                      f'\t\t<td style="text-align:center">{product}</td>\n' \
                                      f'\t\t<td style="text-align:center">{price}</td>\n' \
                                      f'\t\t<td style="text-align:center">{round(price * currency, 2)}</td>\n' \
                                      f'\t</tr>'
        lines_html = lines_html + f'\t<tr>\n' \
                                  f'\t\t<td style="text-align:center">Products summary</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(price_full, 2)}</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(price_full * currency, 2)}</td>\n' \
                                  f'\t</tr>'
        customs_tax = self.check_customs_tax(price_full)
        lines_html = lines_html + f'\t<tr>\n' \
                                  f'\t\t<td style="text-align:center">Customs tax</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(customs_tax, 2)}</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(customs_tax * currency, 2)}</td>\n' \
                                  f'\t</tr>'
        price_full = price_full + customs_tax
        lines_html = lines_html + f'\t<tr>\n' \
                                  f'\t\t<td style="text-align:center">PayPal tax</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(price_full * self.paypal_tax_rate, 2)}</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(price_full * self.paypal_tax_rate * currency, 2)}</td>\n' \
                                  f'\t</tr>'
        price_full = price_full + price_full * self.paypal_tax_rate
        lines_html = lines_html + f'\t<tr>\n' \
                                  f'\t\t<td style="text-align:center">Delivery</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(self.price_delivery, 2)}</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(self.price_delivery * currency, 2)}</td>\n' \
                                  f'\t</tr>'
        price_full = price_full + self.price_delivery
        lines_html = lines_html + f'\t<tr>\n' \
                                  f'\t\t<td style="text-align:center">Order summary</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(price_full, 2)}</td>\n' \
                                  f'\t\t<td style="text-align:center">{round(price_full * currency, 2)}</td>\n' \
                                  f'\t</tr>'
        table_html = f'<tbody>\n{header_html}{lines_html}</tbody>'
        return table_html
