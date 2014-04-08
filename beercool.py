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


print(massofcold(4, tfreeze, tfreeze+20, tfreeze))

print(massofcold(3785, 338, 339))
print(k_to_f(338))
print(k_to_f(339))


# 1 gallon at 151f lower 1 degree f with ice at freezing
tice = 0
tbase = 50
while tbase < 210:
    print(tbase)
    print(num_ice_cubes(1, tbase, tbase + 1, tice))
    print(fcoldmass(1, tbase, tbase+1, tice) * gramgallon)
    tbase += 10
