#---------------------------------------------------------------------------------
# Generate a distribution of points following the Soneira-Peebles fractal model
# Author: Pablo Villanueva Domingo
# Last update: 25/6/20
#---------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

#--- PARAMETERS ---#

# Reduction factor for the radii
lamb = 2
# Number of levels (not including the zero level)
n_levels = 5
# Maximum radius
R0 = 1000
# Size of the window
dimx = R0 + R0/lamb
# Mean number of points per cluster
eta = 5
# If 1, the number of points per cluster is a poisson process with eta as average number
eta_random = 0
# If 1, show scatter points
show_scatter = 1
# If 1, show scatter points
show_circles = 0
# Colors per level
cols = ["cyan", "r", "b", "g", "purple", "m", "k"]
#cols = []
#for i in range(n_levels+1):
#    cols.append("k")
# Random seed
seed = 0
# Size scatter points
s0 = 100
# Transparency for scatter points
alphapoints = .5


#--- FUNCTIONS ---#

# Poisson process in a disk
def poisson_process(eta, originx, originy, Rparent):

    if eta_random:
        num_points = np.random.poisson(eta)
    else:
        num_points = eta

    theta = 2.*np.pi*np.random.uniform(0, 1, num_points)
    rho = Rparent*np.sqrt(np.random.uniform(0, 1, num_points))

    xx = originx + rho*np.cos(theta)
    yy = originy + rho*np.sin(theta)

    return xx, yy

# Soneira-Peebles point process
def soneira_peebles_model(n_levels, eta, lamb, R0, seed):

    fig, ax = plt.subplots()
    margins = {  #     vvv margin in inches
    "left"   :     0.,
    "bottom" :     0.,
    "right"  :  1.,
    "top"    :  1.}
    fig.subplots_adjust(**margins)

    np.random.seed(seed=seed)
    Rparent = R0
    xparents, yparents = [0.], [0.]

    if show_scatter:
        ax.scatter(0., 0., s=s0, color=cols[0], alpha = alphapoints)
    if show_circles:
        circle = plt.Circle((0., 0.), Rparent, color=cols[0], alpha = 0.1)
        ax.add_artist(circle)

    for n in range(n_levels):
        R = Rparent/lamb
        pointsx, pointsy = [], []
        for i, j, in zip(xparents,yparents):
            originx, originy = i, j
            xx, yy = poisson_process(eta, originx, originy, Rparent)
            pointsx.extend(xx); pointsy.extend(yy)

        if show_scatter:
            ax.scatter(pointsx, pointsy, s=s0*(R/R0)**(2.), color=cols[n+1], alpha = alphapoints)
        if show_circles:
            for x, y in zip(pointsx, pointsy):
                circle = plt.Circle((x, y), R, color=cols[n+1], alpha = 0.3)
                ax.add_artist(circle)

        xparents, yparents = pointsx, pointsy
        Rparent = R

    if show_circles:
        plt.xlim([-dimx,dimx])
        plt.ylim([-dimx,dimx])
    plt.axis("off")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("Plots/soneirapeebles_levels_%d_eta_%d_lambda_%d_seed_%d_eta_random_%d.png"%(n_levels, eta, lamb, seed, eta_random), bbox_inches='tight', dpi=300)
    plt.show()
    plt.close(fig)



#--- MAIN ---#

for seed in range(5):
    soneira_peebles_model(n_levels, eta, lamb, R0, seed)
