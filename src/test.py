import os
import sys
import src.vector_extractor as vec
import matplotlib.pyplot as plt


def test_maximas(bird, maximas):
    x1 = [coordinate.x for coordinate in bird]
    y1 = [coordinate.y for coordinate in bird]
    plt.plot(x1, y1, 'b', label='bird')

    x2 = [bird[maxima].x for maxima in maximas]
    y2 = [bird[maxima].y for maxima in maximas]
    color = ['g', 'c', 'm', 'y']
    for index in range(len(x2)):
        plt.scatter(x2[index], y2[index], color=color[index % 4], label=index)

    plt.legend(loc='upper left')
    plt.show()


def test_drawing(bird, vectors):
    x1 = [coordinate.x for coordinate in bird]
    y1 = [coordinate.y for coordinate in bird]

    plt.plot(x1, y1, 'b', label='bird')
    plt.scatter(vectors.center.x, vectors.center.y, color='g', label='center')
    plt.scatter(vectors.head.x, vectors.head.y, color='c', label='head')
    plt.scatter(vectors.tail.x, vectors.tail.y, color='m', label='tail')
    plt.scatter(vectors.wing1.x, vectors.wing1.y, color='y', label='wing1')
    plt.scatter(vectors.wing2.x, vectors.wing2.y, color='k', label='wing2')
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.legend(loc='upper right')
    plt.show()


def test_distances(bird, distances, filtered_distances):
    x = [i for i in range(len(bird))]
    plt.plot(x, distances, 'b', label='distances')
    plt.plot(x, filtered_distances, 'r', label='filtered_distances')
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.legend(loc='upper right')
    plt.show()


def main():
    sys.setrecursionlimit(2000)

    theta = 2.87979
    path = "../image/crows"
    count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])

    for i in range(61, count):
        if i == 2 or i == 7 or i == 13 or i == 14 or i == 20 or i == 26 or i == 27 or i == 37 or i == 40 or i == 42 or i == 47 or i == 52 \
                or i == 53 or i == 54 or i == 55 or i == 57 or i == 61\
                or i == 64 or i == 69 or i == 72 or i == 73 or i == 79 or i == 83 or i == 85 or i == 96 or i == 98 or i == 99\
                or i == 109 or i == 111 or i == 113 or i == 115 or i == 130 or i == 146 or i == 153 or i == 154 or i == 184 or i == 185\
                or i == 195 or i == 212 or i == 216 or i == 218 or i == 220 or i == 233:
            continue
        print("crow%d.png 시도" % (i + 1), end='')
        filename = path + "/crow" + str(i + 1) + ".png"
        vector = vec.get_vectors(filename, theta)
        print(", 완료")


if __name__ == '__main__':
    main()
