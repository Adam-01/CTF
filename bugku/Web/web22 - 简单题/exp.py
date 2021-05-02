import requests
import base64

session = requests.Session()

cookies = {
    'PHPSESSID': 'i6qvcr067dve40nrmavoevjo05'
}

res = session.get('http://114.67.246.176:17590/', cookies=cookies)

flag = base64.b64decode(res.headers['flag'])[-8:]
flag = base64.b64decode(flag)
print(flag)

data = {
    'margin': flag
}

res2 = session.post('http://114.67.246.176:17590/', cookies=cookies, data=data)

print(res2.text)


