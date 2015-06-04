# -*-coding:utf-8-*-

# # # # # # # # # # # # # # # # #
#                               #
#    Projet de MDD              #
#                               #
#    fichier : constantes.py    #
#                               #
# # # # # # # # # # # # # # # # #

# Définition des constantes

# Carte utilisée :
CARTE = "petite"

# Quantité de vie du personnage :
VIE = 10

# Tous les types utilisés dans la carte devront être définis ici et le nom des sons leur correspondant devra être le même que le dictionnaire de conversion.
# Il est possible d'ajouter un type de monstre ou de case dangereuse, etc les ajoutant dans les diverses catégories

# Codes des cases (compris entre 0 et 99 compris) :
PLAINE          = 0
FORET           = 1
CAVERNE         = 2
EAU             = 3
CHATEAU         = 4
SENTIER         = 5
PONT            = 6
SABLE           = 7
MONTAGNE        = 8
MONSTRE         = 10
BOSS            = 11
BOSS_FINAL      = 12
BONUS           = 13
MER             = 14
ENTREECHATEAU   = 15
MAGIE           = 16
FUNNY           = 17
BORDURE         = 97
DEPART          = 98
FIN             = 99

# Dictionnaire de conversion code de case -> nom du fichier son au format wav :

CONV = {
  PLAINE        : "plaine",
  FORET         : "foret",
  CAVERNE       : "caverne",
  EAU           : "eau",
  CHATEAU       : "chateau",
  SENTIER       : "sentier",
  PONT          : "pont",
  SABLE         : "sable",
  MONSTRE       : "monstre",
  BOSS          : "boss",
  BOSS_FINAL    : "boss_final",
  BONUS         : "bonus",
  MER           : "mer",
  ENTREECHATEAU : "porte",
  MAGIE         : "magie",
  FUNNY         : "NyanCatoriginal",
  DEPART        : "depart",
  FIN           : "fin"
}

# Liste (pour python c'est un tuple) de types impraticables (où le joueur ne peut aller) :
NOGO = (
  MONTAGNE,
  BORDURE
)

# Dictionnaire des types à détecter et de leur code de proximité assigné.
# Les codes de proximités pour les environnements qui doivent être détectés lorsque le joueur en est à proximité et donc doivent sonner en arrière plan.
# Ce sont des puissances de 2 pour pouvoir jouer avec les opérateurs bits à bits :

PROX = {
  EAU   : 2 ** 0,
  MER   : 2 ** 1,
  PONT  : 2 ** 2 | 2 ** 0  # On veut entendre l'eau couler avec le bruit du pont pour mieux comprendre que c'est un pont.
}

# Sons de combat.

EPEEHIT       = "epeehit"
EPEEMISSED    = "epeemissed"
MARTEAUHIT    = "marteauhit"
JOUEURBLESSE  = "joueurblesse"
MONSTREBLESSE = "monstreblesse"

# Types de fins, les fichiers sons associés doivent exister et porter le même nom que la chaîne de caractère.

VICTOIRE   = "victoire"
NOYADE     = "noyade"
COMBAT     = "combat"
MORTCOMBAT = "mortcombat"

# Dictionnaire décrivant les différents types de cases démarrant un combat ainsi que les caractéristiques de l'attaquant sous la forme (vie, dégâts)

COMBAT_START = {
  MONSTRE    : (1, 1),
  BOSS       : (2, 2),
  BOSS_FINAL : (3, 3)
}

# Dictionnaire décrivant les différents environnements dangereux, où la mort est instantanée, ainsi que les morts associées:

DANGER = {
  EAU : NOYADE,
  MER : NOYADE
}

##############################################################

# Constantes de l'éditeur (couleurs, ...) :
TAILLE_CASE = 15

# Couleurs :
COULEUR_PLAINE = ('c4B', (150,175,10,0)*4)                              # VERT CLAIR
COULEUR_FORET = ('c4B', (0,100,0,0)*4)                                  # VERT FONCE
COULEUR_CAVERNE = ('c4B', (100,50,0,0)*4)                               # MARRON
COULEUR_EAU = ('c4B', (0,0,255,0)*4)                                    # BLEU
COULEUR_CHATEAU = ('c4B', (150,150,150,0)*4)                            # GRIS CAIR
COULEUR_SENTIER = ('c4B', (10,200,0,0)*4)                               # VERT MARRON
COULEUR_PONT = ('c4B', (100,50,0,0)*2 + (200,100,0,0)*2)                # DEGRADE DE MARRON
COULEUR_SABLE = ('c4B', (255,255,0,0)*4)                                # JAUNE
COULEUR_MONTAGNE = ('c4B', (50,10,0,0)*4)                               # MARRON FONCE
COULEUR_MONSTRE = ('c4B', (255,255,0,0)*2 + (200,70,0,0)*2)             # DEGRADE JAUNE - ORANGE
COULEUR_BOSS = ('c4B', (200,200,0,0)*2 + (255,0,0,0)*2)                 # DEGRADE ORANGE - ROUGE
COULEUR_BOSS_FINAL = ('c4B', (255,0,0,0)*2 + (0,0,0,0)*2)               # DEGRADE ROUGE - NOIR
COULEUR_BONUS = ('c4B', (200,0,200,0)*4)                                # mauve (ou 'mave' selon la provenance)
COULEUR_MER = ('c4B' , (20,20,100,0)*4)                                 # BLEU FONCE
COULEUR_ENTREECHATEAU = ('c4B', (50,50,50,0)*4)                         # GRIS FONCE
COULEUR_BORDURE = ('c4B', (0,)*16)                                      # NOIR
COULEUR_DEPART = ('c4B', (255,255,255,0)*3 + (0,0,0,0))                 # DEGRADE BLANC - NOIR
COULEUR_FIN = ('c4B', (0,0,0,0)*3 + (255,255,255,255))                  # DEGRADE NOIR - BLANC

# Dico de correspondance des type/couleurs :
COULEURS = {
            PLAINE              : COULEUR_PLAINE,
            FORET               : COULEUR_FORET,
            CAVERNE             : COULEUR_CAVERNE,
            EAU                 : COULEUR_EAU,
            CHATEAU             : COULEUR_CHATEAU,
            SENTIER             : COULEUR_SENTIER,
            PONT                : COULEUR_PONT,
            SABLE               : COULEUR_SABLE,
            MONTAGNE            : COULEUR_MONTAGNE,
            MONSTRE             : COULEUR_MONSTRE,
            BOSS                : COULEUR_BOSS,
            BOSS_FINAL          : COULEUR_BOSS_FINAL,
            BONUS               : COULEUR_BONUS,
            MER                 : COULEUR_MER,
            ENTREECHATEAU       : COULEUR_ENTREECHATEAU,
            BORDURE             : COULEUR_BORDURE,
            DEPART              : COULEUR_DEPART,
            FIN                 : COULEUR_FIN
}
