'''

问题：
    Python的函数定义中有两种特殊的情况，即出现*，**的形式。
    如：def myfun1(username, *keys)或def myfun2(username, **keys)等。

解释：
    * 用来传递任意个无名字参数，这些参数会一个Tuple的形式访问。

        **用来处理传递任意个有名字的参数，这些参数用dict来访问。*

应用：
#########################

# “*” 的应用

#########################
'''


def fun1(*keys):
     print ("keys type=%s" % type(keys))
     print ("keys=%s" % str(keys))
     for i in range(0, len(keys)):
          print ("keys[" + str(i) + "]=%s" % str(keys[i]))

fun1(2,3,4,5)

'''
#########################

# “**” 的应用

#########################
'''



def fun2(**keys):
     print ("keys type=%s" % type(keys))
     print ("keys=%s" % str(keys))
     print ("name=%s" % str(keys['name']))


fun2(name="vp", age=19)


