import os
import sys
import numpy as np
from PIL import Image

def pseudoinverse(A):
    return np.linalg.inv((A.T@A))@A.T

def saveResultImage(byte_array, image_name):
    image = Image.new('L', (32, 32))
    image.putdata(byte_array)
    image.save(image_name)

def process_test(testset, eigenfaces):
    x = None
    for i in range(5):
        filename = testset+str(i)+'.jpg'
        image = np.asarray(Image.open(filename, 'r').convert('L')).reshape((1024,))

        x = pseudoinverse(eigenfaces)@image
        saveResultImage(eigenfaces@x, testset+'result'+str(i)+'.jpg')
        print(x)
        

def main():
    print('Construct Eigenface Matrix...')
    eigenfaces = np.empty((30, 1024), dtype=int)
    idx = 0
    for filename in os.listdir('eigenfaces/'):
        if idx == 30:
            break
        vector = np.asarray(Image.open('eigenfaces/'+str(idx)+'.jpg','r')).reshape(1024,)
        eigenfaces[idx] = vector;
        idx += 1
    eigenfaces = eigenfaces.T
    print('Construct Complete')
    print('Test Processing...')
    TC = ['test_sample/test0/', 'test_sample/test1/', 'test_sample/test2/']
    idx = 0
    for testset in TC:
        print('Test #'+str(idx))
        process_test(testset, eigenfaces)
        print('')
        idx+=1
    print('Test Complete')
    
if __name__ == "__main__":
    main()
