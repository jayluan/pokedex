import numpy as np
import cv2
import matplotlib.pyplot as plt
import os, re


#number of pokemon to test
NPOKEMON = 151

#Get the descrptor and key points
def getDescriptorKp(img_file, npts):
    img = cv2.imread(img_file, 0)    #0 = read black and white
    surf = cv2.SIFT(nfeatures=npts)
    kp, des = surf.detectAndCompute(img, None)
    return des, kp


#train on input data, which are both 2d numpy arrays. train_data has row = # samples, cols= num of descriptors * descriptor length
def train_ANN(train_data, classification):
    ninputs = 32*128
    noutput = NPOKEMON
    nhidden = 350 #side of my single hidden layer
    layers = np.array([ninputs, nhidden, noutput])
    nnet = cv2.ANN_MLP(layers, cv2.ANN_MLP_SIGMOID_SYM, 1, 1)    #setup the neural net with sigmoid function
    step_size = 0.01
    nsteps = 10000
    max_err = 0.0001
    momentum = 0
    condition = cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS
    criteria = (condition, nsteps, max_err)
    params = dict( term_crit = criteria, 
               train_method = cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP, 
               bp_dw_scale = step_size, 
               bp_moment_scale = momentum )
    num_iter = nnet.train(train_data, classification,
                      None, params=params)
    return nnet

#normlize values across every feature
def normalize(arr):
    row, col = arr.shape
    for i in range(col):
        mag = np.linalg.norm(arr[:,i])
        arr[:,i] = arr[:,i]/mag

#load images from a given path and parse them into training features and binary traning classifications.
#returns 2d set of training features and 2d set of classifications, where each row should be all 150 0's and one 1 for whatever pokemon the training data represents.
def load_pics(path):
    #get all images
    npts = 32    

    #find all the png files in the current path
    images = [os.path.join(path,f) for f in os.listdir(path) if os.path.splitext(f)[1] == '.png']
    desc_list = np.array(np.zeros(npts*128))
    #numerical classes array
    classy = []

    for pic in images:
        desc, kp = getDescriptorKp(pic, npts)
        #sometimes not all 32 descriptors are returned because there's not enough, in which case we just pad up to 32 descriptors * 128 values/desc
        desc_list = np.vstack( (desc_list, np.resize(desc.flatten(), (1, npts*128))) )

        #figure what pokemon it is from the file name
        match = re.search(r"pokemon-(\d+)-", pic).group(1)
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


def main(path):
    #load training data
    X_train, y_train = load_pics(path)

    #load test data in the 'hidden/' sub-folder 
    X_test, y_test = load_pics(os.path.join(path, 'hidden/'))

    #train on the data
    brain = train_ANN(X_train, y_train)
    predictions = np.empty_like(y_test)
    
    #predict on test data
    brain.predict(X_test, predictions)
    brain.save('ANN_img')

    # svm_params = dict( kernel_type = cv2.SVM_LINEAR,
    #                 svm_type = cv2.SVM_C_SVC,
    #                 C=2.67, gamma=5.383 )
    # svm = cv2.SVM()
    # y_train = (np.float32(np.argmax(y_train, axis=1))+1)/10
    # svm.train(np.float32(X_train), np.float32(y_train), params=svm_params)
    # predictions = np.zeros(10)
    # svm.predict_all(np.float32(X_test), predictions)

    #find the labels that were categorized
    true_labels = np.argmax(y_test, axis=1)+1
    pred_labels = (np.argmax(predictions, axis=1)+1)
    num_correct = np.sum(true_labels == pred_labels)
    print true_labels
    print pred_labels
    print "Number correct: " + str(num_correct)

if __name__=="__main__":
    main('./../sample/test/')



















