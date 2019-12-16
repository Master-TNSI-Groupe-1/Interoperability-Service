from threading import Thread
import sys
import time

import client

class Printer(Thread):
  """Thread chargé simplement d'afficher une lettre dans la console."""

  def __init__(self, id, ip="192.168.43.99", port="8083"):
    Thread.__init__(self)

    self.id = id
    self.ip = ip
    self.port = port

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""
    while(True):
      client.get_data(self.id, self.ip, self.port)

      time.sleep(2)

    print("Exit")