import scipy as sp

'''
每期利息率为：0.05
期数：1
每月等额收支：-600
初始投入：0
支付时点：begin
求：终值
'''
fv1 = sp.fv(0.05, 1, -600, 0,when='begin')
print(fv1)

'''
缴纳养老金：
无初始投入
每月初存入固定金额
30*12个月后共有本息和多少
'''
fv2 = sp.fv(0.05/12,30*12,-600,0,when='begin')
print(fv2)