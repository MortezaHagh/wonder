import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation


class Plotter:
    def __init__(self, model, plot_dyno=False):
        plt.ion()
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.set_title('GA', {'fontsize': 10, 'fontweight': 'normal',
                          'horizontalalignment': 'center', 'fontname': 'serif'})
        self.ax.axis('equal')
        self.ax.axis("off")
        LL = 20
        self.ax.axis([model.x_min-LL, model.x_max+LL,
                      model.y_min-LL, model.y_max+LL])
        self.model = model
        self.plot_model()

    def plot_model(self):

        #
        colors = plt.cm.get_cmap('rainbow', self.model.n_locs)
        self.colors = colors
        i = -1
        for x, y in zip(self.model.x_locs, self.model.y_locs):
            i += 1
            self.ax.plot(x, y, marker='s', markersize=8,
                         markeredgecolor=colors(i), markerfacecolor=colors(i))
            # text
            self.ax.text(x, y, str(i+1), {'fontsize': 10, 'fontweight': 'normal',
                         'horizontalalignment': 'center', 'fontname': 'serif'})

        # Walls
        DL = 15
        lx = self.model.x_max-self.model.x_min + 2*DL
        ly = self.model.y_max-self.model.y_min + 2*DL
        rect = patches.Rectangle((self.model.x_min-DL, self.model.y_min-DL),
                                 lx, ly, linewidth=2, edgecolor='k', facecolor='none')
        self.ax.add_patch(rect)

    def plot_cost(self, costs):
        fig, ax = plt.subplots(1, 1)
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Cost")
        ax.plot(costs)

    def plot_solution(self, sol):
        x = [self.model.x_locs[i] for i in sol]
        y = [self.model.y_locs[i] for i in sol]
        self.ax.plot(x, y, "-", linewidth=1)

    def update1(self, sol):
        x = [self.model.x_locs[i] for i in sol]
        y = [self.model.y_locs[i] for i in sol]
        self.line1, = self.ax.plot(x, y, "-", linewidth=1)

    def update2(self, sol):

        x = [self.model.x_locs[i] for i in sol]
        y = [self.model.y_locs[i] for i in sol]

        # updating data values
        self.line1.set_xdata(x)
        self.line1.set_ydata(y)

        # drawing updated values
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(0.1)
