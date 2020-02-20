import redis


eq_set = {'currency', 'Ballistix Sport LT Rot 16GB DDR4 Kit (2x8GB) RAM', 'ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 1TB', 'Crucial Ballistix Sport LT Rot 16GB DDR4 Kit RAM', 'MSI B450-A PRO MAX', 'MSI Z390-A PRO', 'ADATA XPG SX8200 Pro M.2 NVME PCIe Gen3x4 512GB', 'be quiet! Pure Power 11 80+ Gold 600 Watt', 'be quiet! Pure Power 11 80+ Gold 700 Watt', 'Ballistix Sport LT Rot 16GB DDR4 RAM', ' Intel Core i5-9600KF 6 core (Hexa Core) CPU with 3.70 GHz', 'G.Skill Ripjaws V 16GB DDR4 16GVK Kit RAM', 'G.Skill Ripjaws V 16GB DDR4 K2 16GVK RAM', 'G.Skill Ripjaws V 16GB DDR4 K2 16GVK RAM ', ' be quiet! Pure Power 11 80+ Gold 700 Watt', 'Seasonic Core GC-650 80+ Gold 650 Watt', 'Intel Core i5-9600KF 6 core (Hexa Core) CPU with 3.70 GHz', 'AMD Ryzen 5 3600 Tray'}
product_names = []
product_set = set()
conn = redis.Redis()
keys_list = conn.keys()
keys_list.sort()
print(keys_list)
for i, key in enumerate(keys_list):
    print((conn.hgetall(key)))
    product_names = product_names + list(conn.hgetall(key).keys())

for name in product_names:
    product = bytes(name).decode("utf-8")

    product_set.add(product)

print(product_names)
print(product_set)
print(len(product_set))




