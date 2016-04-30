# -*- coding:gbk -*-
'''
http://www.cnblogs.com/rhcad/archive/2011/12/21/2295507.html
ʾ��8: װ�����������
'''

class locker:
    def __init__(self):
        print("locker.__init__() should be not called.")

    @staticmethod
    def acquire():
        print("locker.acquire() called.�����Ǿ�̬������")

    @staticmethod
    def release():
        print("  locker.release() called.������Ҫ����ʵ����")

def deco(cls):
    '''cls ����ʵ��acquire��release��̬����'''
    def _deco(func):
        def __deco():
            print("before %s called [%s]." % (func.__name__, cls))
            cls.acquire()
            try:
                return func()
            finally:
                cls.release()
        return __deco
    return _deco

@deco(locker)
def func():
    print(" myfunc() called.")

print('--'*20)
func()
print('--'*20)