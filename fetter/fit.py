import numpy as np

def linear_fit(xvals: np.ndarray, yvals: np.ndarray):
    """r
    xvals, yvals: data points given as a list (separately) as input
    Return values:
        a: intercept
        b: slope
        delA2: variance of a
        delB2: variance of b
        cov: covariance of a, b
        chi2: chi^2 / dof
        Linear plot: y = a + b*x
    """
    n = len(xvals)   # number of datapoints

    s, sx, sy, sxx, sxy = 0, 0, 0, 0, 0
    for i in range(n):
        s += 1
        sx += xvals[i]
        sy += yvals[i]
        sxx += xvals[i]**2
        sxy += xvals[i]*yvals[i]

    delta = s*sxx - sx**2
    a = (sxx*sy - sx*sxy) / delta
    b = (s*sxy - sx*sy) / delta

    delA2 = sxx / delta; delB2 = s / delta
    return a, b, delA2, delB2
