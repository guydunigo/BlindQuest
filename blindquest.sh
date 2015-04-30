#!/bin/bash

case $1 in
	""|-3|--python3)
		python3 ./src_3/main.py
	;;
	-2|--python2)
		python2 ./src_2/main.py
	;;
	--install|-i)
		echo "[Desktop Entry]
Comment[fr]=
Comment=
Exec=sh ./blindquest.sh
GenericName[fr]=Jeu d'aventur
GenericName=Jeu d'aventure
Icon="$(pwd)"/blindquest.png
MimeType=
Name[fr]=BlindQuest
Name=BlindQuest
Path="$(pwd)"/
StartupNotify=true
Terminal=true
TerminalOptions=
Type=Application" > blindquest.desktop

	;;
	--map-editor|-m)
		python3 ./scripts/editeur_cartes.py
	;;
	--help|-h)
		echo "Jeu BlindQuest,
Un jeu d'aventure exclusivement basé sur du son

COMMANDE :
	./blindquest.sh [-2|-3|-i|-m|--python2|--python3|--install|--map-editor]

OPTIONS :
	--python2	-2	Utilise python2 pour exécuter le jeu.
	--python3	-3	Utilise python3 (par défaut) pour exécuter le jeu.
 	--install	-i	Crée un fichier .desktop du jeu.
	--map-editor	-m	Ouvre l'éditeur de carte.
	--help		-h	Affiche l'aide.
"
	;;
	*)
	;;
esac
