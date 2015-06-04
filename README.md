# Jeu-Python-S2
Fichier README.TXT
Projet de Méthode de Développement de S2 à L'ENIB

BlindQuest est un petit jeu de rôle exclusivement basé sur le son. Le but est de trouver le boss final et de le vaincre.

Le dossier du jeu contient : 
- blindquest.sh : Script pour lancer le projet, options :

  --python2  -2  Utilise python2 pour exécuter le jeu.
      -2d  Utilise python2 et affiche le fichier d'erreurs à la fin.
      
  --python3  -3  Utilise python3 (par défaut) pour exécuter le jeu.
  -d -3d --debug     Utilise python3 et affiche le fichier d'erreurs à la fin.
  
   --install  -i  Crée un raccourci .desktop du jeu.
   
  --map-editor  -m  Ouvre l'éditeur de carte.
  
  --help    -h  Affiche l'aide.
- divers/ : Contient :
 - logo/ : contient les fichiers GIMP du logo (fichier blindquest.png).
 - copie_cartes/ 
 - documents/ : les documents à rendre avec le jeu (document de conception, cahier des charges)
 - pyglet/ : archives Pyglet
- cartes/ : Contient les fichiers cartes nommés de la forme carte_nom.txt, il contient la carte par défaut, une petite carte, une carte de test pour le développement du projet, et une carte basic pour le premier prototype.
- scripts/ : Contient divers scripts :
 - afficher_texte.py : un exemple d’affichage avec Pyglet
 - editeur_cartes.py 
 - test_volume.py
- sons/ : Contient les fichiers sons au format wav.
- src/ : Contient le code source du projet, en deux dossiers src_2 pour Python 2 et src_3 pour Python 3
 - pyglet/ : tous les fichiers nécessaires à Pyglet
 - main.py 
 - m_carte.py : le module qui contient la classe Carte.
 - m_jeu.py : le module qui contient la classe Jeu.
 - constantes.py : contient les valeurs de tous les environnements du jeu, des codes de proximités, des monstres, et un dictionnaire de conversion pour les sons

En jeu, les commandes sont les suivantes :

H pour afficher l’aide

P met le jeu en pause et reprend la partie

F active et désactive le plein écran

E permet d’attaquer lors d’un combat

ÉCHAP permet d’attaquer lors d’un combat

S pour sauvegarder une partie

C pour charger une partie

La bibliothèque Openal est nécessaire au bon fonctionnement du jeu :
ArchLinux : 
# pacman -S openal
Ubuntu/Debian :
# apt-get install libopenal1
Fedora :
# yum install openal
Mac : installé par défaut
Windows : un fichier d'installation est disponible dans le dossier "divers"

Pour lancer le jeu : 
Sous GNU/Linux & Mac : Depuis le dossier du jeu dans un terminal : sh ./blindquest.sh
Sous windows : Lancer le fichier blindquest_win_py2.bat ou blindquest_win_py3.bat selon la version de python installée. 


<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">BlindQuest</span> de <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">CARON, GOÑI, TAUPIAC</span> est mis à disposition selon les termes de la <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">licence Creative Commons Attribution - Pas d&#39;Utilisation Commerciale - Pas de Modification 4.0 International</a>.
