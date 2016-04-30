import numpy as np
from scipy import exp,sqrt,stats,integrate
from matplotlib import pyplot as plt
import random
import math 

class normalFigure:
    """"""
    #----------------------------------------------------------------------
    def __init__(self,ax,xl=-3,xr=3,yb= -0.1,yt=0.5,mu=0,sigma=1):
        """Constructor"""
        self.ax = ax
        self.xl = xl
        self.xr = xr
        self.yb = yb
        self.yt = yt
        self.mu = mu
        self.sigma = sigma
    #----------------------------------------------------------------------
    def fillZScoreArea(self,z0=-0.5,z1=0.5):
        """"""
        ymin, ymax = plt.ylim()
        xmin, xmax = plt.xlim()
        
        if ymax>self.yt:
            self.yt = ymax
        if xmin<self.xl:
            self.xl = xmin
        
        #mid 4)fill the area between pdf line and x axis
        x2 = np.arange(z0,z1,0.005)
        y3 = stats.norm.pdf(x2,self.mu,self.sigma)
        self.ax.fill_between(x2,y3)

        y = stats.norm.pdf(z1,self.mu,self.sigma)

        USL0 = stats.norm.cdf(z0,self.mu,self.sigma)
        USL1 = stats.norm.cdf(z1,self.mu,self.sigma)
        USL = USL1-USL0

        z = (z0+z1)/2

        y0 = stats.norm.pdf(z0,self.mu,self.sigma)
        y1 = stats.norm.pdf(z1,self.mu,self.sigma)   
        y = stats.norm.pdf(z,self.mu,self.sigma)  
        lengthOfArrow = self.yt * 0.2


        self.ax.annotate('area is '+str(round(USL,4)),
                         xy=(z,y),            #mid address of arrow
                         xytext=(self.xl*0.9,self.yt*0.9),   #mid address of textlable
                         arrowprops=dict(facecolor='red',shrink=0.01))

        self.ax.annotate('z1= '+str(round(z1,4)),
                         xy=(z1,y1),
                         xytext=(self.xl*0.9,self.yt*0.75),
                         arrowprops=dict(facecolor='red',shrink=0.01))         

        self.ax.annotate('z0= '+str(round(z0,4)),
                         xy=(z0,y0),
                         xytext=(self.xl*0.9,self.yt*0.5),
                         arrowprops=dict(facecolor='red',shrink=0.01))   
        return USL
    #----------------------------------------------------------------------
    def drawPDF(self):
        """"""
        ymin, ymax = plt.ylim()
        xmin, xmax = plt.xlim()
        
        if ymax>self.yt:
            self.yt = ymax
        if xmin<self.xl:
            self.xl = xmin
            
        #mid 0)图形输出
        x = np.arange(self.xl,self.xr,0.001)
        y1=stats.norm.pdf(x,self.mu,self.sigma)

        self.ax.plot(x,y1,'r-')

        #mid 1)mu,sigma标记
        #plt.plot(y, 'cx--', y+1, 'mo:', y+2, 'kp-.');  
        self.ax.plot([self.mu,self.mu],[self.yb,self.yt],'cx--')
        self.ax.scatter([self.mu-2*self.sigma,self.mu-self.sigma,self.mu-0,self.mu+self.sigma,self.mu+2*self.sigma],
                        [0,0,0,0,0])
        #mid 2) 刻度设置
        #self.ax.set_ylim(self.yb,self.yt) 
        self.ax.spines['right'].set_color('none') 
        self.ax.spines['top'].set_color('none') 
        self.ax.xaxis.set_ticks_position('bottom') 
        self.ax.spines['bottom'].set_position(('data',0)) 
        self.ax.yaxis.set_ticks_position('left') 
        self.ax.spines['left'].set_position(('data',0))                 

        #mid 3) 公式输出
        label_f1 = "$\mu=%.4f,\ \sigma=%.4f$" % (self.mu,self.sigma)
        self.ax.text(self.xr*0.2,self.yt,
                     label_f1,fontsize=15,
                     verticalalignment="top",
                     horizontalalignment="left") 
        label_f2 = r"$f(x)=\frac{1}{\sqrt{2\pi}\sigma}exp(-\frac{(x-\mu)^2}{2\sigma^2})$"
        self.ax.text(self.xr*0.2,self.yt*0.8,
                     label_f2,fontsize=15,
                     verticalalignment="top",
                     horizontalalignment="left")   
    def normPdf(self,x): 
        left=x*1/(math.sqrt(2*math.pi)*self.sigma) 
        right=math.exp(-math.pow(x-self.mu,2)/(2*math.pow(self.sigma,2))) 
        return left*right 
    def getPartE(self,z0,z1):
        pi_half, err = integrate.quad(self.normPdf, z0, z1)
        return pi_half        
        
if __name__=="__main__":
    #mid 5)
    '''
    以上证指数为标的某个策略，在运行期间共计完成300个投资周期。
    假设:
	这300个投资序列的回报率呈正态分布，期望值为-10%，标准差为300%。
    问题：
        1.回报率在区间[20%,500%]的投资占比？
        2.此投资组合的整体回报期望为-10%，
            回报率在区间[20%,500%]内投资的回报率期望？
    '''
    mu = 1.70
    sigma = 0.1
    z0 = 1.8
    z1 = 1.9
    fig = plt.figure(figsize=(8,4))                 
    ax5 = fig.add_subplot(1,1,1)
    normFigPdf = normalFigure(ax5, xl=-0.1, xr=2.5, yb=-0.1, yt=0.3, mu=mu, sigma=sigma)
    normFigPdf.drawPDF() 

    zscore = normFigPdf.fillZScoreArea(z0=z0,z1=z1)  
    partE = normFigPdf.getPartE(z0, z1)
    
    totalE = partE/zscore
    
    title = "partE=%.4f,totalE=%.4f" % (partE,totalE)
    ax5.set_title(title)

    plt.show()