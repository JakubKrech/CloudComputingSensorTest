import random
import math
import time
from sys import argv

#   temperature     C
#   humidity        %
#   air_pressure    hPa
#   pm10    ug/m3
#   pm2_5   ug/m3
#   pm1     ug/m3

temperature_bounds = [-35, 40]
humidity_bounds = [20, 97.5]
air_pressure_bounds = [980, 1030]
pm10_bounds = [0.5, 200]
pm2_5_bounds = [0.5, 200]
pm1_bounds = [0.5, 200]

def initialize_parameters():
    temperature  = round(random.triangular(*temperature_bounds), 2)
    humidity     = round(random.triangular(*humidity_bounds), 2)
    air_pressure = round(random.triangular(*air_pressure_bounds), 2)
    pm10  = round(random.triangular(*pm10_bounds), 2)
    pm2_5 = round(random.triangular(*pm2_5_bounds), 2)
    pm1   = round(random.triangular(*pm1_bounds), 2)

    return temperature, humidity, air_pressure, pm10, pm2_5, pm1

def clamp_values_to_bounds(value, bounds):
    return round(max(min(value, bounds[1]), bounds[0]), 2)

def perform_next_step_generation(parameters):
    new_temp  = clamp_values_to_bounds(parameters[0] + random.uniform(-0.2, 0.2), temperature_bounds)
    new_humid = clamp_values_to_bounds(parameters[1] + random.uniform(-0.3, 0.3), humidity_bounds)
    new_airPr = clamp_values_to_bounds(parameters[2] + random.uniform(-0.1, 0.1), air_pressure_bounds)
    new_pm10  = clamp_values_to_bounds(parameters[3] + random.uniform(-0.5, 0.5), pm10_bounds)
    new_pm2_5 = clamp_values_to_bounds(parameters[4] + random.uniform(-0.5, 0.5), pm2_5_bounds)
    new_pm1   = clamp_values_to_bounds(parameters[5] + random.uniform(-0.5, 0.5), pm1_bounds)

    return new_temp, new_humid, new_airPr, new_pm10, new_pm2_5, new_pm1

#print(initialize_parameters())

# mockmock = initialize_parameters()
# while 1:
#     print(mockmock)
#     mockmock = perform_next_step_generation(mockmock)
#     time.sleep(0.5)
