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

# Temperature of an average freezer
freezert = 255.372
# Grams per gallon of water
gramgallon = 3785.4
# Ice cubes a gallon of water could make
icegallon = 302.8
# Grams in an ice cube
icegram = 12.5

# The temperature of a freezer is typically 0 degrees fahrenheit or 255.372 Kelvin

def f_to_k(tempf):
    return (tempf + 459.67) * 5.0 / 9.0

def k_to_f(tempk):
    return (tempk * 9.0 / 5.0) - 459.67

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
    else:
        jpg1 = 0.0 - jpg_3(temp_low)
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

# Temperature in Kelvin, mass in grams
def masscold(mass_hot, temp_want, temp_hot, temp_cold):
#    print("mh: " + str(mass_hot))
#    print("tw: " + str(temp_want))
#    print("th: " + str(temp_hot))
#    print("tc: " + str(temp_cold))
    # Joules per gram needed to remove to convert h2o at hot to wanted temperature 
    jpg_htw = jpg(temp_want, temp_hot)
    # Joules per gram required to heat h2o from cold to wanted temperature
    jpg_ctw = jpg(temp_cold, temp_want)
#    print("jpg_htw: " + str(jpg_htw))
#    print("jpg_ctw: " + str(jpg_ctw))
    # Mass of cold is Joules removed from hot divided by jpg_ctw, which is ((jpg_htw * mass_hot) / jpg_ctw)
    return (jpg_htw * mass_hot) / jpg_ctw

# Temperature is in fahrenheit, mass is in grams
def fcoldmass(mass_hot, temp_want, temp_hot, temp_cold=0.0):
    return masscold(mass_hot, f_to_k(temp_want), f_to_k(temp_hot), f_to_k(temp_cold))

# temp in fahrenheit, amount is in gallons, returns the number of grams of ice needed
def ice_cube_grams(gallons_hot, temp_want, temp_hot, temp_cold=0.0):
    return fcoldmass(gallons_hot * gramgallon, temp_want, temp_hot, temp_cold)

def num_ice_cubes(gallons_hot, temp_want, temp_hot, temp_cold=0.0):
    return ice_cube_grams(gallons_hot, temp_want, temp_hot, temp_cold) / icegram

"""def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-h', '--mass_hot', help="Mass of hot " + str(time), default=time, type=float)
    parser.add_argument('-c', '--sounds', help="Number of distinct parts in an identitone, default=" + str(sounds), default=sounds, type=int)
    parser.add_argument('-n', '--notes', help="Number of notes in each part of the identitone, default=" + str(notes), default=notes, type=int)
    parser.add_argument('-r', '--rate', help="Sample rate in Hz, default=" + str(rate), default=rate, type=int)
    parser.add_argument('seed', help="Seed string for creating the hash", type=str)
    parser.add_argument('filename', help="File to generate", type=str)"""


print(masscold(4, tfreeze+0.0001, tfreeze+20, tfreeze))

print(masscold(400, 60 + tfreeze, 61 + tfreeze, tfreeze-10))
print(masscold(400, 30 + tfreeze, 31 + tfreeze, tfreeze-10))

#print(massofcold(3785, 338, 339))
#print(k_to_f(338))
#print(k_to_f(339))


# 1 gallon at 151f lower 1 degree f with ice at freezing
tice = 0
tbase = 50
while tbase < 210:
    print(tbase)
    print(num_ice_cubes(1, tbase, tbase + 1, tice))
    print(fcoldmass(1, tbase, tbase+1, tice) * gramgallon)
    print()
    tbase += 10
