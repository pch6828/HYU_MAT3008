import os
import sys
from PIL import Image
import numpy as np

def visualize_fft(filename):
    fft_result = np.zeros((64, 64), dtype = 'complex128')
    cnt = 10
    pixels = np.asarray(Image.open(filename, 'r').convert('L')).reshape((640,640))

    while cnt > 0:
        cnt -= 1
        x = np.random.randint(0, 640 - 64)
        y = np.random.randint(0, 640 - 64)

        block = np.zeros((64, 64))
        for i in range(64):
            for j in range(64):
                block[i][j] = pixels[x+i][y+j]
        
        fft_result += np.fft.fftshift(np.fft.fft2(block))
    
    fft_result /= 10
    result = 10*np.log(np.abs(fft_result))

    maximum = np.max(result)
    minimum = np.min(result)

    for i in range(64):
        for j in range(64):
            result[i][j] = (result[i][j] - minimum)*255/(maximum-minimum)
    
    return result

def matrix_to_image(matrix, image_name):
    image = Image.new('L', (64, 64))
    image.putdata(matrix.reshape((64*64,)))
    image.save(image_name)

def main():
    for filename in os.listdir('patterns/'):
        matrix_to_image(visualize_fft('patterns/'+filename), 'fft/'+filename)

if __name__ == "__main__":
    main()