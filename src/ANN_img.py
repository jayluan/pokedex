import numpy
import cv2
import matplotlib.pyplot as plt
import os, re

def getDescriptorKp(img_file, npts):
    img = cv2.imread(img_file, 0)    #0 = read black and white
    surf = cv2.SIFT(nfeatures=npts, exended=False)
    kp, des = surf.detectAndCompute(img, None)
    return des, kp


def train_ANN(train_data, classification):
    ninputs = 64*64
    nhidden = 8
    noutput = 151
    layers = numpy.array([ninputs, nhidden, noutput])
    nnet = cv2.ANN_MLP(layers)
    step_size = 0.01
    nsteps = 10000
    max_err = 0.0001
    condition = cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS
    criteria = (condition, nsteps, max_err)
    params = dict( term_crit = criteria, 
               train_method = cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP, 
               bp_dw_scale = step_size, 
               bp_moment_scale = momentum )
    num_iter = nnet.train(train_data, classification,
                      None, params=params)
    return nnet

def main(path):
    #get all images
    npts = 64
    images = [os.path.join(path,f) for f in os.listdir(path) if os.path.splitext(f)[1] == '.png']
    desc_list = np.array()
    classy = np.array()

    for pic in images:
        desc, kp = getDescriptorKp(pic, npts)
        desc_list.append(desc)

        #figure what pokemon it is from the file name
        match = re.search(r"pokemon-(\d+)-", pic).group(1)
        classy.append(int(match))

    #convert classy to binaries
    classfication = np.array
    for i in classy:
        

if __name__=="__main__":
    main('../samples/bulbapedia/')



















