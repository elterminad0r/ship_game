#convert a coordinate to a value in a range, given a tolerance
def to_for(pos, rng, tolerance=50):
    return (pos + tolerance) % (rng + tolerance * 2) - tolerance

#decorator applying a function to each item in an iterable -
#useful in writing a normal instance method for a Particle and applying to each Particle as a static method
def apply_to(l):
    def to_all(func):
        def f():
            for i in l:
                func(i)
        return f
    return to_all

#constants signifying colouring modes
NORMAL_FADE = 0
RAINBOW_FADE = 1
RAINBOW_RAND = 2

#Particle class - fuel emitted by ship
class Particle(object):
    #set of all particles to statically update
    parts = set()
    #current mode
    mode = NORMAL_FADE

    def __init__(self, r, g, b, pos, vel, life, minrad, maxrad):
        #colours
        self.r = r
        self.g = g
        self.b = b
        
        #handle colouring for different modes
        if Particle.mode == NORMAL_FADE:
            colorMode(RGB, 255, 255, 255)
            self.c = color(r, g, b)
        elif Particle.mode == RAINBOW_FADE:
            colorMode(HSB, 255, 255, 255)
            self.c = color(0, 255, 255)
        elif Particle.mode == RAINBOW_RAND:
            colorMode(HSB, 255, 255, 255)
            self.orig = random(0, 255)
            self.c = color(self.orig, 255, 255)

        #position, velocity
        self.pos = pos
        self.vel = vel
        
        #absolute time left and counter of time left in frames
        self.life = self.currlife = life
        
        #minimum and maximum radius
        self.minrad = minrad
        self.maxrad = maxrad
        
        #register to the tracker
        Particle.parts.add(self)

    #statically update all particles, using the decorator apply_to
    @staticmethod
    @apply_to(parts)
    def update(self):
        #mapping of lifetime to range 255, 0
        x = map(self.currlife, self.life, 0, 255, 0)
        #handle colouring depending on mode
        if Particle.mode == NORMAL_FADE:
            colorMode(RGB, 255, 255, 255)
            self.c = color(self.r, self.g, self.b, x)
        elif Particle.mode == RAINBOW_FADE:
            colorMode(HSB, 255, 255, 255)
            self.c = color(x, 255, 255, x)
        elif Particle.mode == RAINBOW_RAND:
            colorMode(HSB, 255, 255, 255)
            self.c = color((self.orig + x) % 255, 255, 255, x)
        
        #decrease time left
        self.currlife -= 1
        #move
        self.pos += self.vel
        #self-destruct and allow garbage collection if time has expired
        if self.currlife < 0:
            Particle.parts.remove(self)
    
    #statically draw all particles, using apply_to
    @staticmethod
    @apply_to(parts)
    def draw(self):
        #mapping for radius
        r = map(self.currlife, self.life, 0, self.minrad, self.maxrad)
        fill(self.c)
        noStroke()
        ellipse(to_for(self.pos.x, width), to_for(self.pos.y, height), r * 2, r * 2)
    