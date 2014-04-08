#!/usr/bin/env python3
import argparse

# All units are in Kelvin and grams

# Specific heat of liquid water
shwater = 4.186 # Joules / gram Kelvin
# Specific heat of ice
shice = 2.09 # Joules / gram Kelvin
# Enthalpy of fusion of ice, energy required to melt ice without changing the temperature at 0C
enthfuse = 334 # Joules / gram
# Temperature of freezing water
tfreeze = 273.16 # Kelvin

# Grams per gallon of water
gramgallon = 3785.4

# Ice cubes a gallon of water could make
icegallon = 302.8

# The temperature of a freezer is typically 0 degrees fahrenheit or 255.372 Kelvin

def f_to_k(tempf):
    return (tempf + 459.67) * 5.0 / 9.0

def k_to_f(tempk):
    return (tempk * 9.0 / 5.0) - 459.67

# Energy released cooling water, mass in grams, temperature in Kelvin
def energy_of_water_cool(mass, temp_diff):
    return shwater * mass * temp_diff

# Energy required to bring ice up to melting point or energy required to bring water down to freezing point, mass in grams, temperature in Kelvin
def energy_of_ice_1(mass, temp_init):
    if temp_init <= tfreeze:
        return shice * mass * (tfreeze - temp_init)
    else:
        return shwater * mass * (tfreeze - temp_init)

# Energy required to change phase of ice to water, mass in grams
def energy_of_ice_2(mass):
    return enthfuse * mass

# Energy required to bring water from freezing point to desired temperature
def energy_of_ice_3(mass, temp_end):
    if temp_end >= tfreeze:
        return shwater * mass * (temp_end - tfreeze)
    else:
        return shice * mass * (temp_end - tfreeze)

# Energy required to bring ice (or water) up to desired temperature OR energy released bringing water (or ice) down to desired temperature
def energy_of_ice_warm(mass, temp_init, temp_end):
    e1 = energy_of_ice_1(mass, temp_init)
    e2 = 0.0
    if temp_init <= tfreeze and temp_end > tfreeze:
        e2 = energy_of_ice_2(mass)
    elif temp_init > tfreeze and temp_end <= tfreeze:
        e2 = 0.0 - energy_of_ice_2(mass)
    e3 = energy_of_ice_3(mass, temp_end)
    return e1 + e2 + e3

# Calculate Joules per gram for difference in temperature

# Joules per gram to bring ice to melting point
def jpg_1(temp_below_freeze):
    return shice * (tfreeze - temp_below_freeze)
# Joules per gram to melt ice
def jpg_2():
    return enthfuse
# Joules per gram to warm water at freezing point
def jpg_3(temp_above_freeze):
    return shwater * (temp_above_freeze - tfreeze)

# Joules per gram required to heat water at temp_low to temp_high
def jpg(temp_low, temp_high):
    jpg1 = 0.0
    if temp_low < tfreeze:
        jpg1 = jpg_1(temp_low)
    jpg2 = 0.0
    if temp_low <= tfreeze and temp_high >= tfreeze:
        jpg2 = jpg_2()
    jpg3 = 0.0
    if temp_high > tfreeze:
        jpg3 = jpg_3(temp_high)
    return jpg1 + jpg2 + jpg3

# Haves:
#  Mass of hot
#  Temp of hot
#  Temp of cold
# Want:
#  Mass of cold

def masscold(mass_hot, temp_want, temp_hot, temp_cold):
    # Joules per gram needed to remove to convert h2o at hot to wanted temperature 
    jpg_htw = jpg(temp_want, temp_hot)
    # Joules per gram required to heat h2o from cold to wanted temperature
    jpg_ctw = jpg(temp_cold, temp_want)
    
    # Mass of cold is Joules removed from hot divided by jpg_ctw, which is ((jpg_htw * mass_hot) / jpg_ctw)
    return (jpg_htw * mass_hot) / jpg_ctw


# Temperature is in Kelvin, mass will be returned in whatever unit you put in
def massofcold(mass_hot, temp_want, temp_hot, temp_cold=255.372):
    top = shwater * mass_hot * (temp_hot - temp_want)
    bottom = (temp_want - tfreeze) * shwater
    if temp_cold <= tfreeze:
        bottom += enthfuse + (tfreeze - temp_cold) * shice
    return top / bottom

# Temperature is in fahrenheit, mass is returned in whatever unit is put in
def fcoldmass(mass_hot, temp_want, temp_hot, temp_cold=0.0):
    return massofcold(mass_hot, f_to_k(temp_want), f_to_k(temp_hot), f_to_k(temp_cold))

# temp in fahrenheit
def num_ice_cubes(gallons_hot, temp_want, temp_hot, temp_cold=0.0):
    return fcoldmass(gallons_hot, temp_want, temp_hot, temp_cold) * icegallon

"""def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-h', '--mass_hot', help="Mass of hot " + str(time), default=time, type=float)
    parser.add_argument('-c', '--sounds', help="Number of distinct parts in an identitone, default=" + str(sounds), default=sounds, type=int)
    parser.add_argument('-n', '--notes', help="Number of notes in each part of the identitone, default=" + str(notes), default=notes, type=int)
    parser.add_argument('-r', '--rate', help="Sample rate in Hz, default=" + str(rate), default=rate, type=int)
    parser.add_argument('seed', help="Seed string for creating the hash", type=str)
    parser.add_argument('filename', help="File to generate", type=str)"""


print(masscold(4, tfreeze+0.0001, tfreeze+20, tfreeze))

#print(massofcold(3785, 338, 339))
#print(k_to_f(338))
#print(k_to_f(339))


# 1 gallon at 151f lower 1 degree f with ice at freezing
tice = 0
tbase = 50
#while tbase < 210:
#    print(tbase)
#    print(num_ice_cubes(1, tbase, tbase + 1, tice))
#    print(fcoldmass(1, tbase, tbase+1, tice) * gramgallon)
#    tbase += 10
