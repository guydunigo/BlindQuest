# # # # # # # # # # # # # # # # #
#				#
#	  Projet de MDD		#
#				#
#     fichier : m_carte.py	#
#				#
# # # # # # # # # # # # # # # # #

#-*-coding:utf-8-*-

class Carte :
	"""Classe qui gère la carte et s'occupe de l'emplacement du joueur."""
	def __init__(self, carte_type = "defaut", position_joueur = None): #Valeur par défaut de la position joueur à changer (comment est-elle définie ? codage sur la carte ? au début du fichier carte ? au hasard ?)
		self.ouvrir_fichier_carte(carte_type)
		self.position_joueur = [0,0] #...

	def ouvrir_fichier_carte(self, carte_type):
		"""Charge la carte du fichier nommé 'carte_nom.txt' présent dans le dossier 'cartes', sous la forme d'un liste de listes d'entiers. Si la carte n'existe pas, la carte par défaut est utilisée."""
		try:		
			with open("cartes/carte_"+carte_type + ".txt", 'r') as carte_fichier :
				#Charger la carte
				self.carte = []
		except TypeError :
			print("Le type de carte choisi n'est pas une chaîne de caractères, utilisation de la carte par défaut.")
			self.ouvrir_fichier_carte("defaut")

		except FileNotFoundError :
			print("Il n'existe pas de fichier carte nommé {} dans le dossier 'cartes', utilisation de la carte par défaut.".format("carte_" + carte_type + ".txt"))
			self.ouvrir_fichier_carte("defaut")
			#Par contre, il faut que la carte par défaut existe sinon on tourne en boucle... :)	
