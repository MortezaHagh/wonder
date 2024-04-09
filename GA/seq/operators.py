import numpy as np
from copy import copy


def single_point_permutation_crossover(xi1, xi2, n):

    x1 = copy(xi1)
    x2 = copy(xi2)

    ci = np.random.randint(1, n-1)

    x11 = x1[:ci+1]
    x12 = x1[ci+1:]

    x21 = x2[:ci+1]
    x22 = x2[ci+1:]

    r1 = np.intersect1d(x11, x22)
    r2 = np.intersect1d(x21, x12)

    x11[np.isin(x11, r1)] = r2
    x21[np.isin(x21, r2)] = r1

    y1 = np.concatenate((x11, x22))
    y2 = np.concatenate((x21, x12))

    return y1, y2


def permutation_mutate(xi, n):
    M = np.random.randint(1, 5)
    x = copy(xi)

    if M == 1:
        return do_swap(x, n)
    elif M == 2:
        return do_reversion(x, n)
    elif M == 3:
        return do_insertion(x, n)
    elif M == 4:
        return do_scramble(x, n)


def do_swap(x, n):
    i = np.random.choice(n, 2, replace=False)
    i1, i2 = i[0], i[1]

    y = np.copy(x)
    y[[i1, i2]] = x[[i2, i1]]
    return y


def do_reversion(x, n):
    i = np.random.choice(n, 2, replace=False)
    i1, i2 = min(i), max(i)

    y = np.copy(x)
    y[i1:i2+1] = x[i2:i1-1 if i1 != 0 else None:-1]
    return y


def do_insertion(x, n):
    i = np.random.choice(n, 2, replace=False)
    i1, i2 = min(i), max(i)

    if i1 < i2:
        y = np.concatenate((x[:i1], x[i1+1:i2+1], [x[i1]], x[i2+1:]))
    else:
        y = np.concatenate((x[:i2], [x[i1]], x[i2:i1], x[i1+1:]))
    return y


def do_scramble(x, n):
    i = np.random.choice(n, 2, replace=False)
    i1, i2 = min(i), max(i)

    m = i2 - i1 + 1
    p = np.arange(i1, i2 + 1)
    q = np.random.permutation(p)

    y = np.copy(x)
    y[p] = x[q]
    return y
