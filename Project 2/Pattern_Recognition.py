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
    result = []
    for i in range(cnt):
        result.append((x[i], y[i], z[i]))
    return result

def get_criterion(data):
    km = KMeans(n_clusters=5, random_state=0)
    km.fit(data)
    label = km.labels_
    criterion = km.cluster_centers_

    maximum_dist = [0,0,0,0,0]
    for i in range(len(data)):
        a = data[i]
        b = np.array(criterion[label[i]])
        maximum_dist[label[i]] = max(maximum_dist[label[i]], dist(a, b))

    return criterion, np.average(maximum_dist)*0.8

def sort_criterion(criterion, means):
    result = []
    for mean in means:
        selected = None
        flag = True
        for crit in criterion:
            if flag:
                flag = False
                selected = crit
            elif dist(np.array(selected), np.array(mean)) > dist(np.array(crit), np.array(mean)):
                selected = crit
        result.append(selected)
    return result

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
    learn_data = []
    cluster_seed = [(0,0,0,1,1,1),
                    (5,6,7,1,1,1),
                    (1,2,3,1,1,1),
                    (10,7,1,1,1,1),
                    (1,9,7,1,1,1)]
    means = []
    print("Making Random Clustered Data... (for Learning)")
    for mx, my, mz, vx, vy, vz in cluster_seed:
        learn_data+=make_cluster(mx, my, mz, vx, vy, vz, 300)
        means.append((mx,my,mz))
    
    print("Evaluate Clustering...")
    criterion, maximum_dist = get_criterion(learn_data)

    criterion = sort_criterion(criterion, means)
    print("Making Random Clustered Data... (for Testing)")
    cluster_seed.append((3,4,3,1,1,1))

    test_data = []
    expected = []
    for i in range(6):
        mx, my, mz, vx, vy, vz = cluster_seed[i]
        test_data+=make_cluster(mx, my, mz, vx, vy, vz, 100)
        for j in range(100):
            expected.append(i)
    
    
    print("Testing...")
    print("Clustering Accuracy : %f%%" % (recognition(criterion,maximum_dist,test_data,expected)))
    


if __name__ == "__main__":
    main()