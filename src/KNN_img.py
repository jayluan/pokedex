from ANN_img_bak import *
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

def KNN_img(path):
    #load training data
    X_train, y_train = load_pics(path)
    y_train = np.argmax(y_train, axis=1)

    #load test data in the 'hidden/' sub-folder 
    X_test, y_test = load_pics(os.path.join(path, 'hidden/'))
    y_test = np.argmax(y_test, axis=1)

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)
    predictions = knn.predict(X_test)
    print "Number right: " + str(np.sum(y_test == predictions))

if __name__ == "__main__":
    KNN_img('./../sample/test/')
















