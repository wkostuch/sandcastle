import math

#File of classes for the various shapes with methods attached 

'''
CONSTANTS for use in the file
'''
SAND_DENSITY = 2082.0 # kg / m^3
SAND_DIAMETER = 0.000375 # diameter in meters, aka 375 micro-meters
SAND_RADIUS = SAND_DIAMETER / 2 #meters
SAND_VOLUME = (4/3) * math.pi * (SAND_RADIUS**3)
WATER_DENSITY = 1023.6 # kg / m^3
GRAVITY = 9.81 # m / s^2
AVG_WAVE_HEIGHT = 0.02 # meters | 1.039 m from two bouys off CA and 3 off FL, but that's when the big ones are breaking
AVG_BREAK_DEPTH = AVG_WAVE_HEIGHT * 1.3 # meters 
#Friendly reminder that N = (kg * m) / s^2

'''
CUBE
'''
class Cube:
    side_length: float
    height: float   
    base_grains: float
    base_radius: float
    base_side_length: float
    base_height: float
    #NOTE: base_radius field is the radius we're using when determining when the sandcastle will fall;
    #      that is, it's the R that is being eroded (updated over time)
    #      base_side_length is the length of the side of the base being eroded (updated over time)
    #      base_height is the height of the Cube that is being hit by the wave (same as wave height)
    
    #to_string method for pretty printing
    def __str__(self):
        return "Cube: side_length: " + str(self.side_length) + " | height: " + str(self.height) + \
                 " | base_radius: " + str(self.base_radius) + " | base_side_length: " + str(self.base_side_length)

    #used in dictionary mapping
    def string_name(self) -> str:
        return "cube"
                

    #Constructor for Cubes
    def __init__(self, side: float):
        self.side_length = side
        self.height = side
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
        return self.base_height * self.base_side_length * self.base_side_length


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

    #Returns # of sand grains in the eroding base
    def get_base_grains(self) -> float:
        global SAND_DIAMETER
        global SAND_VOLUME
        vol = self.get_eroded_vol() #m^3
        grains = vol / SAND_VOLUME
        return grains

    #Returns the surface area of the eroding part of the cube
    def get_eroding_surface_area(self) -> float:
        return self.base_height * self.base_side_length * 4 + 0.00001 #add a little to make sure we don't divide by 0

    #returns cross-sectional area of the top part being eroded
    def get_cross_sectional_area(self) -> float:
        return self.base_side_length * self.base_side_length


    
    


'''
CYLINDER
'''
class Cylinder:
    radius: float
    height: float    
    base_grains: float
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

    #to_string method for pretty printing
    def __str__(self):
        return "Cylinder: radius: " + str(self.radius) + " | height: " + str(self.height) + \
                 " | base_radius: " + str(self.base_radius) 

    #used in dictionary mapping
    def string_name(self):
        return "cylinder"

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
        return base

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

    #Returns # of sand grains in the eroding base
    def get_base_grains(self) -> float:
        global SAND_DIAMETER
        global SAND_VOLUME
        vol = self.get_eroded_vol() #m^3
        grains = vol / SAND_VOLUME
        return grains

    #Returns the surface area of the eroding part of the cylinder
    def get_eroding_surface_area(self) -> float:
        circumference = self.base_radius * 2 * math.pi
        return circumference * self.base_height + 0.00001 #add a little to make sure we don't divide by 0

    #returns cross-sectional area of the top part being eroded
    def get_cross_sectional_area(self) -> float:
        return self.get_eroded_base()





