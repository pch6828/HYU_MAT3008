from PIL import Image
from scipy.fftpack import dct, idct
import numpy as np

BLOCK_SIZE = 16

def dct2(block):
    return dct(dct(block.T, norm = 'ortho').T, norm = 'ortho')

def idct2(block):
    return idct(idct(block.T, norm = 'ortho').T, norm = 'ortho')

def quantize(block):
    sorted = []

    for row in block:
        for n in row:
            sorted.append(n)
    sorted.sort(reverse = True)

    checked = {}
    for k in range(BLOCK_SIZE):
        flag = False
        for i in range(len(block)):
            for j in range(len(block[i])):
                if flag:
                    continue
                if not ((i, j) in checked) and block[i][j] == sorted[k]:
                    checked[(i, j)] = True
                    flag = True
                    

    for i in range(len(block)):
        for j in range(len(block[i])):
            if not ((i, j) in checked):
                block[i][j] = 0
    return block
            

def process_image(filename):
    image = Image.open(filename, 'r')
    R = np.zeros((960, 540), dtype = 'int')
    G = np.zeros((960, 540), dtype = 'int')
    B = np.zeros((960, 540), dtype = 'int')
    R2 = np.zeros((960, 540), dtype = 'int')
    G2 = np.zeros((960, 540), dtype = 'int')
    B2 = np.zeros((960, 540), dtype = 'int')
    for i in range(960):
        for j in range(540):
            R[i][j] = image.getpixel((i, j))[0]
            G[i][j] = image.getpixel((i, j))[1]
            B[i][j] = image.getpixel((i, j))[2]
    
    a = 0
    b = 0
    while a < 960:
        while b < 540:
            blockR = []
            blockG = []
            blockB = []
            for p in range(BLOCK_SIZE):
                rowR = []
                rowG = []
                rowB = []
                for q in range(BLOCK_SIZE):
                    i = a+p
                    j = b+q
                    if i>=960 or j >=540:
                        continue
                    rowR.append(R[i][j])
                    rowG.append(G[i][j])
                    rowB.append(B[i][j])
                blockR.append(rowR)
                blockG.append(rowG)
                blockB.append(rowB)
            dct_result_R = dct2(np.array(blockR))
            dct_result_G = dct2(np.array(blockG))
            dct_result_B = dct2(np.array(blockB))

            idct_result_R = idct2(quantize(dct_result_R))
            idct_result_G = idct2(quantize(dct_result_G))
            idct_result_B = idct2(quantize(dct_result_B))

            for p in range(len(idct_result_R)):
                for q in range(len(idct_result_R[p])):
                    i = a+p
                    j = b+q
                    R2[i][j] = idct_result_R[p][q]
                    G2[i][j] = idct_result_G[p][q]
                    B2[i][j] = idct_result_B[p][q]
            b += BLOCK_SIZE
        
        a += BLOCK_SIZE
        b = 0
    newImg = Image.new('RGB', (960,540))
    pixels = newImg.load()
    for i in range(960):
        for j in range(540):
            pixels[i,j] = (R2[i][j], G2[i][j], B2[i][j])
    newImg.save('restored+'+filename[0]+'.png')

def main():
    for i in range(1, 4):
        filename = str(i)+'.jpg'
        process_image(filename)

if __name__ == "__main__":
    main()