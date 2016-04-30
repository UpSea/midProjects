'''
The  np.npv() function estimates the present values for a given set of future cash
flows. The first input value is the discount rate, and the second input is an array of
future cash flows. This  np.npv() function mimics Excel's  NPV function. Like Excel,
np.npv() is not a true  NPV function. It is actually a  PV function. It estimates the
present value of future cash flows by assuming the first cash flow happens at the
end of the first period.
'''
import scipy as sp
cashflows=[50,40,20,10,50]
npv=sp.npv(0.1,cashflows) #estimate NPV
npvrounded = round(npv,2)

the npv caculated here is not consistent to execel
need to be found why.
print(npvrounded)