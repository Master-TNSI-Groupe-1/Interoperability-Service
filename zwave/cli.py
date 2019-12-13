#!/usr/bin/env python

import sys
assert sys.version_info > (3, 5), "Python is dead, long live Python!" \
                                  " (please use Python 3.5+)"

import argparse, logging
import client, printer

import mylogger as mylog

def handle_printer(args):
  devices = client.get_devices()
  device = None
  for de in devices:
    if(de['id'] == args.action):
      device = de

  if device == None:
    logging.debug("Capteur inexistant ou impossible à trouver.")
  else:
    logging.debug("Capteur trouvé ["+device['id']+"].")
    my_sensor_printer = printer.Printer("CounterTriggeringSensor_14")
    my_sensor_printer.start()

def main():
  logger = mylog.setup_logger(True)
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help="role", dest="role", required=True)
  parser.add_argument('-d', '--debug', action='store_true')

  router_parser = subparsers.add_parser("printer")
  router_parser.add_argument("action", help="Veuillez entrez l'id d'un capteur.")

  router_parser = subparsers.add_parser("reset-sensor")
  router_parser.add_argument("action", help="Veuillez entrez l'id d'un capteur.")

  args = parser.parse_args()


  logger.debug("Python %s", sys.version.replace('\n', ''))
  function_name = "handle_" + args.role
  logger.debug("Calling %s()", function_name)
  globals()[function_name](args)


if __name__ == '__main__':
  main()
