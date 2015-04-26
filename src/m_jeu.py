#-*-coding:utf-8-*-

# # # # # # # # # # # # # # # # #
#				#
#         Projet de MDD         #
#                               #
#       fichier : m_jeu.py      #
#                               #
# # # # # # # # # # # # # # # # #

#Importation des modules fournis avec python :
import time
import os

#Importation du module Pyglet pour python 3. Si il n'est pas trouvé sur le système, on utilise la version présente dans le dossier src :
try :
	import pyglet
except ImportError : 
	import pyglet_py3 as pyglet
	print("Bibliothèque pyglet non trouvée pour python3, utilisation de la version de pyglet du dossier src/ (",pyglet.version,").") 

#Importation des constantes :
import constantes as cs
#Importation de notre module qui gère la carte et la position du joueur :
import m_carte as mc

class Jeu (object) :
	"""Classe qui gère le jeu, la Bibliothèque pyglet, les évènements claviers, la fenêtre et le son."""

	def __init__(self, type_carte = "defaut") :
		"""Constructeur : 
			carte_type : type de carte à utiliser durant le jeu. (carte nommée selon l'exemple : carte_NOM.txt et placée dans le dossier cartes)"""

		#Réglage du dossier de travail de pyglet pour le dossier racine du projet, sinon il ne trouve pas les différents composants :
		working_dir = os.path.dirname(os.path.realpath(__file__))
		pyglet.resource.path = [os.path.join(working_dir,'..')]
		pyglet.resource.reindex()
		#On choisit d'utiliser openal pour l'audio. (pulseaudio ne marche pas)
		pyglet.options['audio'] = ('openal',)

		#Chargement de la carte.
		self.carte = mc.Carte(type_carte)
		#Chargement des sons
		self.charger_sons()
		#Lecteurs (environnement(s), action(s), heartbeats,...)
		self.creer_lecteurs()	
		#Fenêtre (activation du plein écran ?par défaut?)
		self.creer_fenetre()
		#Création des evènements... (clavier, ...) ou utilisation de raw_input? 
		self.init_events()

		#Initialisation de la vie du personnage
		self.vie = 10 #A changer

		#Initialisation des booléens de fin de jeu et de combat :
		self.ENDSIG = False
		self.isCombat = False


	def charger_sons(self) :
		"""Charge tous les sons du dossier 'sons' et les range dans un dictionnaire avec pour étiquette le nom du fichier son sans l'etension '.wav'.
		On charge les sons directement dans la mémoire sans streaming pour éviter les problèmes de source déjà queued. ("Un peu" BOURIN et peut-être bouffe-mémoire)"""

		#On crée le dictionnaire de sons :
		self.sons = {}
		try :
			#On récupère la liste des fichiers du dossier 'sons' :
			liste_sons = os.listdir("sons")

			#On ne garde que les fichiers 'wav' :
			liste_sons = [ fichier for fichier in liste_sons if fichier.find(".wav") != -1]

			#On ouvre les sons avec pyglet et on les range dans le dictionnaire 'sons' avec pour étiquette le nom du fichier son sans l'etension '.wav' :
			for son in liste_sons :
				self.sons[son.replace(".wav",'')] = pyglet.media.load(os.path.join("sons", son), streaming = False)

		except FileNotFoundError :
			print("Le dossier 'sons' contenant les sons (héhé) n'a pas été trouvé.")
			self.sons = None


	def creer_lecteurs(self) :
		"""Crée les lecteurs pyglet, les lecteurs env, eau, et heartbeat sont réglés pour tourner en boucle sur la musique en cours : 
			- env : Pour l'environnement, en boucle.
			- action : Pour les différentes actions (déplacements, coups,...). : peut-être inutile (directement son.play()).
			- monstre : Bruit du monstre qui indique que l'on est sur la case d'un monstre.: peut-être inutile
			- heartbeat : Si il ne reste qu'une vie, on entend un bâttement de coeur, en boucle.
			- Les différents sons de proximité ont leur propre lecteur.
		"""
		
		self.lecteurs = {}
		for lecteur in ("env", "monstre", "action", "heartbeat"):
			self.lecteurs[lecteur] = pyglet.media.Player()
			if lecteur == "env" :
				#En boucle
				self.lecteurs[lecteur].eos_action = self.lecteurs[lecteur].EOS_LOOP
			if lecteur == "heartbeat" :
				self.lecteurs[lecteur].eos_action = self.lecteurs[lecteur].EOS_LOOP
				self.lecteurs[lecteur].queue(self.sons[lecteur])
				self.lecteurs[lecteur].volume = 0.05

		#Création des lecteurs pour les sons de proximité, un lecteur par sons, en boucle, volume faible.
		for lecteur in cs.PROX :
			self.lecteurs[lecteur] = pyglet.media.Player()
			self.lecteurs[lecteur].eos_action = self.lecteurs[lecteur].EOS_LOOP
			self.lecteurs[lecteur].queue(self.sons[cs.CONV[lecteur]])
			self.lecteurs[lecteur].volume = 0.05

		#On restitue l'environnement sonore de départ.
		self.lecteurs["env"].queue(self.sons[cs.CONV[cs.DEPART]])
		self.lecteurs["env"].play()
		self.move()

 
	def creer_fenetre(self) :
		"""Crée la fenêtre pyglet en plein écran."""
		self.window = pyglet.window.Window(fullscreen = True)


	def init_events(self) :
		"""crée les évenements : 
	- claviers : 
		- flèches directionnelles : se déplacer
		- ECHAP : Quitter
		- F : Plein écran
		- H : Aide
		- ..."""
		@self.window.event
		def on_key_press(symbol, modifiers):
			if not self.ENDSIG :
				#Fullscreen
				if symbol == pyglet.window.key.F :
					self.window.set_fullscreen(not self.window.fullscreen)
				#Aide
				elif symbol == pyglet.window.key.H :
					self.afficher_aide()
				#déplacements
				elif symbol == pyglet.window.key.UP :
					self.move("NORD")
				elif symbol == pyglet.window.key.DOWN :
					self.move("SUD")
				elif symbol == pyglet.window.key.RIGHT :
					self.move("EST")
				elif symbol == pyglet.window.key.LEFT :
					self.move("OUEST")

		@self.window.event
		def on_draw():
			"""On efface l'écran, peut-être sera-t-il impossible de voir l'aide : dans ce cas, l'enlever et regarder quand la touche est relachée."""
			self.window.clear()


	def move(self, direction = None) :
		"""Fonction qui déplace le joueur et gère ce qui peut y arriver (mort si environnement dangereux, combat...) et lance les sons d'environnement et de proximité.
			- direction : prend un chaîne de caractère parmis ("OUEST", "EST", "NORD", "SUD"). 
					Si il n'est pas définit (ou à None du coups), le joueur ne bouge pas, ce qui est utile pour avoir l'environnement sonore actuel du joueur."""

		#On déplace le joueur su la carte et on récupère le code de la case d'arrivée. 
		case = self.carte.move(direction)
		#On récupère les informations de proximité de la case (eau, pont...), qui sont écrits sous forme de centaines et au dessus.
		infos_prox = int(case / 100)
		case = case - infos_prox * 100

		print("code case : ",cs.CONV[case],", ",case,", code proximité : ",infos_prox)
		#Restitution de l'environnement actuel :
		#Si la source est déjà active, on la remet au début.
		if self.lecteurs["env"].source == self.sons[cs.CONV[case]] :
			self.lecteurs["env"].seek(0)
		else :
			self.lecteurs["env"].queue(self.sons[cs.CONV[case]])
			self.lecteurs["env"].next_source()

		#Détection des proximités et restitution du son associé :
		for prox in cs.PROX :
			if infos_prox & cs.PROX[prox] == cs.PROX[prox] :
				self.lecteurs[prox].play()
			else :
				self.lecteurs[prox].pause()


	def afficher_aide(self) :
		"""Fonction qui affiche l'aide (tiens, tiens...)."""
		pass


	def fin(self, type_fin) :
		"""Fonction qui gère la fin selon s'il y a victoire ou mort, et s'occupe de quitter le programme.
			- type : chaîne de caractère décrivant la fin parmis celles se trouvant dans le fichier constantes, les fichiers sons associés doivent exister."""

		self.lecteurs["env"].queue(type_fin)
		#

	def run(self) :
	  
		pyglet.app.run()

	#Autres fonctions
