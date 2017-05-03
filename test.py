#!/user/bin/env python
#-*- coding: utf-8 -*-
#这个是注释
code = 1
if code > 20:
    print ">20"
else:
    print "lalalavea"

name = "jing %s age: %d" % ('tianyou', 23)
print name

myList = ['jing', 'tinayou', 'lalala']
print len(myList)
print myList[-1]
print myList[2]
myList.append('jiaiyou')
myList.insert(1, 'hahah')

print myList
print myList.pop(1)

print [1, '123']
#raw_input('input')

def test():
    pass


a = 10
if a > 10:
    pass
else:
    print "123"

arr = range(100)
print arr[:20]
print arr[-1:]
print arr[1:3]


print [m + n for n in  'ABC' for m in 'bcd'] 

d = {'a' : 'A', 'b' : 'B'}
for k, v in d.iteritems():
    print k + "=>" + v

print [s.lower() for s in 'abc']


print "======"
print map(abs, [1, -1, -4])

def add(x, y):
    return x + y

print reduce(add, [1,2,3,4])

print "============"


name = ['abna', 'Hello', 'ANDME']

def format(s):
    return s.capitalize()
print map(format, name)


def prod(x, y):
    return x * y

print reduce(prod, [1,2,3,4,4,5,6,7])


def isInt(a):
    return a.isdigit()

print filter(isInt, ['asd','23'])


@log
def func():
    print '2017-5-1'

def log(func):
    def wrapper(*args, **kw):
        print "call %s()" % func.__name__
        return func(*args, **kw)
    return wrapper

def log(func):
    def wrapper(*args, **kw):
        print "call %s" % func.__name__
        return func(*args, **kw)
    return wrapper

def log(execute):
    def decorate(func):
        def wrapper(*args, **kw):
            print "%s %s():" % ($execute, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorate


#修饰器
def now():
    print "2017-5-1"

def log(text = ''):
    def decorate(text):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print "%s %s():" % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorate
       
