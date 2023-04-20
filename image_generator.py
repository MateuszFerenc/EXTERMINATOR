from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
import random

operands = ['+', '-', '*', '/']


def randommath(num0_min: int = 0, num0_max: int = 100, num1_min: int = 0, num1_max: int = 100) -> tuple[int, str, int, int]:
    assert type(num0_min) is int
    assert type(num0_max) is int
    assert type(num1_min) is int
    assert type(num1_max) is int
    operand = operands[random.randint(0, 3)]
    num0 = random.randint(num0_min, num0_max)
    num1 = 0
    if operand == '/':
        while num1 == 0:
            num1 = random.randint(num1_min, num1_max)
        equation = round(int(num0) / int(num1), 2)
    else:
        num1 = random.randint(num1_min, num1_max)
    equation = 0
    if operand == '+':
        equation = int(num0) + int(num1)
    elif operand == '-':
        equation = int(num0) - int(num1)
    elif operand == '*':
        equation = int(num0) * int(num1)
        
    return num0, operand, num1, equation


def randomcolor(red_min: int = 0, red_max: int = 255, green_min: int = 0, green_max: int = 255, blue_min: int = 0, blue_max: int = 255) -> tuple[int, int, int]:
    red = random.randint(red_min, red_max)
    green = random.randint(green_min, green_max)
    blue = random.randint(blue_min, blue_max)
    return red, green, blue

def captcha_math(ctype: str = "image", width_: int = 320, height_: int = 180, num0_min: int = 0, num0_max: int = 100, num1_min: int = 0, num1_max: int = 100):
    assert type(ctype) is str
    assert ctype in ['image', 'audio']
    assert type(width_) is int
    assert type(height_) is int
    assert type(num0_min) is int
    assert type(num0_max) is int
    assert type(num1_min) is int
    assert type(num1_max) is int
    eq = randommath()
    captcha_text = f"{eq[0]} {eq[1]} {eq[2]}"
    
    if ctype == 'image':
        image = ImageCaptcha(width = width_, height = height_)
        img_data = image.generate_image(captcha_text)
        return img_data
    else:
        #audio = AudioCaptcha()
        #audio_data = audio.generate(captcha_text)
        #return audio
        return None

def captcha_text(text: str, width_: int = 320, height_: int = 180):
    assert type(text) is str
    assert type(width_) is int
    assert type(height_) is int
    image = ImageCaptcha(width = width_, height = height_)
    img_data = image.generate_image(text)
    return img_data


if __name__ == "__main__":
    print("Fatal error! This file should not be run as a standalone.")
    exit(3)
