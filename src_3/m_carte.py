#-*-coding:utf-8-*-

# # # # # # # # # # # # # # # # #
#				#
#	  Projet de MDD		#
#				#
#     fichier : m_carte.py	#
#				#
# # # # # # # # # # # # # # # # #

#Importation des modules fournis avec python :
import os

#Importation du module contenant les constantes :
import constantes as cs

class Carte (object) :
	"""Classe qui gère la carte et s'occupe de l'emplacement et du déplacement du joueur."""

	def __init__(self, type_carte = "defaut", num_sauv = None) : 
		"""Constructeur : Charge la carte dans une liste de liste (attribut carte) et définit la position par défaut du joueur (attributs posx et posy).
			carte_type : Nom de la carte
			num_sauv : Si définit, il charge une sauvegarde, cet argument indique le numéro de la savegarde à charger.
		"""

		#Initialisation de la position du joueur :
		self._posx = 0
		self._posy = 0

		#Si on n'a pas de valeur donnée pour num_sauv (le numéro de la sauvegarde), on ouvre une carte nommée carte_NOM.txt dans le dossier cartes et on recherche le départ (codé 98).
		if num_sauv == None :

			self.ouvrir_fichier_carte("cartes", "carte_" + str(type_carte))
			self.trouver_depart()

		#Pour plus tard lors du chargement de sauvegardes. 
#		else :
#			self.ouvrir_fichier_carte("saves", carte_type + "_" + num_sauv)
#			self.posx = self.carte[-1][1]
#			self.posy = self.carte[-1][2]


	#Encapsulation pour l'absisse du joueur (posx) :
	def _get_posx(self) :
		"""Accesseur de l'attribut posx"""
		return self._posx
	def _set_posx(self, new_posx) :
		"""Mutateur de l'attribut posx. Si la nouvelle valeur est sur la carte et n'est pas un lieu impraticable (définis dans le fichier 'constantes.py'), alors elle est attribuée à l'attribut."""
		if new_posx >= 0 and new_posx < self.nb_colonnes :
			if self.carte[self.posy][new_posx] not in cs.NOGO :
				self._posx = new_posx

	posx = property(_get_posx, _set_posx)


	#Encapsulation pour l'ordonnée du joueur (posy) :
	def _get_posy(self) :
		"""Accesseur de l'attribut posy"""
		return self._posy
	def _set_posy(self, new_posy) :
		"""Mutateur de l'attribut posy. Si la nouvelle valeur est sur la carte et n'est pas un lieu impraticable (définis dans le fichier 'constantes.py'), alors elle est attribuée à l'attribut."""
		if new_posy >= 0 and new_posy < self.nb_lignes :
			if self.carte[new_posy][self.posx] not in cs.NOGO :
				self._posy = new_posy
	posy = property(_get_posy, _set_posy)


	def ouvrir_fichier_carte(self, dossier, nom_fichier) :
		"""Charge la carte du fichier nommé 'nom_fichier.txt', présent dans le dossier donné (classiquement saves ou cartes), sous la forme d'un liste de listes d'entiers.
		Une erreur est levée si un type autre que chaîne de caractères est donné ou si le dossier ou le fichier n'existe pas"""

		try:
			with open(os.path.join(dossier, nom_fichier + ".txt"), 'r') as fichier_carte :
				self.charger_carte(fichier_carte)

		except TypeError :
			raise TypeError("Le type de carte choisi ou le nom du dossier n'est pas une chaîne de caractères, utilisation de la carte par défaut.")

		except FileNotFoundError :
			raise FileNotFoundError("Il n'existe pas de fichier carte nommé {} dans le dossier '{}', utilisation de la carte par défaut.".format(nom_fichier + ".txt", dossier))


	def charger_carte(self, fichier_carte) :
		"""Charge le contenu d'un fichier carte dans une liste de liste de int, si les lignes ne sont pas toutes de la même taille, on les complète par de l'eau."""

		#On initialise la liste carte :
		self.carte = []

		#On récupère les lignes sous forme de chaîne de caractères rangés dans une liste :
		fichier = fichier_carte.read().split("\n")
		#On récupère les entiers séparés par des espaces dans chaque élément de la liste :
		try :
			for i in range(len(fichier) - 1) :
				self.carte.append([int(a) for a in fichier[i].split() if a != ''])
		except ValueError :
			raise ValueError("Un caractère présent sur la carte n'est pas un nombre")

		#On enlève la dernière ligne créée inutilement si un retour à une ligne vide a été fait à la fin du fichier carte :
		if self.carte[-1] == []:
			del(self.carte[-1])

		#On compte le nombre de lignes :
		self.nb_lignes = len(self.carte)
		#On compte le nombre de colonnes et on complète les lignes de taille diférente par de l'eau
		#Init la variable :
		self.nb_colonnes = 0
		#On recherche la ligne la plus grande :
		for liste in self.carte :
			if self.nb_colonnes < len(liste) :
				self.nb_colonnes = len(liste)
		#On complète par de l'eau: 
		for liste in self.carte :
			while len(liste) < self.nb_colonnes :
				liste.append(cs.EAU)


