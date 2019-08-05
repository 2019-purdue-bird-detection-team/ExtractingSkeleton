import matplotlib.pyplot as plt
import math
import scipy.signal
import peakutils
import operator as op
from functools import reduce


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def draw_bird(chain_x, chain_y):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.scatter(chain_x, chain_y, color='black', label='bird')

    plt.legend()
    plt.show()


def draw_bird_graph(chain_x, chain_y, maxima):
    maxima_x, maxima_y = zip(*maxima)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.scatter(chain_x, chain_y, color='black', label='bird')
    ax1.scatter(maxima_x, maxima_y, color='green', label='local maxima')

    plt.legend()
    plt.show()


def draw_bird_vector(chain_x, chain_y, maxima):
    maxima_x, maxima_y = zip(*maxima)
    center_x = []
    center_y = []
    center_x.append(maxima_x[0])
    center_y.append(maxima_y[0])

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.scatter(chain_x, chain_y, color='black', label='bird')
    ax1.scatter(maxima_x, maxima_y, color='green', label='local maxima')
    ax1.scatter(center_x, center_y, color='red', label='body center')

    plt.legend()
    plt.show()


def read_file(filename):
    file = open(filename).read().split()
    array = [int(value) for value in file if value.isdigit()]
    return array


def write_file(coor_array):
    file = open("vectors.txt", "w")
    for xp, yp in coor_array:
        file.write("%d %d\n"% (xp, yp)) #맨 처음 좌표는 중심점좌표
    file.close()


def center_point(bird_x, bird_y):
    cent_x = sum(bird_x) // len(bird_x)
    cent_y = sum(bird_y) // len(bird_y)
    return Point2D(x=cent_x, y=cent_y)


def get_distance(bird_x, bird_y, center):
    distance = []
    for x, y in zip(bird_x, bird_y):
        dot = Point2D(x=x, y=y)
        p1 = dot.x - center.x
        p2 = dot.y - center.y
        distance.append(math.sqrt((p1 ** 2) + (p2 ** 2)))

    return distance


def calculate_maxima(bird_x, bird_y):
    distance = get_distance(bird_x, bird_y, center_point(bird_x, bird_y))
    new_distance = smooth_distance(distance)
    return peakutils.indexes(new_distance, thres=0.02 / max(new_distance), min_dist=100)


def smooth_distance(distance):
    return scipy.signal.savgol_filter(distance, 51, 3)


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return int(numer / denom)


def calculate_radians(theta, x_list, y_list, maximas):
    radians = []
    points = [[0]*2 for i in range(ncr(len(maximas), 2))]
    index = 0
    for i in range(0, len(maximas)):
        for j in range(i, len(maximas)):
            if (i == j):
                continue
            point1 = Point2D(x_list[maximas[i]], y_list[maximas[i]]) # 기준점
            point2 = Point2D(x_list[maximas[j]], y_list[maximas[j]]) # 대조점
            if point2.y > point1.y:
                radians.append(math.atan2(point2.y - point1.y, point2.x - point1.x))
                points[index][0] = maximas[j]
                points[index][1] = maximas[i]
            else:
                radians.append(math.atan2(point1.y - point2.y, point1.x - point2.x))
                points[index][0] = maximas[i]
                points[index][1] = maximas[j]
            index += 1

    if theta > 0:
        return zip(radians, points)

    for index in range(0, len(radians)):
        radians[index] -= math.radians(180)
        for i in range(0, len(radians)):
            points[i] = [points[i][1], points[i][0]]

    return zip(radians, points)


def body_slope(theta, bird_x, bird_y, maximas):
    radians, points = zip(*calculate_radians(theta, bird_x, bird_y, maximas))

    difference = abs(theta - radians[0])
    axis = radians[0]
    point = [points[0][0], points[0][1]]

    for index in range(0, len(radians)):
        if difference > abs(theta - radians[index]):
            difference = abs(theta - radians[index])
            axis = radians[index]
            point = [points[index][0], points[index][1]]

    return axis, point


def body_center(point, bird_x, bird_y):
    center = []
    x = bird_x[point[0]] + bird_x[point[1]]
    y = bird_y[point[0]] + bird_y[point[1]]
    center.append(x / 2)
    center.append(y / 2)
    return center


def extract_wings(maxima, point):
    wings = []
    for index in range(len(maxima)):
        if (maxima[index] == point[0]) or (maxima[index] == point[1]):
            continue
        wings.append(maxima[index])
    return wings


def assemble_vector(center, point, wings):
    vector = []
    vector.append(center)
    vector.append(point[0])
    vector.append(point[1])
    for wing in wings:
        vector.append(wing)
    if len(wings) < 2:
        for index in range(2 - len(wings)):
            vector.append(-1)
    return vector


def bird_coordinates(vector, bird_x, bird_y):
    coordinate_x = []
    coordinate_y = []
    coordinate_x.append(vector[0][0])
    coordinate_y.append(vector[0][1])
    for index in range(1, len(vector)):
        coordinate_x.append(bird_x[vector[index]])
        coordinate_y.append(bird_y[vector[index]])
    return zip(coordinate_x, coordinate_y)


def main():
    theta = 2.8;
    bird_x = read_file('../data/chain_x.txt')
    bird_y = read_file('../data/chain_y.txt')

    maxima = calculate_maxima(bird_x, bird_y)
    # draw_bird(bird_x, bird_y)

    radian, point = body_slope(theta, bird_x, bird_y, maxima)
    center = body_center(point, bird_x, bird_y)
    wings = extract_wings(maxima, point)

    vector = assemble_vector(center, point, wings)
    coordinates = bird_coordinates(vector, bird_x, bird_y)

#    write_file(coordinates) # draw 전에 무슨 코드 사용하니까 draw_bird 오류남
    
    # draw_bird_graph(bird_x, bird_y, coordinates)
    draw_bird_vector(bird_x, bird_y, coordinates)


if __name__ == '__main__':
    main()
