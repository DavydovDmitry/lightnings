from thunder_finder.upload_thunders import upload_thunders_db
from thunder_finder.upload_thunders import upload_thunders_json
from instagram.upload_lightnings_db import upload_lightnings_db
from map.map import build_map

"""
if __name__ == "__main__":
    while True:
        try:
            min_quantity = int(input('min_quantity: '))
            break
        except ValueError as value_error:
            print('Enter number...')
    upload_lightnings_db(min_quantity=min_quantity)
"""

if __name__ == "__main__":
    upload_thunders_json()
    upload_thunders_db()
    upload_lightnings_db(min_quantity=100, limit=50)
    build_map()