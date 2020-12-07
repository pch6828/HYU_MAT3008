import os
import sys
import numpy as np
import scipy.stats as st
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def dist(a, b):
    return np.sqrt(np.dot(a - b, a - b))

def make_cluster(mx, my, mz, vx, vy, vz):
    # TODO
    # make random cluster by Gaussian Distribution of given parameters
    # each vector is 3 dimension 
    pass

def get_criterion(data):
    # TODO
    # calculate mean vectors of 5 clusters
    # by k-means clustering method
    # also calculate maximum distance
    pass

def recognition(criterion, maximum_dist, data, expected):
    # TODO
    # pattern recognition procedure
    # just get minimum distance
    # but if minimum distance is longer than pre_calcluated maximum distance, it'll be recognized as unknown (which is class 5, not 0~4)
    # the result is accuracy expressed in percentage
    pass

def main(): 
    pass   

if __name__ == "__main__":
    main()