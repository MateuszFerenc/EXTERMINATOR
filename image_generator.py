import os

from PIL import Image, ImageDraw, ImageFont
import random

operands = ['+', '-', '*']


class ImageGenerator:
    def __init__(self):
        super(ImageGenerator, self).__init__()
        self.xy_size = (320, 180)
        self.font = "arial.ttf"
        self.font_size = 80

    def set_size(self, x, y):
        self.xy_size = (x, y)

    def set_font(self, type_, size):
        self.font = type_
        self.font_size = size

    def generate_random_equation(self):
        bg = randomcolor(red_min=100, red_max=200, green_min=100, green_max=200, blue_min=100, blue_max=200)

        image = Image.new('RGB', self.xy_size, bg)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font, self.font_size)
        equation = randommath()
        equation_text = str("{:d} {} {:d}".format(equation[0], equation[1], equation[2]))
        text_xy = (
            ((self.xy_size[0]) - (self.font_size * len(equation_text) / 2)),
            ((self.xy_size[1] / 2) - (self.font_size / 2)))
        # random position
        draw.text(text_xy, equation_text, font=font, fill=randomcolor(red_max=100, blue_max=100, green_max=100))
        # image = ImageDraw.Draw(draw)

        image.show()
        # return image, equation[3]


def randommath(num0_min=0, num0_max=100, num1_min=0, num1_max=100):
    num0 = random.randint(num0_min, num0_max)
    num1 = random.randint(num1_min, num1_max)
    operand = operands[random.randint(0, 2)]
    equation = 0
    if operand == '+':
        equation = int(num0) + int(num1)
    elif operand == '-':
        equation = int(num0) - int(num1)
    elif operand == '*':
        equation = int(num0) * int(num1)
    return num0, operand, num1, equation


def randomcolor(red_min=0, red_max=255, green_min=0, green_max=255, blue_min=0, blue_max=255):
    red = random.randint(red_min, red_max)
    green = random.randint(green_min, green_max)
    blue = random.randint(blue_min, blue_max)
    return red, green, blue


if __name__ == "__main__":
    print("ERROR! This file cannot be used standalone!")
    os.abort()
