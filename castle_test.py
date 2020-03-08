import math
import sand_castle_shapes as shapes
import wave as waves
import numpy as np
import calculations as calc


'''
CONSTANTS for use in the file
'''
SAND_DENSITY = 2082.0 # kg / m^3
SAND_DIAMETER = 0.000375 # diameter in meters, aka 375 micro-meters
SAND_RADIUS = SAND_DIAMETER / 2 #meters
SAND_VOLUME = (4/3) * math.pi * (SAND_RADIUS**3)
WATER_DENSITY = 1023.6 # kg / m^3
GRAVITY = 9.81 # m / s^2
Z = 6 #max bond number for sand grains with water
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
#print(c.get_eroded_vol())
#print(c.get_base_grains())
print(c.get_cross_sectional_area())

print("Pyramid:")
c = shapes.Pyramid(1, 3)
c.set_base_height(3)
#print(c.get_eroded_vol())
#print(c.get_base_grains())
print(c.get_eroding_surface_area())
print(c.get_cross_sectional_area())

print("Cylinder:")
r = (1/math.pi)**.5
c = shapes.Cylinder(r, 1)
c.set_base_height(1)
#print(c.get_eroded_vol())
#print(c.get_base_grains())
print(c.get_cross_sectional_area())

print("Cone:")
r = (3/math.pi)**.5
c = shapes.Cone(r, 1)
c.set_base_height(1)
#print(c.get_eroded_vol())
#print(c.get_base_grains())
print(c.get_eroding_surface_area())
print(c.get_cross_sectional_area())
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
    #cohesion_multiplier is how many times more powerful the wave is than the forces holding the sand particles together
    wave_force = wave_force_on_shape(shape, wave) / shape.get_cross_sectional_area()
    global Z
    cohesion = calc.cohesion(Z)
    cohesion_multiplier = wave_force / cohesion
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


#checks to see if the wave obliterates the castle completely
# or if the base has become too eroded to support the top of the castle
def castle_still_standing(shape, wave) -> bool:
    #NOTE: split out obliteration and base-collapse into two separate predicate methods
    return standing_after_wave_hit(shape, wave) #and standing_after_erosion(shape, wave)

#returns the force of a wave as applied to a shape
def wave_force_on_shape(shape, wave) -> float:
    global WATER_DENSITY
    surface_area = shape.get_eroding_surface_area()
    wave_velocity = wave.wave_velocity
    force = WATER_DENSITY * surface_area * wave_velocity * wave_velocity
    return force

#returns a boolean on if the castle is still standing after a wave hit (not erosion)
def standing_after_wave_hit(shape, wave) -> bool:
    global Z
    max_shear_strength = calc.maximum_shear_strength(shape, wave, Z)
    wave_force = wave_force_on_shape(shape, wave)
    #calculate wave shear
    wave_shear = wave_force / shape.get_cross_sectional_area()
    return wave_shear < max_shear_strength






'''
Loop for testing castle configurations
'''
#Cube loop
#make an empty array to hold results
cube_array = list()
#only one way to have a volume of 1 m^3 with a cube
for s in range(1, 2):
    #Make waves one cm at a time
    for h in range(0, 10, 1):
        #now vary depth for wave break
            for d in range(1, 5, 1):
                #now vary distance past the sandcastle
                for dist in range(0, 10, 1):
                    #Make a shape and a wave
                    cube = shapes.Cube(s)
                    w = waves.Wave(h/100, d/5, dist/10)
                    cube.set_base_height(w.wave_height)
                    #now commence the testing!
                    wave_hits = 0
                    while castle_still_standing(cube, w):
                        wave_hits +=1
                        erode_shape(cube, w)
                    #now add the results to the results_array
                    t = (wave_hits, cube, w)
                    cube_array.append(t)


#Cylinder loop
#make an empty array to hold stuff
cylinder_array = list()
#time to permute our stuff
for r in range(1, 11):
    #Make waves one cm at a time
    for h in range(0, 10, 1):
        #now vary depth for wave break
            for d in range(1, 5, 1):
                #now vary distance past the sandcastle
                for dist in range(0, 10, 1):
                    #Make a shape and a wave
                    rad = (r / 10.0) + 0.00001 #Adding this to keep form dividing by zero
                    height = 1 / (math.pi * rad * rad)
                    #print("r: " + str(rad) + " | h: " + str(height))
                    cylinder = shapes.Cylinder(rad, height)
                    w = waves.Wave(h/100, d/5, dist/10)
                    cylinder.set_base_height(w.wave_height)
                    #now commence the testing!
                    wave_hits = 0
                    while castle_still_standing(cylinder, w):
                        wave_hits +=1
                        erode_shape(cylinder, w)
                    #now add the results to the results_array
                    t = (wave_hits, cylinder, w)
                    cylinder_array.append(t)



#Pyramid loop
#make an empty array to hold stuff
pyramid_array = list()
#time to permute our stuff
for l in range(1, 11):
    #Make waves one cm at a time
    for h in range(0, 10, 1):
        #now vary depth for wave break
            for d in range(1, 5, 1):
                #now vary distance past the sandcastle
                for dist in range(0, 10, 1):
                    #Make a shape and a wave
                    length = (l / 10) + 0.00001 #Adding this to keep form dividing by zero
                    height = 3 / (length * length)
                    pyramid = shapes.Pyramid(length, height)
                    w = waves.Wave(h/100, d/5, dist/10)
                    #pyramid.set_base_height(w.wave_height)
                    print("length: " + str(length) + " | h: " + str(height))
                    #now commence the testing!
                    wave_hits = 0
                    while castle_still_standing(pyramid, w):
                        wave_hits +=1
                        erode_shape(pyramid, w)
                    #now add the results to the results_array
                    t = (wave_hits, pyramid, w)
                    pyramid_array.append(t)


#Cone loop
#make an empty array to hold stuff
cone_array = list()
#time to permute our stuff
for r in range(1, 11):
    #Make waves one cm at a time
    for h in range(0, 10, 1):
        #now vary depth for wave break
            for d in range(1, 5, 1):
                #now vary distance past the sandcastle
                for dist in range(0, 10, 1):
                    #Make a shape and a wave
                    rad = (r / 10) + 0.00001 #Adding this to keep form dividing by zero
                    height = 3 / (math.pi * rad * rad)
                    cone = shapes.Cone(rad, h)
                    w = waves.Wave(h/100, d/5, dist/10)
                    cone.set_base_height(w.wave_height)
                    #print("r: " + str(rad) + " | h: " + str(height))
                    #now commence the testing!
                    wave_hits = 0
                    while castle_still_standing(cone, w):
                        wave_hits +=1
                        erode_shape(cone, w)
                    #now add the results to the results_array
                    t = (wave_hits, cone, w)
                    cone_array.append(t)



