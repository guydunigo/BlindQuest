#!/bin/bash

case $1 in
	"")
		python3 ./src/main.py
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
	./blindquest.sh [-i|-m|--install|--map-editor]

OPTIONS : 
 	--install	-i	Crée un fichier .desktop du jeu.
	--map-editor	-m	Ouvre l'éditeur de carte.
	--help		-h	Affiche l'aide.
"
	;;
	*)
	;;
esac
