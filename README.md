
# Interoperabilité

Pour la gestion des capteurs, une interface en ligne de commande a été implémentée. Cette interface permet la création de *printers*. Les *printers* permettent d'afficher ou d'envoyer les données d'un capteur à une API Rest. 

## Command line / cli.py
Pour l'exécution du programme, il faut préciser l'action voulue en paramètre, quatre actions sont actuellement disponibles : 

### Arguments

 - **printer**, suivi de l'id d'un capteur lancera le programme et surveillera l'activité du capteur correspondant à l'id donné. Printer est une méthode de visualisation : un printer créé via cette méthode n'enverra aucune donnée.  
`$ python3 cli.py printer id [ip] [port]`  
Exemple : `$ python3 cli.py printer CounterTriggeringSensor_14`

 - **reset**, suivi de l'id d'un capteur remettra à 0 le nombre de mouvements detectés du capteur correspondant à l'id donné
 `$ python3 cli.py [debug] reset id metrics [ip] [port]`

	`metrics` peut prendre comme valeur : 
	 - scaleTitle
	 - level

	Exemple : `$ python3 cli.py reset CounterTriggeringSensor_14 level`

- **file**, suivi d'un nom de fichier lancera le programme et surveillera l'activité des capteurs correspondants aux ids contenus dans le fichier.  
`$ python3 cli.py [debug] file relative_path [ip] [port]`  
Exemple : `$ python3 cli.py file ma_liste_capteurs.txt`

- **list**, permet de lister tous les appareils connectés à l'API ZWave.  
`$ python [debug] cli.py list [ip] [port]`  
Exemple : `$ python cli.py list` 

### Options 

`-d --debug` 	: Place le niveau d'affichage au niveau `DEBUG`  
`-i --ip`		: Configure l'ip cible de l'API ZWave  
`-p --port`		: Configure le port cible de l'API Zwave  

### Fichier de configuration 

Associer, ligne par ligne, l'id d'un capteur ZWave et l'id d'un capteur en base de donnée.  
Exemple : 
```vim
CounterTriggeringSensor_14	18
LightSensitiveSensor_8 		2
```
