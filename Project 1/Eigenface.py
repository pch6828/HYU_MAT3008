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

def saveResultImage(byte_array, image_name):
    image = Image.new('L', (32, 32))
    image.putdata(byte_array)
    image.save(image_name)

def getCoefficient(name, testset, eigenfaces, mean_face):
    result = np.zeros((eigenfaces.shape[1],))
    for i in range(5):
        filename = testset+str(i)+'.jpg'
        image = np.asarray(
            Image.open(filename, 'r').convert('L')
            ).reshape((1024,))

        x = []
        for row in eigenfaces.T:
           x.append((image@row))
        saveResultImage(eigenfaces@np.array(x)+mean_face,
                        testset+'result'+str(i)+'.jpg')
        result += np.array(x) 
    result /= 5
    return (name, result)

def processTest(coefficient, eigenfaces, filename):
    image = np.asarray(
        Image.open(filename, 'r').convert('L')
        ).reshape((1024,))
    x = []
    for row in eigenfaces.T:
        x.append((image@row))
    x = np.array(x)
    
    dist = None
    result = None
    for name, ce in coefficient:
        v = x - ce
        if dist != None:
            if dist > np.dot(v, v):
                dist = np.dot(v, v)
                result = name
        else:
            dist = np.dot(v, v)
            result = name
    return result

def main():
    print('@Convert Images to Matrix...')
    arr = np.empty((1, 1024), dtype=int)
    for filename in os.listdir('rawdata/'):
        row = np.array([resizeByte(getByteArray('rawdata/'+filename))])
        arr = np.append(arr, row, axis = 0)
    arr = np.delete(arr, [0,0], axis = 0)
    print('@Convert Complete')
    print('')
    print('@Calculate Singular Value Decomposition...')
    mean_vector = np.zeros((arr.shape[1],), dtype=int)
    for row in arr:
        mean_vector += row
    mean_vector //= arr.shape[0]
    
    for i in range(arr.shape[0]):
        arr[i] -= mean_vector
    arr = arr.T

    U, C, V = np.linalg.svd(arr, full_matrices = False)
    U = U.T
    visualized_U = np.empty((1024, 1024), dtype=int)
    print('@SVD Complete')
    print('')
    print('@Visualize Vectors')
    for i in range(U.shape[0]):
        minimum = min(U[i])
        maximum = max(U[i])
        for j in range(U.shape[1]):
            visualized_U[i][j] = int(255*(U[i][j] - minimum)/(maximum-minimum))
        showVectorAsImage(visualized_U[i], 'eigenfaces/'+str(i)+'.jpg')
    
    print('@Visualize Complete')
    print('')
    print('@Construct Face Recognition Information...')
    eigenfaces = U[:70].T
    TC = [('Bill_Clinton','test_sample/test0/'),
          ('George_W_Bush','test_sample/test1/'),
          ('Sylvester_Stallone','test_sample/test2/'),
          ('Yoriko_Kawaguchi','test_sample/test3/'),
          ('Vladimir_Putin','test_sample/test4/'),
          ('Tom_Hanks','test_sample/test5/'),
          ('Roh_Moo_hyun','test_sample/test6/'),
          ('Michael_Jackson','test_sample/test7/'),
          ('Leonardo_Dicaprio','test_sample/test8/'),
          ('Britney_Spears','test_sample/test9/')]
    idx = 0
    coefficient = []
    for name, testset in TC:
        coefficient.append(getCoefficient(name, testset, eigenfaces, mean_vector))
        idx+=1
    print('@Construct Complete')
    print('')
    print('@Face Recognition Test...')
    cmd = input('Select Mode > [1] - Manual | [2] - All file : ')
    if cmd == '1':
        while True:
            filename = input('Input Filename, or "quit" to quit: ')
            if filename == 'quit':
                break
            print(processTest(coefficient, eigenfaces, filename))

    elif cmd == '2':
        for i in range(10):
            print('Test #'+str(i)+' '+TC[i][0])
            for j in range(5):
                filename = TC[i][1]+str(j)+'.jpg'
                print(processTest(coefficient, eigenfaces, filename))
            print('')
    print('@Test Complete')
    
if __name__ == "__main__":
    main()