#	def get_player_info(self):
#		"""Lors du chargement d'une sauvegarde, la dernière ligne de la liste carte est une liste d'informations du joueur sous la forme ['#', posx, posy, vie, bonus...].
#		Cette méthode renvoie cette liste sans les information concernant la position du joueur."""

#		#On récupère la dernière ligne. 
#		infos = self.carte[-1]
#		#On enlève l'absisse et l'ordonnée du joueur.
#		del infos[0:2]
#		#On enlève la dernière ligne de la carte.
#		del self.carte[-1]
		
#		return infos


	def trouver_depart(self) :
		"""Trouve les coordonnées du départ et les range dans posx et posy."""

		#Initialisation des variables :
		i, j = 0, 0
		found = False

		#Boucle des ordonnées :
		while not found and j < len(self.carte) :
			i = 0
			#Boucle des absisses :
			while not found and i < len(self.carte) :
				if self.carte[j][i] == cs.DEPART :
					self.posx, self.posy = i, j
					found = True
				i += 1
			j += 1

		#Si la valeur de départ n'est pas trouvée, on lève une erreur de valeur (ça paraît logique) : 
		#Plus sérieusement, le type d'erreur levée pourra être changé.
		if not found :
			print(self.carte)
			raise ValueError("Aucune case de départ (codée {}) n'a été trouvé sur la carte.".format(cs.DEPART))


	def move(self, direction = None) :
		"""Fonction qui déplace le joueur et renvoie le code de la case d'arrivée du joueur.
			- direction : prend un chaîne de caractère parmis ("OUEST", "EST", "NORD", "SUD").
					Si il n'est pas définit (ou à None du coups), le joueur ne bouge pas, ce qui est utile pour avoir l'environnement sonore actuel du joueur."""

		#On copie les coordonnées du joueur avant le déplacement :
		x, y = self.posx, self.posy

		if direction == "NORD" :
			self.posy -= 1
		elif direction == "SUD" :
			self.posy += 1
		elif direction == "OUEST" :
			self.posx -= 1
		elif direction == "EST" :
			self.posx += 1

		#Si le joueur n'a pas bougé, on renvoie None :
		if x == self.posx and y == self.posy :
			return None
		
		#On renvoie le code de la case ainsi que, à partir des centaines, le code de proximité :
		return self.carte[self.posy][self.posx] + self.detect_prox() * 100

      
	def detect_prox(self) :
		"""Renvoie un entier composé au maximum de 4 puissances de 2 différentes aditionnées pour l'utilisation de l'opérateur bit à bit."""
		#Initialisation de la variable qui sera retournée :
		detect = 0
		#On regarde si les différents types qui doivent être détectés sont à proximité : 
		for prox in cs.PROX :
			#NORD :
			if self.posy > 0 :
				if self.carte[self.posy - 1][self.posx] == prox :
					detect |= cs.PROX[prox]
			#SUD :
			if self.posy < self.nb_lignes -  1 :
				if self.carte[self.posy + 1][self.posx] == prox :
					detect |= cs.PROX[prox]
			#OUEST :
			if self.posx > 0 :
				if self.carte[self.posy][self.posx - 1] == prox :
					detect |= cs.PROX[prox]
			#EST :
			if self.posx < self.nb_colonnes - 1 :
				if self.carte[self.posy][self.posx + 1] == prox :
					detect |= cs.PROX[prox]

		return detect