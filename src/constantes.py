
#Définition des constantes

#Carte utilisée :
CARTE = "petite"

#Tous les types utilisés dans la carte devront être définis ici et le nom des sons leur correspondant devra être le même que le dictionnaire de conversion.
#Il est possible d'ajouter un type de monstre ou de case dangeureuse, etc les ajoutant dans les diverses catégories

#Codes des cases (compris entre 0 et 99 compris) :
PLAINE		= 0
FORET		= 1
CAVERNE		= 2
EAU		= 3
CHATEAU		= 4
SENTIER		= 5
PONT		= 6
SABLE		= 7
MONTAGNE	= 8
MONSTRE		= 10
BOSS		= 11
BOSS_FINAL	= 12
BONUS		= 13
DEPART		= 98
FIN		= 99

#Dictionnaire de conversion code de case -> nom du fichier son au format wav :

CONV = {
	PLAINE		: "plaine",
	FORET		: "foret",
	CAVERNE		: "caverne",
	EAU		: "eau",
	CHATEAU		: "chateau",
	SENTIER		: "sentier",
	PONT		: "pont",
	SABLE		: "sable",
	MONTAGNE	: "montagne",
	MONSTRE		: "monstre",
	BOSS		: "boss",
	BOSS_FINAL	: "boss_final",
	BONUS		: "bonus",
	DEPART		: "depart",
	FIN		: "fin"
}

#Liste (pour python c'est un tuple) de types impraticables (où le joueur ne peut aller :
NOGO = (
	MONTAGNE,
)

#Dictionnaire des types à détecter et de leur code de proximité assigné.
#Les codes de proximités pour les environnements qui doivent être détectés lorsque le joueur en est à proximité et donc doivent sonner en arrière plan. 
#Ce sont des puissances de 2 pour pouvoir jouer avec les opérateurs bits à bits :

PROX = {
	EAU	: 2** 0,
	PONT	: 2** 1
}

#Types de fins, les fichiers sons associés doivent exister et porter le même nom que la châine de caractère.

VICTOIRE	= "victoire"
NOYADE 		= "noyade"
COMBAT		= "combat"

#Dictionnaire décrivant les différents types de cases démarrant un combat ainsi que les caractéristiques de l'attaquant sous la forme (vie, dégats)

COMBAT = {
	MONSTRE		: (1, 1),
	BOSS		: (2, 2),
	BOSS_FINAL	: (3, 3)
}

#Dictionnaire décrivant les différents environnements dangereux, où la mort est instantannée, ainsi que les morts associées:

DANGER = {
	EAU : NOYADE
}
