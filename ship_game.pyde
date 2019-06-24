# vim: ft=python

from collections import defaultdict

from Ship import Ship
from Particle import Particle, NORMAL_FADE, RAINBOW_FADE, RAINBOW_RAND

#track keys pressed
ks = defaultdict(bool)

#mapping from keys z, x, c to particle modes
modes = dict(zip(map(ord, "ZXC"), [NORMAL_FADE, RAINBOW_FADE, RAINBOW_RAND]))

def mousePressed():
    ship.seeking = PVector(mouseX, mouseY)

def mouseDragged():
    mousePressed()

def mouseReleased():
    ship.seeking = None

def keyPressed():
    #set corresponding entry to True
    ks[keyCode] = True
    
    #activate corresponding mode
    if keyCode in modes:
        Particle.parts.clear()
        Particle.mode = modes[keyCode]
    if keyCode == ord('A'):
        ship.autopilot = not ship.autopilot
    elif keyCode == ord('R'):
        setup()
    
def keyReleased():
    #set corresponding entry to False
    ks[keyCode] = False

def setup():
    global ship
    size(1000, 1000)
    background(0)
    #initalize the global Ship ship
    ship = Ship()

def draw():
    background(0)
    #allow ship to handle key presses
    ship.keyPressed(ks)
    #update ship
    ship.update()
    #draw ship
    ship.draw()
    #update and draw particles
    Particle.update()
    Particle.draw()
