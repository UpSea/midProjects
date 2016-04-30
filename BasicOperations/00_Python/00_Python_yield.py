def gen(i):
    print('mid:',i)
    yield 'this is yielded.'
    for j in range(i):
        print('i:',i,',j:',j)
        yield j*'*'
    yield 'end'
ia = gen(5)
print('-------------')
for i in ia:
    print ('i:',i)
        
for i in ia:
    print ('i:',i)
