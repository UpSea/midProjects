import numpy as np
from scipy import integrate

'''mid
Բ��������ԭ�㣬�뾶Ϊ1��Բ�����
'''
def half_circle(x):
    return (1-x**2)**0.5
def half_sphere(x,y):
    return (1-x**2-y**2)**0.5
N = 1000000
x = np.linspace(-1,1,N)

#mid 1)�и
dx = x[1] - x[0]
y = half_circle(x)  #mid y��һ��np.ndarray����ֵ�����Ǻ���������ƾ�������������
s = 2*dx*np.sum(y)
print '%.100f' % s

#mid 2)����ν����귨���
s = np.trapz(y,x) * 2
print '%.100f' % s

#mid 3)��ֵ���ַ�
pi_half, err = integrate.quad(half_circle, -1, 1)
s = pi_half*2
print '%.100f' % s

#mid 4)����������ʹ�ö��ػ���
'''
����x���-1��1���н��л��֣�����y���-half_circle(x)��
half_circle(x)���л���
'''
v_half,err = integrate.dblquad(half_sphere,-1,1,
                      lambda x:-half_circle(x),
                      lambda x:half_circle(x))
print '%.10f' % v_half
