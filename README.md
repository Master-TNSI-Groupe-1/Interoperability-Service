
# Interoperabilité

Pour la gestion des capteurs, une interface en ligne de commande a été implémentée. Cette interface permet la création de *printers*. Les *printers* permettent d'afficher ou d'envoyer les données d'un capteur à une API Rest. 

## Service / capteurs.service

Pour installer le service : 
`$ git clone https://github.com/Master-TNSI-Groupe-1/Interoperability-Service.git`

Pour configurer le service, à placer dans `/etc/systemd/system/capteurs.service` :  
```ini
[Unit]
Description=Service Capteurs
After=network.target
StartLimitIntervalSec=0

[Service]
Type=Simple
Restart=Always
RestartSec=10
User=root
ExecStart=/usr/bin/python3 /var/python/Interoperability-Service/zwave/cli.py
ExecStop=/bin/kill -INT $MAINPID

[Install]
WantedBy=multi-user.target
```

Le service se lance via la commande `$ systemctl start capteurs.service`
Si le fichier de configuration, ou la liste des capteurs associée, est modifié, il faut redémarrer le service via la commande : 
`$ systemctl restart capteurs.service`

## Command line / cli.py

`$ python3 cli.py`

Cette commande lance le service de récupération des données des capteurs pour un Raspberry particulier. 
Les données de connection (IP, port, IP API, Liste de capteurs, etc.) sont définis dans le fichier `properties.ini`
Les arguments surchargent le fichier `properties.ini`.

Pour l'exécution du programme, nous pouvons préciser l'action voulue en paramètre. Quatre actions sont actuellement disponibles. 

### Arguments

#### Positionnels  

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

#### Optionnels

`-d --debug` 		: Place le niveau d'affichage au niveau `DEBUG`
`-a --api`		: Configure l'ip cible de l'API de compteurs   
`-i --ip`		: Configure l'ip cible de l'API ZWave  
`-p --port`		: Configure le port cible de l'API Zwave  

## Fichier de configuration / properties.ini

Un fichier de config `properties.ini`est mis en place pour définir les options de connection. Le fichier est de la forme : 

```ini
[CONFIG]
IP = 192.168.XX.XX
Port = 8080
File = listeCapteurs
Api = 192.168.XX.XX

[LOGIN]
User = root
Passwd = admin
```  

## Liste des capteurs / listSensor

Associer, ligne par ligne, l'id d'un capteur ZWave et l'id d'un capteur en base de donnée :  

```vim
CounterTriggeringSensor_14	18
LightSensitiveSensor_8 		2
```
