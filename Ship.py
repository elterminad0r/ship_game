from Particle import Particle, to_for

def sign(a):
    return a / abs(a)

def conv_all(rng, *args):
    return (to_for(pos, rng) for pos in args)

class Ship(object):
    r = 10
    acc_rate = 0.07
    dec_rate = 0.02
    turn_rate = 0.001
    
    def __init__(self, loc=PVector(500, 500), dir=0, v=0):
        self.loc = loc.copy()
        self.dir = dir
        self.mom = PVector.fromAngle(dir).mult(v)
        self.amom = 0
        
        self.autopilot = False
        
        self.turn_noise = random(100)
        self.acc_noise = random(100)
        
        self.seeking = None

    def update(self):
        self.dir += self.amom
        self.loc += self.mom
        self.mom = self.mom.mult(0.99)
        self.amom *= 0.98

        if self.seeking is not None:
            a = (self.seeking - PVector(to_for(self.loc.x, width), to_for(self.loc.y, height))).heading()
            to_cor = (self.dir - a) % TWO_PI - PI
            self.accelerate(lerp(0, self.acc_rate,
                                 constrain(dist(self.seeking.x, self.seeking.y, self.loc.x, self.loc.y), 0, 500) / 500.0 * abs(to_cor) / PI))
            self.turn(lerp( 0, self.turn_rate, to_cor / PI ))
            
        elif self.autopilot:
            self.turn_noise += 0.05
            self.acc_noise += 0.01
            self.accelerate(map(noise(self.acc_noise), 0, 1, self.acc_rate * 0.2, self.acc_rate))
            self.turn(map(noise(self.turn_noise), 0, 1, -self.turn_rate * 0.7, self.turn_rate * 0.7))
        
    def draw(self):
        colorMode(RGB, 255, 255, 255)
        fill(255)
        noStroke()
        pushMatrix()
        translate(*conv_all(width, self.loc.x, self.loc.y))
        rotate(self.dir - HALF_PI)
        triangle(-10, 0, 10, 0, 0, 25)
        popMatrix()
    
    def checkExtreme(self):
        v = self.mom.mag()
        if self.v < self.minspeed:
            self.v = self.minspeed
        if self.v > self.maxspeed:
            self.v = self.maxspeed

    def accelerate(self, d):
        self.mom = self.mom.add(PVector.fromAngle(self.dir).mult(d))
        #self.checkExtreme()
        Particle(255, 0, 0, self.loc.copy(), PVector.fromAngle(self.dir + PI * (sign(d) / 2 + 0.5) + random(-QUARTER_PI, QUARTER_PI)).mult(0.3), 200, 1, 10)
    
    def turn(self, rad):
        self.amom += rad
        Particle(0, 255, 0, self.loc.copy(), PVector.fromAngle(self.dir + sign(rad) * HALF_PI + random(-QUARTER_PI, QUARTER_PI)).mult(0.3), 200, 1, 3)
    
    def keyPressed(self, ks):
        if ks[UP]:
            self.accelerate(self.acc_rate)
        elif ks[DOWN]:
            self.accelerate(-self.dec_rate)
        
        if ks[LEFT]:
            self.turn(-self.turn_rate)
        elif ks[RIGHT]:
            self.turn(self.turn_rate)