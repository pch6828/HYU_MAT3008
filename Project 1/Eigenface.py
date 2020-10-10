import os
import sys
import numpy as np
from PIL import Image

def getByteArray(filename):
    byte_array = []
    file = open(filename, "rb")
    data = None
    while True:
        data = file.read(1)
        if data == b"":
            break
        try:
            byte_array.append(ord(data))
        except TypeError:
            pass

    return byte_array

def resizeByte(byte_array):
    image = Image.new('L', (128, 128))
    image.putdata(byte_array)
    image = image.resize((32, 32))

    return np.array(image.getdata(), dtype=int)

def showVectorAsImage(vector, image_name):
    image = Image.new('L', (32, 32))
    image.putdata(vector)
    image.save(image_name)

def main():
    print('Convert Images to Matrix...')
    arr = np.empty((1, 1024), dtype=int)
    for filename in os.listdir('rawdata/'):
        row = np.array([resizeByte(getByteArray('rawdata/'+filename))])
        arr = np.append(arr, row, axis = 0)
    arr = np.delete(arr, [0,0], axis = 0)
    print('Convert Complete')
    print('Calculate Singular Value Decomposition...')
    mean_vector = np.zeros((arr.shape[1],), dtype=int)
    for row in arr:
        mean_vector += row
    mean_vector //= arr.shape[0]

    for i in range(arr.shape[0]):
        arr[i] -= mean_vector
    arr = arr.T

    U, C, V = np.linalg.svd(arr, full_matrices = False)
    U = U.T
    print('SVD Complete')
    print('Visualize Vectors')
    for i in range(U.shape[0]):
        minimum = min(U[i])
        maximum = max(U[i])
        for j in range(U.shape[1]):
            U[i][j] = int(255*(U[i][j] - minimum)/(maximum-minimum))
        showVectorAsImage(U[i], 'eigenfaces/'+str(i)+'.jpg')
        
    print('Visualize Complete')
    
if __name__ == "__main__":
    main()
