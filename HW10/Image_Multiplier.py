import os
import sys
from PIL import Image

def parsing_data(filename):
    image = Image.open(filename, 'r').resize((320,320))
    new_image = Image.new('RGB',(640,640))
    pixel = new_image.load()

    for i in range(320):
        for j in range(320):
            pixel[i, j] = image.getpixel((i, j))
            pixel[i+320, j] = image.getpixel((i, j))
            pixel[i, j+320] = image.getpixel((i, j))
            pixel[i+320, j+320] = image.getpixel((i, j))

    return new_image

def main():
    cnt = 0
    for filename in os.listdir('patterns/'):
        parsing_data('patterns/'+filename).save('patterns/'+filename)
        cnt += 1

if __name__ == "__main__":
    main()
