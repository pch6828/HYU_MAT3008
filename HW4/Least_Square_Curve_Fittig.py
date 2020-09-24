import numpy as np
import random as rd

points = [(-2.9, 35.4),
          (-2.1, 19.7),
          (-0.9, 5.7),
          (1.1, 2.1),
          (0.1, 1.2),
          (1.9, 8.7),
          (3.1, 25.7),
          (4.0, 41.5)]

def getMatrix():
    global points
    A = np.zeros((6, 3))
    B = np.zeros((6, 1))
    idx = rd.sample(range(8), 2)
    j = 0
    print("Chosen Point :")
    for i in range(8):
        if i == idx[0] or i == idx[1]:
            continue
        #print("(%10f, %10f)"%(points[i][0], points[i][1]))
        A[j] = np.array([points[i][0]**2, points[i][0], 1])
        B[j] = points[i][1]
        j += 1


    print("\nMatrix A :")
    print(A)
    print("\nVector B :")
    print(B)
    return A, B

def getMatrix2():
    global points
    A = np.zeros((8, 3))
    B = np.zeros((8, 1))
    j = 0
    print("Chosen Point : ALL")
    for i in range(8):
        #print("(%f, %f)"%(points[i][0], points[i][1]))
        A[j] = np.array([points[i][0]**2, points[i][0], 1])
        B[j] = points[i][1]
        j += 1
        
    print("\nMatrix A :")
    print(A)
    print("\nVector B :")
    print(B)
    return A, B

def pseudoinverse(A):
    return np.linalg.inv((A.T@A))@A.T

def getError(x):
    global points
    error = 0
    for p in points:
        print("expected : %f result : %f"
              %(p[1], p[0]**2*x[0]+p[0]*x[1]+x[2]))
        error+=(p[0]**2*x[0]+p[0]*x[1]+x[2]-p[1])**2
    return error

def main():
    A, B = getMatrix2()
    x = pseudoinverse(A)@B
    print("result : %fx^2 + %fx + %f"%(x[0], x[1], x[2]))
    error = getError(x)
    print("Total Error : %f" % error)

if __name__ == "__main__":
    main()
