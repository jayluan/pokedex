import cv2,cv,numpy as np
import os

featsPerPict = 10
nPokes = 151
inDir = '../sample/bulbapedia_resized/'

def detectFromArray(pictArr):
    sift = cv2.SIFT(nfeatures = featsPerPict)
    kps,descs = ([],[])
    for img in pictArr:
        kp, des = sift.detectAndCompute(img,None)
        kps = kps + kp
        descs = descs + des
    return kps,descs

def predictFromDescs(kps,testIm):
    return None

# Behold my gloriously shitty python string parsing abilities! #swag
def parsePoke(str):
    pokeNum = str[8:11]
    hyph = pokeNum.find('-')
    if hyph == -1:
        return(int(pokeNum))
    else:
        return(int(pokeNum[0:hyph]))
    
def getPokes():
    pokes = dict()
    for i in range(0,nPokes):
        pokes[i] = []
    dirList = os.listdir(inDir)
    for i in range(0,len(dirList)):
        poke = parsePoke(dirList[i])
        pokes[poke-1] = pokes[poke-1] + [cv2.imread(inDir+dirList[i])]
    return pokes
    
def main(path):
    pokes = getPokes()
    