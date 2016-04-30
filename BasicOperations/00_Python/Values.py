'''
可以发现：python的类变量和C++的静态变量不同，并不是由类的所有对象共享。
类本身拥有自己的类变量（保存在内存），当一个TestClass类的对象被构造时，
	会将当前类变量拷贝一份给这个对象，当前类变量的值是多少，这个对象拷贝得到的类变量的值就是多少；
而且，通过对象来修改类变量，并不会影响其他对象的类变量的值，因为大家都有各自的副本，
更不会影响类本身所拥有的那个类变量的值；只有类自己才能改变类本身拥有的类变量的值。

类变量定义后 ，通过类变量方式引用和通过实例变量方式引用的是两个变量，只是名字相同而已
'''
class TestClass(object):
    val1 = 100
    def __init__(self):
        #self.val1 = 101        #若有此定义，则实例变量不会拷贝类变量
        self.val2 = 200
    def fcn(self,val = 400):
        val3 = 300
        self.val4 = val
        self.val5 = 500
if __name__ == '__main__':
    inst1 = TestClass()
    inst2 = TestClass()
    
    print (TestClass.val1) # 100
    print (inst1.val1)   # 100
    
    inst1.val1 = 1000 
    print (inst1.val1)   # 1000
    print ('2.1:'+str(inst2.val1))
    print (TestClass.val1) # 100
    
    TestClass.val1 =2000
    print (inst1.val1)   # 1000
    print (TestClass.val1) # 2000
    
    print (inst2.val1)   # 2000   
    
    inst3 = TestClass() 
    print (inst3.val1)   # 2000