import json
import time
import random
import datetime

import requests
import sys

myurl_admin = "http://127.0.0.1:8000/admin/"
myurl = "http://127.0.0.1:8000/send-json/"
client = requests.session()
n = 1

# Retrieve CSRF token
client.get(myurl_admin) # sets cookie
csrftoken = client.cookies['csrftoken']

login_data = dict(username='', password='', csrfmiddlewaretoken=csrftoken, next='/')

while True:
    pollution = random.choice(["good", "average", "bad"])
    temperature = random.uniform(20, 28)
    humidity = random.randint(2000, 2100)
    collection_date = datetime.datetime.now()
    device = 1

    data = {
        "device" : device,
        "data" : {
            "collection_date" : collection_date,
            "pollution" : pollution,
            "temperature" : temperature,
            "humidity" : humidity
            }
    }

    # json.dumps(default=str) is "dirty" way to convert unindentified objects to string

    response = client.post(myurl, data=login_data)

    print("{0} packet send. Response: {1}" .format(n, response.text))

    #print("1 packet send." if n == 1 else "{0} packets send." .format(n))
    n += 1
    time.sleep(2)

