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
  ENTREECHATEAU : "entreechateau",
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

