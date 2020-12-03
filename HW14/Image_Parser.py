import os
import sys
from PIL import Image

def parsing_data(filename):
    image = Image.open(filename, 'r')
    width, height = image.size
    length = min(width, height)
    image = image.crop((0,0, length, length))
    image = image.resize((640, 640))

    return image

def main():
    cnt = 0
    for filename in os.listdir('origin_image/'):
        parsing_data('origin_image/'+filename).save('crop_data/'+str(cnt)+'.jpg')
        cnt += 1

if __name__ == "__main__":
    main()
