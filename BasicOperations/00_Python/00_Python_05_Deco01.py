'''
mid 
此例展示带参数的装饰器如何装饰带参数的函数
此时，装饰器的参数，被装饰的函数，被装饰函数的参数都有确定的传递位置

'''
def d(argDec):                  #1) 装饰器的参数          
    def _d(funcDecored):        #2) 被装饰函数
        def __d(*arg, **karg):  #3) 被装饰函数的参数
            print (argDec)
            print("do sth before decored func..")
            r= funcDecored(*arg, **karg) 
            print("do sth after decored func..")
            return r 
        return __d
    return _d
   
@d("first")
def func01(): 
    print("call func01")
@d("second")
def func02(a, b=2):
    print("call f2")
    print (a+b)
func01()
print ("-"*20)
func02(1)
print ("-"*20)
func02(a=1,b=4)