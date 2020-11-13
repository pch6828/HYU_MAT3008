import os
import sys
from PIL import Image
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as plt

def get_RGB_YUV(filename):
    image_rgb = Image.open(filename)
    image_yuv = image_rgb.convert('YCbCr')
    width, height = image_rgb.size
    filename = filename.split('.')
    filename[0] = 'converted/'+filename[0].split('/')[1]
    R = []
    G = []
    B = []
    Y = []
    U = []
    V = []
    newR = Image.new('RGB', (width, height))
    newRpixel = newR.load()
    newG = Image.new('RGB', (width, height))
    newGpixel = newG.load()
    newB = Image.new('RGB', (width, height))
    newBpixel = newB.load()
    newY = Image.new('YCbCr', (width, height))
    newYpixel = newY.load()
    newU = Image.new('YCbCr', (width, height))
    newUpixel = newU.load()
    newV = Image.new('YCbCr', (width, height))
    newVpixel = newV.load()
    for i in range(width):
        for j in range(height):
            pixel = image_rgb.getpixel((i, j))
            R.append(pixel[0])
            G.append(pixel[1])
            B.append(pixel[2])
            newRpixel[i,j] = (pixel[0], 0, 0)
            newGpixel[i,j] = (0, pixel[1], 0)
            newBpixel[i,j] = (0, 0, pixel[2])
            pixel = image_yuv.getpixel((i, j))
            Y.append(pixel[0])
            U.append(pixel[1])
            V.append(pixel[2])
            newYpixel[i,j] = (pixel[0], 128, 128)
            newUpixel[i,j] = (128, pixel[1], 128)
            newVpixel[i,j] = (128, 128, pixel[2])
    
    newR.save(filename[0]+'R.'+filename[1])
    newG.save(filename[0]+'G.'+filename[1])
    newB.save(filename[0]+'B.'+filename[1])
    newY.save(filename[0]+'Y.'+filename[1])
    newU.save(filename[0]+'U.'+filename[1])
    newV.save(filename[0]+'V.'+filename[1])
    return R, G, B, Y, U, V

def get_correlation(A, B):
    avg_A = 0.0
    avg_B = 0.0
    for a in A:
        avg_A += a
    avg_A /= len(A)
    for b in B:
        avg_B += b
    avg_B /= len(B)

    stdev_A = 0.0
    stdev_B = 0.0
    for a in A:
        stdev_A += (a - avg_A)**2
    for b in B:
        stdev_B += (b - avg_B)**2
    stdev_A /= len(A)
    stdev_B /= len(B)
    stdev_A = np.sqrt(stdev_A)
    stdev_B = np.sqrt(stdev_B)

    covariance = 0.0
    for i in range(len(A)):
        covariance += (A[i]-avg_A)*(B[i]-avg_B)
    covariance /= len(A)

    return covariance/(stdev_A*stdev_B)

def main():
    for filename in os.listdir('crop_data/'):
        print("Filename : %s" % filename)
        print("Get RGV and YUV component...")
        R, G, B, Y, U, V = get_RGB_YUV('crop_data/'+filename)
        print("Evaluate Correlation Coefficient...")
        print("G-R correlation : %10f" % get_correlation(R, G))
        print("G-B correlation : %10f" % get_correlation(G, B))
        print("R-B correlation : %10f" % get_correlation(R, B))
        print("Y-U correlation : %10f" % get_correlation(Y, U))
        print("Y-V correlation : %10f" % get_correlation(Y, V))
        print("U-V correlation : %10f" % get_correlation(U, V))

if __name__ == "__main__":
    main()