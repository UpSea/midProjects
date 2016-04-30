from toolz import groupby, juxt
inc = lambda x: x + 1
double = lambda x: x * 2
exp = lambda x: x*x
a = juxt(inc, double,exp)(10)
b = juxt([inc, double,exp])(10)
c = 0 