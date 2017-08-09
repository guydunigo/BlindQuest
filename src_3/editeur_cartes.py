# -*-coding:utf-8-*-

# # # # # # # # # # # # # # # # #
#                               #
#         Projet de MDD         #
#                               #
#  fichier : editeur_cartes.py  #
#                               #
# # # # # # # # # # # # # # # # #

# Importation du module Pyglet pour python 3. Si il n'est pas trouvé sur le système, on utilise la version présente dans le dossier src :
import pyglet
print("Utilisation de la version de pyglet du dossier src/ (", pyglet.version, ").\n")

# Importation des constantes :
import constantes as cs

class Editeur(object):
    """Classe qui gère l'éditeur de carte."""

    def __init__(self, carte=None):

        self.ouvrir_carte(carte)
        self.window = pyglet.window.Window(width=self.nb_colonnes * cs.TAILLE_CASE, height=self.nb_lignes * cs.TAILLE_CASE)
        self.event_init()

        # Coordonnées du curseur :
        self._cx = 0
        self._cy = 0

        self._type_actif = 0

    def _get_cx(self):
        """Accesseur de l'absisse du curseur"""
        return self._cx

    def _set_cx(self, new_cx):
        """Mutateur de l'absisse du curseur"""
        if new_cx >= self.nb_colonnes:
            self._cx = 0
        elif new_cx < 0:
            self._cx = self.nb_colonnes - 1
        else:
            self._cx = new_cx
    cx = property(_get_cx, _set_cx)

    def _get_cy(self):
        """Accesseur de l'ordonné du curseur"""
        return self._cy

    def _set_cy(self, new_cy):
        """Mutateur de l'ordonné du curseur"""
        if new_cy >= self.nb_lignes:
            self._cy = 0
        elif new_cy < 0:
            self._cy = self.nb_lignes - 1
        else:
            self._cy = new_cy
    cy = property(_get_cy, _set_cy)

    def _get_type_actif(self):
        """Accesseur du type d'environnement actif."""
        return self._type_actif

    def _set_type_actif(self, new_type):
        """Mutateur du type d'environnement actif.
        Si la valeur proposée correspond à un type existant sinon si la valeur proposée est plus grande que la valeur actuelle, on prend la valeur directement supérieure et inversement.
"""
        if new_type < self._type_actif:
            if new_type < 00:
                new_type = 99
            while new_type not in cs.COULEURS:
                new_type -= 1
        elif new_type > self._type_actif:
            if new_type > 99:
                new_type = 00
            while new_type not in cs.COULEURS:
                new_type += 1

        self._type_actif = new_type
    type_actif = property(_get_type_actif, _set_type_actif)

    def ouvrir_carte(self, carte):
        """Essaye d'ouvrir la carte carte_nom.txt (où nom est une chaîne de caractères contenue dans l'argument carte) dans le dossier cartes. Si un mauvais nom est donné ou que la carte n'éxiste pas, on crée une nouvelle carte."""

        try:
            with open("./cartes/carte_" + carte + ".txt", "r") as fichier_carte:
                self.charger_carte(fichier_carte)
                self.nom = carte

        except TypeError:
            if carte is not None:
                print("Mauvais type de nom de carte")
            self.creer()

        except FileNotFoundError:
            print("Carte 'carte_" + carte + ".txt' non trouvée dans le dossier cartes")
            self.creer()

    def creer(self):
        """Demande le nom, le nombre de colonnes et de lignes et crée une carte remplie de plaines"""

        self.nom = input("Entrez le nom de la nouvelle carte :")
        self.nb_lignes = int(input("Entrez le nombre de lignes de la carte : "))
        self.nb_colonnes = int(input("Entrez le nombre de colonnes de la carte : "))

        self.carte = []

        for i in range(self.nb_lignes):
            self.carte.append([])
            for j in range(self.nb_colonnes):
                self.carte[i].append(00)

    def charger_carte(self, fichier_carte):
        """Charge le contenu d'un fichier carte dans une liste et met à jour en conséquence le nombre de colonnes et de lignes."""

        self.carte = []

        fichier = fichier_carte.read().split("\n")
        for i in range(len(fichier)):
            self.carte.append([int(a) for a in fichier[i].split() if a != ''])
        del(self.carte[len(self.carte) - 1])
        if self.carte[len(self.carte) - 1] == []:
            del(self.carte[len(self.carte) - 1])

        self.nb_lignes = len(self.carte)
        self.nb_colonnes = len(self.carte[0])
        print(self.carte, self.nb_colonnes, self.nb_lignes)

    def event_init(self):
        """Crée les événements clavier."""

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.RIGHT:
                self.cx += 1
            elif symbol == pyglet.window.key.LEFT:
                self.cx -= 1
            elif symbol == pyglet.window.key.UP:
                self.cy += 1
            elif symbol == pyglet.window.key.DOWN:
                self.cy -= 1
            elif symbol in (pyglet.window.key.PLUS, pyglet.window.key.NUM_ADD, pyglet.window.key.GREATER):
                self.type_actif += 1
            elif symbol in (pyglet.window.key.MINUS, pyglet.window.key.NUM_SUBTRACT, pyglet.window.key.LESS):
                self.type_actif -= 1
            elif symbol == pyglet.window.key.SPACE:
                self.carte[self.nb_lignes - self.cy - 1][self.cx] = self.type_actif

        @self.window.event
        def on_draw():
            # On raffraichit l'écran.
            self.window.clear()
            self.afficher()
            # On affiche un carré de la couleur du type de carte actif, au centre de la case séléctionnée.
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
            ('v2f', [(self.cx + 0.15) * cs.TAILLE_CASE, (self.cy + 0.15) * cs.TAILLE_CASE,
            (self.cx + 0.85) * cs.TAILLE_CASE, (self.cy + 0.15) * cs.TAILLE_CASE, (self.cx + 0.85) * cs.TAILLE_CASE,
            (self.cy + 0.85) * cs.TAILLE_CASE, (self.cx + 0.15) * cs.TAILLE_CASE, (self.cy + 0.85) * cs.TAILLE_CASE]),
            ('c4B', (255, 0, 0, 0) * 4))
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [(self.cx + 0.20) * cs.TAILLE_CASE,
            (self.cy + 0.20) * cs.TAILLE_CASE, (self.cx + 0.80) * cs.TAILLE_CASE, (self.cy + 0.20) * cs.TAILLE_CASE,
            (self.cx + 0.80) * cs.TAILLE_CASE, (self.cy + 0.80) * cs.TAILLE_CASE, (self.cx + 0.20) * cs.TAILLE_CASE,
            (self.cy + 0.80) * cs.TAILLE_CASE]), cs.COULEURS[self.type_actif])

    def afficher(self):
        """Afficher la carte selon le code couleurs définit au début."""

        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f',
                [j * cs.TAILLE_CASE, (self.nb_lignes - i) * cs.TAILLE_CASE,
                (j + 1) * cs.TAILLE_CASE,
                (self.nb_lignes - i) * cs.TAILLE_CASE, (j + 1) * cs.TAILLE_CASE,
                ((self.nb_lignes - i) - 1) * cs.TAILLE_CASE,
                j * cs.TAILLE_CASE, ((self.nb_lignes - i) - 1) * cs.TAILLE_CASE]),
                cs.COULEURS[self.carte[i][j]])


# Exécution du programme
if __name__ == "__main__":

    CARTE = Editeur(cs.CARTE)

    pyglet.app.run()
