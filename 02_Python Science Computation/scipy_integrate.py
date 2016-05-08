import numpy as np
from scipy import integrate

'''mid
圆心在坐标原点，半径为1的圆面积求法
'''
def half_circle(x):
    return (1-x**2)**0.5
def half_sphere(x,y):
    return (1-x**2-y**2)**0.5
N = 1000000
x = np.linspace(-1,1,N)

#mid 1)切割法
dx = x[1] - x[0]
y = half_circle(x)  #mid y是一个np.ndarray数组值，不是函数，这估计就是向量计算了
s = 2*dx*np.sum(y)
print '%.100f' % s

#mid 2)多边形角坐标法求和
s = np.trapz(y,x) * 2
print '%.100f' % s

#mid 3)数值积分法
pi_half, err = integrate.quad(half_circle, -1, 1)
s = pi_half*2
print '%.100f' % s

#mid 4)求半球体积，使用二重积分
'''
对于x轴从-1到1进行进行积分，对于y轴从-half_circle(x)到
half_circle(x)进行积分
'''
v_half,err = integrate.dblquad(half_sphere,-1,1,
                      lambda x:-half_circle(x),
                      lambda x:half_circle(x))
print '%.10f' % v_half
