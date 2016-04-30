from scipy import integrate
import math 

def xx(x):
    return (-x+3)*x

def half_circle(x):
    return (1-x**2)**0.5

def gd(x): 
    m = 20
    s = 1
    left=x*1/(math.sqrt(2*math.pi)*s) 
    right=math.exp(-math.pow(x-m,2)/(2*math.pow(s,2))) 
    return left*right 

pi_half, err = integrate.quad(gd, 20, 40)
result = pi_half
print(result)