# # # # # # # # # # # # # # # # #
#				#
#	  Projet de MDD		#
#				#
#     fichier : m_carte.py	#
#				#
# # # # # # # # # # # # # # # # #


def creer(type_carte):
	"""type_carte :
	carte par defaut	: 0
	carte miniature		: 1"""

	#Variables de types de carte
	CARTE_DEFAUT = 0
	CARTE_PETITE = 1

	if type_carte == CARTE_PETITE:
		return [[0,10,0,1,3],[0,0,1,1,1],[1,1,1,1,1],[0,0,0,1,0],[13,0,0,10,0]]
	else :
		#Prevue, a faire...
		return None
