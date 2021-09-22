from matplotlib import pyplot as plt
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

def createMovie(filenames):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('deCasteljau.gif', images, fps=24)

if __name__ == '__main__':

    fig, ax = plt.subplots()
    ax.spines[["top", "right","left", "bottom"]].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    x = [0, 1, 3.5, 1.5, 5]
    y = [0, 0.8415, 0.9093, 0.0, 0.5]

    for i in range(len(x)-1):
        ax.plot([x[i],x[i+1]], [y[i],y[i+1]], color="#c9c9c9")

    frames = 160 #anzahl der bilder in gif
    berzier_ordnung = len(x)-1 #ordnung der berzier-kurve (ordnung = punkte - 1)
    berzier_linie_punkte_x, berzier_linie_punkte_y = [], []
    filenames = []

    for i in range(frames+1):

        liste_x, liste_y = deCasteljau(x, y, ordnung=berzier_ordnung, t=i/frames)
        berzier_linie_punkte_x.append(liste_x[berzier_ordnung-1])
        berzier_linie_punkte_y.append(liste_y[berzier_ordnung-1])

        plots = []

        for j in range(berzier_ordnung-1):
            plots.append(plt.plot(liste_x[j], liste_y[j], '-', zorder=10, linewidth=0.7, color='#1C15E6'))

        plots.append(plt.plot(berzier_linie_punkte_x, berzier_linie_punkte_y, '-', zorder=10, linewidth=0.7, color='#F5368C'))
        plots.append(plt.plot(liste_x[3], liste_y[3], 'o', zorder=10, color='#F5368C'))

        plt.savefig('deCasteljauIMG/' + str(i) + '.png', dpi=300)
        filenames.append('deCasteljauIMG/' + str(i) + '.png')

        for plot in plots:
            plot[0].remove()

    for i in range(len(x)-1):
        ax.plot([x[i],x[i+1]], [y[i],y[i+1]], color="#c9c9c9")

    createMovie(filenames)
    plt.show()

