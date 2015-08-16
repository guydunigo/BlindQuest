# -*- coding: utf-8 -*-

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


class Editeur(object):
    """Classe qui gère l'éditeur de carte."""

    def __init__(self, type_carte=None):

        # On initialise le type actif à la plaine :
        self._type_actif = cs.PLAINE
        # Initialisation de la position du joueur :
        self._posx = 0
        self._posy = 0
        # On sauvegarde le nom de la carte :
        self.type_carte = type_carte
        # On définit l'état de base de l'éditeur :
        self.state = "edit"

        # Si un nom de carte est donné, on essaie de la charger
        # Si ladite carte n'existe pas, on en crée une :
        if type_carte is not None:
            try:
                self.carte = self.ouvrir_fichier_carte("cartes", "carte_" + str(type_carte))
            except FileNotFoundError:
                print(u" Fichier carte introuvable !!! Création d'une nouvelle carte.")
                self.creer()
        # Sinon, on en crée une :
        else:
            self.creer()

        # On crée la fenêtre pyglet de la taille de la carte à charger, plus une ligne pour les informations :
        self.window = pyglet.window.Window(width=self.nb_colonnes * cs.TAILLE_CASE, height=(self.nb_lignes + 1) * cs.TAILLE_CASE)

        # On initialise les événements :
        self.event_init()

        # On affiche la carte de base.
        # self.afficher()

    def __repr__(self):
        """Méthode spéciale appelée lors d'un print de l'objet.
        En clair : print(carte) donne un tableau de valeurs de la carte comme représenté dans le fichier carte."""
        string = ""
        for i in self.carte:
            for j in i:
                if len(str(j)) == 1:
                    string += '0' + str(j) + ' '
                else:
                    string += str(j) + ' '
            string += '\n'
        return string

    # Encapsulation pour l’abscisse du joueur (posx) :
    def _get_posx(self):
        """Accesseur de l'attribut posx"""
        return self._posx

    def _set_posx(self, new_posx):
        """Mutateur de l'attribut posx.
        Si la nouvelle valeur est sur la carte et n'est pas un lieu impraticable (définis dans le fichier 'constantes.py'), alors elle est attribuée à l'attribut.
        Si new_posx dépasse les limites de la carte, on retourne de l'autre côté."""
        while new_posx < 0 and new_posx >= self.nb_colonnes:
            if new_posx < 0:
                new_posx = self.nb_colonnes + new_posx
            elif new_posx >= self.nb_colonnes:
                new_posx -= self.nb_colonnes
        self._posx = new_posx

    posx = property(_get_posx, _set_posx)

    # Encapsulation pour l'ordonnée du joueur (posy) :
    def _get_posy(self):
        """Accesseur de l'attribut posy"""
        return self._posy

    def _set_posy(self, new_posy):
        """Mutateur de l'attribut posy.
        Si la nouvelle valeur est sur la carte et n'est pas un lieu impraticable (définis dans le fichier 'constantes.py'), alors elle est attribuée à l'attribut.
        Si new_posy dépasse les limites de la carte, on retourne de l'autre côté."""
        while new_posy < 0 and new_posy >= self.nb_colonnes:
            if new_posy < 0:
                new_posy = self.nb_lignes + new_posy
            elif new_posy >= self.nb_lignes:
                new_posy -= self.nb_lignes
        self._posy = new_posy

    posy = property(_get_posy, _set_posy)

    # Encapsulation pour la case du joueur :
    def _get_case(self):
        """Accesseur de l'attribut case"""
        return self.carte[self.posy][self.posx]

    def _set_case(self, new_case):
        """Mutateur de l'attribut case.
        Permet de modifier la case du joueur si le type existe."""
        if new_case in cs.CONV:
            self.carte[self.posy][self.posx] = new_case

    case = property(_get_case, _set_case)

    def _get_nb_colonnes(self):
        return len(self.carte[0])

    def _set_nb_colonnes(self, new):
        if new > self.nb_colonnes:
            for a in range(self.nb_colonnes - new):
                for i in self.carte:
                    i.append(cs.BORDURE)
        elif new < self.nb_colonnes and a >= 1:
            for a in range(new):
                for i in self.carte:
                    del i[-1]

    nb_colonnes = property(_get_nb_colonnes, _set_nb_colonnes)

    def _get_nb_lignes(self):
        return len(self.carte)

    def _set_nb_lignes(self, new):
        if new > self.nb_lignes:
            for a in range(self.nb_lignes - new):
                self.carte.append([cs.BORDURE for i in range(self.nb_colonnes)])
        elif new < self.nb_lignes:
            for a in range(new):
                del self.carte[-1]

    nb_lignes = property(_get_nb_lignes, _set_nb_lignes)

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

    def event_init(self):
        """Crée les événements clavier."""

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.RIGHT:
                self.posx += 1
            elif symbol == pyglet.window.key.LEFT:
                self.posx -= 1
            elif symbol == pyglet.window.key.UP:
                self.posy += 1
            elif symbol == pyglet.window.key.DOWN:
                self.posy -= 1
            elif symbol in (pyglet.window.key.PLUS, pyglet.window.key.NUM_ADD, pyglet.window.key.GREATER):
                self.type_actif += 1
            elif symbol in (pyglet.window.key.MINUS, pyglet.window.key.NUM_SUBTRACT, pyglet.window.key.LESS):
                self.type_actif -= 1
            elif symbol == pyglet.window.key.SPACE:
                self.carte[self.nb_lignes - self.posy - 1][self.posx] = self.type_actif
            elif symbol == pyglet.window.key.H:
                self.help()
            elif symbol == pyglet.window.key.A:
                self.nb_colonnes += 1
            elif symbol == pyglet.window.key.Z:
                self.nb_colonnes -= 1
            elif symbol == pyglet.window.key.Q:
                self.nb_lignes += 1
            elif symbol == pyglet.window.key.S:
                self.nb_lignes -= 1

        @self.window.event
        def on_draw():
            # On rafraîchit l'écran.
            self.window.clear()
            self.afficher()
            # On affiche un carré de la couleur du type de carte actif, au centre de la case séléctionnée.
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [(self.posx + 0.15) * cs.TAILLE_CASE, (self.posy + 0.15) * cs.TAILLE_CASE, (self.posx + 0.85) * cs.TAILLE_CASE, (self.posy + 0.15) * cs.TAILLE_CASE, (self.posx + 0.85) * cs.TAILLE_CASE, (self.posy + 0.85) * cs.TAILLE_CASE, (self.posx + 0.15) * cs.TAILLE_CASE, (self.posy + 0.85) * cs.TAILLE_CASE]), ('c4B', (255, 0, 0, 0) * 4))
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [(self.posx + 0.20) * cs.TAILLE_CASE, (self.posy + 0.20) * cs.TAILLE_CASE, (self.posx + 0.80) * cs.TAILLE_CASE, (self.posy + 0.20) * cs.TAILLE_CASE, (self.posx + 0.80) * cs.TAILLE_CASE, (self.posy + 0.80) * cs.TAILLE_CASE, (self.posx + 0.20) * cs.TAILLE_CASE, (self.posy + 0.80) * cs.TAILLE_CASE]), cs.COULEURS[self.type_actif])

    def afficher(self):
        """Afficher la carte selon le code couleurs définit au début."""

        if self.state == "normal":
            for i in range(self.nb_lignes):
                for j in range(self.nb_colonnes):
                    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [j * cs.TAILLE_CASE, (self.nb_lignes - i) * cs.TAILLE_CASE, (j + 1) * cs.TAILLE_CASE, (self.nb_lignes - i) * cs.TAILLE_CASE, (j + 1) * cs.TAILLE_CASE, ((self.nb_lignes - i) - 1) * cs.TAILLE_CASE, j * cs.TAILLE_CASE, ((self.nb_lignes - i) - 1) * cs.TAILLE_CASE]), cs.COULEURS[self.carte[i][j]])

        elif self.state == "help":
            height = 2
            for i in cs.CONV:
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [20, height * cs.TAILLE_CASE, 20 + cs.TAILLE_CASE, height * cs.TAILLE_CASE, 20 + cs.TAILLE_CASE, (height + 1) * cs.TAILLE_CASE, 20, (height + 1) * cs.TAILLE_CASE]), cs.COULEURS[i])
                pyglet.text.Label(cs.CONV[i], x=20 + cs.TAILLE_CASE, y=height).draw()
                height += 1

    def creer(self):
        """Demande le nom, le nombre de colonnes et de lignes et crée une carte remplie de plaines"""

        self.type_carte = input(u"Entrez le nom de la nouvelle carte : ")
        self.nb_lignes = int(input(u"Entrez le nombre de lignes de la carte : "))
        self.nb_colonnes = int(input(u"Entrez le nombre de colonnes de la carte : "))

    def help(self):
        """Affiche l'aide (commandes et la légende."""

        if self.state == "edit":
            self.state = "help"
        else:
            self.state = "edit"

    def ouvrir_fichier_carte(self, dossier, nom_fichier):
        """Charge la carte du fichier nommé 'nom_fichier.txt', présent dans le dossier donné (classiquement saves ou cartes), sous la forme d'un liste de listes d'entiers.
        Une erreur est levée si le dossier ou le fichier n'existe pas.
        Ne pas oublier d'utiliser la méthode get_player_info si on charge une sauvegarde."""

        if dossier in os.listdir('.') and str(nom_fichier) + ".txt" in os.listdir(dossier):
            with open(os.path.join(dossier, str(nom_fichier) + ".txt"), 'r') as fichier_carte:
                self.charger_carte(fichier_carte)
        else:
            raise FileNotFoundError("Il n'existe pas de fichier carte nommé {} dans le dossier '{}'.".format(nom_fichier + ".txt", dossier))

    def charger_carte(self, fichier_carte):
        """Charge le contenu d'un fichier carte dans une liste de liste de int, si les lignes ne sont pas toutes de la même taille, on les complète par de l'eau."""

        # On initialise la liste carte :
        self.carte = []

        # On récupère les lignes sous forme de chaîne de caractères rangés dans une liste :
        fichier = fichier_carte.read().split("\n")
        # On récupère les entiers séparés par des espaces dans chaque élément de la liste :
        try:
            for i in range(len(fichier) - 1):
                self.carte.append([int(a) for a in fichier[i].split() if a != ''])
        except ValueError:
            raise ValueError("FICHIER CARTE CORROMPU : Un caractère présent sur la carte n'est pas un nombre")

        # On enlève la dernière ligne créée inutilement si un retour à une ligne vide a été fait à la fin du fichier carte :
        if self.carte[-1] == []:
            del(self.carte[-1])

        # On compte le nombre de lignes :
        nb_lignes = len(self.carte)
        # On compte le nombre de colonnes et on complète les lignes de taille différente par de l'eau
        # Init la variable :
        nb_colonnes = 0
        # On recherche la ligne la plus grande :
        for liste in self.carte:
            if nb_colonnes < len(liste):
                nb_colonnes = len(liste)
        # On complète par de l'eau:
        for liste in self.carte:
            while len(liste) < nb_colonnes:
                liste.append(cs.EAU)

    def save(self, player_info):  # A modif
        """Sauvegarde dans un fichier la carte et les informations du joueur (position, vie, ...)
        Sauvegarde dans le fichier de sauvegarde nommé sous la forme : "typeCarte_num.txt" dans le dossier saves s'il existe, sinon il sera créé.
        (player_info : une liste contenant la vie et d'autres informations concernant du joueur)"""

        sauv = self.carte
        sauv.append([self.posx, self.posy] + player_info)

        # Si il n'existe pas de dossier saves, on en crée un :
        if "saves" not in os.listdir():
            os.mkdir("saves")
            num_sauv = "0"
        # Sinon on recherche les sauvegardes existantes de la carte utilisée et on prend le numéro directement supérieur :
        else:
            list_sauv = [i.replace(self.type_carte + '_', '').replace(".txt", '') for i in os.listdir("saves") if self.type_carte in i] + ['0']
            list_sauv.sort()
            num_sauv = str(int(list_sauv[-1]) + 1)

        # On écrit dans le fichier :
        with open("saves/{}.txt".format(self.type_carte + "_" + num_sauv), 'w') as fichier:
            for i in sauv:
                for j in i:
                    if j < 10:
                        j = '0' + str(j)
                    else:
                        j = str(j)
                    fichier.write(j + " ")
                fichier.write("\n")

# Exécution du programme
if __name__ == "__main__":
    edit = Editeur("defaut")
    pyglet.app.run()
