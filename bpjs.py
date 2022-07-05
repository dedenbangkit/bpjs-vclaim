import sys
import os
import lzstring
import requests
import hashlib
import base64
import hmac
import json
from Crypto.Cipher import AES
from datetime import datetime

is_valid = 1
for a in ["VCLAIM_ID", "SECRET_ID", "USER_KEY", "SERVICE_URL", "REST_URL"]:
    if not os.environ.get(a):
        is_valid = 0
        print(f"NOT FOUND: {a}")

if not is_valid:
    exit(1)

VCLAIM_ID = os.environ["VCLAIM_ID"]
SECRET_ID = os.environ["SECRET_ID"]
USER_KEY = os.environ["USER_KEY"]
SERVICE_URL = os.environ["SERVICE_URL"]
REST_URL = os.environ["REST_URL"]


def decrypt_data(keys, encrypts):
    decompress = None
    if encrypts:
        x = lzstring.LZString()
        key_hash = hashlib.sha256(keys.encode('utf-8')).digest()
        decryptor = AES.new(key_hash[0:32], AES.MODE_CBC, IV=key_hash[0:16])
        plain = decryptor.decrypt(base64.b64decode(encrypts))
        decompress = json.loads(
            x.decompressFromEncodedURIComponent(plain.decode('utf-8')))
    return json.dumps(decompress)


def rest_bpjs(url):
    timestamp = str(int(datetime.today().timestamp()))
    message = f"{VCLAIM_ID}&{timestamp}"
    signature = hmac.new(bytes(SECRET_ID, 'UTF-8'), bytes(message, 'UTF-8'),
                         hashlib.sha256).digest()
    encodeSignature = base64.b64encode(signature)
    headers = {
        'X-cons-id': f"{VCLAIM_ID}",
        'X-timestamp': timestamp,
        'X-signature': encodeSignature.decode('UTF-8'),
        'user_key': USER_KEY,
        'Content-Type': 'Application/x-www-form-urlencoded',
        'Accept': '*/*'
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return json.dumps({
            "status_code": res.status_code,
            "message": "Invalid URL"
        })
    if res.status_code == 200:
        try:
            res = res.json()
            keys = f"{VCLAIM_ID}{SECRET_ID}{timestamp}"
            return decrypt_data(keys, res["response"])
        except ValueError:
            pass
    return res.text


REST_URL = f"{SERVICE_URL}/{REST_URL}/"
if len(sys.argv) > 1:
    REST_URL = f"{REST_URL}/{sys.argv[1]}"

res = rest_bpjs(REST_URL)
print(res)
