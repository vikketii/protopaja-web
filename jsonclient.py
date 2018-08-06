import json
import time
import random
import datetime

import requests
import sys


# typo fixed in the url
myurl = "http://167.99.139.198/send-json/"
client = requests.session()
n = 1

# Retrieve CSRF token, this doesn't seem to work
# client.get("http://127.0.0.1:8000/admin") # sets cookie
# csrftoken = client.cookies['csrftoken']

#login_data = dict(username='testi', password='prototesti', csrfmiddlewaretoken=csrftoken, next='/')

while True:
    pollution = random.choice(["good", "average", "bad"])
    temperature = random.randint(20, 28)
    humidity = random.randint(2000, 2100)
    collection_date = datetime.datetime.now()
    device_id = '1'


    #json object, didn't get inner json working -> only 1 json
    data = {
        "username": 'testi',
        "password" : 'prototesti',
        #"csrfmiddlewaretoken" : csrftoken,
        "device_id" : device_id,
        "collection_date" : collection_date,
        "pollution" : pollution,
        "temperature" : temperature,
        "humidity" : humidity

    }
    header = {'content-type': 'application/json'}

    # json.dumps(default=str) is "dirty" way to convert unindentified objects to string

    response = client.post(myurl, data=data)

    # response content is human readable whereas response itself is messy
    print("{0}. packet send. Response (first 40 char): {1}" .format(n, response.content[:40]))

    n += 1
    time.sleep(2)
