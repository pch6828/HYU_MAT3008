import os
import sys
import numpy as np
from PIL import Image

def resizeImage(image_name, save_name):
    image = Image.open(image_name, 'r').convert('L')
    image = image.resize((32, 32))
    image.save(save_name)

def parseTestSet(src, dist):
    i = 0
    for filename in os.listdir('test_sample/'+src):
        resizeImage('test_sample/'+src+filename, 'test_sample/'+dist+str(i)+'.jpg')
        i+=1

def main():
    srcs = ['Bill_Clinton/', 'George_W_Bush/', 'Sylvester_Stallone/']
    dists = ['test0/', 'test1/', 'test2/']
    for i in range(3):
        parseTestSet(srcs[i], dists[i])

if __name__ == "__main__":
    main()
