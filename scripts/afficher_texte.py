""" Petit exemple d'affichage de texte avec pyglet """
import pyglet

#Voilà les différentes options du constructeur de l'objet Label de pyglet (cadre de texte).
#Accessible via : pyglet.text.Label([args]).
#Pour plus d'informations, taper : "import pyglet", puis : "help(pyglet.text.Label)" dans python.

#Tous les paramètres sont facultatifs (les valeurs données ci-dessous sont celles par défaut).
#(text='', font_name=None, font_size=None, bold=False, italic=False, color=(255, 255, 255, 255), x=0, y=0, width=None, height=None, anchor_x='left', anchor_y='baseline', align='left', multiline=False)

#Exemple de texte simple en blanc, situé en bas à gauche de l'écran... :
TEXT = pyglet.text.Label("Salut, comment ça va ?")

#multiline à True si tu veux afficher sur plusieurs lignes (width doit être un int dans ce cas)
#Exemple d'affichage multiligne en couleur (orange je crois) :
TEXT_MULTILIGNE = pyglet.text.Label('bateau\nasa', color=(255, 55, 25, 255), x=30, y=75, width=100, multiline=True)

WINDOW = pyglet.window.Window()

@WINDOW.event
def on_draw():
    """ Affichage du texte """
    WINDOW.clear()
    TEXT.draw()
    TEXT_MULTILIGNE.draw()

pyglet.app.run()
