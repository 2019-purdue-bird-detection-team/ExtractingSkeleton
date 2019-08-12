#%%
from frame import Frame
from image import ImageConverter
from chain import Chain, Coordinate, Point


def find_neighbor_border(frame, point, chain):
    if is_dead_end(frame, point):
        chain.isReturning = True

    # check east
    if is_neighbor(frame, point.column_plus(), chain):
        chain.add_chain(0, point.column_plus())
        return chain
    # check southeast
    if is_neighbor(frame, point.all_plus(), chain):
        chain.add_chain(1, point.all_plus())
        return chain
    # check south
    if is_neighbor(frame, point.row_plus(), chain):
        chain.add_chain(2, point.row_plus())
        return chain
    # check southwest
    if is_neighbor(frame, point.row_plus_column_minus(), chain):
        chain.add_chain(3, point.row_plus_column_minus())
        return chain
    # check west
    if is_neighbor(frame, point.column_minus(), chain):
        chain.add_chain(4, point.column_minus())
        return chain
    # check northwest
    if is_neighbor(frame, point.all_minus(), chain):
        chain.add_chain(5, point.all_minus())
        return chain
    # check north
    if is_neighbor(frame, point.row_minus(), chain):
        chain.add_chain(6, point.row_minus())
        return chain
    # check northeast
    if is_neighbor(frame, point.row_minus_column_plus(), chain):
        chain.add_chain(7, point.row_minus_column_plus())
        return chain

    # no neighbor
    chain.set_point(point)
    return chain


def is_dead_end(frame, point):
    for row in range(point.row - 1, point.row + 2):
        for column in range(point.column - 1, point.column + 2):
            if row == point.row and column == point.column:
                continue
            if frame.pixels[row][column] == 0:
                continue
            if frame.visited[row][column] == 0:
                return False
    return True


def hang_chain(frame, chain):
    index = chain.point

    chain = find_neighbor_border(frame, chain.point, chain)
    frame.visited[index.row][index.column] = 1

    # end if point is came back to starting point, finish
    if chain.point.is_equal(frame.starting_point):
        return chain

    if frame.visited[chain.point.row][chain.point.column] == 0:
        return hang_chain(frame, chain)
    elif chain.isReturning:
        chain.isReturning = False
        return hang_chain(frame, chain)
    else:
        return chain


def is_neighbor(frame, point, chain):
    if is_border(frame, point) is False:
        return False
    if is_unvisited(frame.visited, point) is True or chain.isReturning is True:
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


def extract_chains():
    image = ImageConverter("crow1.png")  # input("Filename: ")
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


def get_coordinates():
    return calculate_coordinates(extract_chains(), Coordinate()).coordinates


def rotate_coordinates(coordinates, index):
    new_coordinates = []
    for i in range(index, len(coordinates)):
        new_coordinates.append(coordinates[i])
    for i in range(index):
        new_coordinates.append(coordinates[i])
    return new_coordinates


def main():
    coordinats = calculate_coordinates(extract_chains(), Coordinate()).coordinates


if __name__ == '__main__':
    main()


#%%
