from src.frame import Frame, Point as P
from src.image import ImageConverter
from src.chain import Chain, Coordinate, Point
import sys


def add_chain(chain, number, point):
    chain.add_chain(number, point)
    # print("%d" % number, end=' ')
    return chain


def find_neighbor_border(frame, point, chain):
    next_chain = -1
    next_point = Point(-1, -1)

    if is_dead_end(frame, point):
        chain.isEnd = True
        chain.isReturning = True

    # check east
    if is_neighbor(frame, point.column_plus(), chain, 0):
        if is_unvisited(frame.visited, point.column_plus()) is True:
            return add_chain(chain, 0, point.column_plus())
        if chain.isReturning:
            next_chain = 0
            next_point = point.column_plus()
    # check southeast
    if is_neighbor(frame, point.all_plus(), chain, 1):
        if is_unvisited(frame.visited, point.all_plus()) is True:
            return add_chain(chain, 1, point.all_plus())
        if chain.isReturning:
            next_chain = 1
            next_point = point.all_plus()
    # check south
    if is_neighbor(frame, point.row_plus(), chain, 2):
        if is_unvisited(frame.visited, point.row_plus()) is True:
            return add_chain(chain, 2, point.row_plus())
        if chain.isReturning:
            next_chain = 2
            next_point = point.row_plus()
    # check southwest
    if is_neighbor(frame, point.row_plus_column_minus(), chain, 3):
        if is_unvisited(frame.visited, point.row_plus_column_minus()) is True:
            return add_chain(chain, 3, point.row_plus_column_minus())
        if chain.isReturning:
            next_chain = 3
            next_point = point.row_plus_column_minus()
    # check west
    if is_neighbor(frame, point.column_minus(), chain, 4):
        if is_unvisited(frame.visited, point.column_minus()) is True:
            return add_chain(chain, 4, point.column_minus())
        if chain.isReturning:
            next_chain = 4
            next_point = point.column_minus()
    # check northwest
    if is_neighbor(frame, point.all_minus(), chain, 5):
        if is_unvisited(frame.visited, point.all_minus()) is True:
            return add_chain(chain, 5, point.all_minus())
        if chain.isReturning:
            next_chain = 5
            next_point = point.all_minus()
    # check north
    if is_neighbor(frame, point.row_minus(), chain, 6):
        if is_unvisited(frame.visited, point.row_minus()) is True:
            return add_chain(chain, 6, point.row_minus())
        if chain.isReturning:
            next_chain = 6
            next_point = point.row_minus()
    # check northeast
    if is_neighbor(frame, point.row_minus_column_plus(), chain, 7):
        if is_unvisited(frame.visited, point.row_minus_column_plus()) is True:
            return add_chain(chain, 7, point.row_minus_column_plus())
        if chain.isReturning:
            next_chain = 7
            next_point = point.row_minus_column_plus()

    if next_chain != -1:
        return add_chain(chain, next_chain, next_point)

    # no neighbor
    chain.set_point(point)
    return chain


def is_dead_end(frame, point):
    count = 0
    for row in range(point.row - 1, point.row + 2):
        for column in range(point.column - 1, point.column + 2):
            if row == point.row and column == point.column:
                continue
            if frame.pixels[row][column] == 0:
                continue
            if frame.visited[row][column] == 0:
                return False
            count += 1
    if count > 1:
        return False
    return True


def hang_chain(frame, chain):
    index = chain.point

    frame.visited[index.row][index.column] = 1
    chain = find_neighbor_border(frame, chain.point, chain)

    # end if point is came back to starting point, finish
    if chain.point.is_equal(frame.starting_point):
        return chain

    if frame.visited[chain.point.row][chain.point.column] == 0:
        chain.isReturning = False
        return hang_chain(frame, chain)
    elif chain.isReturning:
        return hang_chain(frame, chain)
    else:
        return chain


def is_neighbor(frame, point, chain, number):
    if is_border(frame, point) is False:
        return False
    if is_unvisited(frame.visited, point) is True:
        return True
    if chain.isReturning is False:
        return False
    if chain.isEnd is True:
        chain.isEnd = False
        return True

    previous = chain.chains[len(chain.chains) - 1]
    if previous == 0 and number != 4:
        return True
    elif previous == 1 and number != 5:
        return True
    elif previous == 2 and number != 6:
        return True
    elif previous == 3 and number != 7:
        return True
    elif previous == 4 and number != 0:
        return True
    elif previous == 5 and number != 1:
        return True
    elif previous == 6 and number != 2:
        return True
    elif previous == 7 and number != 3:
        return True
    return False


def is_border(frame, point):
    if frame.pixels[point.row][point.column] == 0:
        return False

    if point.row == 0 or point.row == frame.height:
        return True
    if point.column == 0 or point.column == frame.width:
        return True

    if point.column > 0:
        if frame.pixels[point.row][point.column - 1] == 0:
            return True
    if point.column < frame.width:
        if frame.pixels[point.row][point.column + 1] == 0:
            return True
    if point.row > 0:
        if frame.pixels[point.row - 1][point.column] == 0:
            return True
    if point.row < frame.height:
        if frame.pixels[point.row + 1][point.column] == 0:
            return True
    return False


def is_unvisited(visited, point):
    if visited[point.row][point.column] == 0:
        return True
    return False


def extract_chains(filename):
    image = ImageConverter(filename)
    frame = Frame(image)
    chain = find_neighbor_border(frame, frame.starting_point, Chain())
    return hang_chain(frame, chain)


def calculate_coordinates(chain, coordinates):
    x = coordinates.current.x
    y = coordinates.current.y
    coordinates.coordinates = []
    for index in range(len(chain.chains)):
        if chain.chains[index] == 0:
            x += 1
        elif chain.chains[index] == 1:
            x += 1
            y -= 1
        elif chain.chains[index] == 2:
            y -= 1
        elif chain.chains[index] == 3:
            x -= 1
            y -= 1
        elif chain.chains[index] == 4:
            x -= 1
        elif chain.chains[index] == 5:
            x -= 1
            y += 1
        elif chain.chains[index] == 6:
            y += 1
        elif chain.chains[index] == 7:
            x += 1
            y += 1

        if x < 0:
            coordinates.current.add_x(50)
            return calculate_coordinates(chain, coordinates)
        if y < 0:
            coordinates.current.add_y(50)
            return calculate_coordinates(chain, coordinates)

        coordinates.append(Point(x, y))
    return coordinates


def get_coordinates(filename):
    return calculate_coordinates(extract_chains(filename), Coordinate()).coordinates


def rotate_coordinates(coordinates, index):
    new_coordinates = []
    for i in range(index, len(coordinates)):
        new_coordinates.append(coordinates[i])
    for i in range(index):
        new_coordinates.append(coordinates[i])
    return new_coordinates


def main():
    # print(sys.getrecursionlimit())
    sys.setrecursionlimit(2500)
    coordinates = calculate_coordinates(extract_chains("../image/crows/crow27.png"), Coordinate()).coordinates


if __name__ == '__main__':
    main()
