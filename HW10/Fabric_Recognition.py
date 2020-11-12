import os
import sys
from PIL import Image
import numpy as np

BLOCK_CNT = 10
BLOCK_SIZE = 64
TEST_SIZE = (BLOCK_SIZE//2, BLOCK_SIZE//2)

def visualize_fft(filename):
    global BLOCK_CNT
    global BLOCK_SIZE
    fft_result = np.zeros((BLOCK_SIZE, BLOCK_SIZE), dtype = 'complex128')
    cnt = BLOCK_CNT
    pixels = np.asarray(Image.open(filename, 'r').convert('L')).reshape((640,640))

    while cnt > 0:
        cnt -= 1
        x = np.random.randint(0, 640 - BLOCK_SIZE)
        y = np.random.randint(0, 640 - BLOCK_SIZE)

        block = np.zeros((BLOCK_SIZE, BLOCK_SIZE))
        for i in range(BLOCK_SIZE):
            for j in range(BLOCK_SIZE):
                block[i][j] = pixels[x+i][y+j]
        
        fft_result += np.fft.fftshift(np.fft.fft2(block))
    
    fft_result /= BLOCK_CNT
    fft_result = np.abs(fft_result)
    for i in range(BLOCK_SIZE):
        for j in range(BLOCK_SIZE):
            if fft_result[i][j]==0:
                fft_result[i][j] = 1

    result = 10*np.log(fft_result)
    maximum = np.max(result)
    minimum = np.min(result)

    for i in range(BLOCK_SIZE):
        for j in range(BLOCK_SIZE):
            result[i][j] = int((result[i][j] - minimum)*255/(maximum-minimum))
    
    return result, fft_result

def matrix_to_image(matrix, image_name):
    global BLOCK_SIZE
    image = Image.new('L', (BLOCK_SIZE, BLOCK_SIZE))
    image.putdata(matrix.reshape((BLOCK_SIZE*BLOCK_SIZE,)))
    image.save(image_name)

def normalize(vector):
    return vector / np.sqrt(np.dot(vector, vector))

def make_coefficient_vector(fft_vector):
    global BLOCK_SIZE, TEST_SIZE
    fft_matrix = fft_vector.reshape((BLOCK_SIZE, BLOCK_SIZE))
    coefficient_matrix = np.zeros(TEST_SIZE)

    for i in range(TEST_SIZE[0]):
        for j in range(TEST_SIZE[1]):
            coefficient_matrix[i][j] = fft_matrix[i+(BLOCK_SIZE-TEST_SIZE[0])][j+(BLOCK_SIZE-TEST_SIZE[1])]

    return normalize(coefficient_matrix.reshape((TEST_SIZE[0]*TEST_SIZE[1],)))

def make_coefficient_map(fft_map):
    coefficient_map = {}

    for filename in fft_map:
        coefficient_map[filename] = make_coefficient_vector(fft_map[filename])

    return coefficient_map

def pattern_recognition(filename, coefficient_map):
    global BLOCK_SIZE
    pixel, fft_result = visualize_fft(filename)
    pattern_vector = fft_result.reshape((BLOCK_SIZE*BLOCK_SIZE))
    pattern_vector[BLOCK_SIZE*BLOCK_SIZE//2+BLOCK_SIZE//2] = 0
    pattern_vector = make_coefficient_vector(pattern_vector)

    min_dist = None
    recognized = None
    for filename2 in coefficient_map:
        sub_vector = coefficient_map[filename2] - pattern_vector
        dist = np.sqrt(np.dot(sub_vector, sub_vector))

        if min_dist == None or min_dist > dist:
            min_dist = dist
            recognized = filename2

    return recognized

def main():
    global BLOCK_SIZE
    fft_map = {}
    print("DFT Analysis on Images...")
    for filename in os.listdir('patterns/'):
        pixel, fft_result = visualize_fft('patterns/'+filename)
        matrix_to_image(pixel, 'fft/'+filename)

        fft_vector = fft_result.reshape((BLOCK_SIZE*BLOCK_SIZE,))
        fft_vector[np.argmax(fft_vector)] = 0
        fft_map[filename] = fft_vector

    print("Make Criterion for Fabric Recognition...")
    coefficient_map = make_coefficient_map(fft_map) 

    print("Manual Test...")
    while(True):
        filename = input("Input Filename or \"quit\" to Stop Testing > ")

        if filename == "quit":
            break

        print("Recognized as %s" % pattern_recognition(filename, coefficient_map))
    
    print("Evaluate Accuracy...")
    accuracy = 0
    for filename in os.listdir('patterns/'):
        for abc in range(5):
            recognized = pattern_recognition('patterns/'+filename, coefficient_map)
            
            if recognized == filename:
                accuracy += 1

    print("Accuracy : %d%%" % accuracy)
    
if __name__ == "__main__":
    main()