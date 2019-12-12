# importing the requests library
import requests
import time
import datetime


def to_string(data):
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
  URL = "http://192.168.43.100:8083/ZAutomation/api/v1/devices/"+id
  # defining a params dict for the parameters to be sent to the API
  PARAMS = {}

  # sending get request and saving the response as response object
  r = requests.get(url=URL, auth=('admin', 'adminadmin'))

  # extracting data in json format
  resp = r.json()
  data = resp['data']
  print(to_string(data))