import json
import time
import random
import datetime
import urllib.request

myurl = "http://127.0.0.1:8000/devicedata/"
n = 1

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
    json_string = json.dumps(data, indent=4, sort_keys=True, default=str)
    json_as_bytes = json_string.encode('utf-8') # needs to be bytes
    """
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')

    req.add_header('Content-Length', len(json_as_bytes))
    response = urllib.request.urlopen(req, json_as_bytes)

    print("{0} packet send. Response: {1}" .format(n, response))
    """
    print("1 packet send." if n == 1 else "{0} packets send." .format(n))
    n += 1
    time.sleep(2)

