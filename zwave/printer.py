from threading import Thread
import time

import client

class Printer(Thread):
  """Thread chargé simplement d'afficher une lettre dans la console."""

  def __init__(self):
    Thread.__init__(self)

  def run(self):
    """Code à exécuter pendant l'exécution du thread."""
    while(True):
      client.get_data()
      time.sleep(2)


thread_1 = Printer()
thread_1.start()
