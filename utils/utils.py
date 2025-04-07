import random

import requests


def create_random_code(size:int):
    var = ''
    for item in range(0, size):
        var += str(random.choice(range(0, 10)))
    return var

def send_sms(recipients, code):
    response = requests.get(url=f'http://ippanel.com/class/sms/webservice/send_url.php?from=fromnumber&to=yourtdestnumber&msg=yourmsg&uname=youruname&pass=yourpass')