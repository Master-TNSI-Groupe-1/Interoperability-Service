import sys

import logging

LOG_FILENAME = "zwave.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def setup_logger(debug):
  logger = logging.getLogger("ZWAVE")
  logger.setLevel(logging.DEBUG if debug else logging.INFO)

  formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

  for handler in [logging.StreamHandler(sys.stdout),
                  logging.FileHandler("ZWAVE.log")]:
    handler.setFormatter(formatter)
    logger.addHandler(handler)

  return logger
