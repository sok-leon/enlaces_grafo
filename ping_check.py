from ping3 import ping
import json
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor


def ping_device(hostname) -> bool:
    try:
        response = ping(hostname, timeout=3)
        if response is not None:
            return True
    except KeyboardInterrupt:
        return False
      

def valid(device: dict) -> tuple:

    name = device.get("name", "Unknown")
    ip = device["ip"]
    neighbors = device["neighbors"]
    prevous_status = False
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
    
    #send_telegram_alert(message)
    return name, ip, state,  neighbors


def load_devices_from_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data['devices']
    

def get_json_status():

    last_status = {}
    results = []
    devices = load_devices_from_json("test.json")

    with ThreadPoolExecutor(max_workers=5) as executor:
            for name, ip, status, neighbors  in map(lambda d: valid(d), devices ):
                prev_status = last_status.get(name)
                if prev_status != status:  
                    last_status[name] = status
                    print (">>", name, "enviao alerta", status)

                    results.append({
                            "name": name,
                            "ip": ip,
                            "status": status,
                            "neighbors": neighbors
                        })
    print (results)
    return json.dumps(results, indent=4)
    #return results


# if __name__ == "__main__":
#     devices = load_devices_from_json("test.json")
#     for device in devices:
#         print ( valid(device))