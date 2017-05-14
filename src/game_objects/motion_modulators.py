from math import sin

def passthru(self):
    pass

def wiggle_y(self, speed, amt):
    self.y = self.y + sin( self.driver.t * speed ) * amt

motion_modulators = {
    "passthru"          : passthru,
    "wiggle_y(spd,amt)" : wiggle_y
}

