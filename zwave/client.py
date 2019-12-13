# importing the requests library
import requests
import time
import datetime

ZWAVE_URL = "http://192.168.43.99:8083"
ZAUTOMATION_URL = "/ZAutomation/api/v1/"

def sensor_to_string(data):
  creation_timestamp = datetime.datetime.fromtimestamp(data['creationTime'])
  creation_time = creation_timestamp.strftime("%x %X")
  update_timestamp = datetime.datetime.fromtimestamp(data['updateTime'])
  update_time = update_timestamp.strftime("%x %X")
  metrics = data['metrics']
  title = metrics["title"]
  level = metrics["level"]
  scale = metrics["scaleTitle"]
  return f'[{update_time}] - {title} : {level} {scale}'


def get_data(id):
  # api-endpoint
  URL = ZWAVE_URL + ZAUTOMATION_URL + "devices/" + id
  # defining a params dict for the parameters to be sent to the API
  PARAMS = {}
  try:
    # sending get request and saving the response as response object
    r = requests.get(url=URL, auth=('admin', 'adminadmin'))
    r.raise_for_status()
    # extracting data in json format
    resp = r.json()
    data = resp['data']
    print(sensor_to_string(data))
  except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
  except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
  except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
  except requests.exceptions.RequestException as err:
    print("OOps: Something Else", err)


def get_devices():
  # api-endpoint
  URL = ZWAVE_URL + ZAUTOMATION_URL + "devices"
  # defining a params dict for the parameters to be sent to the API
  PARAMS = {}
  devices = []
  try:
    # sending get request and saving the response as response object
    r = requests.get(url=URL, auth=('admin', 'adminadmin'))
    r.raise_for_status()
    # extracting data in json format
    resp = r.json()
    devices = resp['data']['devices']
  except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
  except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
  except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
  except requests.exceptions.RequestException as err:
    print("OOps: Something Else", err)

  return devices

def reset_sensor(id, metrics, value):
  URL = ZWAVE_URL + "/JS/Run/this.controller.devices.get(%22"+id+"%22).set(%22metrics:"+metrics+"%22,"+value+")"
  try:
    requests.get(url=URL, auth=('admin', 'adminadmin'))
  except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
  except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
  except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
  except requests.exceptions.RequestException as err:
    print("OOps: Something Else", err)