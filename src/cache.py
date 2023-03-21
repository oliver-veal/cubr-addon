import bpy
import os
import json


class Cache:
    CACHE_FILE = os.path.join(
        bpy.utils.user_resource('SCRIPTS', path="cubr_cache", create=True),
        ".cache"
    )

    def read():
        if not os.path.exists(Cache.CACHE_FILE):
            return {}
        with open(Cache.CACHE_FILE, "rb") as f:
            data = f.read().decode('utf-8')
            return json.loads(data)

    def get_key(key):
        cache_data = Cache.read()
        if key in cache_data:
            return cache_data[key]

    def save_key(key, value):
        cache_data = Cache.read()
        cache_data[key] = value
        with open(Cache.CACHE_FILE, 'wb+') as f:
            f.write(json.dumps(cache_data).encode('utf-8'))

    def delete_key(key):
        cache_data = Cache.read()
        if key in cache_data:
            del cache_data[key]

        with open(Cache.CACHE_FILE, 'wb+') as f:
            f.write(json.dumps(cache_data).encode('utf-8'))
