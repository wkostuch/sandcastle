import math
import sand_castle_shapes as shapes
import wave 


'''
CONSTANTS for use in the file
'''
SAND_DENSITY = 2082.0 # kg / m^3
SAND_DIAMETER = 0.000375 # diameter in meters, aka 375 micro-meters
SAND_RADIUS = SAND_DIAMETER / 2 #meters
SAND_VOLUME = (4/3) * math.pi * (SAND_RADIUS**3)
WATER_DENSITY = 1023.6 # kg / m^3
GRAVITY = 9.81 # m / s^2
#Friendly reminder that N = (kg * m) / s^2

#NOTE:
# Workflow for making and testing shapes:
#   Step 1: Create the shape with the appropriate dimensions
#   Step 2: Update the shape's fields by calling set_base_height(h) with h = wave_height being tested 
#               (which should populate other needed fields that depend on that data)
#   Step 3: Start eroding in a loop by calling 
#   
#   
'''
print("Cube:")
c = shapes.Cube(1)
c.set_base_height(.5)
print(c.get_eroded_vol())
print(c.get_base_grains())

print("Pyramid:")
c = shapes.Pyramid(1, 3)
c.set_base_height(3)
print(c.get_eroded_vol())
print(c.get_base_grains())
print(c.get_eroding_surface_area())

print("Cylinder:")
r = (1/math.pi)**.5
c = shapes.Cylinder(r, 1)
c.set_base_height(.5)
print(c.get_eroded_vol())
print(c.get_base_grains())

print("Cone:")
r = (3/math.pi)**.5
c = shapes.Cone(r, 1)
c.set_base_height(1)
print(c.get_eroded_vol())
print(c.get_base_grains())
print(c.get_eroding_surface_area())
'''

#Erodes the shape object with a wave
def erode_shape(shape, wave):
    pre_erosion_radius = shape.base_radius
    sand_washed_away = num_grains_eroded(shape, wave)
    layers_eroded = num_layers_eroded(shape, sand_washed_away)
    depth_eroded = grains_to_meters(layers_eroded)
    #Now update the base radius of the shape
    post_erosion_radius = pre_erosion_radius - depth_eroded
    shape.update_base_radius(post_erosion_radius)
    #If the shape has a base_side_length, update it
    if type(shape) is shapes.Cube or type(shape) is shapes.Pyramid:
        old_length = shape.base_side_length
        new_length = old_length - 2 * depth_eroded
        shape.base_side_length = new_length



#calculates the number of grains washed away
def num_grains_eroded(shape, wave) -> int:
    #NOTE: update this once cohesion force is known
    ''' NEED SAND BOND STRENGTH + WAVE FORCE '''
    #cohesion_multiplier is how many times more powerful the wave is than the forces holding the sand particles together
    cohesion_multiplier = 0 
    #Round to an int so that if it's below the required force to break sand-bonds then the product is 0 and no sand is removed
    sand_removed = wave.wave_height * wave.wave_distance_past_castle * int(cohesion_multiplier)
    return sand_removed

#calculates the number of layers eroded by a wave
def num_layers_eroded(shape, num_grains: int) -> int:
    surface_area = shape.get_eroding_surface_area()
    layers = num_grains / surface_area
    #Can think of layers as the depth of sand being removed from the base
    return int(layers)

#converts sand grains to meters; sand grains lined up in a row
#n is the number of sand grains
def grains_to_meters(n: float) -> float:
    global SAND_DIAMETER
    return n * SAND_DIAMETER


c = shapes.Cone(1, 3)
c.set_base_height(1)
w = wave.Wave(.1, 1, 2)
print(c.get_eroding_surface_area())
erode_shape(c, w)
print(c.get_eroding_surface_area())


'''
Loop for testing castle configurations
'''

