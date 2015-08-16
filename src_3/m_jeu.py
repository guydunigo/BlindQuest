# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # #
#                               #
#         Projet de MDD         #
#                               #
#       fichier : m_jeu.py      #
#                               #
# # # # # # # # # # # # # # # # #

# Importation des modules fournis avec python :
import time
import os
import random

# Importation du module Pyglet pour python 3. Si il n'est pas trouvé sur le système, on utilise la version présente dans le dossier src :
import pyglet
print("Utilisation de la version de pyglet du dossier source (", pyglet.version, ").\n")

# Importation des constantes :
import constantes as cs
# Importation de notre module qui gère la carte et la position du joueur :
import m_carte as mc


class Jeu (object):
    """Classe qui gère le jeu, la Bibliothèque pyglet, les événements claviers, la fenêtre et le son."""

    def __init__(self, type_carte="defaut"):
        """Constructeur :
      carte_type : type de carte à utiliser durant le jeu. (carte nommée selon l'exemple : carte_NOM.txt et placée dans le dossier cartes)"""

        # Si le dossier de travail de python (le dossier depuis lequel python a été lancé) est le dossier du code source ('src_3'), on va dans le dossier principal.
        if "/src_3" in os.getcwd()[-6:]:
            print(u"Le programme a été lancé depuis le dossier src_3, changement du dossier vers le dossier parent (dossier principal du projet).\n")
            os.chdir("../")
        # Réglage du dossier de travail de pyglet pour le dossier racine du projet, sinon il ne trouve pas les différents composants :
        working_dir = os.path.dirname(os.path.realpath(__file__))
        pyglet.resource.path = [os.path.join(working_dir, '..')]
        pyglet.resource.reindex()

        # On choisit d'utiliser openal pour l'audio. (pulseaudio ne marchait pas (segfaults))
        pyglet.options['audio'] = ('openal', )

        # Chargement de la carte :
        self.carte = mc.Carte(type_carte)
        # Chargement des sons :
        self.charger_sons()
        # Lecteurs (environnement(s), action(s), heartbeats,...) :
        self.creer_lecteurs()
        # Fenêtre (activation du plein écran par défaut) :
        self.creer_fenetre()
        # Création des événements :
        self.init_events()

        # Initialisation de la vie du personnage
        self._vie = cs.VIE

        # Initialisation de variables d'état ("debut", "combat", "normal") accompagné d'un H lorsque l'on affiche l'aide, C lors d'un chargement ou de S lors d'une sauvegarde et P lors de la mise ne pause :
        self.state = "debut"
        # Initialisation du numéro de sauvegarde qui sera chargée :
        self.num_sauv = ""
        # Initialisation de la liste des lecteurs en pause (par extension, indique si le jeu est en pause lorsqu'elle est vide) :
        self.paused = []

    # Encapsulation pour la vie du joueur :
    def _get_vie(self):
        """Accesseur de l'attribut vie"""
        return self._vie

    def _set_vie(self, new_vie):
        """Mutateur de l'attribut vie.
        Si la nouvelle valeur est inférieure ou égale à 3, on déclenche les battements de cœur pour avertir le joueur."""
        if new_vie > 0:
            self._vie = new_vie
        else:
            self._vie = 0

        if new_vie <= 3:
            self.lecteurs["heartbeat"].play()
            self.lecteurs["env"].volume = 0.3
        else:
            self.lecteurs["heartbeat"].pause()
            self.lecteurs["env"].volume = 0.7

    vie = property(_get_vie, _set_vie)

    def charger_sons(self):
        """Charge tous les sons du dossier 'sons' et les range dans un dictionnaire avec pour étiquette le nom du fichier son sans l'extension '.wav'.
    On charge les sons directement dans la mémoire sans streaming pour éviter les problèmes de 'source already queued'."""

        # On prévient que le temps de chargement est normal :
        print(u"Chargement des sons en mémoire...")

        # On crée le dictionnaire de sons :
        self.sons = {}

        if "sons" in os.listdir('.'):
            # On récupère la liste des fichiers du dossier 'sons' :
            liste_sons = os.listdir("sons")

            # On ne garde que les fichiers 'wav' :
            liste_sons = [fichier for fichier in liste_sons if fichier.find(".wav") != -1]

            # On ouvre les sons avec pyglet et on les range dans le dictionnaire 'sons' avec pour étiquette le nom du fichier son sans l'extension '.wav' :
            for son in liste_sons:
                self.sons[son.replace(".wav", '')] = pyglet.media.load(os.path.join("sons", son), streaming=False)
        else:
            # On lève une erreur si le dossier 'sons' n'a pas été trouvé.
            raise FileNotFoundError(u"Le dossier 'sons' n'a pas été trouvé.")

    def creer_lecteurs(self):
        """Crée les lecteurs pyglet, les lecteurs env, heartbeat, et les lecteurs de proximités (définis dans le fichier constantes) sont réglés pour tourner en boucle sur la musique en cours :
      - env : Pour l'environnement ou le combat, en boucle.
      - heartbeat : Si il ne reste qu'une vie, on entend un battement de cœur, en boucle.
      - Les différents sons de proximité ont leur propre lecteur, en boucle.
    """

        try:
            self.lecteurs = {}
            for lecteur in ("env", "heartbeat"):
                self.lecteurs[lecteur] = pyglet.media.Player()
                # En boucle
                self.lecteurs[lecteur].eos_action = self.lecteurs[lecteur].EOS_LOOP
                if lecteur == "env":
                    self.lecteurs[lecteur].volume = 0.7
                if lecteur == "heartbeat":
                    self.lecteurs[lecteur].queue(self.sons[lecteur])
                    self.lecteurs[lecteur].volume = 3.0

            # Création des lecteurs pour les sons de proximité, un lecteur par son, en boucle, volume faible.
            for lecteur in cs.PROX:
                self.lecteurs[lecteur] = pyglet.media.Player()
                self.lecteurs[lecteur].eos_action = self.lecteurs[lecteur].EOS_LOOP
                self.lecteurs[lecteur].queue(self.sons[cs.CONV[lecteur]])
                self.lecteurs[lecteur].volume = 0.7

            # On restitue l'environnement sonore de départ.
            self.lecteurs["env"].queue(self.sons[cs.CONV[cs.DEPART]])
            self.lecteurs["env"].play()

        except AttributeError:
            print(u"OpenAl n'est pas installé, veuillez l'installer si vous voulez jouer.")
            raise(FileNotFoundError, u"## OpenAl is missing ! ##")

    def creer_fenetre(self):
        """Crée la fenêtre pyglet en plein écran et affiche l'aide pendant 5 secondes."""
        self.window = pyglet.window.Window(fullscreen=True)

    def init_events(self):
        """Crée les événements :
      - claviers :
        - À tous moments :
          - ECHAP : Quitter
          - F : Plein écran
          - H : Aide
          - C : Charger une Sauvegarde
          - P : Mettre en pause et reprendre
        - Lors de pérégrinations diverses :
          - flèches directionnelles : se déplacer
          - S : Sauvegarder
        - Lors d'un combat :
        - ..."""

        @self.window.event
        def on_key_press(symbol, modifiers):
            # Fullscreen
            if symbol == pyglet.window.key.F:
                self.window.set_fullscreen(not self.window.fullscreen)
            # Aide
            elif symbol == pyglet.window.key.H:
                if 'H' not in self.state:
                    self.state += 'H'
            # Pause
            elif symbol == pyglet.window.key.P:
                self.pause()
            # Charger
            elif symbol == pyglet.window.key.C and "C" not in self.state:
                self.state += "C"
                self.num_sauv = ''

            # En cas de chargement :
            elif "C" in self.state:
                if symbol == pyglet.window.key.ENTER:
                    self.load()
                elif symbol == pyglet.window.key.NUM_0 or symbol == pyglet.window.key._0:
                    self.num_sauv += "0"
                elif symbol == pyglet.window.key.NUM_1 or symbol == pyglet.window.key._1:
                    self.num_sauv += "1"
                elif symbol == pyglet.window.key.NUM_2 or symbol == pyglet.window.key._2:
                    self.num_sauv += "2"
                elif symbol == pyglet.window.key.NUM_3 or symbol == pyglet.window.key._3:
                    self.num_sauv += "3"
                elif symbol == pyglet.window.key.NUM_4 or symbol == pyglet.window.key._4:
                    self.num_sauv += "4"
                elif symbol == pyglet.window.key.NUM_5 or symbol == pyglet.window.key._5:
                    self.num_sauv += "5"
                elif symbol == pyglet.window.key.NUM_6 or symbol == pyglet.window.key._6:
                    self.num_sauv += "6"
                elif symbol == pyglet.window.key.NUM_7 or symbol == pyglet.window.key._7:
                    self.num_sauv += "7"
                elif symbol == pyglet.window.key.NUM_8 or symbol == pyglet.window.key._8:
                    self.num_sauv += "8"
                elif symbol == pyglet.window.key.NUM_9 or symbol == pyglet.window.key._9:
                    self.num_sauv += "9"
            # En temps normal :
            elif self.state == "normal":
                # Déplacements
                if symbol == pyglet.window.key.UP:
                    self.move("NORD")
                elif symbol == pyglet.window.key.DOWN:
                    self.move("SUD")
                elif symbol == pyglet.window.key.RIGHT:
                    self.move("EST")
                elif symbol == pyglet.window.key.LEFT:
                    self.move("OUEST")
                # Sauvegarder
                elif symbol == pyglet.window.key.S:
                    self.save()
            # Durant un combat :
            elif self.state == "combat":
                if symbol == pyglet.window.key.E:
                    self.tour_combat()
            # Au début :
            elif self.state == "debut" and symbol == pyglet.window.key.SPACE:
                self.state = "normal"
            # A la fin, on ferme la fenêtre et on relance le jeu :
            elif self.state == "fin" and symbol == pyglet.window.key.SPACE:
                self.window.close()
                self.__init__(self.carte.type_carte)
                pyglet.app.run()

        @self.window.event
        def on_key_release(symbol, modifiers):
            if 'H' in self.state:
                self.state = self.state.replace('H', '')
            if 'S' in self.state:
                time.sleep(1)
                self.state = self.state.replace('S', '')

        @self.window.event
        def on_draw():
            """Méthode qui affiche les différentes informations selon l'état du jeu."""

            # On efface d'abord l'écran :
            self.window.clear()
            # Au début, on affiche l'aide et on demande d'appuyer sur 'ESPACE' pour commencer :
            if self.state == "debut":
                # On affiche l'aide :
                self.afficher_aide()
                # On affiche le message de bienvenue :
                pyglet.text.Label(u"Appuyez sur la touche ESPACE pour commencer...", x=20, y=20).draw()
            # Si on est en pause, on l'indique :
            elif self.paused != []:
                pyglet.text.Label("Partie en pause, appuyez sur la touche P pour reprendre...", x=20, y=20).draw()
            # Si le jeu est finit : on propose de redémarrer une partie :
            elif self.state == "fin":
                pyglet.text.Label("Fin du jeu, appuyez sur la touche ESPACE pour recommencer une partie...", x=20, y=20).draw()
            # Affichage de l'aide :
            if 'H' in self.state:
                self.afficher_aide()
            # On indique que l'on est en train de sauvegarder :
            if 'S' in self.state:
                pyglet.text.Label("Sauvegarde en cours...", x=20, y=20).draw()
            # On affiche la liste des sauvegardes et l'entrée utilisateur :
            elif 'C' in self.state:
                self.afficher_load()

    def move(self, direction=None):
        """Fonction qui déplace le joueur et gère ce qui peut y arriver (mort si environnement dangereux, combat...) et lance les sons d'environnement et de proximité.
      - direction : prend un chaîne de caractère parmi ("OUEST", "EST", "NORD", "SUD").
          Si il n'est pas définit (ou à None), le joueur ne bouge pas mais on met tout de même le son à jour (utile après avoir utilisé la méthode empty par exemple)."""

        # On déplace le joueur su la carte et on récupère le code de la case d'arrivée :
        case = self.carte.move(direction)
        if direction is None or case is not None:
            if case is not None:
                # On récupère les informations de proximité de la case (eau, pont...), qui sont écrites sous forme de mot binaire à partir des centaines :
                infos_prox = int(case / 100)
                case = case - infos_prox * 100

                # Si le joueur arrive sur une case létale, on active à la fin.
                if case in cs.DANGER:
                    self.fin(cs.DANGER[case])
                    # On renvoie None pour arrêter la fonction là :
                    return None
                # Si on arrive sur une case bonus, le joueur reprend toute sa vie et on entend le jingle associé :
                elif case == cs.BONUS:
                    # On joue le jingle :
                    self.sons[cs.CONV[cs.BONUS]].play()
                    # On remet la vie du joueur au maximum :
                    self.vie = cs.VIE
                    # On vide la case et on récupère le nouveau type d'environnement :
                    case = self.carte.empty()
                    # On met à jour les valeurs de case et de proximité :
                    infos_prox = int(case / 100)
                    case = case - infos_prox * 100
                # Si on arrive sur une case combat, on passe en mode combat, ... :
                elif case in cs.COMBAT_START:
                    self.combat_init()
            # Sinon on récupère les informations de la case actuelle :
            else:
                case = self.carte.case
                infos_prox = self.carte.detect_prox()

            print("code case : ", cs.CONV[case], ", ", case, ", code proximité : ", infos_prox)

            # Restitution de l'environnement actuel :
            # Si la source est déjà active, on la remet au début :
            if self.lecteurs["env"].source == self.sons[cs.CONV[case]] or self.lecteurs["env"].source in [self.sons[cs.CONV[i]] for i in cs.COMBAT_START]:
                self.lecteurs["env"].seek(0)
            else:
                self.lecteurs["env"].queue(self.sons[cs.CONV[case]])
                self.lecteurs["env"].next_source()

            # Détection des proximités et restitution du son associé :
            for prox in cs.PROX:
                if infos_prox & cs.PROX[prox] == cs.PROX[prox]:
                    self.lecteurs[prox].play()
                else:
                    self.lecteurs[prox].pause()

    def afficher_aide(self):
        """Fonction qui affiche l'aide (tiens, tiens...)."""

        pyglet.text.Label(u"\t\t\t\tBienvenue dans BlindQuest !\nVous traquerez les monstres en parcourant le monde grâce aux flèches directionnelles.", color=(255, 55, 25, 255), x=20, y=240, width=self.window.width, multiline=True).draw()
        pyglet.text.Label(u"La touche H vous permet d'afficher de nouveau cette aide.\n\
↑ pour aller au nord, ↓ pour le sud, ← pour l'ouest, et ⇥ pour l'est \n\
P met le jeu en pause et reprend la partie.\nF active et désactive le plein écran.\n\
E permet d'attaquer lors d'un combat.\nÉCHAP permet de quitter le jeu à tout moment.\n\
Enfin, appuyez sur C pour charger une partie préalablement sauvegardée avec la touche S.", color=(140, 140, 140, 255), x=20, y=180, width=self.window.width, multiline=True).draw()

    def fin(self, type_fin):
        """Fonction qui gère la fin selon s'il y a victoire ou mort, et s'occupe de quitter le programme.
      - type : chaîne de caractère décrivant la fin parmi celles se trouvant dans le fichier constantes, les fichiers sons associés doivent exister."""

        # On restitue le sons associé à la mort :
        self.lecteurs["env"].eos_action = self.lecteurs["env"].EOS_STOP
        self.lecteurs["env"].next()
        self.lecteurs["env"].next()
        self.lecteurs["env"].queue(self.sons[type_fin])
        self.lecteurs["env"].play()

        # On arrête le heartbeat :
        self.lecteurs["heartbeat"].pause()

        # On met en pause les lecteurs de proximité :
        for i in cs.PROX:
            self.lecteurs[i].pause()

        # On active l'état fin qui empêche de se déplacer et de sauvegarder : :
        self.state = "fin"

    def pause(self):
        """Cette méthode met en pause le jeu, c'est à dire les lecteurs actifs, et les remets en route."""

        # Si self.paused est une liste vide  (aka : aucun lecteur n'est en pause), on ajoute les lecteurs actifs a cette liste et on met ces derniers en pause :
        if self.paused == []:
            for i in self.lecteurs:
                if self.lecteurs[i].playing:
                    self.paused.append(i)
                    self.lecteurs[i].pause()
        # Si des lecteurs sont en pause, on les remet en route :
        else:
            for i in self.paused:
                self.lecteurs[i].play()
            self.paused = []

    def save(self):
        """Sauvegarde la partie."""
        # Si on n'est pas déjà en mode sauvegarde, on l'active et on sauvegarde :
        if "S" not in self.state:
            self.state += "S"
            self.carte.save([self.vie])

    def load(self):
        """Charge une partie en utilisant l'attribut num_sauv, si c'est une chaîne vide, on utilise la dernière sauvegarde."""
        # Si la chaîne est vide :
        liste_saves = [i.replace(".txt", "") for i in os.listdir("saves") if i[-4:] == ".txt"]
        if self.num_sauv != '' and int(self.num_sauv) < len(liste_saves):
            sauv = liste_saves[int(self.num_sauv)].split('_')
            self.carte = mc.Carte(sauv[0], sauv[1])
            self.vie = self.carte.player_info[0]
            self.state = "debut"
            self.move()
        self.state = self.state.replace('C', '')

    def afficher_load(self):
        """Demande de choisir une sauvegarde et affiche les possibilités.
    - Ajouter un affichage en 2 colonnes."""
        if "saves" in os.listdir('.'):
            liste_sauv = [i.replace(".txt", "") for i in os.listdir("saves") if i[-4:] == ".txt"]
            if liste_sauv != []:
                message = u"Choisissez une sauvegarde à charger :\n"
                for i, j in enumerate(liste_sauv):
                    message += u"{} : {}\n".format(i, j)
        else:
            message = u"Le dossier de sauvegardes ('saves') ne contient pas de sauvegardes."

        pyglet.text.Label(message, x=20, y=self.window.height - 30, width=1000, multiline=True).draw()  # Texte à changer
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, 0, self.window.width, 0, self.window.width, 47, 0, 47]), ('c4B', (0, 0, 0, 255) * 4))
        pyglet.text.Label(u"Entrez le numéro correspondant à la sauvegarde choisie : {}".format(self.num_sauv), x=20, y=20).draw()

    def combat_init(self):
        """ Fonction qui initialise les combats """

        self.state = "combat"

        # En fonction de pos x et pos y, récupère le type de monstre
        monstre = self.carte.case
        # On récupère la vie du monstre
        self.vie_monstre = cs.COMBAT_START[monstre][0]
        # Et son nombre de dégâts
        self.degats_monstre = cs.COMBAT_START[monstre][1]

    def tour_combat(self):
        """ Fonction qui gère le tour du combat : attaque du joueur et attaque du monstre """

        # Attaque du joueur
        attaque = self.attaque(70)
        self.vie_monstre -= attaque
        # Si on fait des dégâts, on fait un son d'épée qui touche :
        if attaque > 0:
            self.sons[cs.EPEEHIT].play()
            time.sleep(.4)
            self.sons[cs.MONSTREBLESSE].play()
        else:
            self.sons[cs.EPEEMISSED].play()

        # On attend un peu avant l'attaque du monstre :
        time.sleep(.7)

        # Si on ne l'a pas tué, il réplique
        if self.vie_monstre > 0:
            attaque = self.degats_monstre * self.attaque(70)
            self.vie -= attaque
            if attaque > 0:
                self.sons[cs.MARTEAUHIT].play()
                time.sleep(.3)
                self.sons[cs.JOUEURBLESSE].play()

            # Si on est mort, fin du jeu
            if self.vie <= 0:
                self.fin(cs.MORTCOMBAT)

        # Si on a vaincu le monstre
        if self.vie_monstre <= 0:
            # et que c'était le boss final : fin du jeu
            if self.carte.case == cs.BOSS_FINAL:
                self.fin(cs.VICTOIRE)
            # Sinon : on continue la partie
            else:
                del self.vie_monstre
                del self.degats_monstre
                # On vide la case et on récupère le nouveau type d'environnement :
                self.carte.empty()
                self.move()
                # On passe l'état du jeu en normal :
                self.state = "normal"

    def attaque(self, proba):
        """ Fonction qui permet d'attaquer, proba étant un nombre entier """

        alea = random.randint(1, 100)
        # proba est la probabilité de réussite d'une attaque
        if alea <= proba:
            return 1
        else:
            return 0

    def run(self):
        """Lance la boucle de simulation pyglet."""
        pyglet.app.run()
