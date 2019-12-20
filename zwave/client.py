# importing the requests library
import configparser
import datetime
import os
import requests
import time
import sys

import mylogger

ZWAVE_URL = "http://localhost:8083"
ZWAVE_IP = "localhost"
ZWAVE_PORT = "8083"
ZAUTOMATION_URL = "/ZAutomation/api/v1/"
LOGIN = None

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
  mylogger.logger.debug("In Get_Data")
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
    r = requests.get(url=URL, auth=(LOGIN[0], LOGIN[1]))
    r.raise_for_status()
    # extracting data in json format
    resp = r.json()
    data = resp['data']
    mylogger.logger.debug("Data for device "+ id +" : "+ str(data))
    #print(sensor_to_string(data))
    return get_level_from_data(data)
  except (Exception) as err:
    mylogger.logger.error(err)
    print("Error caught : Please check logs.")
    sys.exit(1)

def get_devices(ip=None, port=None):
  mylogger.logger.debug("In Get_Devices")
  if ip == None:
    ip = ZWAVE_IP
  if port == None:
    port = ZWAVE_PORT

  # api-endpoint
  URL = "http://" + ip + ":" + port + "/ZAutomation/api/v1/devices"
  # defining a params dict for the parameters to be sent to the API
  PARAMS = {}
  devices = []
  try:
    # sending get request and saving the response as response object
    r = requests.get(url=URL, auth=(LOGIN[0], LOGIN[1]))
    r.raise_for_status()
    # extracting data in json format
    resp = r.json()
    devices = resp['data']['devices']
    mylogger.logger.debug("Devices : "+ str(devices))
  except (Exception) as err:
    mylogger.logger.error(err)
    print("Error caught : Please check logs.")
    sys.exit(1)

  return devices

def reset_sensor(id, metrics,ip=None, port=None):
  mylogger.logger.debug("In Reset_Sensor")
  if ip == None:
    ip = ZWAVE_IP
  if port == None:
    port = ZWAVE_PORT

    # api-endpoint
    URL = "http://" + ip + ":" + port + "/JS/Run/this.controller.devices.get(%22"+id+"%22).set(%22metrics:"+metrics+"%22,0)"
  try:
    requests.get(url=URL, auth=(LOGIN[0], LOGIN[1]))
    mylogger.logger.debug("Capteur "+ id + " remis à 0")
    print("Capteur "+ id + " remis à 0")
  except (Exception) as err:
    mylogger.logger.error(err)
    print("Error caught : Please check logs.")
    sys.exit(1)

def get_login():
  filepath = os.path.abspath("./properties.ini")
  print(filepath)
  if not os.path.isfile(filepath):
    print("[Get Login] File path {} does not exist. Exiting...".format(filepath))
    mylogger.logger.debug("[Get Login] File path {} does not exist. Exiting...".format(filepath))
    sys.exit(1)

  config = configparser.ConfigParser()
  config.read(filepath)
  user = config.get('LOGIN', 'User')
  passwd = config.get('LOGIN', 'Passwd')
  return user,passwd

if(LOGIN == None):
  LOGIN = get_login()