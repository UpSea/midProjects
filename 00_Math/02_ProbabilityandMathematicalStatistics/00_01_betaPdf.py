'''mid
beta分布只需确定两个参数就可以得出其密度函数
这两个参数为：alpha，beta
在程序中，使用a代表alpha，b代表beta
一个确定的概率密度函数，有其均值和标准差
通过beta分布的alpha和beta可以直接求出此分布的mu和sigma
通过其mu和sigma也可以求出其alpha和beta
'''
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
        a = p[0]                                #mid alpha
        b = p[1]                                #mid beta
        u = a/(a+b)                             #mid mu
        s = ((a*b)/((a+b)**2*(a+b+1)))**0.5     #mid sigma
        plt.plot(x, y, label="$\\alpha=%.4f$, $\\beta=%.4f$, $\\mu=%.4f$, $\\sigma=%.4f$" % (a,b,u,s))
    plt.xlabel("$\\theta$, Fairness")
    plt.ylabel("Density")
    plt.legend(title="Parameters")
    plt.show()
