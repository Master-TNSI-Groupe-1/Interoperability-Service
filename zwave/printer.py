from threading import Thread
import sys
import time
from threading import Thread

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
    client.get_devices()
    temp = client.get_data(self.id)
    while True:
      mouvements = client.get_data(self.id)
      if mouvements < temp:
        temp = 0

      if mouvements != temp:
        for i in range(mouvements - temp):
          self.send_to_api()

      temp = mouvements
      time.sleep(2)

    print("Exit")


  def send_to_api(self):
    print("Mouvement détecté sur le capteur " + self.id)