'''
PYRAMID
'''
class Pyramid:
    side_length: float
    height: float
    angle: float #internal angle of the pyramid (two base angles of a cut-away pyramid slice)
    base_grains: float
    base_radius: float
    base_side_length: float
    base_height: float
    #NOTE: base_radius field is the radius we're using when determining when the sandcastle will fall;
    #      that is, it's the R that is being eroded (updated over time)
    #      base_side_length is the length of the side of the base being eroded (updated over time)
    #      base_height is the height of the Cube that is being hit by the wave (same as wave height)


    #Constructor for Pyramids
    def __init__(self, side: float, height: float):
        self.side_length = side
        self.height = height
        self.base_radius = Pyramid.determine_square_radius(self, side)
        self.base_side_length = side
        self.angle = math.atan(height / (side / 2))


    #to_string method for pretty printing
    def __str__(self):
        return "Pyramid: side_length: " + str(self.side_length) + " | height: " + str(self.height) + \
                 " | base_radius: " + str(self.base_radius) + " | base_side_length: " + str(self.base_side_length)

    #used in dictionary mapping
    def string_name(self):
        return "pyramid"
    
    #sets the base_height value
    def set_base_height(self, h: float) -> float:
        self.base_height = h

    #Returns the volume of the pyramid
    def get_volume(self) -> float:
        #volume of the area unchanged by wave erosion
        top_vol = self.get_top_vol()
        #volume of the area being eroded
        bottom_vol = self.get_eroded_vol()
        return top_vol + bottom_vol

    #returns volume of a classic pyramid, NOT ours in particular
    #s = length of the side
    #h = height of the pyramid
    def get_pyramid_vol(self, s: float, h: float) -> float:
        return (s * s * h) / 3

    #returns vol of pyramid not being eroded
    def get_top_vol(self) -> float:
        length = self.get_length_at_h(self.side_length, self.base_height)
        height = self.height - self.base_height
        return self.get_pyramid_vol(length, height)


    #returns the length of the Pyramid at height h
    #NOTE that base_length is not self here, it varies 
    def get_length_at_h(self, base_length: float, h: float) -> float:
        triangle_adj = h / (math.tan(self.angle) + 0.000001) #add a little to not divide by 0
        return base_length - (2 * triangle_adj)
        

    #returns vol of part of pyramid being eroded
    def get_eroded_vol(self) -> float:
        #Compute volume by getting volume of the rectangular brick and then adding the "ramps" 
        # on each side of the base
        #Get the theta value for the angle in the triangle we're considering
        theta =  self.angle
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

    #Returns # of sand grains in the eroding base
    def get_base_grains(self) -> float:
        global SAND_DIAMETER
        global SAND_VOLUME
        vol = self.get_eroded_vol() #m^3
        grains = vol / SAND_VOLUME
        return grains


    #Returns the surface area of the eroding part of the pyramid
    def get_eroding_surface_area(self) -> float:
        #Get the theta value for the angle in the triangle we're considering
        theta =  self.angle
        #Make opposite, adjacent, and hypotenuse values
        #See pics in git repo of big_board for the diagram on these values
        opp = self.base_height 
        hyp = opp / math.sin(theta)
        adj = math.cos(theta) * hyp
        #Get the lateral surface area of the frustum
        #From: https://keisan.casio.com/exec/system/1223368185
        a = self.base_side_length
        b = a - 2*adj
        h = self.base_height
        surface_area = 2 * (a + b) * \
                        (   ((a - b) / 2)**2 + h**2)**.5
        return surface_area + 0.00001 #add a little to make sure we don't divide by 0

    #returns cross-sectional area of the top part being eroded
    def get_cross_sectional_area(self) -> float:
        #Get the theta value for the angle in the triangle we're considering
        theta =  self.angle
        #Make opposite, adjacent, and hypotenuse values
        #See pics in git repo of big_board for the diagram on these values
        opp = self.base_height 
        hyp = opp / math.sin(theta)
        adj = math.cos(theta) * hyp
        #Get the lateral surface area of the frustum
        #From: https://keisan.casio.com/exec/system/1223368185
        a = self.base_side_length
        b = a - 2*adj
        return b * b


'''
CONE
'''

