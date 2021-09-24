import requests
import datetime
import time
from tqdm import tqdm
import json

# from pprint import pprint

url = 'https://api.vk.com/method/photos.get'
params = {'user_id': '552934290',
          'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
          'v': '5.131', 'album_id': 'profile', 'extended': '1', 'photo_sizes': '1'}
res = requests.get(url, params=params)
# pprint(res.json())


token_ya = ''


def _headers():
    return {'Content-type': 'application/json', 'Authorization': 'OAuth {}'.format(token_ya)}


def put_folder(path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'
    headers = _headers()
    params = {'path': path, 'url': url}
    requests.put(url, headers=headers, params=params)
    return path


def post_file(file_url, file_name):
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = _headers()
    params = {'path': f'/{file_name}', 'url': file_url}
    response = requests.post(upload_url, headers=headers, params=params)
    return response.json()


folder_name = put_folder(input("введите имя папки для загрузки фотографий: "))
name_list = []
data = []
size_list = []

for photos in tqdm(res.json()['response']['items']):

    sizes = photos['sizes']

    for picture in sizes:
        size_list.append(picture['type'])
        size_list.sort(reverse=True)

    for picture1 in sizes:
        data_dict = {}
        if picture1['type'] == size_list[0]:
            href = picture1['url']
            filename = photos['likes']['count']
            if filename in name_list:
                filename = f"{photos['likes']['count']}+{datetime.datetime.fromtimestamp(photos['date']).isoformat().replace(':', '|')}"
                post_file(href, f"{folder_name}/{filename}")
                data_dict['file_name'] = filename
                data_dict['size'] = picture1['type']


            else:
                post_file(href, f"{folder_name}/{filename}")
                data_dict['file_name'] = filename
                data_dict['size'] = picture1['type']
            data.append(data_dict)

    name_list.append(filename)
    size_list.clear()

    time.sleep(1)
with open('foto.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
