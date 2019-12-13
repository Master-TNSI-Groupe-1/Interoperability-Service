#!/usr/bin/env python

import sys
assert sys.version_info > (3, 5), "Python is dead, long live Python!" \
                                  " (please use Python 3.5+)"

import argparse
import client, printer

import mylogger

def handle_sensor(args):
  devices = client.get_devices()
  device = None
  for de in devices:
    if (de['id'] == args.id):
      device = de

  if device == None:
    mylogger.logger.info("Capteur inexistant ou impossible à trouver.")
    return False
  else:
    mylogger.logger.info("Capteur trouvé [" + device['id'] + "].")
    return True

def handle_printer(args):
  my_sensor_printer = printer.Printer(args.id)
  my_sensor_printer.start()

def handle_reset(args):
  client.reset_sensor(args.id, args.metrics, args.value)

def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help="role", dest="role", required=True)
  parser.add_argument('-d', '--debug', action='store_true')

  router_parser = subparsers.add_parser("printer")
  router_parser.add_argument("id", help="Veuillez entrer l'id d'un capteur.")

  router_parser = subparsers.add_parser("reset")
  router_parser.add_argument("id", help="Veuillez entrer l'id d'un capteur.")
  router_parser.add_argument("metrics", help="Veuillez entrer la mesure à réinitialiser")
  router_parser.add_argument("value", help="Veuillez entrez une valeur supérieure à 0.")


  args = parser.parse_args()

  mylogger.logger.debug("Python %s", sys.version.replace('\n', ''))
  function_name = "handle_" + args.role
  mylogger.logger.info("Calling %s()", function_name)

  if(handle_sensor(args)):
    globals()[function_name](args)

if __name__ == '__main__':
  main()
