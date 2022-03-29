#--------------------------------------------------------------------------------------------------------------------------------------
# Generate a distribution of points following the Mandelbrot's fractal model of galaxy clustering based on Rayleigh-Lévy random walks
# Author: Pablo Villanueva Domingo
# Last update: 27/6/20
#--------------------------------------------------------------------------------------------------------------------------------------

import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt

#--- PARAMETERS ---#

# Characteristic length for the probability distribution function of distances
l0 = 5.
# Fractal dimension and slope for the probability distribution function of distances. Must be larger than 0.
# The larger Df, the sparser is the distribution
Df = 1.
# Length of the box
lbox = 40.
# Minimum distance considered
x0 = 0.001
# Maximum distance considered
x1 = lbox
# Number of steps per random walk
n_steps = 100
# Number of random walks
n_walks = 5
# List of random seeds
llavors = range(10) # [0]


#--- FUNCTIONS ---#

# Sample from probability distribution function, from https://stackoverflow.com/questions/4265988/generate-random-numbers-with-a-given-numerical-distribution
# Suggests a list of size random samples between x0 and x1 and accepts the suggestion with probability CustDist(l)
# CustDist noes not need to be normalized. Add this condition to increase performance.
def sample_from_pdf(x0, x1, CustDist, size, nControl=10**6):

    samples=[]
    nLoop=0
    while len(samples)<size and nLoop<nControl:
        x=np.random.uniform(low=x0,high=x1)
        prop = CustDist(x)
        assert prop>=0# and prop<=1 # is a pdf, not need to be <1
        if np.random.uniform(low=0,high=1) <=prop:
            samples += [x]
        nLoop+=1
    return samples

# Probability distribution function for distances
# Note: this is the pdf, not the cumulative!
# i.e., this is p(r), defined from P(>l)=\int_l^\infty p(r)dr ( = \int_l^\infty \tilde{p}(r)d^n r, in n dimensions, where \tilde{p} is f_1 in Peebles' book )
def prob_dist(l):
    prob = Df*(l0/l)**(Df+1.)/l0
    if l<l0:
        return 0.
    else:
        return prob

# Produce a Rayleigh-Levy random walk
def rayleigh_levy_random_walk():
    x, y = np.random.uniform(-lbox, lbox), np.random.uniform(-lbox, lbox)
    pointsx, pointsy = [x], [y]
    ball_sizes = [10.]

    for step in range(n_steps):
        l = sample_from_pdf(x0, x1, prob_dist, size=1)[0]
        angle =  2.*np.pi*np.random.uniform(0, 1)
        x, y = x+np.cos(angle)*l, y+np.sin(angle)*l
        pointsx.append(x); pointsy.append(y); ball_sizes.append(1.- (step+1)/n_steps)

    return pointsx, pointsy, ball_sizes


#--- MAIN ---#

for llavor in llavors:

    np.random.seed(llavor)

    fig, ax = plt.subplots()

    pointsx, pointsy = [], []
    for walk in range(n_walks):
        px, py, ball_sizes = rayleigh_levy_random_walk()
        ax.scatter(px, py, s=ball_sizes)
        pointsx.extend(px); pointsy.extend(py)

    plt.axis("off")
    #ax.scatter(pointsx, pointsy, s=0.5, color="b")
    plt.savefig("Plots/rayleigh_levy_fractal_l0_%d_Df_%d_n_steps_%d_n_walks_%d_seed_%d.png"%(int(l0), int(Df), n_steps, n_walks, llavor), bbox_inches='tight', dpi=300)
    #plt.show()
    plt.close(fig)
