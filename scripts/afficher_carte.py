import pyglet

TAILLE_CASE = 30 

PLAINE = 0
FORET = 1
CAVERNE = 2
EAU = 3
CHATEAU = 4
SENTIER = 5
PONT = 6
SABLE = 7
MONTAGNE = 8
MOB = 10
BOSS = 11
BOSS_FINAL = 12
BONUS = 13
DEBUT = 98
FIN = 99


COULEUR_PLAINE = ('c4B', (0,200,0, 0)*4)					# VERT CLAIR
COULEUR_FORET = ('c4B', (0,0,100, 0)*4)					# VERT FONCE
COULEUR_CAVERNE = ('c4B', (100,0,100, 0)*4)				# MARRON
COULEUR_EAU = ('c4B', (0,0,255, 0)*4)					# BLEU
COULEUR_CHATEAU = ('c4B', (200,200,200, 0)*3, (100, 100, 100, 0))	# GRIS CAIR DEGRADE
COULEUR_SENTIER = ('c4B', (255,0,255, 0)*4)				# VERT MARRON
COULEUR_PONT = ('c4B', (0,0,255, 0)*4)
COULEUR_SABLE = ('c4B', (0,0,255, 0)*4)
COULEUR_MONTAGNE = ('c4B', (0,0,255, 0)*4)
COULEUR_MOB = ('c4B', (0,0,255, 0)*4)
COULEUR_BOSS = ('c4B', (0,0,255, 0)*4)
COULEUR_BOSS_FINAL = ('c4B', (255,0,0, 0)*4)
COULEUR_BONUS = ('c4B', (0,0,255, 0)*4)
COULEUR_DEBUT = ('c4B', (0,0,255, 0)*4)
COULEUR_FIN = ('c4B', (100,100,100, 0)*4)


class Carte :
	def __init__(self, carte = None) :

			self.ouvrir_carte(carte)
			self.window = pyglet.window.Window(width = self.nb_colonnes * TAILLE_CASE, height = self.nb_lignes * TAILLE_CASE)
			self.event_init()

			#Coordonnées du curseur :
			self._cx = 0
			self._cy = 0 

	def _get_cx(self) :
		"""Accesseur de l'absisse du curseur"""
		return self._cx
	def _set_cx(self, new_cx) :
		"""Mutateur de l'absisse du curseur"""
		if new_cx >= self.nb_colonnes :
			self._cx = 0
		elif new_cx < 0 :
			self._cx = self.nb_colonnes - 1
	cx = property(_get_cx, _set_cx)
	
	def _get_cy(self) :
		"""Accesseur de l'ordonné du curseur"""
		return self._cy
	def _set_cy(self, new_cy) :
		"""Mutateur de l'ordonné du curseur"""
		if new_cy >= self.nb_lignes :
			self._cy = 0
		elif new_cy < 0 :
			self._cy = self.nb_lignes - 1
	cy = property(_get_cy, _set_cy)

	def ouvrir_carte(self, carte) :
		"""Essaye d'ouvrir la carte carte_nom.txt (où nom est une chaîne de caractères contenue dans l'argument carte) dans le dossier cartes. Si un mauvais nom est donné ou que la carte n'éxiste pas, on crée une nouvelle carte."""

		try :
			with open("../cartes/carte_" + carte + ".txt", "r") as fichier_carte :
				self.charger_carte(fichier_carte)

		except TypeError :
			if carte != None :
				print("Mauvais type de nom de carte")
			self.creer()

		except FileNotFoundError :
			print("Carte 'carte_" + carte + ".txt' non trouvée dans le dossier cartes")
			self.creer()


	def creer(self) :

		self.nb_lignes = int(input("Entrez le nombre de lignes de la carte : "))
		self.nb_colonnes = int(input("Entrez le nombre de colonnes de la carte : "))

		self.carte = []

		for i in range(self.nb_lignes) :
			self.carte.append([])
			for j in range(self.nb_colonnes) :
				self.carte[i].append(00)

	def charger_carte(self, fichier_carte) :

		self.carte = []
		
		fichier = fichier_carte.read().split("\n") 
		for i in range(len(fichier)) :
			self.carte.append([a for a in fichier[i].split() if a != ''])
		del(self.carte[len(self.carte) - 1])
		
		self.nb_lignes = len(self.carte)
		self.nb_colonnes = len(self.carte[0])
		print(self.carte,self.nb_colonnes, self.nb_lignes)

	def event_init(self) :
		@self.window.event
		def on_key_press(symbol, modifiers) :
			if symbol == pyglet.window.key.RIGHT :
				self.cx += 1
			elif symbol == pyglet.window.key.LEFT : 
				self.cx -= 1
			elif symbol == pyglet.window.key.UP :
				self.cy += 1
			elif symbol == pyglet.window.key.DOWN :
				self.cy -= 1

			self.window.clear()
			self.afficher()

			if symbol in (pyglet.window.key.DOWN, pyglet.window.key.UP, pyglet.window.key.LEFT, pyglet.window.key.RIGHT) :
				pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [curs[0] * taille_case, curs[1] * taille_case, (curs[0] + 1) * taille_case, curs[1] * taille_case, (curs[0] + 1) * taille_case, (curs[1] + 1) * taille_case, curs[0] * taille_case, (curs[1] + 1) * taille_case]), ('c4B', (255, 0, 0, 0)*4))

	def afficher(self) :
		for i in range(len(self.carte)) :
			for j in self.carte[i] :
				pass

if __name__ == "__main__" :
	carte = Carte("defaut")

	pyglet.app.run()
