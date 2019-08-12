from PIL import Image


# def convert_into_rgb(pixel):
#     rgb = pixel[0] << 16 | pixel[1] << 8 | pixel[2] | pixel[3] << 24
#     if rgb >= 1 << 31:
#         rgb -= 1 << 32
#     return rgb


# def convert_into_binary(pixel):
#     if pixel != -1:
#         return 1
#     else:
#         return 0

def convert_rgb(pixel):
    if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
        return 0
    return 1


class ImageConverter:
    def __init__(self, filename):
        path = "../image/crows/"
        self.image = Image.open(path + filename)
        self.width, self.height = self.image.size
        self.pixels = [[0] * self.width for row in range(self.height)]
        self.initialize_pixels()

    def initialize_pixels(self):
        self.image = self.image.convert('RGBA')
        for row in range(0, self.height):
            for column in range(0, self.width):
                self.pixels[row][column] = self.image.getpixel((column, row))
                self.pixels[row][column] = convert_rgb(self.pixels[row][column])
          #     self.pixels[row][column] = convert_into_binary(self.pixels[row][column])
