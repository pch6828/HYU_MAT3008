import os
import sys
import numpy as np
import scipy.stats as st
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def dist(a, b):
    return np.sqrt(np.dot(a - b, a - b))

def make_cluster(mx, my, mz, vx, vy, vz, cnt):
    x = np.random.normal(mx, vx, cnt)
    y = np.random.normal(my, vy, cnt)
    z = np.random.normal(mz, vz, cnt)

    return np.array([x,y,z]).T

def get_criterion(data):
    km = KMeans(n_clusters=5, random_state=0)
    km.fit(data)
    label = km.labels_
    criterion = km.cluster_centers_

    maximum_dist = 0
    for i in range(len(data)):
        a = data[i]
        b = np.array(criterion[label[i]])
        maximum_dist = max(maximum_dist, dist(a, b))
    
    return criterion, maximum_dist

def recognition(criterion, maximum_dist, data, expected):
    total = len(expected)
    cnt = 0
    
    for i in range(total):
        a = data[i]
        minimum_dist = maximum_dist
        cluster_id = 5
        for cluster in range(5):
            b = np.array(criterion[cluster])
            d = dist(a, b)
            if minimum_dist > d:
                minimum_dist = d
                cluster_id = cluster
        if cluster_id == expected[i]:
            cnt += 1
    
    return cnt/total*100

def main(): 
    pass   

if __name__ == "__main__":
    main()