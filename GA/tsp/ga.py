import numpy as np
from model import Model
from plotter import Plotter
import matplotlib.pyplot as plt
from utils import roulette_wheel_selection
from operators import single_point_permutation_crossover, permutation_mutate


class Sol:
    def __init__(self) -> None:
        self.tour = []
        self.position = []
        self.cost = None


class Params:
    def __init__(self) -> None:
        self.n_pop = 50
        self.max_it = 100

        self.p_c = 0.8
        self.n_c_2 = int(round(self.p_c * self.n_pop / 2))
        self.n_c = 2 * self.n_c_2
        self.p_m = 0.5
        self.n_m = int(round(self.p_m * self.n_pop))

        self.beta = 8
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
        self.n = self.model.n_locs

        # initialize
        self.initialize()

        # plot
        if self.plot:
            self.plotter = Plotter(self.model)
            self.plotter.update1(self.best_sol.position)

        # main
        self.ga()

        # final results and plot
        self.final()

    def cal_cost(self, sol: Sol):
        self.nfe += 1
        sol.tour = np.insert(sol.position, 0, sol.position[-1])
        d = [self.model.distances[sol.tour[i], sol.tour[i+1]]
             for i in range(self.n)]
        sol.cost = sum(d)

    def create_random_sol(self):
        return np.random.permutation(self.model.n_locs)

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
                p1.position, p2.position, self.n)

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
            ind_m = np.random.randint(1, self.n-1)
            x = permutation_mutate(self.pop[ind_m].position, self.n)
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
        plotter = Plotter(self.model)
        plt.ioff()
        plotter.plot_solution(self.best_sol.tour)
        plotter.plot_cost(self.best_costs)
        plt.show()


if __name__ == "__main__":

    ga = GA()
