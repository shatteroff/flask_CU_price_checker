import datetime

import redis
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import URL

from config import Config
from order_table import OrderTable
from redis_helper import RedisHelper
from table import Table

app = Flask(__name__)
scheduler = BackgroundScheduler()
Bootstrap(app)
app.config.from_object(Config)
csrf = CSRFProtect(app)
redis_helper = RedisHelper()
table = Table()
conn = Config.conn
table.update(conn)


# conn.close()


class MainForm(FlaskForm):
    product_link = StringField("Product link:", validators=[URL(message="Invalid URL")])
    # product_name = StringField("Product name:", validators=[DataRequired()])
    submit = SubmitField("Add")


class CalcForm(FlaskForm):
    proc = SelectMultipleField('Processors (CPUs)')
    mobo = SelectMultipleField('Motherboards')
    psu = SelectMultipleField('Power Supplies')
    memory = SelectMultipleField('Memory')
    ssd = SelectMultipleField('Solid State Drives (SSD)')
    # proc = SelectField('Processors (CPUs)',
    #                    choices=list((x, x) for x in products_dict.get('Processors (CPUs)')))
    # mobo = SelectField('Motherboards', choices=list((x, x) for x in products_dict.get('Motherboards')))
    # psu = SelectField('Power Supplies', choices=list((x, x) for x in products_dict.get('Power Supplies')))
    # memory = SelectField('Memory', choices=list((x, x) for x in products_dict.get('Memory')))
    # ssd = SelectField('Solid State Drives (SSD)',
    #                   choices=list((x, x) for x in products_dict.get('Solid State Drives (SSD)')))
    submit = SubmitField("Calculate")

    def __init__(self, *args, **kwargs):
        super(CalcForm, self).__init__(*args, **kwargs)
        conn_calc = conn
        products_dict = redis_helper.get_products_dict(conn_calc)
        conn_calc.close()
        self.proc.choices = list((x, x) for x in products_dict.get('Processors (CPUs)'))
        self.mobo.choices = list((x, x) for x in products_dict.get('Motherboards'))
        self.psu.choices = list((x, x) for x in products_dict.get('Power Supplies'))
        self.memory.choices = list((x, x) for x in products_dict.get('Memory'))
        self.ssd.choices = list((x, x) for x in products_dict.get('Solid State Drives (SSD)'))


# @scheduler.scheduled_job('interval', minutes=30)
@scheduler.scheduled_job('cron', hour=Config.hour_for_update, minute=Config.minute_for_update)
def update_prices():
    print(datetime.datetime.now())
    conn2 = conn
    redis_helper.update_date()
    redis_helper.load_prices(conn2)
    redis_helper.add_product(conn2)
    table.update(conn2)
    conn2.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        conn1 = conn
        link = form.product_link.data
        if redis_helper.is_link_exist(link, conn1):
            flash('This product already exist')
        else:
            flash('Your link is {}'.format(link))
            redis_helper.add_to_links_list(link, conn1)
        conn1.close()
        # return redirect('/career')
    return render_template('main_table_page.html', table=table.table_html, form=form)


@app.route('/calc/', methods=['GET', 'POST'])
def calc():
    calc_form = CalcForm()
    if calc_form.submit.data:
        # conn = redis.Redis(db=1)
        prices_dict = redis_helper.get_fresh_prices_dict(conn)
        conn.close()
        print('Pressed')
        check_chosen_products_list = [calc_form.proc.data, calc_form.mobo.data, calc_form.psu.data,
                                      calc_form.memory.data, calc_form.ssd.data]
        products_chosen_list = []
        for product in check_chosen_products_list:
            if product:
                products_chosen_list.append(product[0])
        print(products_chosen_list)
        order_table = OrderTable(prices_dict, products_chosen_list)
        table_html = order_table.create_html()
        flash(table_html)
    return render_template('calc_page.html', table=table, form=calc_form)


@app.route('/career/')
def career():
    return 'Career Page'


@app.route('/feedback/')
def feedback():
    return 'Feedback Page'


@app.route('/user/<id>/')
def user_profile(id):
    return "Procfile page of user #{}".format(id)


if __name__ == "__main__":
    scheduler.start()
    app.run()
