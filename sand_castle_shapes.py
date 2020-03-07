import math

#File of classes for the various shapes with methods attached 

'''
CONSTANTS for use in the file
'''
SAND_DENSITY = 2082.0 # kg / m^3
WATER_DENSITY = 1023.6 # kg / m^3
GRAVITY = 9.81 # m / s^2
#Friendly reminder that N = (kg * m) / s^2

'''
CUBE
'''
class Cube:
    side_length: float
    sand_grain_number: float
    base_radius: float
    base_side_length: float
    base_height: float
    #NOTE: base_radius field is the radius we're using when determining when the sandcastle will fall;
    #      that is, it's the R that is being eroded (updated over time)
    #      base_side_length is the length of the side of the base being eroded (updated over time)
    #      base_height is the height of the Cube that is being hit by the wave (same as wave height)
    

    #Constructor for Cubes
    def __init__(self, side: float):
        self.side_length = side
        self.base_radius = Cube.determine_square_radius(self, side)
        self.base_side_length = side
    
    #sets the base_height value
    def set_base_height(self, h: float) -> float:
        self.base_height = h

    #Returns the volume of the cube
    def get_volume(self) -> float:
        #volume of the area unchanged by wave erosion
        top_vol = self.get_top_vol()
        #volume of the area being eroded
        bottom_vol = self.get_eroded_vol
        return self.top_vol + self.bottom_vol

    #returns vol of cube not being eroded
    def get_top_vol(self) -> float:
        return self.side_length * self.side_length * (self.side_length - self.base_height)

    #returns vol of part of cube being eroded
    def get_eroded_vol(self) -> float:
        self.base_height * self.base_side_length * self.base_side_length


    #returns the average of the radii of the circle inscribed in the square base of the Cube
    # and of the circle that circumscribes the Cube
    def determine_square_radius(self, length: float) -> float:
        big_radius = math.sqrt(2 * (self.side_length * self.side_length))
        small_radius = self.side_length / 2
        avg = (big_radius + small_radius) / 2
        return avg

    #updates the base_radius field
    def update_base_radius(self, n: float):
        self.base_radius = n

    #Returns the force of the top sand weighing down on our eroding base
    def get_normal_sand(self) -> float:
        global SAND_DENSITY
        global GRAVITY
        top_vol = self.get_top_vol()
        weight = top_vol * SAND_DENSITY * GRAVITY
        return weight


    
    


'''
CYLINDER
'''
class Cylinder:
    radius: float
    height: float
    sand_grain_number: float
    base_radius: float
    base_height: float
    #NOTE: base_radius field is the radius we're using when determining when the sandcastle will fall;
    #      that is, it's the R that is being eroded
    #      base_height is the height of the Cube that is being hit by the wave (same as wave height)


    #Constructor for Cylinders
    def __init__(self, r: float, h: float):
        self.radius = r
        self.height = h
        self.base_radius = r

    #sets the base_height value
    def set_base_height(self, h: float) -> float:
        self.base_height = h

    #Returns the area of the top of the Cylinder 
    def get_top_area(self) -> float:
        top = math.pi * self.radius * self.radius
        return top

    #Returns the area of the of the base of the Cylinder, even during erosion process
    def get_eroded_base(self) -> float:
        base = math.pi * self.base_radius * self.base_radius

    #Returns the volume of the Cylinder as it currently stands
    def get_volume(self) -> float:
        top_vol = self.get_top_vol()
        bottom_vol = self.get_eroded_vol()
        return top_vol + bottom_vol

    #Returns the volume of the top part of the Cylinder that never gets eroded by a wave
    def get_top_vol(self) -> float:
        return (self.height - self.base_height) * self.get_top_area()

    #Returns the volume of the bottom part of the Cylinder that does get hit by waves
    def get_eroded_vol(self) -> float:
        return self.base_height * self.get_eroded_base()

    #updates the base_radius
    def update_base_radius(self, n: float):
        self.base_radius = n

    #Returns the force of the top of the Cylinder weighing down on the eroding base
    def get_normal_sand(self) -> float:
        global SAND_DENSITY
        global GRAVITY
        top_vol = self.get_top_vol()
        weight = top_vol * SAND_DENSITY * GRAVITY
        return weight


'''
PYRAMID
'''
class Pyramid:
    side_length: float
    height: float
    angle: float #angle from vertical that the pyramid faces are leaning towards each other on, in radians
    sand_grain_number: float
    base_radius: float
    base_side_length: float
    base_height: float
    #NOTE: base_radius field is the radius we're using when determining when the sandcastle will fall;
    #      that is, it's the R that is being eroded (updated over time)
    #      base_side_length is the length of the side of the base being eroded (updated over time)
    #      base_height is the height of the Cube that is being hit by the wave (same as wave height)


    #Constructor for Pyramids
    def __init__(self, side: float, height:float ):
        self.side_length = side
        self.height = height
        self.base_radius = Pyramid.determine_square_radius(self, side)
        self.base_side_length = side
    
    #sets the base_height value
    def set_base_height(self, h: float) -> float:
        self.base_height = h

    #Returns the volume of the pyramid
    def get_volume(self) -> float:
        #volume of the area unchanged by wave erosion
        top_vol = self.get_top_vol()
        #volume of the area being eroded
        bottom_vol = self.get_eroded_vol
        return self.top_vol + self.bottom_vol

    #returns volume of a classic pyramid, NOT ours in particular
    #s = length of the side
    #h = height of the pyramid
    def get_pyramid_vol(self, s: float, h: float) -> float:
        return (s * s * h) / 3

    #returns vol of pyramid not being eroded
    def get_top_vol(self) -> float:
        return self.get_pyramid_vol(self.base_side_length, (self.height - self.base_height))

    #returns vol of part of pyramid being eroded
    def get_eroded_vol(self) -> float:
        #Compute volume by getting volume of the rectangular brick and then adding the "ramps" 
        # on each side of the base
        #Get the theta value for the angle in the triangle we're considering
        theta =  (math.pi / 2) - self.angle
        #Make opposite, adjacent, and hypotenuse values
        #See pics in git repo of big_board for the diagram on these values
        opp = self.base_height 
        hyp = opp / math.sin(theta)
        adj = math.cos(theta) * hyp
        #Get the volume of the frustum
        #From: https://keisan.casio.com/exec/system/1223368185
        a = self.base_side_length
        b = a - 2*adj
        h = self.base_height
        vol = ((a**2 + a*b + b**2) * h) / 3
        return vol


        


    #returns the average of the radii of the circle inscribed in the square base of the Cube
    # and of the circle that circumscribes the Cube
    def determine_square_radius(self, length: float) -> float:
        big_radius = math.sqrt(2 * (self.side_length * self.side_length))
        small_radius = self.side_length / 2
        avg = (big_radius + small_radius) / 2
        return avg

    #updates the base_radius field
    def update_base_radius(self, n: float):
        self.base_radius = n

    #Returns the force of the top sand weighing down on our eroding base
    def get_normal_sand(self) -> float:
        global SAND_DENSITY
        global GRAVITY
        top_vol = self.get_top_vol()
        weight = top_vol * SAND_DENSITY * GRAVITY
        return weight


'''
CONE
'''

