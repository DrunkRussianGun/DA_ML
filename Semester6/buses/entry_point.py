import json
import requests

bus_data = requests.get("http://data.kzn.ru:8082/api/v0/dynamic_datasets/bus.json").content
bus_json = json.loads(bus_data)
print(bus_json)