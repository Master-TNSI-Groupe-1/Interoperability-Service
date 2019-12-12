from threading import Thread
import time

import client

class Printer(Thread):
  """Thread chargé simplement d'afficher une lettre dans la console."""

  def __init__(self, id):
    Thread.__init__(self)
    self.id = id

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""
    while(True):
      client.get_data(self.id)
      time.sleep(2)


thread_1 = Printer("CounterTriggeringSensor_14")
thread_2 = Printer("15_CorrectValue_90")
thread_1.start()
thread_2.start()
