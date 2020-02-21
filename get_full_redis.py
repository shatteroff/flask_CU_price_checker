from config import Config

links_list_name = 'new_link'

conn = Config.conn
keys_list = conn.keys()
keys_list.sort()
print(keys_list)
for key in keys_list:
    key_str = bytes(key).decode("utf-8")
    if key_str != links_list_name:
        print(f'{key_str}' + ' {')
        key_dict = conn.hgetall(key)
        fields_list = list(key_dict.keys())
        for field in fields_list:
            name = bytes(key_dict[field]).decode("utf-8")
            link = bytes(field).decode("utf-8")
            print(f'\t{link} : {name}\n')
        print('}')
    else:
        items_list = conn.lrange(links_list_name, 0, -1)
        print(f'Waiting for price download:\n{items_list}')
