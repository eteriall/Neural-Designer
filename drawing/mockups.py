from time import sleep

from requests import get, post
import base64

key = 'k9hrbe0y-p0hd-urrj:eke4-lzuxt9js5zae'
key = base64.b64encode(bytes(key, 'utf-8'))
keyDecoded = key.decode('ascii')
header = {'Authorization': 'Basic ' + keyDecoded}


def get_task_key(link):
    json = {
        "variant_ids": [4012],
        "format": "png",
        "files": [
            {
                "placement": "front",
                "image_url": link,
                "position": {
                    "area_width": 1800,
                    "area_height": 2400,
                    "width": 1800,
                    "height": 1800,
                    "top": 300,
                    "left": 0
                }
            }
        ]
    }
    data = post("https://api.printful.com/mockup-generator/create-task/71", headers=header, json=json).json()
    if data['code'] != 200:
        return None
    task_key = data['result']['task_key']
    return task_key


def parse_mockups(data):
    if data['code'] != 200 or data['result']['status'] != 'completed':
        return None
    return list(map(lambda x: x['url'], data['result']['mockups'][0]['extra']))


def get_mockups(task_key):
    data = get(f"https://api.printful.com/mockup-generator/task?task_key={task_key}", headers=header).json()
    if data['code'] != 200 or data['result']['status'] != 'completed':
        return None
    return data


task_key = get_task_key(
    "https://i.ibb.co/w0hn3K0/3-1.png")

while True:
    data = get_mockups(task_key)
    sleep(1)
    if data is not None:
        break
print(*parse_mockups(data), sep='\n')
