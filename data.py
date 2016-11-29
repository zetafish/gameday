import json
import base64

data = {
    'Id': 'eko-1',
    'TotalNumber': 4,
    'PartNumber': 0,
    'Data': 'hello'
}


print base64.b64encode(json.dumps(data))
