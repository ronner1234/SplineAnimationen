from matplotlib import pyplot as plt
import numpy as np
import math
from scipy.special import comb
from datetime import datetime
from matplotlib.animation import PillowWriter
import sys
import imageio

def deCasteljau(x, y, t, ordnung):
    """
    Wertet die de Cateljau Formel p(t) aus.
    :param x: array mit x werten
    :param y: array mit y werten
    :param t: zeit parameter 0 <= t <= 1
    :param ordnung: ordnung der berzier-kurve
    :return: 2-dimensionales array mit punkten der rekursion
    """
    rekusionstiefe = 0
    liste_x,liste_y = [x], [y]

    for i in range(ordnung-rekusionstiefe):
        temp_x,temp_y = [],[]
        for j in range(len(liste_x[i])-1):
            temp_x.append(liste_x[i][j] + (t) * (liste_x[i][j + 1] - liste_x[i][j]))
            temp_y.append(liste_y[i][j] + (t) * (liste_y[i][j + 1] - liste_y[i][j]))
        liste_x.append(temp_x)
        liste_y.append(temp_y)

    return liste_x[1:], liste_y[1:]
def bezierpunkteAusGewichtspunkten(x, y):
    bezier_x = [x[0]]
    bezier_y = [y[0]]

    for i in range(4):
        xn, yn = kubischeBezierAusGewichtspunkten(x[i:i + 4], y[i:i + 4])
        bezier_x.extend(xn)
        bezier_y.extend(yn)
    xlast, ylast = kubischeBezierAusGewichtspunktenEndpunkte(x[4:6], y[4:6])

    bezier_x.extend(xlast)
    bezier_y.extend(ylast)
    bezier_x.append(4)
    bezier_y.append(0.7)
    return bezier_x, bezier_y

def kubischeBezierAusGewichtspunkten(x,y):
    b1x = (1/3) * (2 * x[0] +     x[1])
    b2x = (1/3) * (    x[0] + 2 * x[1])
    b3x = (1/6) * (    x[0] + 4 * x[1] + x[2])

    b1y = (1 / 3) * (2 * y[0] + y[1])
    b2y = (1 / 3) * (y[0] + 2 * y[1])
    b3y = (1 / 6) * (y[0] + 4 * y[1] + y[2])

    return [b1x,b2x,b3x] , [b1y,b2y,b3y]

def kubischeBezierAusGewichtspunktenEndpunkte(x, y):
    b2x = (1 / 3) * (x[0] + 2 * x[1])
    b1x = (1/3) * (2 * x[0] +     x[1])

    b2y = (1 / 3) * (y[0] + 2 * y[1])
    b1y = (1 / 3) * (2 * y[0] + y[1])

    return [b1x, b2x] , [b1y,b2y]

def createMovie(filenames):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('deCasteljauSpline.gif', images, fps=15)

def animatedGifCreator():
    fig, ax = plt.subplots()
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    x = [0, 1, 3.5, 1.5, 5, 4]
    y = [0, 0.8415, 0.9093, 0.0, 0.5, 0.7]

    berzier_x, berzier_y = bezierpunkteAusGewichtspunkten(x,y)

    plt.plot(berzier_x, berzier_y, '-', color="#c9c9c9")

    colors = ['#F5368C', '#E38F2B']

    for i in range(len(x) - 1):
        ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], color="#c9c9c9")

    filenames = []

    for j in range(5):
        frames = 30  # anzahl der bilder in gif
        berzier_ordnung = 3

        prev_berzier_linie_punkte_x, prev_berzier_linie_punkte_y = berzier_x[j * 3], berzier_y[j * 3]

        for i in range(frames + 1):
            liste_x, liste_y = deCasteljau(berzier_x[j * 3:j * 3 + 4], berzier_y[j * 3:j * 3 + 4], ordnung=berzier_ordnung, t=i / frames)
            berzier_linie_punkte_x = liste_x[berzier_ordnung - 1][0]
            berzier_linie_punkte_y = liste_y[berzier_ordnung - 1][0]

            plots = []

            for z in range(berzier_ordnung - 1):
                plots.append(plt.plot(liste_x[z], liste_y[z], '-', zorder=10, color='#1C15E6'))

            plots.append(plt.plot(liste_x[2], liste_y[2], 'o', zorder=10, color='#F5368C'))

            plt.plot([prev_berzier_linie_punkte_x, berzier_linie_punkte_x],
                     [prev_berzier_linie_punkte_y, berzier_linie_punkte_y],
                     '-', zorder=10, color=colors[j%2])

            prev_berzier_linie_punkte_x, prev_berzier_linie_punkte_y = berzier_linie_punkte_x, berzier_linie_punkte_y

            plt.savefig('deCasteljauSplineIMG/' + str(j) + '-' + str(i) + '.png', dpi=300)
            filenames.append('deCasteljauSplineIMG/'  + str(j) + '-' + str(i) + '.png')

            for plot in plots:
                plot[0].remove()

    createMovie(filenames)
    plt.show()

if __name__ == '__main__':
    animatedGifCreator()

