import numpy as np
from findiff import FinDiff

'''x, y = [np.linspace(0, 1, 10)]*2
dx, dy = x[1] - x[0], y[1] - y[0]
X, Y = np.meshgrid(x, y, indexing='ij')
#f = np.sin(X) * np.cos(Y) * np.sin(Z)
def f(X,Y):
    return np.sin(X) * np.cos(Y)
d3_dx2dy = FinDiff((0, dx, 2), (1, dy))
result = d3_dx2dy(f(X,Y))
print(result)'''

dalpha = .05
dbeta = .1
alpha = np.linspace(0,1,int(1/ dalpha))
beta = np.linspace(0,1,int(1/ dbeta))
#def f(alphaIn,betaIn):
#    return alphaIn * 2 + betaIn * .5
A,B = np.meshgrid(alpha,beta, indexing='ij')
f = A *3 + B *3
d3_dx2dy = FinDiff((0, dalpha), (1, dbeta))
#for i in range(int(100 * dalpha)):
#    print(d3_dx2dy(f(alpha,beta)))
#print(d3_dx2dy(f))
print(f)

'''x, y= [np.linspace(0, 10, 100)]*2
dx, dy = x[1] - x[0], y[1] - y[0]
f = x^3+y^2
print(f.shape)'''