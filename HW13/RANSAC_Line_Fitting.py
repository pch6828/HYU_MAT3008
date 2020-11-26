import numpy as np
import random as rd

def getSample():
    print("Construct Sample with Gaussian Noise")
    X = np.linspace(-5,6,12)
    Y = X * 2 - np.ones((12,)) + np.random.normal(0,1,12)
    return X, Y

def getMatrix(X, Y, partial = True):
    size = 12
    idx = []
    if partial:
        idx = rd.sample(range(12), 6)
        size = 6   
    A = np.zeros((size, 2))
    B = np.zeros((size, 1))

    j = 0
    for i in range(12):
        if i in idx:
            continue
        A[j] = np.array([X[i], 1])
        B[j] = Y[i]
        j += 1

    return A, B

def pseudoinverse(A):
    return np.linalg.inv((A.T@A))@A.T

def getError(X, Y, coefficient, verbose=False):
    error = 0
    for i in range(12):
        if verbose:
            print("expected : %f result : %f" %(Y[i], X[i]*coefficient[0]+coefficient[1]))
        error+=(Y[i] - (X[i]*coefficient[0]+coefficient[1]))**2
    if verbose:
        print()
    return error/12

def get_single_result(X, Y, A, B):
    now_result = pseudoinverse(A)@B
    now_error = getError(X, Y, now_result)  
    return now_result, now_error
    
def ransac(X, Y, test = 4):
    result = None
    error = None
    while test > 0:
        partial_A, partial_B = getMatrix(X, Y)
        now_result, now_error = get_single_result(X, Y, partial_A, partial_B)
        if error == None or now_error < error:
            error = now_error
            result = now_result
        test -= 1
    return result, error

def main():
    X, Y = getSample()
    print("Construct Matrix with Whole Sample...")
    print("X : %s"%str(X))
    print("Y : %s"%str(Y))
    full_A, full_B = getMatrix(X, Y, partial=False)

    print("Start RANSAC Process...")
    partial_result, partial_error = ransac(X, Y, test=10)
    full_result, full_error = get_single_result(X, Y, full_A, full_B)

    print("Whole Sample Test Result \t: ( %f )x+( %f )"%(full_result[0], full_result[1]))
    print("RANSAC Test Result \t\t: ( %f )x+( %f )"%(partial_result[0], partial_result[1]))
    print("Whole Sample Test Error \t: %f" % full_error)
    print("RANSAC Test Error \t\t: %f" % partial_error)

if __name__ == "__main__":
    main()
