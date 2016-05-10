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
'''mid
1����Ŭ����Ȼ���������Ϊһ����ֵ
    ���ܣ����ݦ�����
    1��֪��ʵ��ֲ����ʵ�����£��������ֵĸ���
    2�����磬��֪head���ֵĸ���Ϊ�ȣ�����һ��ʵ���У�
        ����Ϊhead�ĸ����ܶ����£�
            P(H|��) = ��
        ����Ϊtail�ĸ������£�
            p(T|��) = 1-��
    3)��1����head��0����tail��k = {0,1}
        ��2)����ʽ������д�����£�
            P(k|��) = (��**k)*(1-��)**(1-k)
    4)N�˲�Ŭ��ʵ���У�z��heads�ĸ���Ϊ��heads���ʳ���tails����
        P(z,N|��) = ��**z * (1-��)**(N-z)
        ���磺5��ʵ����3��heads�ĸ�������:
            ��**3 * (1-��)**2
2��Beta�ֲ�����������Ϊһ�������ܶȺ���
    ���ܣ�����alpha,beta������ȵķֲ�

3��һ��Beta�ֲ���������һ����Ŭ����Ȼ������������Beta������ʽһ��
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
    #mid ��Ŭ��ʵ������б�
    number_of_trials = [0, 2, 10, 20, 50, 500,1000,2000]
    #mid ���������������ʵ������1Ϊͷ��0Ϊβ
    data = stats.bernoulli.rvs(0.5, size=number_of_trials[-1])
    #mid x��̶Ȼ���
    x = np.linspace(0, 1, 100)
    #mid ���������1���ֵĸ��ʵĽ���ֲ��������;�ֵ��
    priorMu = 0.5
    priorSigma = 0.28867511
    #mid �����������;�ֵ����alpha��beta
    priorAlpha = 1.0*int(((1-priorMu)/priorSigma**2-1/priorMu)*priorMu**2)
    priorBeta = 1.0*int(priorAlpha*(1/priorMu-1)) 
    
    print priorAlpha,priorBeta    
    
    #mid �ֱ�Բ�ͬ��ʵ������Ľ�����н�����������������ó�����ķֲ���������
    for i, N in enumerate(number_of_trials):
        #mid �����ǰʵ������µ�heads���ֵĴ���
        heads = data[:N].sum()
        #mid ������ͼ���˴���Ҫʵ������б�Ϊż������
        ax = plt.subplot(len(number_of_trials) / 2, 2, i + 1)
        ax.set_title("%s trials, %s heads" % (N, heads))
        ax.set_xlabel("$P(H)$, Probability of Heads")
        ax.set_ylabel("Density")
        #mid Ϊ��һ�����ȷֲ�����ͼ����y��̶ȷ�Χ�������裬�������
        if i == 0:
            plt.ylim([0.0, 2.0])
        #plt.setp(ax.get_yticklabels(), visible=False)
        #mid ��������������µ�ʵ֤���ݼ���������
        postAlpha,postBeta,postMu,postSigma = getPosteriors(priorAlpha, priorBeta, heads)
        #mid ���ݺ������������������beta�ֲ���x��Χ�ڵ��ܶ�ֵ
        y = stats.beta.pdf(x, postAlpha, postBeta)
        #mid ��ͼ
        label01 = "observe %d tosses, %d heads" % (N, heads)
        label02 = "$\\alpha=%.4f$, $\\beta=%.4f$, $\\mu=%.4f$, $\\sigma=%.4f$" % (postAlpha,postBeta,postMu,postSigma)
        ax.set_title(label01+'\n'+label02)
        ax.plot(x, y, label=label01+label02)
        ax.fill_between(x, 0, y, color="#aaaadd", alpha=0.5)
        #mid ���˴ι��Ƶõ��Ĳ�����Ϊ�´�ʵ����������
        priorAlpha = postAlpha
        priorBeta = postBeta
    plt.tight_layout()
    plt.show()
