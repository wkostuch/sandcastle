import math
import sand_castle_shapes as shapes
import wave 


#NOTE:
# Workflow for making and testing shapes:
#   Step 1: Create the shape with the appropriate dimensions
#   Step 2: Update the shape's fields by calling set_base_height(h) with h = wave_height being tested 
#               (which should populate other needed fields that depend on that data)
#   Step 3: Start eroding in a loop by calling 
#   
#   

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


#Erodes the shape object with a wave
def erode_shape(shape, wave):
    pre_hit_vol = shape.get_eroded_vol()
