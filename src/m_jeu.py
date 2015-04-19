# # # # # # # # # # # # # # # # #
#				#
#         Projet de MDD         #
#                               #
#       fichier : m_jeu.py      #
#                               #
# # # # # # # # # # # # # # # # #

#-*-coding:utf-8-*-

import pyglet
import time
import os

import m_carte as mc

class Jeu :

	def __init__(self, carte_type = "defaut") :
		
		#Chargement de la carte.
		self.carte = mc.Carte(carte_type)
		#Chargement des sons
		self.charger_sons()
		#Lecteurs (environnement(s), action(s), heartbeats,...)
		self.creer_lecteurs()	
		#Fenêtre (activation du plein écran ?par défaut?)
		self.creer_fenetre()
		#Création des evènements... (clavier, ...) ou utilisation de raw_input? 
		self.event_init()

		#Initialisation de la vie du personnage
		self.vie = 3 #A changer

	def charger_sons(self):
		#Peut-être charger les sons automatiquement avec os.listdir() et charger tous les sons au format wav du répertoire 'sons' : ("Un peu" BOURIN et peut-être bouffe-mémoire)
		try :
			os.chdir("sons")		#On rentre dans le dossier 'sons'
			liste_sons = os.listdir()	#On récupère la liste des fichiers.

			#On ne garde que les fichiers 'wav' :
			liste_sons = [ fichier for fichier in liste_sons if fichier.find(".wav") != -1]

			for son in liste_sons :
				self.sons[son.replace(".wav",'')] = pyglet.resource.media(son)

			os.chdir("..")

		except FileNotFoundError :
			print("Le dossier 'sons' contenant les sons (héhé) n'a pas été trouvé.")
			self.sons = None
	def creer_lecteurs(self):
		"""Crée les lecteurs pyglet, les lecteurs env, eau, et heartbeat sont réglés pour tourner en boucle sur la musique en cours : 
	- env : Pour l'environnement.
	- eau : Pour l'eau à proximité de la case.
	- action : Pour les différentes actions (déplacements, coups,...).
	- monstre : Bruit du monstre qui indique que l'on est sur la case d'un monstre.
	- heartbeat : Si il ne reste qu'une vie, on entend un bâttement de coeur.
	"""
		self.lecteurs = {}
		for type in ("env", "eau", "monstre", "action", "heartbeat"):
			self.lecteurs[type] = pyglet.media.Player()
			if type in ("env", "eau", "heartbeat") :
				self.lecteurs[type].eos_action = self.lecteurs[type].EOS_LOOP
 
	def creer_fenetre(self):
		"""Crée la fenêtre pyglet en plein écran."""
		self.window = pyglet.window.Window(fullscreen = True)

	def event_init(self):
		"""crée les évenements : 
	- claviers : 
		- F : plein écran
		- ..."""
		@self.window.event
		def on_key_press(symbol, modifiers):
			if symbol == pyglet.window.key.F :
				self.window.set_fullscreen(not self.window.fullscreen)
		
	def run(self):

		pyglet.app.run()

	#Autres fonctions
