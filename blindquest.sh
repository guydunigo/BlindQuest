#!/bin/bash
if [[ -z $1 ]]
then
	python3 ./src/main.py

elif [ $1=="--install"i ]
then
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

fi

