import math

'''
CONSTANTS
'''
GRAVITY = 9.81 # m / s^2


#Wave class for packaging data and any methods we may need
class Wave:
    wave_height: float # meters
    break_depth: float # meters
    wave_speed: float # m / s
    wave_distance_past_castle: float # meters; 

    def __init__(self, height: float, depth: float, dist: float):
        global GRAVITY
        self.wave_height = height
        self.break_depth = depth
        self.wave_distance_past_castle = dist
        self.wave_speed = (depth * GRAVITY)**.5
        