import random

import requests


def create_random_code(size: int):
    var = ''
    for item in range(0, size):
        var += str(random.choice(range(0, 10)))
    return var


def send_sms(recipients, code):
    response = requests.post(url="https://api2.ippanel.com/api/v1/sms/pattern/normal/send", headers={
        'apikey': "OWU4MWYyY2MtMDI4OS00OTg4LWI1YjctZjA0Mzg2NjllOGEzYzExMzU0YzAwYmUwNzJlYWQ4MjI5ZGQ3ZGRkNTg1M2Q=",
        'Content-Type': 'application/json'
    }, json={
        "code": "fqmt1275wjd02wg",
        "sender": "+983000505",
        "recipient": recipients,
        "variable": {
            "verification-code": code,
        }
    })
    return response
