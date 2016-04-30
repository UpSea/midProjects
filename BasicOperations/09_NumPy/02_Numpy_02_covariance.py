import numpy as np

def Cov(xs, ys, meanx=None, meany=None):
    '''mid compute covariance of xs and ys'''
    xs = np.asarray(xs)
    ys = np.asarray(ys)
    if meanx is None:
        meanx = np.mean(xs)
    if meany is None:
        meany = np.mean(ys)
    cov = np.dot(xs-meanx, ys-meany) / len(xs)
    return cov

