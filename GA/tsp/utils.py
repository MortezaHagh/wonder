import numpy as np


def roulette_wheel_selection(p):
    r = np.random.rand()
    ca = p.cumsum()
    return np.where(ca > r)[0][0]
