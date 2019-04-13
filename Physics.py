"""Program for practicing physics"""
# Ryan Allard, April 2019

import random

# 10 ^ x Hz for frequency
frequencies = {"radio": 8, "microwave": 10, "infrared": 12, "visible": 14, "ultraviolet": 16, "xray": 18, "gamma": 20}
# 10 ^ x meters for wave length
wavelengths = {"radio": 0, "microwave": -2, "infrared": -4, "visible": -6, "ultraviolet": -8, "xray": -10, "gamma": -12}
# Nanometers of wave length
lightWaves = {"red": 700, "violet": 400}

while True:

    if random.randint(1, 2) == 1:
        freq = random.choice(list(frequencies.keys()))

        answer = input(f"What is the OOM of the frequency of {freq} waves? ")

        if answer == str(frequencies[freq]):
            print(f"correct!, it is 10^{answer} Hz")
        else:
            print(f"Its actually {frequencies[freq]}")

    else:
        wave = random.choice(list(wavelengths.keys()))

        answer = input(f"What is the OOM of the wavelength of {wave} waves? ")

        if answer == str(wavelengths[wave]):
            print(f"correct!, it is 10^{answer} meters")
        else:
            print(f"Its actually {wavelengths[wave]}")
