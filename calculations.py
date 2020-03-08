import math
import sand_castle_shapes
import wave


#returns max shear strength given a shape, wave height, and bond number
def maximum_shear_strength(shape, wave, z) -> float:

    #set the height based on this particular wave
    shape.set_base_height(wave.wave_height)

    #Set the needed variables for the function
    #Normal stress
    normal_force = shape.get_normal_sand()
    area = shape.get_cross_sectional_area()
    mu = 0.66
    

    #Calculate the shear strength
    shear_strength = ((normal_force / area) *  mu) + cohesion(z)

    return shear_strength

#Determin the cohesion for a given bond number z 
def cohesion(z) -> float:
    
    volume_correction = (3 / (4 * math.pi))
    phi = 0.6 
    kappa = 0.4
    s = 0.5
    sand_size = 0.000375
    mu = 0.66

    cohesion = ((volume_correction) * s * mu * ((phi * kappa * z) / sand_size))
    return cohesion





    