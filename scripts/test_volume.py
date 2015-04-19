import pyglet
import time
import sys

aa = {"son_env": pyglet.resource.media('son_env.wav'), "son_eau":pyglet.resource.media('son_eau.wav')}

players = {"env":pyglet.media.Player(),"eau":pyglet.media.Player()}

players["env"].queue(aa["son_env"])
players["eau"].queue(aa["son_eau"])

players["env"].play()
players["eau"].play()
players["eau"].volume = 0.1
window = pyglet.window.Window()

@window.event
def on_key_press(symbol, modifiers):
	if symbol == pyglet.window.key.UP:
		players["eau"].volume += 0.01
	elif symbol == pyglet.window.key.DOWN:
		players["eau"].volume -= 0.01
	print(players["eau"].volume, players["env"].volume)
pyglet.app.run()
