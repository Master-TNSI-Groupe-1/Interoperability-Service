# importing the requests library
import datetime
import requests
import time
import sys

import mylogger

ZWAVE_URL = "http://192.168.43.99:8083"
ZWAVE_IP = "192.168.43.99"
ZWAVE_PORT = "8083"
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

def get_level_from_data(data):
  metrics = data['metrics']
  return metrics["level"]


def get_data(id, ip=None, port=None):
  if ip == None:
    ip = ZWAVE_IP
  if port == None:
    port = ZWAVE_PORT
  # api-endpoint
  URL = "http://" + ip + ":" + port + "/ZAutomation/api/v1/devices/" + id
  # defining a params dict for the parameters to be sent to the API
  PARAMS = {}
  try:
    # sending get request and saving the response as response object
    r = requests.get(url=URL, auth=('admin', 'adminadmin'))
    r.raise_for_status()
    # extracting data in json format
    resp = r.json()
    data = resp['data']
    # print(sensor_to_string(data))
    return get_level_from_data(data)
  except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
  except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
  except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
  except requests.exceptions.RequestException as err:
    print("OOps: Something Else", err)
    print(sensor_to_string(data))
  except (Exception) as err:
    mylogger.logger.error(err)
    sys.exit(1)

def get_devices(ip=None, port=None):
  if ip == None:
    ip = ZWAVE_IP
  if port == None:
    port = ZWAVE_PORT

  print(ip)
  print(port)
  # api-endpoint
  URL = "http://" + ip + ":" + port + "/ZAutomation/api/v1/devices"
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
  except (Exception) as err:
    mylogger.logger.error(err)
    sys.exit(1)

  return devices

def reset_sensor(id, metrics, value):
  URL = ZWAVE_URL + "/JS/Run/this.controller.devices.get(%22"+id+"%22).set(%22metrics:"+metrics+"%22,"+value+")"
  try:
    requests.get(url=URL, auth=('admin', 'adminadmin'))
  except (Exception) as err:
    mylogger.logger.error(err)
    sys.exit(1)