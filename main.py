import redis
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import SubmitField, SelectMultipleField, widgets

from config import Config
from order_table import OrderTable
from redis_helper import RedisHelper

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)
csrf = CSRFProtect(app)
rh = RedisHelper()


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CalcForm(FlaskForm):
    conn = redis.Redis(db=1)
    products_dict = rh.get_products_dict(conn)
    conn.close()
    proc = SelectMultipleField('Processors (CPUs)',
                               choices=list((x, x) for x in products_dict.get('Processors (CPUs)')))
    mobo = SelectMultipleField('Motherboards', choices=list((x, x) for x in products_dict.get('Motherboards')))
    psu = SelectMultipleField('Power Supplies', choices=list((x, x) for x in products_dict.get('Power Supplies')))
    memory = SelectMultipleField('Memory', choices=list((x, x) for x in products_dict.get('Memory')))
    ssd = SelectMultipleField('Solid State Drives (SSD)',
                              choices=list((x, x) for x in products_dict.get('Solid State Drives (SSD)')))
    # available = MultiCheckboxField('Available', choices=AVAILABLE_CHOICES)
    submit = SubmitField("Submit")


table = """
<tbody>
	<tr>
<th style="text-align:center">Date</th>
<th style="text-align:center">Currency</th>
		<th colspan="2" style="text-align:center">be quiet! Pure Power 11 80+ Gold 600 Watt</th>
		<th colspan="2" style="text-align:center">ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 1TB</th>
		<th colspan="2" style="text-align:center">MSI Z390-A PRO</th>
		<th colspan="2" style="text-align:center">ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 512GB</th>
		<th colspan="2" style="text-align:center">be quiet! Pure Power 11 80+ Gold 700 Watt</th>
		<th colspan="2" style="text-align:center">G.Skill Ripjaws V 16GB DDR4 16GVK Kit RAM</th>
		<th colspan="2" style="text-align:center">AMD Ryzen 5 3600 Tray</th>
		<th colspan="2" style="text-align:center">G.Skill Ripjaws V 16GB DDR4 K2 16GVK RAM</th>
		<th colspan="2" style="text-align:center">Ballistix Sport LT Rot 16GB DDR4 RAM</th>
		<th colspan="2" style="text-align:center">Seasonic Core GC-650 80+ Gold 650 Watt</th>
		<th colspan="2" style="text-align:center">MSI B450-A PRO MAX</th>
		<th colspan="2" style="text-align:center">Crucial Ballistix Sport LT Rot 16GB DDR4 Kit RAM</th>
		<th colspan="2" style="text-align:center">Ballistix Sport LT Rot 16GB DDR4 Kit (2x8GB) RAM</th>
		<th colspan="2" style="text-align:center">Intel Core i5-9600KF 6 core (Hexa Core) CPU with 3.70 GHz</th>
	</tr>
	<tr>
<th style="text-align:center"></th>
<th style="text-align:center"></th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
		<th style="text-align:center">EUR</th>
		<th style="text-align:center">RUB</th>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-03</td>
		<td style="text-align:center">69.8226</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4405.8</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9352.7</td>
		<td style="text-align:center">89.08</td>
		<td style="text-align:center;background-color:#f0f0f0">6235.6</td>
		<td style="text-align:center">73.31</td>
		<td style="text-align:center;background-color:#f0f0f0">5131.7</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5229.7</td>
		<td style="text-align:center">103.28</td>
		<td style="text-align:center;background-color:#f0f0f0">7229.6</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10876.6</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5882.1</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4111.8</td>
		<td style="text-align:center">60.29</td>
		<td style="text-align:center;background-color:#f0f0f0">4220.3</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5288.5</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f0f0f0">4758.6</td>
		<td style="text-align:center">67.07</td>
		<td style="text-align:center;background-color:#f0f0f0">4694.9</td>
		<td style="text-align:center">174.71</td>
		<td style="text-align:center;background-color:#f0f0f0">12229.7</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-04</td>
		<td style="text-align:center">69.7443</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4394.63</td>
		<td style="text-align:center">128.49</td>
		<td style="text-align:center;background-color:#f0f0f0">8971.51</td>
		<td style="text-align:center">88.7</td>
		<td style="text-align:center;background-color:#f0f0f0">6193.26</td>
		<td style="text-align:center">67.22</td>
		<td style="text-align:center;background-color:#f0f0f0">4693.48</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5216.45</td>
		<td style="text-align:center">103.28</td>
		<td style="text-align:center;background-color:#f0f0f0">7211.28</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10849.04</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5867.19</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4101.38</td>
		<td style="text-align:center">59.96</td>
		<td style="text-align:center;background-color:#f0f0f0">4186.56</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5275.1</td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center">171.93</td>
		<td style="text-align:center;background-color:#f0f0f0">12004.6</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-05</td>
		<td style="text-align:center">69.7443</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4389.71</td>
		<td style="text-align:center">128.49</td>
		<td style="text-align:center;background-color:#f0f0f0">8961.45</td>
		<td style="text-align:center">88.7</td>
		<td style="text-align:center;background-color:#f0f0f0">6186.32</td>
		<td style="text-align:center">67.22</td>
		<td style="text-align:center;background-color:#f0f0f0">4688.21</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5210.6</td>
		<td style="text-align:center">103.28</td>
		<td style="text-align:center;background-color:#f0f0f0">7203.19</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10836.87</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5860.61</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4096.78</td>
		<td style="text-align:center">59.96</td>
		<td style="text-align:center;background-color:#f0f0f0">4181.87</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5269.18</td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center">171.93</td>
		<td style="text-align:center;background-color:#f0f0f0">11991.14</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-10</td>
		<td style="text-align:center">69.6288</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4389.71</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9318.54</td>
		<td style="text-align:center">89.08</td>
		<td style="text-align:center;background-color:#f0f0f0">6212.82</td>
		<td style="text-align:center">73.31</td>
		<td style="text-align:center;background-color:#f0f0f0">5112.95</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5210.6</td>
		<td style="text-align:center">103.28</td>
		<td style="text-align:center;background-color:#f0f0f0">7203.19</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10836.87</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5860.61</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4096.78</td>
		<td style="text-align:center">60.34</td>
		<td style="text-align:center;background-color:#f0f0f0">4208.37</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5269.18</td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center">174.71</td>
		<td style="text-align:center;background-color:#f0f0f0">12185.03</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-11</td>
		<td style="text-align:center">69.7684</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4382.44</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9303.1</td>
		<td style="text-align:center">90.67</td>
		<td style="text-align:center;background-color:#f0f0f0">6313.24</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5201.97</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5201.97</td>
		<td style="text-align:center">100.45</td>
		<td style="text-align:center;background-color:#f0f0f0">6994.21</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10818.92</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5850.91</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4090.0</td>
		<td style="text-align:center">60.07</td>
		<td style="text-align:center;background-color:#f0f0f0">4182.6</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5260.46</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f0f0f0">4733.37</td>
		<td style="text-align:center">67.07</td>
		<td style="text-align:center;background-color:#f0f0f0">4670.0</td>
		<td style="text-align:center">174.71</td>
		<td style="text-align:center;background-color:#f0f0f0">12164.85</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-12</td>
		<td style="text-align:center">68.7843</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4391.22</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9321.76</td>
		<td style="text-align:center">90.67</td>
		<td style="text-align:center;background-color:#f0f0f0">6325.9</td>
		<td style="text-align:center">74.61</td>
		<td style="text-align:center;background-color:#f0f0f0">5205.42</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5212.4</td>
		<td style="text-align:center">100.45</td>
		<td style="text-align:center;background-color:#f0f0f0">7008.24</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10840.61</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5862.64</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4098.2</td>
		<td style="text-align:center">60.15</td>
		<td style="text-align:center;background-color:#f0f0f0">4196.57</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5271.0</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f0f0f0">4742.86</td>
		<td style="text-align:center">67.07</td>
		<td style="text-align:center;background-color:#f0f0f0">4679.37</td>
		<td style="text-align:center">174.55</td>
		<td style="text-align:center;background-color:#f0f0f0">12178.07</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-13</td>
		<td style="text-align:center">69.1795</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4329.28</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9190.27</td>
		<td style="text-align:center">90.67</td>
		<td style="text-align:center;background-color:#f0f0f0">6236.67</td>
		<td style="text-align:center">77.23</td>
		<td style="text-align:center;background-color:#f0f0f0">5312.21</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5138.88</td>
		<td style="text-align:center">100.42</td>
		<td style="text-align:center;background-color:#f0f0f0">6907.32</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10687.7</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5779.94</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4040.39</td>
		<td style="text-align:center">60.1</td>
		<td style="text-align:center;background-color:#f0f0f0">4133.94</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5196.65</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f0f0f0">4675.96</td>
		<td style="text-align:center">67.21</td>
		<td style="text-align:center;background-color:#f0f0f0">4622.99</td>
		<td style="text-align:center">171.34</td>
		<td style="text-align:center;background-color:#f0f0f0">11785.5</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-14</td>
		<td style="text-align:center">68.771</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4354.16</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9243.07</td>
		<td style="text-align:center">90.67</td>
		<td style="text-align:center;background-color:#f0f0f0">6272.51</td>
		<td style="text-align:center">77.23</td>
		<td style="text-align:center;background-color:#f0f0f0">5342.73</td>
		<td style="text-align:center">74.7</td>
		<td style="text-align:center;background-color:#f0f0f0">5167.71</td>
		<td style="text-align:center">100.42</td>
		<td style="text-align:center;background-color:#f0f0f0">6947.01</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10749.11</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5813.15</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4063.6</td>
		<td style="text-align:center">64.25</td>
		<td style="text-align:center;background-color:#f0f0f0">4444.78</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5226.51</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f0f0f0">4702.82</td>
		<td style="text-align:center">67.21</td>
		<td style="text-align:center;background-color:#f0f0f0">4649.55</td>
		<td style="text-align:center">171.34</td>
		<td style="text-align:center;background-color:#f0f0f0">11853.22</td>
	</tr>
</tbody>
"""
table2 = """
<tbody>
	<tr>
		<th style="text-align:center">Date</th>
		<th style="text-align:center">currency</th>
		<th colspan="2" style="text-align:center">Intel Core i5-9600KF 6 core (Hexa Core) CPU with 3.70 GHz</th>
		<th colspan="2" style="text-align:center">MSI Z390-A PRO</th>
		<th colspan="2" style="text-align:center">AMD Ryzen 5 3600 Tray</th>
		<th colspan="2" style="text-align:center">MSI B450-A PRO MAX</th>
		<th colspan="2" style="text-align:center">Ballistix Sport LT Rot 16GB DDR4 Kit (2x8GB) RAM</th>
		<th colspan="2" style="text-align:center">Crucial Ballistix Sport LT Rot 16GB DDR4 Kit RAM</th>
		<th colspan="2" style="text-align:center">Ballistix Sport LT Rot 16GB DDR4 RAM</th>
		<th colspan="2" style="text-align:center">G.Skill Ripjaws V 16GB DDR4 K2 16GVK RAM</th>
		<th colspan="2" style="text-align:center">G.Skill Ripjaws V 16GB DDR4 16GVK Kit RAM</th>
		<th colspan="2" style="text-align:center">be quiet! Pure Power 11 80+ Gold 600 Watt</th>
		<th colspan="2" style="text-align:center">Seasonic Core GC-650 80+ Gold 650 Watt</th>
		<th colspan="2" style="text-align:center">be quiet! Pure Power 11 80+ Gold 700 Watt</th>
		<th colspan="2" style="text-align:center">ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 512GB</th>
		<th colspan="2" style="text-align:center">ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 1TB</th>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-03</td>
		<td style="text-align:center">69.82</td>
		<td style="text-align:center">174.71</td>
		<td style="text-align:center;background-color:#f0f0f0">12198.71</td>
		<td style="text-align:center">89.08</td>
		<td style="text-align:center;background-color:#f0f0f0">6219.8</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10849.04</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5275.1</td>
		<td style="text-align:center">67.07</td>
		<td style="text-align:center;background-color:#f0f0f0">4683.0</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f0f0f0">4746.54</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4101.38</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5867.19</td>
		<td style="text-align:center">103.28</td>
		<td style="text-align:center;background-color:#f0f0f0">7211.28</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4394.63</td>
		<td style="text-align:center">60.29</td>
		<td style="text-align:center;background-color:#f0f0f0">4209.6</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5216.45</td>
		<td style="text-align:center">73.31</td>
		<td style="text-align:center;background-color:#f0f0f0">5118.69</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9329.0</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-04</td>
		<td style="text-align:center">69.74</td>
		<td style="text-align:center;color:red">171.93</td>
		<td style="text-align:center;background-color:#f0f0f0">11991.14</td>
		<td style="text-align:center;color:red">88.7</td>
		<td style="text-align:center;background-color:#f0f0f0">6186.32</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10836.87</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5269.18</td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4096.78</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5860.61</td>
		<td style="text-align:center">103.28</td>
		<td style="text-align:center;background-color:#f0f0f0">7203.19</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4389.71</td>
		<td style="text-align:center;color:red">59.96</td>
		<td style="text-align:center;background-color:#f0f0f0">4181.87</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5210.6</td>
		<td style="text-align:center;color:red">67.22</td>
		<td style="text-align:center;background-color:#f0f0f0">4688.21</td>
		<td style="text-align:center;color:red">128.49</td>
		<td style="text-align:center;background-color:#f0f0f0">8961.45</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-05</td>
		<td style="text-align:center">69.74</td>
		<td style="text-align:center">171.93</td>
		<td style="text-align:center;background-color:#f0f0f0">11991.14</td>
		<td style="text-align:center">88.7</td>
		<td style="text-align:center;background-color:#f0f0f0">6186.32</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10836.87</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5269.18</td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4096.78</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5860.61</td>
		<td style="text-align:center">103.28</td>
		<td style="text-align:center;background-color:#f0f0f0">7203.19</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4389.71</td>
		<td style="text-align:center">59.96</td>
		<td style="text-align:center;background-color:#f0f0f0">4181.87</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5210.6</td>
		<td style="text-align:center">67.22</td>
		<td style="text-align:center;background-color:#f0f0f0">4688.21</td>
		<td style="text-align:center">128.49</td>
		<td style="text-align:center;background-color:#f0f0f0">8961.45</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-10</td>
		<td style="text-align:center">69.63</td>
		<td style="text-align:center;color:green">174.71</td>
		<td style="text-align:center;background-color:#f0f0f0">12164.85</td>
		<td style="text-align:center;color:green">89.08</td>
		<td style="text-align:center;background-color:#f0f0f0">6202.53</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10818.92</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5260.46</td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center"></td>
		<td style="text-align:center;background-color:#f0f0f0"></td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4090.0</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5850.91</td>
		<td style="text-align:center">103.28</td>
		<td style="text-align:center;background-color:#f0f0f0">7191.26</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4382.44</td>
		<td style="text-align:center;color:green">60.34</td>
		<td style="text-align:center;background-color:#f0f0f0">4201.4</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5201.97</td>
		<td style="text-align:center;color:green">73.31</td>
		<td style="text-align:center;background-color:#f0f0f0">5104.49</td>
		<td style="text-align:center;color:green">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9303.1</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-11</td>
		<td style="text-align:center">69.77</td>
		<td style="text-align:center">174.71</td>
		<td style="text-align:center;background-color:#f0f0f0">12189.24</td>
		<td style="text-align:center;color:green">90.67</td>
		<td style="text-align:center;background-color:#f0f0f0">6325.9</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10840.61</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5271.0</td>
		<td style="text-align:center">67.07</td>
		<td style="text-align:center;background-color:#f0f0f0">4679.37</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f0f0f0">4742.86</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4098.2</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5862.64</td>
		<td style="text-align:center;color:red">100.45</td>
		<td style="text-align:center;background-color:#f0f0f0">7008.24</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4391.22</td>
		<td style="text-align:center;color:red">60.07</td>
		<td style="text-align:center;background-color:#f0f0f0">4190.99</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5212.4</td>
		<td style="text-align:center;color:green">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5212.4</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9321.76</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-12</td>
		<td style="text-align:center">68.78</td>
		<td style="text-align:center;color:red">174.55</td>
		<td style="text-align:center;background-color:#f0f0f0">12006.3</td>
		<td style="text-align:center">90.67</td>
		<td style="text-align:center;background-color:#f0f0f0">6236.67</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10687.7</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5196.65</td>
		<td style="text-align:center">67.07</td>
		<td style="text-align:center;background-color:#f0f0f0">4613.36</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f0f0f0">4675.96</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4040.39</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5779.94</td>
		<td style="text-align:center">100.45</td>
		<td style="text-align:center;background-color:#f0f0f0">6909.38</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4329.28</td>
		<td style="text-align:center;color:green">60.15</td>
		<td style="text-align:center;background-color:#f0f0f0">4137.38</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5138.88</td>
		<td style="text-align:center;color:red">74.61</td>
		<td style="text-align:center;background-color:#f0f0f0">5132.0</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9190.27</td>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-13</td>
		<td style="text-align:center">69.18</td>
		<td style="text-align:center;color:red">171.34</td>
		<td style="text-align:center;background-color:#f0f0f0">11853.22</td>
		<td style="text-align:center">90.67</td>
		<td style="text-align:center;background-color:#f0f0f0">6272.51</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f0f0f0">10749.11</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f0f0f0">5226.51</td>
		<td style="text-align:center;color:green">67.21</td>
		<td style="text-align:center;background-color:#f0f0f0">4649.55</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f0f0f0">4702.82</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f0f0f0">4063.6</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f0f0f0">5813.15</td>
		<td style="text-align:center;color:red">100.42</td>
		<td style="text-align:center;background-color:#f0f0f0">6947.01</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f0f0f0">4354.16</td>
		<td style="text-align:center;color:red">60.1</td>
		<td style="text-align:center;background-color:#f0f0f0">4157.69</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f0f0f0">5168.4</td>
		<td style="text-align:center;color:green">77.23</td>
		<td style="text-align:center;background-color:#f0f0f0">5342.73</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f0f0f0">9243.07</td>
	</tr>
</tbody>
"""
table3 = """
<tbody>
	<tr>
		<th style="text-align:center">Date</th>
		<th style="text-align:center">Currency</th>
		<th colspan="2" style="text-align:center">Intel Core i5-9600KF</th>
		<th colspan="2" style="text-align:center">AMD Ryzen 5 3600</th>
		<th colspan="2" style="text-align:center">ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 512GB</th>
		<th colspan="2" style="text-align:center">ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 1TB</th>
		<th colspan="2" style="text-align:center">G.Skill Ripjaws V 16GB DDR4 16GVK Kit RAM</th>
		<th colspan="2" style="text-align:center">G.Skill Ripjaws V 16GB DDR4 K2 16GVK RAM</th>
		<th colspan="2" style="text-align:center">Ballistix Sport LT Rot 16GB DDR4 RAM</th>
		<th colspan="2" style="text-align:center">Crucial Ballistix Sport LT Rot 16GB DDR4 Kit RAM</th>
		<th colspan="2" style="text-align:center">Ballistix Sport LT Rot 16GB DDR4 Kit (2x8GB) RAM</th>
		<th colspan="2" style="text-align:center">be quiet! Pure Power 11 80+ Gold 700 Watt</th>
		<th colspan="2" style="text-align:center">Seasonic Core GC-650 80+ Gold 650 Watt</th>
		<th colspan="2" style="text-align:center">be quiet! Pure Power 11 80+ Gold 600 Watt</th>
		<th colspan="2" style="text-align:center">MSI Z390-A PRO</th>
		<th colspan="2" style="text-align:center">MSI B450-A PRO MAX</th>
	</tr>
	<tr>
		<td style="text-align:center">2020-02-13</td>
		<td style="text-align:center">68.78</td>
		<td style="text-align:center">174.61</td>
		<td style="text-align:center;background-color:#f9f9f9">12010.43</td>
		<td style="text-align:center">155.38</td>
		<td style="text-align:center;background-color:#f9f9f9">10687.7</td>
		<td style="text-align:center">77.05</td>
		<td style="text-align:center;background-color:#f9f9f9">5299.83</td>
		<td style="text-align:center">133.61</td>
		<td style="text-align:center;background-color:#f9f9f9">9190.27</td>
		<td style="text-align:center">100.42</td>
		<td style="text-align:center;background-color:#f9f9f9">6907.32</td>
		<td style="text-align:center">84.03</td>
		<td style="text-align:center;background-color:#f9f9f9">5779.94</td>
		<td style="text-align:center">58.74</td>
		<td style="text-align:center;background-color:#f9f9f9">4040.39</td>
		<td style="text-align:center">67.98</td>
		<td style="text-align:center;background-color:#f9f9f9">4675.96</td>
		<td style="text-align:center">67.21</td>
		<td style="text-align:center;background-color:#f9f9f9">4622.99</td>
		<td style="text-align:center">74.71</td>
		<td style="text-align:center;background-color:#f9f9f9">5138.88</td>
		<td style="text-align:center">60.12</td>
		<td style="text-align:center;background-color:#f9f9f9">4135.31</td>
		<td style="text-align:center">62.94</td>
		<td style="text-align:center;background-color:#f9f9f9">4329.28</td>
		<td style="text-align:center">90.67</td>
		<td style="text-align:center;background-color:#f9f9f9">6236.67</td>
		<td style="text-align:center">75.55</td>
		<td style="text-align:center;background-color:#f9f9f9">5196.65</td>
	</tr>
</tbody>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CalcForm()
    if form.submit.data:
        conn = redis.Redis(db=1)
        prices_dict = rh.get_fresh_prices_dict(conn)
        conn.close()
        print('Pressed')
        check_chosen_products_list = [form.proc.data, form.mobo.data, form.psu.data, form.memory.data, form.ssd.data]
        products_chosen_list = []
        for product in check_chosen_products_list:
            if product:
                products_chosen_list.append(product[0])
        # products_chosen_list = [form.proc.data[0], form.mobo.data[0], form.psu.data[0], form.memory.data[0]]
        # form.ssd.data[0]]
        # print(f'{form.ssd.data}')

        print(products_chosen_list)
        order_table = OrderTable(prices_dict, products_chosen_list)
        table_html = order_table.create_html()
        flash(table_html)
        # print(f'{form.proc.data} --- {prices_dict.get(form.proc.data[0])}')
        # print(f'{form.mobo.data} --- {prices_dict.get(form.mobo.data[0])}')
        # print(f'{form.psu.data} --- {prices_dict.get(form.psu.data[0])}')
        # print(f'{form.memory.data} --- {prices_dict.get(form.memory.data[0])}')
        # print(f'{form.ssd.data} --- {prices_dict.get(form.ssd.data[0])}')
        # if form.ssd.data == ['ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 1TB']:
        #     flash(table2)
        # else:
        #     flash(table)
        # return redirect('/career')
    return render_template('calc_page.html', table=table, form=form)


@app.route('/career/')
def career():
    return 'Career Page'


@app.route('/feedback/')
def feedback():
    return 'Feedback Page'


@app.route('/user/<id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
