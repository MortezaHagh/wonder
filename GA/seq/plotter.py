import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation


class Plotter:
    def __init__(self, model, plot_dyno=False):
        # plt.ion()
        self.fig, self.ax = plt.subplots(1, 1)  # , figsize=(12, 8)
        self.ax.set_title('GA', {'fontsize': 10, 'fontweight': 'normal',
                          'horizontalalignment': 'center', 'fontname': 'serif'})
        # self.ax.axis('equal')
        # self.ax.axis("off")
        LL = 20
        self.ax.axis([model.x_min-LL, model.x_max+LL,
                      model.y_min-LL, model.y_max+LL])
        self.model = model
        self.plot_model()

    def plot_model(self):

        # Zones
        colors = plt.cm.get_cmap('rainbow', self.model.n_zones)
        self.colors = colors
        for i, z in enumerate(self.model.zones_b):
            self.ax.plot(z.x1, z.y1, marker='s', markersize=8,
                         markeredgecolor=colors(i), markerfacecolor=colors(i))
            self.ax.plot(z.x2, z.y2, marker='s', markersize=8,
                         markeredgecolor=colors(i), markerfacecolor=colors(i))
            # self.ax.plot(z.cx, z.cy, marker='o', markersize=8,
            #              markeredgecolor=colors(i), markerfacecolor=colors(i))
            dcircle = plt.Circle((z.cx, z.cy), z.rad)
            self.ax.add_artist(dcircle)
            # # text
            # self.ax.text(z.x1, z.y1+1, "z"+str(z.id)+"-1", {'fontsize': 10, 'fontweight': 'normal',
            #              'horizontalalignment': 'center', 'fontname': 'serif'})
            # self.ax.text(z.x2, z.y2+1, "z"+str(z.id)+"-2", {'fontsize': 10, 'fontweight': 'normal',
            #              'horizontalalignment': 'center', 'fontname': 'serif'})

        # zones
        for i, sz in enumerate(self.model.zones):
            self.ax.text(sz.x, sz.y-2, sz.name, {'fontsize': 10, 'fontweight': 'normal',
                         'horizontalalignment': 'center', 'fontname': 'serif'})

        # DS
        for i, ds in enumerate(self.model.dss):
            self.ax.plot(ds.x, ds.y, marker='s', markersize=8,
                         markeredgecolor='k', markerfacecolor='k')
            self.ax.text(ds.x, ds.y+1, "ds"+str(ds.id), {'fontsize': 7, 'fontweight': 'normal',
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

    def plot_solution(self, sol, color="k"):
        x = [self.model.xx[self.model.all_id_dict[i]] for i in sol]
        y = [self.model.yy[self.model.all_id_dict[i]] for i in sol]
        xm = [(x[i]+x[i+1])/2 for i in range(len(x)-1)]
        ym = [(y[i]+y[i+1])/2 for i in range(len(y)-1)]
        tm = [str(i) for i in range(len(y)-1)]
        self.ax.plot(x, y, "-", color=color, linewidth=1)
        for i in range(len(tm)):
            self.ax.text(xm[i], ym[i], tm[i], {'fontsize': 10, 'fontweight': 'normal',
                                               'horizontalalignment': 'center', 'fontname': 'serif', 'color': 'red'})

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
