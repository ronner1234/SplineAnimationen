import matplotlib.pyplot as plt
import numpy as np
import imageio

def deBoor(k: int, x, t, c, p: int):
    """
    k: Index im knoten interval das x beinhaltet.
    x: Wert (position).
    t: Array knoten vektor.
    c: Array mit GPS-Punkten
    p: Grad des B-spline.
    """
    d = [c[j + k - p] for j in range(0, p + 1)]
    temp = []
    for r in range(1, p + 1):
        for j in range(p, r - 1, -1):
            alpha = (x - t[j + k - p]) / (t[j + 1 + k - r] - t[j + k - p])
            d[j] = (1.0 - alpha) * d[j - 1] + alpha * d[j]
            temp.append(d[j])
    return d[p], temp

def createMovie(filenames):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('deBoorSpline.gif', images, fps=24)


def bSplineAnimation():

    x = [55., 57., 40., 40.,30.,33.]
    y = [19., 2., 4., 20., 10, 5]

    degree = 3

    t = np.clip(np.arange(len(x) + degree + 1) - degree, 0, len(x) - degree)
    print(t)

    fig, ax = plt.subplots()
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.xticks(font='Bahnschrift')

    plt.plot(x,y,'-',color="#c9c9c9")
    colors = ['#F5368C', '#E38F2B', '#F5368C', '#E38F2B', '#F5368C', '#E38F2B']
    filenames = []
    outputx = []
    outputy = []

    lastx = x[0]
    lasty = y[0]

    for j in range(degree,len(t)-degree-1):
        c = np.linspace(t[j], t[j+1], 60)
        z = 0

        for i in c:
            tempx,dx = deBoor(j, i, t, x, degree)
            outputx.append(tempx)
            tempy, dy = deBoor(j, i, t, y, degree)
            outputy.append(tempy)
            am, = plt.plot(dx[0:3], dy[0:3], '-', color= '#1C15E6')
            am1, = plt.plot(dx[3:5], dy[3:5], '-', color = '#1C15E6')
            punkt, = plt.plot(tempx, tempy, 'o', color = '#E38F2B')
            plt.plot([lastx, tempx], [lasty, tempy], color=colors[j - degree])
            lastx = tempx
            lasty = tempy

            plt.savefig('deBoorIMG/' + str(j) + '-' + str(z) + '.png', dpi=300)
            filenames.append('deBoorIMG/' + str(j) + '-' + str(z) + '.png')

            am.remove()
            am1.remove()
            punkt.remove()

            z+=1

    createMovie(filenames)

    plt.plot(x,y,'o', color='#1C15E6', zorder=10)
    plt.show()

if __name__ == '__main__':
    bSplineAnimation()