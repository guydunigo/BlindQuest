#-*-coding:utf-8-*-

# # # # # # # # # # # # # # # # #
#                               #
#         Projet de MDD         #
#                               #
#       fichier : main.py       #
#                               #
# # # # # # # # # # # # # # # # #

import constantes
import m_jeu

jeu = m_jeu.Jeu(constantes.CARTE)

jeu.run()