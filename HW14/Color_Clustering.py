import os
import sys
from PIL import Image, ImageCms
import numpy as np
import scipy.stats as st
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
import matplotlib.pyplot as plt

def drawplot(data, name):
    # Extract x and y
    x = []
    y = []
    for d in data:
        x.append(d[1])
        y.append(d[2])
    # Define the borders
    deltaX = (max(x) - min(x))/10
    deltaY = (max(y) - min(y))/10
    xmin = min(x) - deltaX
    xmax = max(x) + deltaX
    ymin = min(y) - deltaY
    ymax = max(y) + deltaY
    # Create meshgrid
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)
    fmax = np.max(f)
    fmin = np.min(f)
    f -= fmin
    f /= (fmax - fmin)
    f *= 255

    fig = plt.figure(figsize=(13, 7))
    ax = plt.axes(projection='3d')
    surf = ax.plot_surface(xx, yy, f, rstride=1, cstride=1, cmap='coolwarm', edgecolor='none')
    ax.set_xlabel('u')
    ax.set_ylabel('v')
    ax.set_zlabel('Normalized Density')
    ax.set_title(name)
    fig.colorbar(surf, shrink=0.5, aspect=5) # add color bar indicating the PDF
    ax.view_init(35, 35)
    plt.savefig(name)

def image_process(filename):
    srgb_p = ImageCms.createProfile("sRGB")
    lab_p  = ImageCms.createProfile("LAB")

    rgb2lab = ImageCms.buildTransformFromOpenProfiles(srgb_p, lab_p, "RGB", "LAB")
    lab2rgb = ImageCms.buildTransformFromOpenProfiles(lab_p, srgb_p, "LAB", "RGB")

    image = ImageCms.applyTransform(Image.open('crop_data/'+filename), rgb2lab)
    width, height = image.size
    pixels = []
    for i in range(width):
        for j in range(height):
            pixels.append(image.getpixel((i, j)))

    bandwidth = estimate_bandwidth(pixels, quantile=0.05, n_samples=3200)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(pixels)
    ms_labels = ms.labels_
    ms_cluster_centers = ms.cluster_centers_
    km = KMeans(n_clusters=len(ms_cluster_centers), random_state=0)
    km.fit(pixels)
    km_labels = km.labels_
    km_cluster_centers = km.cluster_centers_

    ms_image = Image.new('LAB', (640, 640))
    ms_pixels = ms_image.load()
    km_image = Image.new('LAB', (640, 640))
    km_pixels = km_image.load()
    for i in range(640):
        for j in range(640):
            pixel = ms_cluster_centers[ms_labels[i*640+j]]
            ms_pixels[i, j] = (int(pixel[0]),int(pixel[1]),int(pixel[2]))
            pixel = km_cluster_centers[km_labels[i*640+j]]
            km_pixels[i ,j] = (int(pixel[0]),int(pixel[1]),int(pixel[2]))
    
    print("# of clusters of %s : %d(ms), %d(km)"%(filename,len(ms_cluster_centers), len(km_cluster_centers)))
    ImageCms.applyTransform(ms_image, lab2rgb).save('clustered/ms_'+filename)
    ImageCms.applyTransform(km_image, lab2rgb).save('clustered/km_'+filename)
    drawplot(pixels, 'plot/'+filename)

def main():
    for filename in os.listdir('crop_data/'):
        image_process(filename)

if __name__ == "__main__":
    main()