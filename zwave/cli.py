#!/usr/bin/env python

import sys
assert sys.version_info > (3, 5), "Python is dead, long live Python!" \
                                  " (please use Python 3.5+)"

import argparse, logging
import client, printer

logger=None
LOG_FILENAME = "zwave.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

def handle_printer(args):
  devices = client.get_devices()
  device = None
  for de in devices:
    if(de['id'] == args.action):
      device = de

  if device == None:
    logging.debug("Capteur inexistant ou impossible à trouver.")
    print("Capteur inexistant ou impossible à trouver.")
  else:
    logging.debug("Capteur trouvé ["+device['id']+"].")
    print("Capteur trouvé ["+device['id']+"].")
    my_sensor_printer = printer.Printer("CounterTriggeringSensor_14")
    my_sensor_printer.start()


def setup_logger(debug):
  global logger
  logger = logging.getLogger("ZWAVE")
  logger.setLevel(logging.DEBUG if debug else logging.INFO)

  formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

  for handler in [logging.StreamHandler(sys.stdout),
                  logging.FileHandler("ZWAVE.log")]:
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help="role", dest="role", required=True)
  parser.add_argument('-d', '--debug', action='store_true')

  router_parser = subparsers.add_parser("printer")
  router_parser.add_argument("action", help="Veuillez entrez l'id d'un capteur.")

  args = parser.parse_args()

  setup_logger(args.debug)
  logger.debug("Python %s", sys.version.replace('\n', ''))
  function_name = "handle_" + args.role
  logger.debug("Calling %s()", function_name)
  globals()[function_name](args)


if __name__ == '__main__':
  main()
