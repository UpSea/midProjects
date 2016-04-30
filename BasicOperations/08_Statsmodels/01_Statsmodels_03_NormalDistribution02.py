import math 
import pylab as pl 
import numpy as np 
def gd(x,m,s): 
    left=1/(math.sqrt(2*math.pi)*s) 
    right=math.exp(-math.pow(x-m,2)/(2*math.pow(s,2))) 
    return left*right 
def showfigure(): 
    x=np.arange(-4,5,0.1) 
    y=[] 
    for i in x: 
        y.append(gd(i,0,1)) 
    pl.plot(x,y)   
    pl.xlim(-4.0,5.0) 
    pl.ylim(-0.2,0.5) 
# 
    ax = pl.gca() 
    ax.spines['right'].set_color('none') 
    ax.spines['top'].set_color('none') 
    ax.xaxis.set_ticks_position('bottom') 
    ax.spines['bottom'].set_position(('data',0)) 
    ax.yaxis.set_ticks_position('left') 
    ax.spines['left'].set_position(('data',0)) 
    #add param 
    label_f1 = "$\mu=0,\ \sigma=1$"
    pl.text(2.5,0.3,label_f1,fontsize=15,verticalalignment="top", 
            horizontalalignment="left") 
    label_f2 = r"$f(x)=\frac{1}{\sqrt{2\pi}\sigma}exp(-\frac{(x-\mu)^2}{2\sigma^2})$"
    pl.text(1.5,0.4,label_f2,fontsize=15,verticalalignment="top"
            ,horizontalalignment="left") 
    pl.show() 
showfigure()