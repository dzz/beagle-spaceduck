from math import sin
from functools import partial

def passthru(self):
    pass

def wiggle_y(self, speed, amt):
    self.y = self.y + sin( self.driver.t * speed ) * amt

motion_modulators = {
    "passthru" : passthru,
    "wiggle_y" : wiggle_y
}

