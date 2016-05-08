'''
P(A|B)=P(B|A)*P(A)/P(B) 

P(A):
    ������ʡ�
    ֮���Գ�Ϊ"����"����Ϊ���������κ�B��������ء�
P(A|B):
    ������ʡ�
    ����֪B������A���������ʣ�Ҳ���ڵ���B��ȡֵ��������A�ĺ�����ʡ�
P(B|A):
    ��Ȼ�ȡ�
    ����֪A������B���������ʣ�Ҳ���ڵ���A��ȡֵ��������B�ĺ�����ʡ�
P(B):
    ֤�ݻ��׼��������
    ��B��������ʻ��Ե���ʣ�Ҳ����׼��������normalized constant����
P(B|A)/P(B):
    ��׼��Ȼ�ȡ�


����Щ���Bayes����ɱ���Ϊ��
������� = (��Ȼ�� * �������)/��׼��������Ҳ����˵�����������������ʺ���Ȼ��
�ĳ˻������ȡ�
���⣬����P(B|A)/P(B)Ҳ��ʱ��������׼��Ȼ�ȣ�standardised likelihood����
Bayes����ɱ���Ϊ��
������� = ��׼��Ȼ�� * �������
'''
'''
�˳���0.5�ĸ��������ɲ�Ŭ��ʵ�飬
Ȼ��ʹ��ʵ����������Ҷ˹�ƶ�
��ʵ������㹻��󣬻�õ�theta�ķֲ�����ʮ����խ�ķֲ���0.5����
'''
# beta_binomial.py

import numpy as np
from scipy import stats
from matplotlib import pyplot as plt


if __name__ == "__main__":
    # Create a list of the number of coin tosses ("Bernoulli trials")
    number_of_trials = [0, 2, 10, 20, 50, 500,1000,2000]

    # Conduct 500 coin tosses and output into a list of 0s and 1s
    # where 0 represents a tail and 1 represents a head
    data = stats.bernoulli.rvs(0.5, size=number_of_trials[-1])

    # Discretise the x-axis into 100 separate plotting points
    x = np.linspace(0, 1, 100)

    # Loops over the number_of_trials list to continually add
    # more coin toss data. For each new set of data, we update
    # our (current) prior belief to be a new posterior. This is
    # carried out using what is known as the Beta-Binomial model.
    # For the time being, we won't worry about this too much.
    
    priorMu = 0.5
    priorSigma = 0.28867511

    priorAlpha = 1.0*int(((1-priorMu)/priorSigma**2-1/priorMu)*priorMu**2)
    priorBeta = 1.0*int(priorAlpha*(1/priorMu-1)) 
    print priorAlpha,priorBeta    
    
    for i, N in enumerate(number_of_trials):
        # Accumulate the total number of heads for this
        # particular Bayesian update
        heads = data[:N].sum()
        # Create an axes subplot for each update
        ax = plt.subplot(len(number_of_trials) / 2, 2, i + 1)
        ax.set_title("%s trials, %s heads" % (N, heads))
        # Add labels to both axes and hide labels on y-axis
        ax.set_xlabel("$P(H)$, Probability of Heads")
        ax.set_ylabel("Density")
        if i == 0:
            plt.ylim([0.0, 2.0])
        #plt.setp(ax.get_yticklabels(), visible=False)
        # Create and plot a Beta distribution to represent the
        # posterior belief in fairness of the coin.

        
        postAlpha = heads + priorAlpha
        postBeta = N-heads+priorBeta
        postMu = (postAlpha/(postAlpha+postBeta))                         #mid mu
        postSigma = (((postAlpha*postBeta)/((postAlpha+postBeta)**2*(postAlpha+postBeta+1)))**0.5)   #mid sigma        
        y = stats.beta.pdf(x, postAlpha, postBeta)
        label01 = "observe %d tosses, %d heads" % (N, heads)
        label02 = "$\\alpha=%.4f$, $\\beta=%.4f$, $\\mu=%.4f$, $\\sigma=%.4f$" % (postAlpha,postBeta,postMu,postSigma)
        ax.set_title(label01+'\n'+label02)
        ax.plot(x, y, label=label01+label02)
        
        ax.fill_between(x, 0, y, color="#aaaadd", alpha=0.5)
        
        priorAlpha = postAlpha
        priorBeta = postBeta
    # Expand plot to cover full width/height and show it
    plt.tight_layout()
    plt.show()
