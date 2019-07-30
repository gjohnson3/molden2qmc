#!/usr/bin/env python3

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from numpy.linalg import norm, det
import numpy as np

def plot_implicit(fn, bbox=(-4, 4)):
    ''' create a plot of an implicit function
    fn  ...implicit function (plot where fn==0)
    bbox ..the x,y,and z limits of plotted interval'''
    xmin, xmax, ymin, ymax, zmin, zmax = bbox*3
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    A = np.linspace(xmin, xmax, 100) # resolution of the contour
    B = np.linspace(xmin, xmax, 15) # number of slices
    A1, A2 = np.meshgrid(A, A) # grid on which the contour is plotted

    for z in B: # plot contours in the XY plane
        X, Y = A1, A2
        Z = fn(X, Y, z)
        cset = ax.contour(X, Y, Z+z, [z], zdir='z')
        # [z] defines the only level to plot for this contour for this value of z

    for y in B: # plot contours in the XZ plane
        X, Z = A1, A2
        Y = fn(X, y, Z)
        cset = ax.contour(X, Y+y, Z, [y], zdir='y')

    for x in B: # plot contours in the YZ plane
        Y, Z = A1, A2
        X = fn(x, Y, Z)
        cset = ax.contour(X+x, Y, Z, [x], zdir='x')

    # must set plot limits because the contour will likely extend
    # way beyond the displayed level.  Otherwise matplotlib extends the plot limits
    # to encompass all values in the contour.
    ax.set_xlim3d(xmin, xmax)
    ax.set_ylim3d(ymin, ymax)
    ax.set_zlim3d(zmin, zmax)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    plt.show()

# http://www.theochem.ru.nl/~pwormer/Knowino/knowino.org/wiki/Slater_orbital.html
def slater_1s(r):
    Z = 3
    return np.sqrt(Z**3/np.pi) * np.exp(-Z*norm(r))

def slater_2s(r):
    Z = 3
    return np.sqrt(Z**5/(3*np.pi)) * norm(r) * np.exp(-Z*norm(r))

def slater_2px(r):
    Z = 2
    return np.sqrt(Z**5/np.pi) * r[0] * np.exp(-Z*norm(r))

def slater_2py(r):
    Z = 2
    return np.sqrt(Z**5/np.pi) * r[1] * np.exp(-Z*norm(r))

def slater_2pz(r):
    Z = 2
    return np.sqrt(Z**5/np.pi) * r[2] * np.exp(-Z*norm(r))

def Be_1s2s(r1, r2):
    return slater_1s(r1) * slater_2s(r2) - slater_1s(r2) * slater_2s(r1)

def Be_1s2px(r1, r2):
    return slater_1s(r1) * slater_2px(r2) - slater_1s(r2) * slater_2px(r1)

def Be_1s2py(r1, r2):
    return slater_1s(r1) * slater_2py(r2) - slater_1s(r2) * slater_2py(r1)

def Be_1s2pz(r1, r2):
    return slater_1s(r1) * slater_2pz(r2) - slater_1s(r2) * slater_2pz(r1)

def Be(r12_minus, r34_minus, r12_plus):
    r34_plus = 5.0
    B = np.pi/4.0
    r1n = (r12_plus + r12_minus)/2.0
    r2n = (r12_plus - r12_minus)/2.0
    r1 = r1n, 0, 0
    r2 = r2n*np.cos(B), r2n*np.sin(B), 0
    r3n = (r34_plus + r34_minus)/2,0
    r4n = (r34_plus - r34_minus)/2.0
    r3 = r3n, 0, 0
    r4 = r4n*np.cos(B), r4n*np.sin(B), 0
    return Be_1s2s(r1, r2) * Be_1s2s(r3, r4)

def Be_4det(r12_minus, r34_minus, r12_plus):
    r34_plus = 6.0
    vec_1 = vec_3 = [1, 0, 0]
    B = np.pi/4.0
    vec_2 = vec_4 = [np.cos(B), np.sin(B), 0]
    C = -0.15
    r1n = (r12_plus + r12_minus)/2.0
    r2n = (r12_plus - r12_minus)/2.0
    r1 = r1n * vec_1[0], 0, 0
    r2 = r2n * vec_2[0], r2n * vec_2[1], 0
    r3n = (r34_plus + r34_minus)/2.0
    r4n = (r34_plus - r34_minus)/2.0
    r3 = r3n * vec_3[0], 0, 0
    r4 = r4n * vec_4[0], r4n * vec_4[1], 0
    return Be_1s2s(r1, r2) * Be_1s2s(r3, r4) + \
           C * Be_1s2pz(r1, r2) * Be_1s2pz(r3, r4) + \
           C * Be_1s2py(r1, r2) * Be_1s2py(r3, r4) + \
           C * Be_1s2px(r1, r2) * Be_1s2px(r3, r4)

#plot_implicit(Be)
plot_implicit(Be_4det)
