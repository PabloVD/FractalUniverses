#--------------------------------------------------------------------------------------------------------------------------------------
# Generate a distribution of points following a Multiplicative Random Process
# See e.g. Meakin 1987; Martinez, Jones et al 1990
# Author: Pablo Villanueva Domingo
# Last update: 30/6/20
#--------------------------------------------------------------------------------------------------------------------------------------

import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt
import random

#--- PARAMETERS ---#

# Maximum and minimum lengths
lmax = 10.
lmin = 0.

# Probabilities
# For multifractal, for example
p1 = 1.
p2 = 0.75
p3 = 0.5
p4 = 0.25

# For simple fractal
"""p1 = 1.
p2 = 1.
p3 = 1.
p4 = 0."""

# Random seed
seed = 0
np.random.seed(seed)

# Number of steps
n_steps = 8

cmap = "Greys"#"gray"

#--- FUNCTIONS ---#

def multiplicative(xx, yy, probs, delta):

    x_new, y_new, probs_new = [], [], []

    for x, y, p in zip(xx, yy, probs):

        x1 = x #- delta/2
        x2 = x + delta
        y1 = y #- delta/2
        y2 = y + delta

        """rand = np.random.uniform(0.,1.)
        if rand<p:
            p = 1.
        else:
            p = 0."""

        # Take random selection of probabilities
        pvec = random.sample([p1*p, p2*p, p3*p, p4*p], 4)

        x_new.extend([x1, x2, x1, x2])
        y_new.extend([y1, y1, y2, y2])
        probs_new.extend(pvec)

    return x_new, y_new, probs_new

#--- MAIN ---#

x = [lmin, lmax, lmin, lmax]
y = [lmin, lmin, lmax, lmax]
probs = [p1, p2, p3, p4]

for step in range(n_steps):
    x, y, probs = multiplicative(x, y, probs, lmax/2**(step+1))

logprobs = np.zeros_like(probs)
for i, p in enumerate(probs):
    #if p==0.:
    if p<=1.e-5:
        logprobs[i] = -5
    else:
        logprobs[i] = np.log10(p)

plt.scatter(x, y, s=2, c=logprobs, cmap=cmap)
plt.axis("off")
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig("Plots/multiplicative_levels_%d_probs_%04.2f_%04.2f_%04.2f_%04.2f_seed_%d.png"%(n_steps, p1, p2, p3, p4, seed), bbox_inches='tight', dpi=300)
plt.show()
plt.close()
