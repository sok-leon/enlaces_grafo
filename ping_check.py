from ping3 import ping
import json
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor


def ping_device(hostname) -> bool:
    try:
        response = ping(hostname, timeout=1)
        if response is not None:
            return True
    except KeyboardInterrupt:
        return False
      

def valid(device: dict) -> tuple:

    name = device.get("name", "Unknown")
    id = device["id"]
    prevous_status = False

    for interface  in device["interfaces"]:
        ip = interface["ip"]
        status = ping_device(ip)

        if not status:
            status = ping_device(ip)
            prevous_status = True
        
        if prevous_status and not status:
            message = f"❌ {name} ({ip}) está caído."
            state = "down"

        elif status:
            message = f"✅ {name} ({ip}) activo."
            state = "up"
        
        interface["status"]= state
        state = None
        #print (message)            
    
    return device


def load_devices_from_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data['devices']
    

def get_json_status():

    results = []
    devices = load_devices_from_json("test.json")
    with ThreadPoolExecutor(max_workers=20) as executor:
            for device  in map(lambda d: valid(d), devices ):
                results.append(device)



    # results = []
    # devices = load_devices_from_json("test.json")
    # for device in devices:
        
    #     results.append(valid(device))

    #return json.dumps(results, indent=4)
    return results


# if __name__ == "__main__":
#     # devices = load_devices_from_json("test.json")
#     # #print (devices)
#     # for device in devices:
#     #     print (valid(device))
#     # #    print ( valid(device))

#     last_status = {}
#     results = []
#     devices = load_devices_from_json("test.json")
#     with ThreadPoolExecutor(max_workers=15) as executor:
#             for device  in map(lambda d: valid(d), devices ):
#                 results.append(device)
#     print( json.dumps(results, indent=4))