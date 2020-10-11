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
        resizeImage('test_sample/'+src+filename,
                    'test_sample/'+dist+str(i)+'.jpg')
        i+=1

def main():
    srcs = ['Bill_Clinton/',
            'George_W_Bush/',
            'Sylvester_Stallone/',
            'Yoriko_Kawaguchi/',
            'Vladimir_Putin/',
            'Tom_Hanks/',
            'Roh_Moo_hyun/',
            'Michael_Jackson/',
            'Leonardo_Dicaprio/',
            'Britney_Spears/']
    dists = ['test0/',
             'test1/',
             'test2/',
             'test3/',
             'test4/',
             'test5/',
             'test6/',
             'test7/',
             'test8/',
             'test9/']
    for i in range(10):
        parseTestSet(srcs[i], dists[i])

if __name__ == "__main__":
    main()
