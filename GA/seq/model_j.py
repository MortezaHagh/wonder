
import json
import numpy as np
from copy import deepcopy
from plotter import Plotter
import matplotlib.pyplot as plt


class Robot:
    def __init__(self) -> None:
        self.cap = 4


class DS:
    def __init__(self, id, x, y) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.r = 1
        self.name = "ds"+str(id)
        self.type = "dock"


class Zone:
    def __init__(self, id, x1, y1, x2, y2, cx, cy, res) -> None:
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cx = cx
        self.cy = cy
        self.res = res
        self.rad = res/4
        self.name = "z"
        self.type = "zone"


class ZoneS:
    def __init__(self, id, x, y, res, id2) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.res = res
        self.id2 = id2
        self.name = "z"+str(id)
        self.type = "zone"


class Model:
    def __init__(self) -> None:

        # Robot
        self.robot = Robot()
        # self.n_zones = 6
        # self.n_ds = 2

        # Opening JSON file
        path = "/home/morteza/dev/GA/problems.json"
        with open(path) as json_file:
            input_data = json.load(json_file)

        data = input_data[5]
        self.data = data

        # zones
        self.zones_b = []
        for i, z in enumerate(data['zones']):
            id = i
            x1 = z["point1"][0]
            y1 = z["point1"][1]
            x2 = z["point2"][0]
            y2 = z["point2"][1]
            cx = (x1+x2)/2
            cy = (y1+y2)/2
            res = z["resources"]
            self.zones_b.append(Zone(id, x1, y1, x2, y2, cx, cy, res))
        self.n_zones = len(self.zones_b)
        print(self.n_zones)

        # ZoneS
        self.zones = []
        self.sum_z_d = 0
        for z in self.zones_b:
            sz1 = ZoneS(z.id, z.x1, z.y1, z.res, z.id + self.n_zones)
            self.zones.append(sz1)
            sz2 = ZoneS(z.id+self.n_zones, z.x2, z.y2, z.res, z.id)
            self.zones.append(sz2)
        self.zones_ids = [z.id for z in self.zones]
        self.zones_id_dict = {id: i for i, id in enumerate(self.zones_ids)}

        # DS
        k = 2*self.n_zones
        self.dss = []
        for i, ds in enumerate(data['dockings']):
            id = k+i
            x = ds['position'][0]
            y = ds['position'][1]
            self.dss.append(DS(id, x, y))
        self.n_ds = len(self.dss)
        self.dss_ids = [d.id for d in self.dss]
        self.dss_id_dict = {id: i for i, id in enumerate(self.dss_ids)}
        self.id_start = self.dss_ids[0]  # ----------------

        # All
        self.all = deepcopy(self.zones)
        self.all.extend(self.dss)

        #
        self.n_all = len(self.all)
        self.all_ids = [a.id for a in self.all]
        self.all_id_dict = {id: i for i, id in enumerate(self.all_ids)}
        self.xx = [a.x for a in self.all]
        self.yy = [a.y for a in self.all]

        #
        self.locs = [np.array((x, y))
                     for x, y in zip(self.xx, self.yy)]

        # distances
        distances = np.empty((self.n_all, self.n_all))
        for i in range(distances.shape[0]-1):
            for j in range(i, distances.shape[1]):
                distances[i, j] = np.linalg.norm(self.locs[self.all_id_dict[i]]-self.locs[self.all_id_dict[j]])
                distances[j, i] = distances[i, j]
        self.distances = distances

        # sum_z_d
        for sz in self.zones:
            self.sum_z_d += np.linalg.norm(self.locs[self.all_id_dict[sz.id]]-self.locs[self.all_id_dict[sz.id2]])
        self.sum_z_d = self.sum_z_d / 2

        # limits
        self.x_min = np.min(self.xx)
        self.x_max = np.max(self.xx)
        self.y_min = np.min(self.yy)
        self.y_max = np.max(self.yy)


if __name__ == "__main__":
    # create model
    model = Model()

    # plot
    Plotter(model)
    plt.ioff()
    plt.show()
