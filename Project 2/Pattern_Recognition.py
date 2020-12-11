import os
import sys
import numpy as np
import scipy.stats as st
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# multiplier for mean constant
MEAN_CONSTANT = 1
# constant for variance
VAR_CONSTANT = 1


def dist(a, b):
    return np.sqrt(np.dot(a - b, a - b))

def make_cluster(mx, my, mz, vx, vy, vz, cnt):
    x = np.random.normal(mx, vx, cnt)
    y = np.random.normal(my, vy, cnt)
    z = np.random.normal(mz, vz, cnt)
    result = []
    for i in range(cnt):
        result.append((x[i], y[i], z[i]))
    return result, x, y, z

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
    global MEAN_CONSTANT, VAR_CONSTANT
    learn_data = []
    cluster_seed = [(0*MEAN_CONSTANT,0*MEAN_CONSTANT,0*MEAN_CONSTANT,1+VAR_CONSTANT,1+VAR_CONSTANT,1+VAR_CONSTANT),
                    (5*MEAN_CONSTANT,6*MEAN_CONSTANT,7*MEAN_CONSTANT,2+VAR_CONSTANT,0.8+VAR_CONSTANT,1.5+VAR_CONSTANT),
                    (1*MEAN_CONSTANT,2*MEAN_CONSTANT,3*MEAN_CONSTANT,0.8+VAR_CONSTANT,0.5+VAR_CONSTANT,0.8+VAR_CONSTANT),
                    (10*MEAN_CONSTANT,7*MEAN_CONSTANT,1*MEAN_CONSTANT,2+VAR_CONSTANT,3+VAR_CONSTANT,2+VAR_CONSTANT),
                    (3*MEAN_CONSTANT,12*MEAN_CONSTANT,7*MEAN_CONSTANT,1.5+VAR_CONSTANT,1+VAR_CONSTANT,0.5+VAR_CONSTANT)]
    means = []
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    print("Making Random Clustered Data... (for Learning)")
    for mx, my, mz, vx, vy, vz in cluster_seed:
        cluster,x,y,z = make_cluster(mx, my, mz, vx, vy, vz, 300)
        learn_data+=cluster
        ax.scatter(x,y,z,marker='o')
        means.append((mx,my,mz))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    #plt.show()
    ax.view_init(35, -35)
    plt.savefig('plot.jpg')
    print("Evaluate Clustering...")
    criterion, maximum_dist = get_criterion(learn_data)

    criterion = sort_criterion(criterion, means)
    print("Making Random Clustered Data... (for Testing)")
    cluster_seed.append((-1*MEAN_CONSTANT,4*MEAN_CONSTANT,-3*MEAN_CONSTANT,0.5+VAR_CONSTANT,0.7+VAR_CONSTANT,0.5+VAR_CONSTANT))

    test_data = []
    expected = []
    for i in range(6):
        mx, my, mz, vx, vy, vz = cluster_seed[i]
        cluster,x,y,z = make_cluster(mx, my, mz, vx, vy, vz, 100)
        test_data+=cluster
        for _ in range(100):
            expected.append(i)
    
    print("Testing...")
    print("Clustering Accuracy : %f%%" % (recognition(criterion,maximum_dist,test_data,expected)))
    
if __name__ == "__main__":
    main()