class Cone:
    radius: float
    height: float
    angle: float #internal angle of the cylinder in radians
    base_grains: float
    base_height_ratio: float #used for getting r at a height for the truncated cone
    base_radius: float
    base_height: float
    radius_above_base_height: float #radius of the Cone just above the erosion
    #NOTE: base_radius field is the radius we're using when determining when the sandcastle will fall;
    #      that is, it's the R that is being eroded
    #      base_height is the height of the Cube that is being hit by the wave (same as wave height)


    #Constructor for Cones
    def __init__(self, r: float, h: float):
        self.radius = r
        self.height = h
        self.base_radius = r
        self.height_radius_ratio = h / r
        self.angle = math.atan(h / r)

    #to_string method for pretty printing
    def __str__(self):
        return "Cone: radius: " + str(self.radius) + " | height: " + str(self.height) + \
                 " | base_radius: " + str(self.base_radius)
        
    #used in dictionary mapping
    def string_name(self):
        return "cone"

    #sets the base_height value, and the radius_above_base_height value as well
    def set_base_height(self, h: float) -> float:
        self.base_height = h
        self.radius_above_base_height = self.get_radius_at_h(self.radius, h) #this value is used for top_volume method

    #Returns the radius value at base_height (so: radius at the top of the wave-erosion area)
    def get_radius_at_base_height(self) -> float:
        #h is the height of the imaginary cone extending from the truncated cone that is the 
        # base being eroded; use the base_height_ratio to keep it consistent
        #h = self.height_radius_ratio * self.base_radius #use the original height to radius ratio to find the height of the imaginary cone
        r = self.get_radius_at_h(self.base_radius, self.base_height)
        return r

    #returns the radius of the Cone at height h
    #NOTE that base_radius is not self here, it varies 
    def get_radius_at_h(self, base_radius: float, h: float) -> float:
        triangle_adj = h / (math.tan(self.angle) + 0.000001) #add a little to not divide by 0
        return base_radius - triangle_adj


    #Returns the area of the base of the Cone that doesn't get eroded
    def get_top_area(self) -> float:
        top = math.pi * self.radius_above_base_height * self.radius_above_base_height
        return top

    #Returns the area of the of the base of the Cone, even during erosion process
    def get_eroded_base(self) -> float:
        base = math.pi * self.base_radius * self.base_radius

    #Returns the volume of the Cone as it currently stands
    def get_volume(self) -> float:
        top_vol = self.get_top_vol()
        bottom_vol = self.get_eroded_vol()
        return top_vol + bottom_vol

    #Returns the volume of the top part of the Cone that never gets eroded by a wave
    def get_top_vol(self) -> float:
        return ((self.height - self.base_height) * self.get_top_area() ) / 3

    #Returns the volume of the bottom part of the Cone that does get hit by waves
    def get_eroded_vol(self) -> float:
        #From: https://keisan.casio.com/exec/system/1223372110
        r1 = self.base_radius
        r2 = self.get_radius_at_base_height()
        h = self.base_height
        vol = (math.pi * h * ( (r1 * r1) + (r1 * r2) + (r2 * r2) ) ) / 3
        return vol
        

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

    #Returns # of sand grains in the eroding base
    def get_base_grains(self) -> float:
        global SAND_DIAMETER
        global SAND_VOLUME
        vol = self.get_eroded_vol() #m^3
        grains = vol / SAND_VOLUME
        return grains


    #Returns the lateral surface area of the bottom part of the Cone that does get hit by waves
    def get_eroding_surface_area(self) -> float:
        #From: https://keisan.casio.com/exec/system/1223372110
        r1 = self.base_radius
        r2 = self.get_radius_at_base_height()
        h = self.base_height
        surface_area = math.pi * (r1 + r2) * \
                        (  (r1 - r2)**2   + h**2   )**.5
        return surface_area + 0.00001 #add a little to make sure we don't divide by 0

    #returns cross-sectional area of the top part being eroded
    def get_cross_sectional_area(self) -> float:
        return self.get_radius_at_base_height()


