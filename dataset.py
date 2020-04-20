import os
import numpy as np

def get_random_prefix(dataset, length=0):
    with open("datasets/{}".format(dataset), "r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line[:length] for line in lines if len(line) >= length and line != "\n"]
    random_prefix = np.random.choice(lines)
    return random_prefix
    

    