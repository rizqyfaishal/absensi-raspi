import csv
import time
from bluetooth import *
import requests
import json
from sets import set


while True:
    print ""
    print "..Searching.." + time.strftime("%a, %d %b %Y %H:%M:%S")

    nearby_devices = discover_devices(lookup_names = True)
    mac_address = [addr for addr,name in nearby_devices]

    # for ma in mac_address:
    #     mac_address_store.add(ma)

    print "found %d devices" % len(nearby_devices)
    response = requests.request("POST", "http://absensikampus.herokuapp.com/absensi/forward-data",
        data=json.dumps({"mac_address":mac_address, "ruangan":"K301", "timestamp_raspi": str(int(time.time()))}))

    print(response.text)

    # if response.status == 200:
    #     data = json.loads(response.text)
    #     temp = set()
    #     for ma in data:
    #         temp.add(ma)
    #     mac_address_store = mac_address_store.difference_update(temp)

    for addr, name in nearby_devices:   
        print " %s - %s" % (addr, name)

    time.sleep(1)
