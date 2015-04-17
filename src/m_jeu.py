# # # # # # # # # # # # # # # # #
#				#
#         Projet de MDD         #
#                               #
#       fichier : m_jeu.py      #
#                               #
# # # # # # # # # # # # # # # # #

import pyglet
import time
import os

import m_carte as mc

class Jeu :

	jeu_lance = False

	def __init__(self, carte_type) :
		try :
			assert  not self.jeu_lance == True
		except AssertionError:
			print("Il existe déjà un objet jeu.")
		
		self.jeu_lance = True
		#Chargement de la carte.
		self.carte = mc.Carte(carte_type)
		#Chargement des sons
		self.charger_sons()
		#Lecteurs (environnement(s), action(s), heartbeats,...)
		lecteurs = {}	
		#Fenêtre (activation du plein écran ?par défaut?)
		self.window = pyglet.window.Window(fullscreen = True)
		#Création des evènements... (clavier, ...) ou utilisation de raw_input? 
		self.event_init()

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
