
import numpy as np
from plotter import Plotter
import matplotlib.pyplot as plt


class Model:
    def __init__(self) -> None:

        # locations
        self.x_locs = [31, 36, 93, 22, 7, 34, 30, 9, 99,
                       84, 33, 3, 70, 61, 66, 31, 75, 50, 72, 4]
        self.y_locs = [62, 21, 27, 75, 99, 55, 1, 93, 89,
                       28, 32, 60, 49, 20, 72, 86, 13, 39, 87, 3]
        self.locs = [np.array((x, y))
                     for x, y in zip(self.x_locs, self.y_locs)]
        n_locs = len(self.x_locs)
        self.n_locs = n_locs

        # distances
        distances = np.empty((n_locs, n_locs))
        for i in range(distances.shape[0]-1):
            for j in range(i, distances.shape[1]):
                distances[i, j] = np.linalg.norm(self.locs[i]-self.locs[j])
                distances[j, i] = distances[i, j]

        self.distances = distances

        self.x_min = np.min(self.x_locs)
        self.x_max = np.max(self.x_locs)
        self.y_min = np.min(self.y_locs)
        self.y_max = np.max(self.y_locs)


if __name__ == "__main__":
    # create model
    model = Model()

    # plot
    Plotter(model)
    plt.show()
