# # # # # # # # # # # # # # # # #
#				#
#	  Projet de MDD		#
#				#
#     fichier : m_carte.py	#
#				#
# # # # # # # # # # # # # # # # #

#-*-coding:utf-8-*-

class Carte :
	"""Classe qui gère la carte et s'occupe de l'emplacement et du déplacement du joueur."""

	def __init__(self, carte_type = "defaut", num_sauv = None) : 
		"""carte_type : Nom de la carte
		num_sauv : Si définit, il charge une sauvegarde, cet argument indique le numéro de la savegarde à charger.
		
		Charge la carte dans une liste de liste (carte) et définit la position par défaut du joueur (posx et posy).
		"""

		#Initialisation de la position du joueur. 
		self._posx = 0
		self._posy = 0

		#Si on n'a pas de valeur donnée pour num_sauv (le numéro de la sauvegarde), on ouvre une carte nommée carte_NOM.txt dans le dossier cartes et on recherche le départ (codé 98).
		if num_sauv == None :

			self.ouvrir_fichier_carte("cartes", "carte_" + str(carte_type))
			self.trouver_depart()

		#Pour plus tard lors du chargement de sauvegardes. 
#		else :
#			self.ouvrir_fichier_carte("saves", carte_type + "_" + num_sauv)
#			self.posx = self.carte[-1][0]
#			self.posy = self.carte[-1][1]

	#Encapsulation pour l'absisse du joueur (posx).
	def _get_posx(self) :
		"""Accesseur de l'attribut posx"""
		return self._posx
	def _set_posx(self, new_posx) :
		"""Mutateur de l'attribut posx. Si la nouvelle valeur est sur la carte, alors elle est attribuée à l'attribut."""
		if new_posx >= 0 and new_posx < len(self.carte[0]) :
			self._posx = new_posx
	posx = property(_get_posx, _set_posx)

	#Encapsulation pour l'ordonnée du joueur (posy).
	def _get_posy(self) :
		"""Accesseur de l'attribut posy"""
		return self._posy
	def _set_posy(self, new_posy) :
		"""Mutateur de l'attribut posy. Si la nouvelle valeur est sur la carte, alors elle est attribuée à l'attribut."""
		if new_posy >= 0 and new_posy < len(self.carte) :
			self._posy = new_posy
	posy = property(_get_posy, _set_posy)

	def ouvrir_fichier_carte(self, dossier, nom_fichier) :
		"""Charge la carte du fichier nommé 'nom_fichier.txt', présent dans le dossier donné (classiquement saves ou cartes), sous la forme d'un liste de listes d'entiers.
		Une erreur est levée si un type autre que chaîne de caractères est donné ou si le dossier ou le fichier n'existe pas"""

		try:
			with open(dossier + "/" + nom_fichier + ".txt", 'r') as fichier_carte :
				self.charger_carte(fichier_carte)

		except TypeError :
			raise TypeError("Le type de carte choisi ou le nom du dossier n'est pas une chaîne de caractères, utilisation de la carte par défaut.")

		except FileNotFoundError :
			raise FileNotFoundError("Il n'existe pas de fichier carte nommé {} dans le dossier '{}', utilisation de la carte par défaut.".format(nom_fichier + ".txt", dossier))

	def charger_carte(self, fichier_carte) :
		"""Charge le contenu d'un fichier carte dans une liste de liste de int."""

		#On initialise la liste carte.
		self.carte = []

		#On récupère les lignes sous forme de chaîne de caractères rangés dans une liste.
		fichier = fichier_carte.read().split("\n")
		#On récupère les entiers séparés par des espaces dans chaque élément de la liste.
		for i in range(len(fichier) - 1) :
			self.carte.append([int(a) for a in fichier[i].split() if a != ''])
		#On enlève la dernière ligne créée inutilement si un retour à une ligne vide a été fait à la fin du fichier carte.
		if self.carte[-1] == []:
			del(self.carte[len(self.carte) - 1])

#	def get_player_infos():
#		"""Lors du cahrgement d'une sauvegarde, la dernière ligne de la liste carte est une liste d'informations du joueur sous la forme ['#', posx, posy, vie, bonus...].
#		Cette méthode renvoie cette liste sans les information concernant la position du joueur."""

#		#On récupère la dernière ligne. 
#		infos = self.carte[-1]
#		#On enlève l'absisse et l'ordonnée du joueur.
#		del infos[0:2]
#		#On enlève la dernière ligne de la carte.
#		del self.carte[-1]
		
#		return infos

	def trouver_depart(self) :
		"""Touve le départ (numéro 98) et le range dans posx et posy."""

		#Initialisation des variables.
		i, j = 0, 0
		found = False

		#Boucle des ordonnées.
		while not found and j < len(self.carte) :
			i = 0
			#Boucle des absisses.
			while not found and i < len(self.carte) :
				if self.carte[j][i] == 98 :
					self.posx, self.posy = i, j
					found = True
				i += 1
			j += 1

		#Si la valeur de départ n'est pas trouvée, on lève une erreur de valeur (ça paraît logique) : 
		if not found :
			raise ValueError("Aucune case de départ (codée 98) n'a été trouvé sur la carte.")


	def move(self, direction) :
		"""Fonction qui déplace le joueur et renvoie le code de la case d'arrivée du joueur.
		direction prend un chaîne de caractère parmis ("OUEST", "EST", "NORD", "SUD")."""

		if direction == "OUEST" :
			self.posx -= 1
		elif direction == "EST" :
			self.posx += 1
		elif direction == "NORD" :
			self.posy -= 1
		elif direction == "SUD" :
			self.posy += 1

		return self.catre[self.posy][self.posx]
