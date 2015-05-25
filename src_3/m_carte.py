# -*-coding:utf-8-*-

# # # # # # # # # # # # # # # # #
#                               #
#         Projet de MDD         #
#                               #
#     fichier : m_carte.py      #
#                               #
# # # # # # # # # # # # # # # # #

# Importation des modules fournis avec python :
import os

# Importation du module contenant les constantes :
import constantes as cs


class Carte (object):
    """Classe qui gère la carte et s'occupe de l'emplacement et du déplacement du joueur."""

    def __init__(self, type_carte="defaut", num_sauv=None):
        """Constructeur : Charge la carte dans une liste de listes (attribut carte) et définit la position par défaut du joueur (attributs posx et posy), et stocke le nom de la carte (attribut type_carte).
        Il existe un attribut 'case' qui donne le type de case sur laquelle le joueur se trouve, cet attribut permet aussi de modifier cette case.
        - Arguments :
      carte_type : Nom de la carte utilisée
      num_sauv : Si définit, il charge une sauvegarde, cet argument indique le numéro de la sauvegarde à charger.
     """

        # Initialisation de la position du joueur :
        self._posx = 0
        self._posy = 0
        # On sauvegarde le nom de la carte :
        self.type_carte = type_carte

        # Si on n'a pas de valeur donnée pour num_sauv (le numéro de la sauvegarde), on ouvre une carte nommée carte_NOM.txt dans le dossier cartes et on recherche le départ (codé 98).
        if num_sauv is None:

            self.ouvrir_fichier_carte("cartes", "carte_" + str(type_carte))
            self.trouver_depart()
            self.player_info = []

        # Lors du chargement de sauvegardes (quand num_sauv est définit) :
        else:
            self.ouvrir_fichier_carte("saves", type_carte + "_" + num_sauv)
            self.get_player_info()

    # Encapsulation pour l’abscisse du joueur (posx) :
    def _get_posx(self):
        """Accesseur de l'attribut posx"""
        return self._posx

    def _set_posx(self, new_posx):
        """Mutateur de l'attribut posx.
        Si la nouvelle valeur est sur la carte et n'est pas un lieu impraticable (définis dans le fichier 'constantes.py'), alors elle est attribuée à l'attribut.
        Si new_posx dépasse les limites de la carte, on retourne de l'autre côté."""
        if new_posx < 0:
            new_posx = self.nb_colonnes + new_posx
        elif new_posx >= self.nb_colonnes:
            new_posx -= self.nb_colonnes
        if new_posx >= 0 and new_posx < self.nb_colonnes:
            if self.carte[self.posy][new_posx] not in cs.NOGO:
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
        if new_posy < 0:
            new_posy = self.nb_lignes + new_posy
        elif new_posy >= self.nb_lignes:
            new_posy -= self.nb_lignes
        if self.carte[new_posy][self.posx] not in cs.NOGO:
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
        self.nb_lignes = len(self.carte)
        # On compte le nombre de colonnes et on complète les lignes de taille différente par de l'eau
        # Init la variable :
        self.nb_colonnes = 0
        # On recherche la ligne la plus grande :
        for liste in self.carte:
            if self.nb_colonnes < len(liste):
                self.nb_colonnes = len(liste)
        # On complète par de l'eau:
        for liste in self.carte:
            while len(liste) < self.nb_colonnes:
                liste.append(cs.EAU)

    def get_player_info(self):
        """Lors du chargement d'une sauvegarde, la dernière ligne de la liste carte est une liste d'informations du joueur sous la forme [posx, posy, vie, bonus...].
        Cette méthode stocke cette liste sans les informations concernant la position du joueur qui sont, elles, rangées dans leur attribut correspondant."""

        # On récupère la dernière ligne :
        self.player_info = self.carte[-1]
        # On récupère l'abscisse et l'ordonnée du joueur et on les enlève de player_info :
        self.posx, self.posy = self.player_info[0:2]
        del self.player_info[0:2]
        # On enlève la dernière ligne de la carte :
        del self.carte[-1]
        # On met à jour le nombre de lignes :
        self.nb_lignes -= 1

    def trouver_depart(self):
        """Trouve les coordonnées du départ et les range dans posx et posy."""

        # Initialisation des variables :
        i, j = 0, 0
        found = False

        # Boucle des ordonnées :
        while not found and j < len(self.carte):
            i = 0
            # Boucle des abscisses :
            while not found and i < len(self.carte):
                if self.carte[j][i] == cs.DEPART:
                    self._posx, self._posy = i, j
                    found = True
                i += 1
            j += 1

        # Si la valeur de départ n'est pas trouvée, on lève une erreur de valeur (ça paraît logique) :
        if not found:
            raise ValueError("Aucune case de départ (codée {}) n'a été trouvée sur la carte.".format(cs.DEPART))

    def move(self, direction=None):
        """Fonction qui déplace le joueur et renvoie le code de la case d'arrivée du joueur.
        direction : prend un chaîne de caractère parmi ("OUEST", "EST", "NORD", "SUD").
          Si il n'est pas définit (ou à None du coups), le joueur ne bouge pas.
        Quand le joueur ne bouge pas, on revoie None."""

        # On copie les coordonnées du joueur avant le déplacement :
        x, y = self.posx, self.posy

        # On bouge le joueur en fonction de la direction choisie :
        if direction == "NORD":
            self.posy -= 1
        elif direction == "SUD":
            self.posy += 1
        elif direction == "OUEST":
            self.posx -= 1
        elif direction == "EST":
            self.posx += 1

        # Si le joueur n'a pas bougé, on renvoie None :
        if x == self.posx and y == self.posy:
            return None

        # On renvoie le code de la case ainsi que, à partir des centaines, le code de proximité :
        return self.case + self.detect_prox() * 100

    def detect_prox(self):
        """Renvoie un entier composé au maximum de 4 (pour les point cardinaux) puissances de 2 différentes additionnées pour l'utilisation de l'opérateur bit à bit."""

        # Initialisation de la variable qui sera retournée :
        detect = 0
        # On regarde si les différents types qui doivent être détectés sont à proximité :
        for prox in cs.PROX:
            # NORD :
            if self.carte[self.posy - 1][self.posx] == prox:
                detect |= cs.PROX[prox]
            # SUD :
            if self.posy < self.nb_lignes - 1:
                if self.carte[self.posy + 1][self.posx] == prox:
                    detect |= cs.PROX[prox]
            else:
                if self.carte[0][self.posx] == prox:
                    detect |= cs.PROX[prox]
            # OUEST :
            if self.carte[self.posy][self.posx - 1] == prox:
                detect |= cs.PROX[prox]
            # EST :
            if self.posx < self.nb_colonnes - 1:
                if self.carte[self.posy][self.posx + 1] == prox:
                    detect |= cs.PROX[prox]
            else:
                if self.carte[self.posy][0] == prox:
                    detect |= cs.PROX[prox]

        return detect

    def empty(self):
        """Méthode qui affecte à la case actuelle la valeur de la case à l'ouest si elle existe et si ce n'est pas la case départ, bonus, ou de combat ou une case où le joueur ne peut aller, sinon à l'est, au nord et enfin au sud.
        Si aucune des cases environnantes n'est utilisable, on utilise la plaine.
        Renvoie le code de la nouvelle case actuelle.
        Par exemple : après avoir récupéré un bonus ou après avoir tué un monstre."""

        redefinie = False

        # On parcoure les cases aux points cardinaux :
        for x, y in [(self.posx - 1, self.posy), (self.posx + 1, self.posy), (self.posx, self.posy - 1), (self.posx, self.posy + 1)]:
            # Si la case n'est pas la case départ, un bonus, une case de combat, de non go, on affecte la nouvelle valeur :
            if not redefinie and x >= 0 and x < self.nb_colonnes - 1 and y >= 0 and y < self.nb_lignes - 1 and self.carte[y][x] not in cs.NOGO + (cs.DEPART, cs.BONUS) and self.carte[y][x] not in cs.COMBAT_START:
                # On affecte la nouvelle valeur :
                self.case = self.carte[y][x]
                # On indique que l'on a redéfini la case :
                redefinie = True

        # Si malgré tout, il n'y a pas de case adjacente adéquate, on utilise la plaine :
        if not redefinie:
            self.case = cs.PLAINE

        # On retourne la nouvelle valeur de la case :
        return self.case + self.detect_prox() * 100

    def save(self, player_info):
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
