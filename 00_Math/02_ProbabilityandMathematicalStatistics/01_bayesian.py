'''
P(A|B)=P(B|A)*P(A)/P(B) 

P(A):
    先验概率。
    之所以称为"先验"是因为它不考虑任何B方面的因素。
P(A|B):
    后验概率。
    是已知B发生后A的条件概率，也由于得自B的取值而被称作A的后验概率。
P(B|A):
    似然度。
    是已知A发生后B的条件概率，也由于得自A的取值而被称作B的后验概率。
P(B):
    证据或标准化常量。
    是B的先验概率或边缘概率，也作标准化常量（normalized constant）。
P(B|A)/P(B):
    标准似然度。


按这些术语，Bayes法则可表述为：
后验概率 = (似然度 * 先验概率)/标准化常量　也就是说，后验概率与先验概率和似然度
的乘积成正比。
另外，比例P(B|A)/P(B)也有时被称作标准似然度（standardised likelihood），
Bayes法则可表述为：
后验概率 = 标准似然度 * 先验概率
'''
'''
此程序按0.5的概率做若干伯努立实验，
然后使用实验数据做贝叶斯推断
当实验次数足够多后，会得到theta的分布函数十分狭窄的分布在0.5左右
'''
# beta_binomial.py
'''mid
1）伯努利似然函数，结果为一个数值
    功能：依据θ求结果
    1）知道实验分布概率的情况下，求结果出现的概率
    2）例如，已知head出现的概率为θ，则在一次实验中，
        其结果为head的概率密度如下：
            P(H|θ) = θ
        其结果为tail的概率如下：
            p(T|θ) = 1-θ
    3)以1代表head，0代表tail，k = {0,1}
        则2)中两式可联合写作如下：
            P(k|θ) = (θ**k)*(1-θ)**(1-k)
    4)N此伯努利实验中，z次heads的概率为，heads概率乘以tails概率
        P(z,N|θ) = θ**z * (1-θ)**(N-z)
        例如：5次实验中3次heads的概率如下:
            θ**3 * (1-θ)**2
2）Beta分布函数，其结果为一个概率密度函数
    功能：依据alpha,beta参数求θ的分布

3）一个Beta分布函数乘以一个伯努利似然函数，其结果与Beta函数形式一致
'''

import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
def getPosteriors(priorAlpha,priorBeta,heads):
    postAlpha = heads + priorAlpha
    postBeta = N-heads+priorBeta
    postMu = (postAlpha/(postAlpha+postBeta))                                                   #mid mu
    postSigma = (((postAlpha*postBeta)/((postAlpha+postBeta)**2*(postAlpha+postBeta+1)))**0.5)  #mid sigma        
    return postAlpha,postBeta,postMu,postSigma

if __name__ == "__main__":
    #mid 伯努利实验次数列表
    number_of_trials = [0, 2, 10, 20, 50, 500,1000,2000]
    #mid 按最大次数生成随机实验结果，1为头，0为尾
    data = stats.bernoulli.rvs(0.5, size=number_of_trials[-1])
    #mid x轴刻度划分
    x = np.linspace(0, 1, 100)
    #mid 设置先验的1出现的概率的结果分布的期望和均值，
    priorMu = 0.5
    priorSigma = 0.28867511
    #mid 自先验期望和均值计算alpha和beta
    priorAlpha = 1.0*int(((1-priorMu)/priorSigma**2-1/priorMu)*priorMu**2)
    priorBeta = 1.0*int(priorAlpha*(1/priorMu-1)) 
    
    print priorAlpha,priorBeta    
    
    #mid 分别对不同的实验次数的结果进行结合先验条件的评估得出后验的分布参数估计
    for i, N in enumerate(number_of_trials):
        #mid 求出当前实验次数下的heads出现的次数
        heads = data[:N].sum()
        #mid 创建子图，此处需要实验次数列表为偶数长度
        ax = plt.subplot(len(number_of_trials) / 2, 2, i + 1)
        ax.set_title("%s trials, %s heads" % (N, heads))
        ax.set_xlabel("$P(H)$, Probability of Heads")
        ax.set_ylabel("Density")
        #mid 为第一个均匀分布的子图设置y轴刻度范围，若不设，则会填满
        if i == 0:
            plt.ylim([0.0, 2.0])
        #plt.setp(ax.get_yticklabels(), visible=False)
        #mid 根据先验参数和新的实证数据计算后验参数
        postAlpha,postBeta,postMu,postSigma = getPosteriors(priorAlpha, priorBeta, heads)
        #mid 根据后验参数计算后验参数下beta分布在x范围内的密度值
        y = stats.beta.pdf(x, postAlpha, postBeta)
        #mid 绘图
        label01 = "observe %d tosses, %d heads" % (N, heads)
        label02 = "$\\alpha=%.4f$, $\\beta=%.4f$, $\\mu=%.4f$, $\\sigma=%.4f$" % (postAlpha,postBeta,postMu,postSigma)
        ax.set_title(label01+'\n'+label02)
        ax.plot(x, y, label=label01+label02)
        ax.fill_between(x, 0, y, color="#aaaadd", alpha=0.5)
        #mid 将此次估计得到的参数作为下次实验的先验参数
        priorAlpha = postAlpha
        priorBeta = postBeta
    plt.tight_layout()
    plt.show()
