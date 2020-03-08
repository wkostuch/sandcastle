import math

'''
CONSTANTS
'''
GRAVITY = 9.81 # m / s^2
WATER_DENSITY = 1023.6 # kg / m^3
AVG_WAVE_HEIGHT = 0.02 # meters | 1.039 m from two bouys off CA and 3 off FL, but that's when the big ones are breaking
AVG_BREAK_DEPTH = AVG_WAVE_HEIGHT * 1.3 # meters 


#Wave class for packaging data and any methods we may need
class Wave:
    wave_height: float # meters
    break_depth: float # meters
    wave_speed: float # m / s
    wave_distance_past_castle: float # meters; 

    #Constructor
    def __init__(self, height: float, depth: float, dist: float):
        global GRAVITY
        self.wave_height = height
        self.break_depth = depth
        self.wave_distance_past_castle = dist
        self.wave_speed = (depth * GRAVITY)**.5

    def __str__(self):
        return "Height: " + str(self.wave_height) + " , Depth: " + str(self.break_depth) + " , Speed: " + str(self.wave_speed) + " , Distance " + str(self.wave_distance_past_castle)
        
    #returns the momentum of the wave as its strength
    def wave_strength(self) -> float:
        global WATER_DENSITY
        momentum = WATER_DENSITY * self.wave_height * self.wave_speed