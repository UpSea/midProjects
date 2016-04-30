'''
The  sp.pmt() function is used to answer the following question: What is the monthly
cash flow to pay off a mortgage of $250,000 over 30 years with an annual percentage
rate (APR) of 4.5 percent, compounded monthly?
'''
import scipy as sp

'''
贷款:200'000.00
年利率：5%
还款周期：月
贷款年限：3年
每月还款：5'994.18
'''
payment2 = sp.pmt(0.05/12,3*12,200000,fv=0,when='end')
print (payment2)