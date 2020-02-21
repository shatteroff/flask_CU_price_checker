import redis


def check_db_keys():
    conn = redis.Redis(db=1)
    keys_list = conn.keys()
    keys_list.sort()
    print(keys_list)
    return keys_list


def check_full_db():
    conn = redis.Redis(db=1)
    for key in check_db_keys():
        key_str = bytes(key).decode("utf-8")
        print(f'{key_str}' + ' {')
        key_dict = conn.hgetall(key)
        fields_list = list(key_dict.keys())
        for field in fields_list:
            name = bytes(key_dict[field]).decode("utf-8")
            link = bytes(field).decode("utf-8")
            print(f'\t{link} : {name}\n')
        print('}')


def delete_full_db():
    conn = redis.Redis(db=1)
    keys_list = conn.keys()
    for key in keys_list:
        conn.delete(key)


def delete_one_key(name):
    conn = redis.Redis(db=1)
    conn.delete(name)


def read_list(list_key):
    conn = redis.Redis(db=1)
    items_list = conn.lrange(list_key, 0, -1)
    print(items_list)


delete_one_key('new_link')

check_db_keys()

# delete_one_key("new_link")
# read_list("new_link")

# delete_full_db()
# delete_one_key('2020-02-14')
# check_full_db()
