#!/usr/bin/env python

import os
import signal
import sys
assert sys.version_info > (3, 5), "Python is dead, long live Python!" \
                                  " (please use Python 3.5+)"

import argparse, configparser
import client, printer

import mylogger

def handle_sensor(args):
  mylogger.logger.debug("In Handle_Sensor")
  if(args.role == "printer" or args.role == "reset"):
    devices = client.get_devices(args.ip, args.port)
    device = None
    for de in devices:
      if (de['id'] == args.id):
        device = de
    if device == None:
      mylogger.logger.debug("Capteur inexistant ou impossible à trouver.")
      return False
    else:
      mylogger.logger.debug("Capteur trouvé [" + device['id'] + "].")
      return True
  else:
    return True

def handle_printer(args):
  mylogger.logger.debug("In Handle_Printer")
  my_sensor_printer = printer.Printer(args.id, 0, args.ip, args.port)
  my_sensor_printer.start()
  try:
    while 1:
      time.sleep(.01)
  except Exception as err:
    my_sensor_printer.join()
    print("Exit")

def handle_reset(args):
  mylogger.logger.debug("In Handle_Reset")
  client.reset_sensor(args.id, args.metrics, args.ip, args.port)

def handle_list(args):
  mylogger.logger.debug("In Handle_List")
  devices = client.get_devices(args.ip, args.port)
  print("Devices ID : ")
  for d in devices:
   print(d['id'])
  print("   ")


def handle_file(args):
  mylogger.logger.debug("In Handle_File")
  filepath = args.path
  if not os.path.isfile(filepath):
    print("File path {} does not exist. Exiting...".format(filepath))
    sys.exit()

  with open(filepath) as file:
    # print("Liste des capteurs :")
    devices = client.get_devices(args.ip, args.port)
    for line in file:
      device = None
      filedevice = format(line).split()[0]
      deviceid = format(line).split()[1]
      # print("DEVICE : " + filedevice)
      # print("DEVICE ID : " + deviceid)
      # filedevice = format(line).replace('\n', '').replace('\r', '')
      for de in devices:
        if (de['id'] == filedevice):
          device = de

      if device == None:
        mylogger.logger.error("Capteur [" + filedevice + "] inexistant ou impossible à trouver.")
      else:
        mylogger.logger.debug("Capteur trouvé [" + filedevice + "].")
        my_sensor_printer = printer.Printer(filedevice, deviceid, args.ip, args.port)
        my_sensor_printer.start()

def signal_handler(signal, frame):
  print('\nVous avez quitté le programme ! ')
  try:
    sys.exit(0)
  except SystemExit:
    os._exit(0)

def main():
  signal.signal(signal.SIGINT, signal_handler)
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help="role", dest="role", required=False)
  parser.add_argument('-d', '--debug', action='store_true')
  parser.add_argument('-a', '--api')

  router_parser = subparsers.add_parser("printer")
  router_parser.add_argument("id", help="Veuillez entrer l'id d'un capteur.")
  router_parser.add_argument("-i","--ip", help="Veuillez entrer l'ip du réseaux", required=False)
  router_parser.add_argument("-p","--port", help="Veuillez entrer le port du réseaux", required=False)

  router_parser = subparsers.add_parser("reset")
  router_parser.add_argument("id", help="Veuillez entrer l'id d'un capteur.")
  router_parser.add_argument("metrics", help="Veuillez entrer la mesure à réinitialiser")
  router_parser.add_argument("-i","--ip", help="Veuillez entrer l'ip du réseaux", required=False)
  router_parser.add_argument("-p","--port", help="Veuillez entrer le port du réseaux", required=False)

  router_parser = subparsers.add_parser("file")
  router_parser.add_argument("--path", help="Veuillez entrer le nom d'un fichier contentant les ids des capteurs.", required=False)
  router_parser.add_argument("-i", "--ip", help="Veuillez entrer l'ip du réseaux", required=False)
  router_parser.add_argument("-p", "--port", help="Veuillez entrer le port du réseaux", required=False)

  router_parser = subparsers.add_parser("list")
  router_parser.add_argument("-i","--ip", help="Veuillez entrer l'ip du réseaux", required=False)
  router_parser.add_argument("-p","--port", help="Veuillez entrer le port du réseaux", required=False)

  args = parser.parse_args()
  print(args)
  setup_config(args)
  print(args)
  mylogger.setup_logger(args.debug)
  args = setup_config(args)

  mylogger.logger.debug("Args : " + str(args))
  mylogger.logger.debug("Python %s", sys.version.replace('\n', ''))
  mylogger.logger.debug("IP : %s, Port : %s", args.ip, args.port )
  function_name = "handle_" + ("file" if args.role == None else args.role)
  mylogger.logger.debug("Calling %s()", function_name)

  if(handle_sensor(args)):
    globals()[function_name](args)

def setup_config(args):
  config = configparser.ConfigParser()
  config.read("properties.ini")
  if(args.role == None):
      args.ip = config.get('CONFIG', 'IP')
      args.port = config.get('CONFIG', 'Port')
      args.path = config.get('CONFIG', 'File')

  if (args.role == "printer" or args.role == "reset" or args.role == "list"):
    if (args.ip == None):
      args.ip = config.get('CONFIG', 'IP')
    if (args.port == None):
      args.port = config.get('CONFIG', 'Port')

  if (args.role == "file"):
    if (args.ip == None):
      args.ip = config.get('CONFIG', 'IP')
    if (args.port == None):
      args.port = config.get('CONFIG', 'Port')
    if (args.path == None):
      args.path = config.get('CONFIG', 'File')

  return args


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt as err:
    print('Exit')
    sys.exit(1)