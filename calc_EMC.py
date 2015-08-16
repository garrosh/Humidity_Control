# Equilibrium Moisture Content Calculating function



def calc_EMC(temp, h):
    """ This function calculates the Equilibrium Moisture Content
    based on the Hailwood-Horrobin equation.

    Usage: calc_EMC(temperature, relative_humidity) where
    temperature = the temperature of ambiant air,
                  in Fahrenheit
    relative_humidity = the relative humidity of ambiant air,
                        as a ratio (0 to 1)

    ref: https://en.wikipedia.org/wiki/Equilibrium_moisture_content
    """
    temp_squared = temp * temp
    
    W = 330 + .452*temp + 0.00415*temp_squared
    k = .791 + 4.63e-4*temp - 8.44e-7 * temp_squared
    k1 = 6.34 + 7.75e-4*temp - 9.35e-5 * temp_squared
    k2 = 1.09 + 2.84e-2*temp - 9.04e-5 * temp_squared

    k_times_h = k * h
    
    Meq = 1800 / W * (k * h / (1 - k_times_h) + (k1 * k_times_h +
          2 * k1 * k2 * k_times_h * k_times_h) /
          (1 + k1 * k_times_h + k1 * k2 * k_times_h * k_times_h))
    return Meq
