# beta_plot.py

import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    sns.set_palette("deep", desat=.6)
    sns.set_context(rc={"figure.figsize": (8, 4)})
    x = np.linspace(0, 1, 100)
    params = [
        (0.5, 0.5),
        (1.0, 1.0),
        (4.0, 3.0),
        (2.0, 5.0),
        (6.0, 6.0)
    ]
    for p in params:
        y = beta.pdf(x, p[0], p[1])
        a = p[0]
        b = p[1]
        u = a/(a+b)
        s = ((a*b)/((a+b)**2*(a+b+1)))**0.5
        plt.plot(x, y, label="$\\alpha=%.4f$, $\\beta=%.4f$, $\\mu=%.4f$, $\\sigma=%.4f$" % (a,b,u,s))
    plt.xlabel("$\\theta$, Fairness")
    plt.ylabel("Density")
    plt.legend(title="Parameters")
    plt.show()
