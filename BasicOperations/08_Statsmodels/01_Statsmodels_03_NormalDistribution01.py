import numpy as np
from scipy import exp,sqrt,stats
from matplotlib import pyplot as plt
import random
'''
标准正态分布：
	1.均值 mu=0
	2.标准差 sigma=1
	3.为实数域上连续函数
	4.x轴刻度单位为sigma(一个标准差)
	5.y轴刻度表示某个标准差的观测值的概率密度
	6.某个x<=a的定积分值为累积分布概率值
'''
''' 
有投资回报序列X(同样可以研究最大可能回报，最大可能损失)
1.绘制hist，观测分布
	plt.hist(X, bins=25, normed=True, alpha=0.6, color='g')
2.大致符合norm分布，拟合之
	mu, sigma = norm.fit(X)
3.绘制mu,sigma决定的norm分布
	xmin, xmax = plt.xlim()
	x = np.linspace(xmin, xmax, 100)
	p = norm.pdf(x, mu, sigma)
	plt.plot(x, p, 'k', linewidth=2)
4.求某个回报率区间的投资次数理论占比(按norm分布函数求)
	x1=0.5
	x2=0.8
	z = norm.cdf(x2,mu,sigma)-morm.cdf(x1,mu,sigma)
5.求某个回报率区间的投资的总回报率(按norm分布函数求)
        1.)
            0<x1<x2
            z = norm.cdf(x2,mu,sigma)-morm.cdf(x1,mu,sigma)            
	2.)
            x1<0<x2
            z = norm.cdf(x2,mu,sigma)-morm.cdf(0,mu,sigma)
	3.)
            x1<x2<0
            z = (norm.cdf(x2,mu,sigma)-morm.cdf(x1,mu,sigma))
	z-norm.cdf(0,mu,sigma)
        
概率密度函数pdf的积分为累积分布函数cdf
cdf的极值为1

pdf函数的x轴单位为标准差sigma
pdf函数的y轴表示概率
标准正态分布表示mu=0，sigma=1的正态分布函数。

非标准正态函数都可以转化为标准正态函数

标准正态函数意义
	方便计算z-score
	1.编制标准正态分布的累积密度表
	2.获得某个非标准正态的正态分布函数的变量值
	3.将此变量转化为z值
	4.查z值在z-score表中的密度值

在有程序帮助的情况下，计算非标准正态的正态分布的累积密度值已不需如此周折，直接计算即可        
'''
########################################################################
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
                         xytext=(self.xl,self.yt),   #mid address of textlable
                         arrowprops=dict(facecolor='red',shrink=0.01))
        
        self.ax.annotate('z1= '+str(round(z1,4)),
                         xy=(z1,y1),
                         xytext=(self.xl,self.yt*0.75),
                         arrowprops=dict(facecolor='red',shrink=0.01))         
        
        self.ax.annotate('z0= '+str(round(z0,4)),
                         xy=(z0,y0),
                         xytext=(self.xl,self.yt*0.5),
                         arrowprops=dict(facecolor='red',shrink=0.01))   
        return USL
    #----------------------------------------------------------------------
    def drawPDF(self):
        """"""
        #mid 0)图形输出
        x = np.arange(self.xl,self.xr,0.1)
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
        self.ax.text(self.xr*0.5,self.yt,
                     label_f1,fontsize=15,
                     verticalalignment="top",
                     horizontalalignment="left") 
        label_f2 = r"$f(x)=\frac{1}{\sqrt{2\pi}\sigma}exp(-\frac{(x-\mu)^2}{2\sigma^2})$"
        self.ax.text(self.xr*0.5,self.yt*0.8,
                     label_f2,fontsize=15,
                     verticalalignment="top",
                     horizontalalignment="left")      
    #----------------------------------------------------------------------
    def drawNormalCDF(self):
        #mid 3)cumulative distribution function
        self.ax.set_ylim(self.yb,self.yt)      
        x = np.arange(self.xl,self.xr,0.1)    
        y2 = stats.norm.cdf(x,self.mu,self.sigma)
        self.ax.plot(x,y2)
        
        self.ax.spines['right'].set_color('none') 
        self.ax.spines['top'].set_color('none') 
        self.ax.xaxis.set_ticks_position('bottom') 
        self.ax.spines['bottom'].set_position(('data',0)) 
        self.ax.yaxis.set_ticks_position('left') 
        self.ax.spines['left'].set_position(('data',0))          
if __name__=="__main__":
    #mid 0)for sampling values
    return0 = 0.2
    return1 = 0.8
    muS = -0.2
    sigmaS = 0.6

    z0 = (return0-muS)/sigmaS
    z1 = (return1-muS)/sigmaS    

    fig = plt.figure(figsize=(8,4))

    ax1 = fig.add_subplot(3,2,1)
    ax1.set_title('Standard normal distribution')
    normFigPdf = normalFigure(ax1, xl=-5, xr=5, yb=-0.1, yt=0.5, mu=0, sigma=1)
    normFigPdf.drawPDF() 
    zscore = normFigPdf.fillZScoreArea(z0=z0,z1=z1)

    ax2 = fig.add_subplot(3,2,2) 
    normFigPdf = normalFigure(ax2, xl=-5, xr=5, yb=-0.1, yt=0.5, mu=0.5, sigma=1)
    normFigPdf.drawPDF() 
    zscore = normFigPdf.fillZScoreArea(z0=z0,z1=z1)


    ax3 = fig.add_subplot(3,2,3)
    normFigPdf = normalFigure(ax3, xl=-5, xr=5, yb=-0.1, yt=0.5, mu=0.0, sigma=1.5)
    normFigPdf.drawPDF() 
    zscore = normFigPdf.fillZScoreArea(z0=z0,z1=z1)

    ax4 = fig.add_subplot(3,2,4)
    normFigPdf = normalFigure(ax4, xl=-20, xr=20, yb=-0.1, yt=0.3, mu=-0.05, sigma=4)
    normFigPdf.drawPDF() 
    zscore = normFigPdf.fillZScoreArea(z0=z0,z1=z1)  

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
    mu = 70
    sigma = 10
    z0 = 75
    z1 = 80
    ax5 = fig.add_subplot(3,2,5)
    normFigPdf = normalFigure(ax5, xl=-10, xr=10, yb=-0.1, yt=0.3, mu=mu, sigma=sigma)
    normFigPdf.drawPDF() 
    
    zscore = normFigPdf.fillZScoreArea(z0=z0,z1=z1)  
    zu = zscore*sigma+mu
    title = "mu=%.4f,sigma=%.4f,zscore=%.4f,zu=%.4f" % (mu,sigma,zscore,zu)
    ax5.set_title(title)
    
    ax6 = fig.add_subplot(3,2,6)
    normFigPdf = normalFigure(ax6, xl=-10, xr=10, yb=-0.1, yt=1, mu=3, sigma=3)      
    normFigPdf.drawNormalCDF()
    plt.show()