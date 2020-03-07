import math

'''
CONSTANTS
'''
GRAVITY = 9.81 # m / s^2


#Wave class for packaging data and any methods we may need
class Wave:
    wave_height: float #meters
    break_depth: float # meters
    wave_speed: float # m / s

    def __init__(self, h: float, d: float):
        global GRAVITY
        self.wave_height = h
        self.break_depth = d
        self.wave_speed = (d * GRAVITY)**.5
        