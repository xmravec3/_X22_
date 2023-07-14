import os, random

def match_climbers(folder):
    m0 = random.choice(os.listdir(f"{folder}")).split(".")[0]
    m1 = random.choice(os.listdir(f"{folder}")).split(".")[0]
    return m0, m1
    
path = ""
print(match_climbers(path))
