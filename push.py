import json
import requests

endpoint = 'http://localhost:5000/'

headers = {
    'Content-type': 'application/json'
}

def make_data(id, total, num):
    return {
        'Id': 'id-%s' % id,
        'Data': '[%s-%s]' % (id, num),
        'TotalNumbers': total,
        'PartNumber': num
    }

def push(id, total):
    for i in range(total):
        part = json.dumps(make_data(id, total, i))
        requests.post(endpoint, data=part, headers=headers)


for i in range(10):
    push(i, 2)
