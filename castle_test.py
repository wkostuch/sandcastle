import math
import sand_castle_shapes as shapes
import waves 


#NOTE:
# Workflow for making and testing shapes:
#   Step 1: Create the shape with the appropriate dimensions
#   Step 2: Update the shape's fields by calling set_base_height(h) with h = wave_height being tested 
#               (which should populate other needed fields that depend on that data)
#   Step 3: Start eroding in a loop by calling 
#   
#   

c = shapes.Cube(1)
c.set_base_height(.5)
print(c.get_eroded_vol())
print(c.get_base_grains())