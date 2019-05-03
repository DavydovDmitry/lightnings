import json

import requests


if __name__ == "__main__":
    response = requests.get('http://www.lightnings.ru/vr44_24.php')
    content = response.content.replace(b'rs', b'"rs"')
    with open('./output/responce.txt', 'wb') as output:
        output.write(content)

    max_longitude = -180.0
    max_latitude = -90.0
    min_longitude = 180.0
    min_latitude = 90.0
    for item in json.loads(content)['rs']:
        max_t = max(map(float, [item['p1t'], item['p2t'], item['p3t'], item['p4t']]))
        max_n = max(map(float, [item['p1n'], item['p2n'], item['p3n'], item['p4n']]))
        if max_t > max_longitude: max_longitude = max_n
        if max_n > max_latitude: max_latitude = max_t

        min_t = min(map(float, [item['p1t'], item['p2t'], item['p3t'], item['p4t']]))
        min_n = min(map(float, [item['p1n'], item['p2n'], item['p3n'], item['p4n']]))
        if min_t < min_longitude: min_longitude = min_n
        if min_n < min_latitude: min_latitude = min_t
    print(min_latitude, '< latitude < ', max_latitude)
    print(min_longitude, '< longitude < ', max_longitude)