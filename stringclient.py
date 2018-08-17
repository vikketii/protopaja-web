import json
import time
import random
import datetime

import requests
import sys


# typo fixed in the url
#myurl = "http://192.168.100.44:80/send-json/"
myurl = "http://127.0.0.1:8000/send_string/"
client = requests.session()
n = 1



while True:
    dust = random.randint(40,90)
    temperature = random.randint(20, 40)
    humidity = random.randint(50, 70)
    light = random.randint(0,9)
    device_id = str(random.randint(1,3))
    volts = random.uniform(3,4)
    #device_id = '2'

    

    data = "username: testi, password:prototesti, device_id:"+ device_id + ", temp:" + str(temperature) + ",humd:" + str(humidity) + ",dust:" + str(dust) +",light:" + str(light) + ", volts:" +str(volts)
    
    
    # json.dumps(default=str) is "dirty" way to convert unindentified objects to string

    response = client.post(myurl, data=data)

    # response content is human readable whereas response itself is messy
    print("{0}. packet send. Response (first 40 char): {1}" .format(n, response.content[:40]))

    n += 1
    time.sleep(20)