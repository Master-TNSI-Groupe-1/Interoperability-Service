import sys

import logging

LOG_FILENAME = "ZWAVE.log"
logger = None

def setup_logger(debug):
  global logger
  logger = logging.getLogger("ZWAVE")
  logger.setLevel(logging.DEBUG if debug else logging.INFO)

  formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

  if(logger.hasHandlers()):
      logger.handlers.clear()

  for handler in [logging.FileHandler("ZWAVE.log"), logging.StreamHandler(sys.stdout)]:
    handler.setFormatter(formatter)
    logger.addHandler(handler)

  return logger

if(logger == None):
    logger = setup_logger(False)
