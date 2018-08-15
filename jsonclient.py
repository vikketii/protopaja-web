import json
import time
import random
import datetime

import requests
import sys


# typo fixed in the url
myurl = "http://127.0.0.1:8000/send-json/"
client = requests.session()
n = 1
temperature = 20
humidity = 50
dust = 50


# Retrieve CSRF token, this doesn't seem to work
# client.get("http://127.0.0.1:8000/admin") # sets cookie
# csrftoken = client.cookies['csrftoken']

#login_data = dict(username='testi', password='prototesti', csrfmiddlewaretoken=csrftoken, next='/')

while True:
    dust += random.randint(-2,2)
    temperature += random.randint(-1, 1)
    humidity += random.randint(-3, 3)
    light = random.randint(0, 10)
    collection_date = datetime.datetime.now()
    device_id = '1'


    #json object, didn't get inner json working -> only 1 json
    data = {
        "username": 'testi',
        "password" : 'prototesti',
        #"csrfmiddlewaretoken" : csrftoken,
        "device_id" : device_id,
        "collection_date" : collection_date,
        "temperature" : temperature,
        "humidity" : humidity,
        "dust" : dust,
        "light" : light,

    }
    header = {'content-type': 'application/json'}

    # json.dumps(default=str) is "dirty" way to convert unindentified objects to string

    response = client.post(myurl, data=data)

    # response content is human readable whereas response itself is messy
    print("{0}. packet send. Response (first 40 char): {1}" .format(n, response.content[:40]))

    n += 1
    time.sleep(2)
