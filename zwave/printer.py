from threading import Thread
import sys
import time
from threading import Thread

import client
import mylogger
import client, requests

class Printer(Thread):
  """Thread chargé simplement d'afficher une lettre dans la console."""

  def __init__(self, name, id, ip="localhost", port="8083"):
    Thread.__init__(self)
    self.name = name
    self.id = id
    self.ip = ip
    self.port = port

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""
    client.get_devices(self.ip, self.port)
    temp = client.get_data(self.name, self.ip, self.port)
    while True:
      mouvements = client.get_data(self.name, self.ip, self.port)
      mylogger.logger.debug("Mouvements : "+ str(mouvements))
      mylogger.logger.debug("Temp : "+str(temp))

      if mouvements < temp:
        mylogger.logger.debug("Temp reset (=0)")
        temp = 0

      if mouvements != temp:
        for i in range(mouvements - temp):
          if(self.id != 0):
            self.send_to_api()

      temp = mouvements
      time.sleep(2)

    print("Exit")

  def send_to_api(self):
    mylogger.logger.debug("In SendToApi")
    print(requests.get("http://100.24.5.45/get/sensor/pulsation/" + self.id))
    print("Mouvement détecté sur le capteur",self.id)
