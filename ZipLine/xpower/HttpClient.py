import requests

url = 'http://192.168.1.129:8000/a/b/c'
req = requests.get(url)

for line in req.iter_lines():
    print(repr(line))
    
    