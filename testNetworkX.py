
a = [1,-2,3,-4]

b = map(abs,a)
print(list(b))

def sq(x):
    return x**2

c = map(sq,a)
print(list(c))

# With an anonymous function
d = map(lambda x:x**2,a)
print(list(d))

e = map(lambda x: chr(ord(x)+1), ['a','h','f'])
print(list(e))

def fahrenheit(T):
    return ((float(9)/5)*T + 32)

def celsius(T):
    return (float(5)/9)*(T-32)

temperatures = [36.5, 37, 37.5, 38, 39]

F = list(map(fahrenheit, temperatures))
print(F)

C = list(map(celsius, F))
print(C)
