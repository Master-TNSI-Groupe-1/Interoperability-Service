## Interoperabilité

Pour l'exécution du programme, il faut préciser l'action voulue en paramètres, trois actions sont actuellement disponibles : 

printer, suivi de l'id d'un capteur lancera le programme et surveillera l'activité du capteur correspondant à l'id donné
Exemple : python3 cli.py printer CounterTriggeringSensor_14

reset-sensor, suivi de l'id d'un capteur remettra à 0 le nombre de mouvements detectés du capteur correspondant à l'id donné
Exemple : python3 cli.py reset-sensor CounterTriggeringSensor_14

file, suivi d'un nom de fichier lancera le programme et surveillera l'activité des capteurs correspondants aux ids contenus dans le fichier
Exemple : python3 cli.py file liste_capteurs.txt