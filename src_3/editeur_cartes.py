# -*-coding:utf-8-*-

# # # # # # # # # # # # # # # # #
#                               #
#         Projet de MDD         #
#                               #
#  fichier : editeur_cartes.py  #
#                               #
# # # # # # # # # # # # # # # # #

# Importation des modules fournis avec python :
import time
import os
import random

# Importation du module Pyglet pour python 3. Si il n'est pas trouvé sur le système, on utilise la version présente dans le dossier src :
import pyglet
print("Utilisation de la version de pyglet du dossier src/ (", pyglet.version, ").\n")

# Importation des constantes :
import constantes as cs
# Importation de notre module qui gère la carte et la position du joueur :
import m_carte as mc

class Map(mc.Carte):
    """Classe qui hérite de la classe map"""
    
    def __init__(self,carte=None):
        mc.Carte.__init__(self,carte)
        self._nb_colonnes, self._nb_lignes = self.nb_colonnes, self.nb_lignes
        print(self._nb_colonnes,self._nb_lignes,self.nb_colonnes,nb_lignes)

    def _get_nb_colonnes(self):
        return self._nb_colonnes
    def _set_nb_colonnes(self, new_nb):
        if new_nb > self.nb_colonnes:
            for j in range(new_nb):
                for i in self.carte:
                    i.append(cs.NOGO)
        elif new_nb < self.nb_colonnes:
            for j in range(new_nb):
                for i in self.carte.carte:
                    del i[-1]

    nb_colonnes = property(_get_nb_colonnes, _set_nb_colonnes)

    def _get_nb_lignes(self):
        return self._nb_lignes
    def _set_nb_lignes(self, new_nb):
        if new_nb > self.nb_lignes:
                self.carte.append([cs.NOGO for i in range(self.carte[i])])
        elif new_nb < self.nb_lignes:
            del self.carte[-1]

    nb_lignes = property(_get_nb_lignes, _set_nb_lignes)

class Editeur(object):
    """Classe qui gère l'éditeur de carte."""

    def __init__(self, carte=None):

        # Si un nom de carte est donné, on essaie de la charger
        # Si ladite carte n'existe pas, on en crée une :
        if carte is not None:
            try:
                carte = Map(carte)
            except FileNotFoundError:
                print(u" Fichier carte introuvable !!!")
                self.creer()
        # Sinon, on en crée une :
        else:
            self.creer()

        # On crée la fenêtre pyglet de la taille de la carte à charger, plus une ligne pour les informations :
        self.window = pyglet.window.Window(width=self.nb_colonnes * cs.TAILLE_CASE, height=(self.nb_lignes + 1) * cs.TAILLE_CASE)

        # On initialise les événements :
        self.event_init()

        # On initialise le type actif à la plaine :
        self._type_actif = cs.PLAINE

        # On affiche la carte de base.
        self.afficher()

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

    def creer(self):
        """Demande le nom, le nombre de colonnes et de lignes et crée une carte remplie de plaines"""

        self.nom = input(u"Entrez le nom de la nouvelle carte : ")
        self.carte.nb_lignes = int(input(u"Entrez le nombre de lignes de la carte : "))
        self.carte.nb_colonnes = int(input(u"Entrez le nombre de colonnes de la carte : "))

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
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [(self.cx + 0.15) * cs.TAILLE_CASE, (self.cy + 0.15) * cs.TAILLE_CASE, (self.cx + 0.85) * cs.TAILLE_CASE, (self.cy + 0.15) * cs.TAILLE_CASE, (self.cx + 0.85) * cs.TAILLE_CASE, (self.cy + 0.85) * cs.TAILLE_CASE, (self.cx + 0.15) * cs.TAILLE_CASE, (self.cy + 0.85) * cs.TAILLE_CASE]), ('c4B', (255, 0, 0, 0) * 4))
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [(self.cx + 0.20) * cs.TAILLE_CASE, (self.cy + 0.20) * cs.TAILLE_CASE, (self.cx + 0.80) * cs.TAILLE_CASE, (self.cy + 0.20) * cs.TAILLE_CASE, (self.cx + 0.80) * cs.TAILLE_CASE, (self.cy + 0.80) * cs.TAILLE_CASE, (self.cx + 0.20) * cs.TAILLE_CASE, (self.cy + 0.80) * cs.TAILLE_CASE]), cs.COULEURS[self.type_actif])

    def afficher(self):
        """Afficher la carte selon le code couleurs définit au début."""

        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [j * cs.TAILLE_CASE, (self.nb_lignes - i) * cs.TAILLE_CASE, (j + 1) * cs.TAILLE_CASE, (self.nb_lignes - i) * cs.TAILLE_CASE, (j + 1) * cs.TAILLE_CASE, ((self.nb_lignes - i) - 1) * cs.TAILLE_CASE, j * cs.TAILLE_CASE, ((self.nb_lignes - i) - 1) * cs.TAILLE_CASE]), cs.COULEURS[self.carte[i][j]])


# Exécution du programme
if __name__ == "__main__":
    edit = Editeur(cs.CARTE)
    pyglet.app.run()
