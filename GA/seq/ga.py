import numpy as np
from copy import copy
from model import Model  # model model_j
from plotter import Plotter
from time import process_time
import matplotlib.pyplot as plt
from utils import roulette_wheel_selection
from operators import single_point_permutation_crossover, permutation_mutate


class Sol:
    def __init__(self) -> None:
        self.tour = []
        self.tour2 = []
        self.position = []
        self.d = None
        self.dd = None
        self.cost = None
        self.caps = None
        self.types = None


class Params:
    def __init__(self) -> None:
        self.n_pop = 100
        self.max_it = 100
        self.p_c = 0.8
        self.n_c_2 = int(round(self.p_c * self.n_pop / 2))
        self.n_c = 2 * self.n_c_2
        self.p_m = 0.5
        self.n_m = int(round(self.p_m * self.n_pop))
        self.beta = 6
        self.n_tournoment = 3
        self.selection_method = "RouletteWheel"  # Tournoment - Random - RouletteWheel


class GA:
    def __init__(self) -> None:

        # init
        self.plot = False
        self.nfe = 0
        self.iter = -1
        self.pop = []
        self.costs = []
        self.best_costs = []
        self.best_sol = None
        self.worst_sol = None
        self.selection_p = None

        # params and settings
        self.params = Params()
        self.nfe_iters = np.empty(self.params.max_it)

        # create model
        self.model = Model()
        self.n_p = self.model.n_zones * 2
        self.n_t = self.model.n_zones + 1

        # initialize
        self.initialize()

        # plot
        if self.plot:
            self.plotter = Plotter(self.model)
            self.plotter.update1(self.best_sol.position)

        # main
        tic = process_time()
        self.ga()
        toc = process_time()
        self.proc_time = toc - tic

        # final results and plot
        self.final()

    def cal_cost(self, sol: Sol):
        self.nfe += 1

        # tour
        temp = list(copy(sol.position))
        tour = list(copy(sol.position))
        for t in temp:
            if t in tour:
                tour.remove(self.model.zones[self.model.zones_id_dict[t]].id2)
        zones = copy(tour)
        tour = np.insert(tour, 0, self.model.id_start)
        tour = np.append(tour, self.model.id_start)
        sol.tour = tour

        # zones_ds - caps
        init_cap = self.model.robot.cap
        caps = [init_cap]
        zones_ds = []
        for i, z in enumerate(zones):
            init_cap = init_cap-self.model.zones[self.model.zones_id_dict[z]].res
            if init_cap < 0:
                init_cap = self.model.robot.cap
                # find best ds
                zones_ds.append(self.find_dock_st(zones[i-1], z))  # //////// ds
                caps.append(round(init_cap, 2))
                init_cap = init_cap - self.model.zones[self.model.zones_id_dict[z]].res
            caps.append(round(init_cap, 2))
            zones_ds.append(z)
        sol.caps = caps

        # tour2 - types
        tour2 = [self.model.id_start]
        t_type = ["dock"]
        for t in zones_ds:
            ind = self.model.all_id_dict[t]
            tour2.append(t)
            if self.model.all[ind].type == "zone":
                tour2.append(self.model.all[ind].id2)
                t_type.append("zone")
                t_type.append("zone")
            else:
                t_type.append("dock")
        tour2 = np.append(tour2, self.model.id_start)
        t_type.append("dock")
        sol.tour2 = tour2
        sol.types = t_type

        # distance
        dd = [self.model.distances[tour2[i], tour2[i+1]] for i in range(len(tour2)-1)]
        d = sum(dd) - self.model.sum_z_d

        #
        sol.d = d
        sol.dd = dd
        sol.cost = d

    def find_dock_st(self, z1, z2):
        dists = [self.model.distances[z1, d] + self.model.distances[d, z2] for d in self.model.dss_ids]
        min_ind = np.argmin(dists)
        return self.model.dss_ids[min_ind]

    def create_random_sol(self):
        s = np.random.permutation(self.model.zones_ids)
        return s

    def ga(self):

        for it in range(self.params.max_it):
            self.iter += 1
            self.best_costs.append(self.best_sol.cost)

            # Calculate Selection Probablities
            self.selection_probability()

            # Crossover
            popc = self.crossover()

            # Mutation
            popm = self.mutation()

            # Merg, Sort, Truncation
            self.next_pop(popc, popm)

            # Results
            self.iter_results()
            if self.plot:
                self.plotter.update2(self.best_sol.position)

    def crossover(self):
        popc = []
        for ic in range(self.params.n_c_2):
            #  select patrents
            ip1 = roulette_wheel_selection(self.selection_p)
            ip2 = roulette_wheel_selection(self.selection_p)
            p1 = self.pop[ip1]
            p2 = self.pop[ip2]

            sol1 = Sol()
            sol2 = Sol()
            x1, x2 = single_point_permutation_crossover(
                p1.position, p2.position, self.n_p)

            sol1.position = x1
            sol2.position = x2
            self.cal_cost(sol1)
            self.cal_cost(sol2)
            popc.append(sol1)
            popc.append(sol2)
        return popc

    def mutation(self):
        popm = []
        for im in range(self.params.n_m):
            ind_m = np.random.randint(1, self.params.n_pop)
            x = permutation_mutate(self.pop[ind_m].position, self.n_p)
            sol = Sol()
            sol.position = x
            self.cal_cost(sol)
            popm.append(sol)
        return popm

    def next_pop(self, popc, popm):
        self.pop.extend(popc)
        self.pop.extend(popm)
        self.sort_pop()
        self.pop = self.pop[:self.params.n_pop]
        self.costs = self.costs[:self.params.n_pop]

    def iter_results(self):
        self.best_sol = self.pop[0]
        self.worst_sol = self.pop[-1]
        self.nfe_iters[self.iter] = self.nfe
        print("Iteration:", self.iter, "Best Cost:", self.best_sol.cost)

    def selection_probability(self):
        p = np.exp(self.params.beta * self.costs / self.worst_sol.cost)
        self.selection_p = p / sum(p)

    def sort_pop(self):
        costs = [p.cost for p in self.pop]
        sort_inds = np.argsort(costs)
        self.costs = np.sort(costs)
        self.pop = [self.pop[i] for i in sort_inds]

    def initialize(self):
        for i in range(self.params.n_pop):
            sol = Sol()
            sol.position = self.create_random_sol()
            self.cal_cost(sol)
            self.pop.append(sol)
        self.sort_pop()
        self.best_sol = self.pop[0]
        self.worst_sol = self.pop[-1]

    def final(self):
        # print("sol tour: ", self.best_sol.tour)
        # print("sol tour2: ", self.best_sol.tour2)
        names = [self.model.all[self.model.all_id_dict[i]].name for i in self.best_sol.tour2]
        print("sol names: ", names)
        # print("sol types: ", self.best_sol.types)
        print("sol caps: ", self.best_sol.caps)
        # print("sol dd: ", self.best_sol.dd)
        print("sol d: ", round(self.best_sol.d, 2))
        print("process time:", self.proc_time)

        #
        plotter = Plotter(self.model)
        plt.ioff()
        # plotter.plot_solution(self.best_sol.tour)
        plotter.plot_solution(self.best_sol.tour2, 'g')
        plotter.plot_cost(self.best_costs)

        #
        if self.model.data is not None:
            print(" ==========================")
            print(self.model.data['solution'])
            print(" ==========================")

        plt.show()


if __name__ == "__main__":

    ga = GA()
