from sklearn  import KNeighborsClassifier
import numpy as np

def KNN_one_neigh(path):
    #load training data
    X_train, y_train = get_pic_corpus(path,32)
    y_train = np.argmax(y_train, axis=1)

    #load test data in the 'hidden/' sub-folder 
    X_test, y_test = get_pic_corpus(os.path.join(path, 'hidden/'),1)
    y_test = np.argmax(y_test, axis=1)

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)
    predictions = knn.predict(X_test)
    print "Number right: " + str(np.sum(y_test == predictions))
    
    
def get_pic_corpus(path,npts):
    #find all the png files in the current path
    images = [os.path.join(path,f) for f in os.listdir(path) if os.path.splitext(f)[1] == '.png']
    desc_list = np.array(np.zeros(128))
    #numerical classes array
    classy = []

    for pic in images:
        desc, kp = getDescriptorKp(pic, npts)
        
        #figure what pokemon it is from the file name
        match = re.search(r"pokemon-(\d+)-", pic).group(1)
        # Add a "neighbor" to desc_list for every descriptor, we'll keep track of which is which using the "classy" array
        for d in desc:
            desc_list = np.vstack((desc_list, d))
            classy.append(int(match))

    #convert classy array to a set of logical arrays
    classfication = np.array(np.zeros(NPOKEMON))
    for i in classy:
        tmp = np.zeros(NPOKEMON)
        tmp[i-1] = 1
        classfication = np.vstack( (classfication, tmp) )

    #remove the first row of dummy values
    desc_list = np.delete(desc_list, 0, 0)
    classfication = np.delete(classfication, 0, 0)

    #normalize training features
    normalize(desc_list)
    return desc_list, classfication
