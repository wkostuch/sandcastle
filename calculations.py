import math
import sand_castle_shapes


#returns max shear strength given a shape, wave height, and bond number

def maximum_shear_strength(shape, wave_height, z) -> float:

    #set the height based on this particular wave
    shape.set_base_height(wave_height)

    
    #Set the needed variables for the function

    #Normal stress
    normal_force = shape.get_normal_sand()
    area = get_cross_sectional_area()
    mu = 0.66

    #Cohesion 
    volume_correction = (3 / (4 * math.pi))
    phi = 0.6 
    kappa = 0.4
    s = 0.5

    #Calculate the shear strength
    shear_strength = ((normal_force / area) *  mu) + ((volume_correction) * s * mu * ((phi * kappa * z) / sand_density))

    return shear_strength




    