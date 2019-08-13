class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Point:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def row_plus(self):
        return Point(self.row + 1, self.column)

    def column_plus(self):
        return Point(self.row, self.column + 1)

    def all_plus(self):
        return Point(self.row + 1, self.column + 1)

    def row_minus(self):
        return Point(self.row - 1, self.column)

    def column_minus(self):
        return Point(self.row, self.column - 1)

    def all_minus(self):
        return Point(self.row - 1, self.column - 1)

    def row_minus_column_plus(self):
        return Point(self.row - 1, self.column + 1)

    def row_plus_column_minus(self):
        return Point(self.row + 1, self.column - 1)

    def add(self, number):
        if number == 0:
            return Point(self.row, self.column + 1)
        if number == 1:
            return Point(self.row + 1, self.column + 1)
        if number == 2:
            return Point(self.row + 1, self.column)
        if number == 3:
            return Point(self.row + 1, self.column - 1)
        if number == 4:
            return Point(self.row, self.column - 1)
        if number == 5:
            return Point(self.row - 1, self.column - 1)
        if number == 6:
            return Point(self.row - 1, self.column)
        if number == 7:
            return Point(self.row - 1, self.column + 1)

    def is_equal(self, point):
        if self.row == point.row and self.column == point.column:
            return True
        return False


class Frame:
    def __init__(self, image):
        self.width = image.width
        self.height = image.height
        self.pixels = image.pixels
        self.visited = [[0] * self.width for row in range(self.height)]
        self.starting_point = self.find_starting_point()
        self.end_point = self.find_end_point()
        self.shape_size = Size(self.calculate_height(), self.calculate_width())
        self.initialize_starting_point()

    def find_starting_point(self):
        for row in range(self.height):
            for column in range(self.width):
                if self.pixels[row][column] == 1:
                    return Point(row, column)

    def find_end_point(self):
        for row in range(self.height - 1, 0, -1):
            for column in range(self.width - 1, 0, -1):
                if self.pixels[row][column] == 1:
                    return Point(row, column)

    def initialize_starting_point(self):
        while True:
            new_starting_point = self.next_starting_point()
            if new_starting_point.row == -1 and new_starting_point.column == -1:
                return
            self.pixels[self.starting_point.row][self.starting_point.column] = 0
            self.starting_point = new_starting_point

    def calculate_height(self):
        self.end_point.row - self.starting_point.row + 1

    def next_starting_point(self):
        count = 0
        new_starting_point = Point(-1, -1)
        for row in range(self.starting_point.row - 1, self.starting_point.row + 2):
            for column in range(self.starting_point.column - 1, self.starting_point.column + 2):
                if row == self.starting_point.row and column == self.starting_point.column:
                    continue
                if self.pixels[row][column] == 0:
                    continue
                count += 1
                new_starting_point = Point(row, column)
        if count == 1:
            return new_starting_point
        return Point(-1, -1)

    def calculate_width(self):
        end = start = 0
        for column in range(self.width):
            for row in range(self.height):
                if self.pixels[row][column] == 1:
                    end = column
        for column in range(self.width -1, 0, -1):
            for row in range(self.height - 1, 0, -1):
                if self.pixels[row][column] == 1:
                    start = column
        return end - start + 1
