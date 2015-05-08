#!/bin/bash

#Création du dossier de logs
mkdir log 2> /dev/null

#Si aucun argument n'est donné, on teste si python 3 est présent, sinon on utilise python 2
if [ $1="" ] & [ -z $(command -v "python3") ]
then
echo "Python version 3 non trouvé, utilisation de la version 2."
arg='-2'
else
arg=$1
fi

case $arg in
	""|-3|-3d|--python3|-d|--debug)
		echo "

[$(date) on $OSTYPE]

" >> log/errors_py3.log
		python3 ./src_3/main.py 2>> log/errors_py3.log
	;;
	-2|-2d|--python2)
		echo "

[$(date) on $OSTYPE]

" >> log/errors_py2.log
		python2 ./src_2/main.py 2>> log/errors_py2.log
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
	*)
		echo "Jeu BlindQuest,
Un jeu d'aventure exclusivement basé sur du son

COMMANDE :
	./blindquest.sh [options]

OPTIONS :
	--python2	-2	Utilise python2 pour exécuter le jeu.
			-2d	Utilise python2 et affiche le fichier d'erreurs à la fin.
	--python3	-3	Utilise python3 (par défaut) pour exécuter le jeu.
	-d -3d --debug 		Utilise python3 et affiche le fichier d'erreurs à la fin.
 	--install	-i	Crée un raccourci .desktop du jeu.
	--map-editor	-m	Ouvre l'éditeur de carte.
	--help		-h	Affiche cette aide.
"
	;;
esac

case $arg in
	-d|-3d|--debug)
		cat log/errors_py3.log 
	;;
	-2d)
		cat log/errors_py2.log
	;;
esac
