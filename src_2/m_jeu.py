#-*-coding:utf-8-*-

# # # # # # # # # # # # # # # # #
#        #
#         Projet de MDD         #
#                               #
#       fichier : m_jeu.py      #
#                               #
# # # # # # # # # # # # # # # # #

#Importation des modules fournis avec python :
import time
import os

#Importation du module Pyglet pour python 3. Si il n'est pas trouvé sur le système, on utilise la version présente dans le dossier src :

import pyglet
print("Utilisation de la version de pyglet du dossier src/ (",pyglet.version,").")
print()

#Importation des constantes :
import constantes as cs
#Importation de notre module qui gère la carte et la position du joueur :
import m_carte as mc

class Jeu (object) :
  """Classe qui gère le jeu, la Bibliothèque pyglet, les évènements claviers, la fenêtre et le son."""

  def __init__(self, type_carte = "defaut") :
    """Constructeur : 
      carte_type : type de carte à utiliser durant le jeu. (carte nommée selon l'exemple : carte_NOM.txt et placée dans le dossier cartes)"""

    #Si le dossier de travail de python (le dossier depuis lequel python a été lancé) est le dossier du code source ('src_3'), on va dans le dossier principal.
    if "/src_3" in os.getcwd()[-6:] :
      print("Le programme a été lancé depuis le dossier src_3, changement du dossier vers le dossier parent (dossier principal du projet).")
      print()
      os.chdir("../")
    #Réglage du dossier de travail de pyglet pour le dossier racine du projet, sinon il ne trouve pas les différents composants :
    working_dir = os.path.dirname(os.path.realpath(__file__))
    pyglet.resource.path = [os.path.join(working_dir,'..')]
    pyglet.resource.reindex()

    #On choisit d'utiliser openal pour l'audio. (pulseaudio ne marchait pas)
    #pyglet.options['audio'] = ('openal',)

    #Chargement de la carte :
    self.carte = mc.Carte(type_carte)
    #Chargement des sons :
    self.charger_sons()
    #Lecteurs (environnement(s), action(s), heartbeats,...) :
    self.creer_lecteurs()  
    #Fenêtre (activation du plein écran ?par défaut?) :
    self.creer_fenetre()
    #Création des evènements... (clavier, ...) ou utilisation de raw_input? 
    self.init_events()

    #Initialisation de la vie du personnage
    self.vie = cs.VIE

    #Initialisation de variables d'état ("debut", "combat", "normal") accompagné d'un H lorsque l'on affiche l'aide, C lors d'un chargement ou de S lors d'une sauvegarde :
    self.state = "debut"
    #Initialisation de la liste des lecteurs en pause (par extension, indique si le jeu est en pause lorsqu'elle est vide) :
    self.paused = []


  def charger_sons(self) :
    """Charge tous les sons du dossier 'sons' et les range dans un dictionnaire avec pour étiquette le nom du fichier son sans l'extension '.wav'.
    On charge les sons directement dans la mémoire sans streaming pour éviter les problèmes de 'source already queued'. ("Un peu" BOURIN et bouffe-mémoire)"""

    #On prévient que le temps de chargement est normal :
    print("Chargement des sons en mémoire...")

    #On crée le dictionnaire de sons :
    self.sons = {}

    if "sons" in os.listdir('.') :
      #On récupère la liste des fichiers du dossier 'sons' :
      liste_sons = os.listdir("sons")

      #On ne garde que les fichiers 'wav' :
      liste_sons = [ fichier for fichier in liste_sons if fichier.find(".wav") != -1]

      #On ouvre les sons avec pyglet et on les range dans le dictionnaire 'sons' avec pour étiquette le nom du fichier son sans l'etension '.wav' :
      for son in liste_sons :
        self.sons[son.replace(".wav",'')] = pyglet.media.load(os.path.join("sons", son), streaming = False)


  def creer_lecteurs(self) :
    """Crée les lecteurs pyglet, les lecteurs env, heartbeat, et les lecteurs de proximités (définits dans le fichier constantes) sont réglés pour tourner en boucle sur la musique en cours : 
      - env : Pour l'environnement ou le combat, en boucle.
      - heartbeat : Si il ne reste qu'une vie, on entend un bâttement de coeur, en boucle.
      - Les différents sons de proximité ont leur propre lecteur, en boucle.
      - Monstre : peut-être inutile, bruit du monstre de temps en temps.
    """
    
    self.lecteurs = {}
    for lecteur in ("env", "monstre", "heartbeat"):
      self.lecteurs[lecteur] = pyglet.media.Player()
      if lecteur == "env" :
        #En boucle
        self.lecteurs[lecteur].eos_action = self.lecteurs[lecteur].EOS_LOOP
        self.lecteurs[lecteur].volume = 0.7
      if lecteur == "heartbeat" :
        self.lecteurs[lecteur].eos_action = self.lecteurs[lecteur].EOS_LOOP
        self.lecteurs[lecteur].queue(self.sons[lecteur])
        self.lecteurs[lecteur].volume = 1.0

    #Création des lecteurs pour les sons de proximité, un lecteur par sons, en boucle, volume faible.
    for lecteur in cs.PROX :
      self.lecteurs[lecteur] = pyglet.media.Player()
      self.lecteurs[lecteur].eos_action = self.lecteurs[lecteur].EOS_LOOP
      self.lecteurs[lecteur].queue(self.sons[cs.CONV[lecteur]])
      self.lecteurs[lecteur].volume = 0.5

    #On restitue l'environnement sonore de départ.
    self.lecteurs["env"].queue(self.sons[cs.CONV[cs.DEPART]])
    self.lecteurs["env"].play()

    #Affichage des volumes des différents lecteurs :
    print("   Volume des lecteurs :")
    for i in self.lecteurs :
        print("    - ",i," : ",self.lecteurs[i].volume)

 
  def creer_fenetre(self) :
    """Crée la fenêtre pyglet en plein écran et affiche l'aide pendant 5 secondes."""
    self.window = pyglet.window.Window(fullscreen = True)


  def init_events(self) :
    """crée les évenements : 
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
    def on_key_press(symbol, modifiers) :
      #Fullscreen
      if symbol == pyglet.window.key.F :
        self.window.set_fullscreen(not self.window.fullscreen)
      #Aide
      elif symbol == pyglet.window.key.H :
        if self.state[-1] != 'H' :
          self.state += 'H'
      #Pause
      elif symbol == pyglet.window.key.P :
        self.pause()
      #Charger
      elif symbol == pyglet.window.key.C :
        self.load()

      if self.state == "normal" :
        #Déplacements
        if symbol == pyglet.window.key.UP :
          self.move("NORD")
        elif symbol == pyglet.window.key.DOWN :
          self.move("SUD")
        elif symbol == pyglet.window.key.RIGHT :
          self.move("EST")
        elif symbol == pyglet.window.key.LEFT :
          self.move("OUEST")
        #Sauvegarder
        elif symbol == pyglet.window.key.S :
          self.save()
      elif self.state == "combat" :
        if symbol == pyglet.window.key.A : # À changer.
          pass
      elif self.state == "debut" and symbol == pyglet.window.key.SPACE :
        self.state = "normal"

    @self.window.event
    def on_key_release(symbol, modifiers) :
      print(self.state)
      if self.state[-1] == 'H' :
        self.state = self.state.replace('H','')


    @self.window.event
    def on_draw() :
      """On efface l'écran, peut-être sera-t-il impossible de voir l'aide : dans ce cas, l'enlever et regarder quand la touche est relachée."""
      self.window.clear()
      if self.state == "debut" :
        #On affiche l'aide :
        self.afficher_aide()
        #On affiche le messae de bienvenue :
        pyglet.text.Label(u"Réglez le volume sonore puis appuyez sur la touche ESPACE pour commencer...", x = 20, y = 20).draw()
      elif self.paused != [] :
        pyglet.text.Label("Partie en pause, appuyez sur la touche P pour reprendre...", x = 20, y = 20).draw()
      if self.state[-1] == 'H' :
        self.afficher_aide()


  def move(self, direction = None) :
    """Fonction qui déplace le joueur et gère ce qui peut y arriver (mort si environnement dangereux, combat...) et lance les sons d'environnement et de proximité.
      - direction : prend un chaîne de caractère parmis ("OUEST", "EST", "NORD", "SUD"). 
          Si il n'est pas définit (ou à None du coups), le joueur ne bouge pas, ce qui est utile pour avoir l'environnement sonore actuel du joueur."""

    #On déplace le joueur su la carte et on récupère le code de la case d'arrivée. 
    case = self.carte.move(direction)
    if case != None :
      #On récupère les informations de proximité de la case (eau, pont...), qui sont écrits sous forme de centaines et au dessus.
      infos_prox = int(case / 100)
      case = case - infos_prox * 100

      print("code case : ",cs.CONV[case],", ",case,", code proximité : ",infos_prox)

      #Si le joueur arrive sur une case létale, on active la fin. 
      if case in cs.DANGER :
        self.fin(cs.DANGER[case])
      
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
    pyglet.text.Label("test de l'aide", x = 20, y = 200).draw()


  def fin(self, type_fin) :
    """Fonction qui gère la fin selon s'il y a victoire ou mort, et s'occupe de quitter le programme.
      - type : chaîne de caractère décrivant la fin parmis celles se trouvant dans le fichier constantes, les fichiers sons associés doivent exister."""

    #On restitue le sons associé à la mort :
    self.lecteurs["env"].queue(self.sons[type_fin])
    self.lecteurs["env"].next_source()

    #On active l'état fin qui empèche de se déplacer et de sauvegarder : :
    self.isEnd = True


  def pause(self) :
    """Cette méthode met en pause le jeu, c'est à dire les lecteurs actifs, et les remets en route."""
    #Si self.paused est une liste vide  (aka aucun lecteur n'est en pause), on ajoute les lecteurs actifs a cette liste et on met ces derniers en pause :
    if self.paused == [] :
      for i in self.lecteurs :
        if self.lecteurs[i].playing :
          self.paused.append(i)
          self.lecteurs[i].pause()
    #SI des lecteurs sont en pause, on les remet en route :
    else :
      for i in self.paused :
        self.lecteurs[i].play()
      self.paused = []


  def save(self) :
    """Sauvegarde la partie."""
    if "saves" not in os.listdir('.') :
      os.mkdir("saves")


  def load(self) :
    """Charge une partie."""
    #Demander nom de la sauvegarde ou afficher le nom de la sauvegarde :
    if "saves" in os.listdir('.') :
      liste_sauv = [i.replace(".txt", "") for i in os.listdir("saves") if i[-4:] == ".txt"]
      if liste_sauv != [] :
        message = "Choisissez une sauvegarde à charger :\n"
        for i, j in enumerate(liste_sauv) :
          message.append("{} : {}".format(i,j)) 
        self.carte = mc.Carte(carte, num)
      else :
        message = "Le dossier de sauvegardes ('saves') ne contient pas de sauvegardes."
        #Afficher un message : pas sauvegardes

      pyglet.text.Label(message).draw() #Texte à changer
      
    else :
      pass
      #Afficher un message, pas de dossier de sauvegardes trouvé

  def run(self) :

    pyglet.app.run()
