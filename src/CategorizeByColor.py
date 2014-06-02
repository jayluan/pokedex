import cv2
import numpy as np
import findPokeMask as fpm

imDir = '../sample/bulbapedia_resized/'
# FIRST GEN FOREVER
nPokes = 10
nBins = 15
histArr = np.zeros((nPokes,nBins))

# For each pokemon, get the histogram of its hue color channel
for poke in range(0,nPokes):
    aPoke = cv2.imread(imDir + 'pokemon-' + str(poke+1) + '-1y.png')
    k,j = np.meshgrid(np.arange(aPoke.shape[1]),np.arange(aPoke.shape[0]))
    pokeArray = [cv2.cvtColor(aPoke,cv2.COLOR_RGB2HSV)[j,k,1]]
    aPoke = cv2.imread(imDir + 'pokemon-' + str(poke+1) + '-2g.png')
    if aPoke != None:
        pokeArray = pokeArray + [cv2.cvtColor(aPoke,cv2.COLOR_RGB2HSV)[j,k,1]]
    aPoke = cv2.imread(imDir + 'pokemon-' + str(poke+1) + '-2s.png')
    if aPoke != None:
        pokeArray = pokeArray + [cv2.cvtColor(aPoke,cv2.COLOR_RGB2HSV)[j,k,1]]
    aPoke = cv2.imread(imDir + 'pokemon-' + str(poke+1) + '-3r.png')
    if aPoke != None:
        pokeArray = pokeArray + [cv2.cvtColor(aPoke,cv2.COLOR_RGB2HSV)[j,k,1]]
    aPoke = cv2.imread(imDir + 'pokemon-' + str(poke+1) + '-4d.png')
    if aPoke != None:
        pokeArray = pokeArray + [cv2.cvtColor(aPoke,cv2.COLOR_RGB2HSV)[j,k,1]]
    
    pokeHist = np.zeros(nBins)
    for im in range(0,len(pokeArray)):
        mask = fpm.findPokeMask(pokeArray[im])
        pokeHist = pokeHist + np.histogram(np.where(pokeArray[im] * mask),nBins)[0]
    histArr[poke,] = pokeHist / sum(pokeHist)
    print 'done with poke ' + str(poke)
        

# Now predict the 5th gen pokemon from the first 4
for poke in range(0,2):
    # Get the pokemon
    testPoke = cv2.imread(imDir + 'pokemon-' + str(poke+1) + '-5b.png')
    if testPoke == None:
        continue
    k,j = np.meshgrid(np.arange(testPoke.shape[1]),np.arange(testPoke.shape[0]))
    pokeHSV = cv2.cvtColor(testPoke,cv2.COLOR_RGB2HSV)[j,k,1]
    mask = fpm.findPokeMask(testPoke)
    hist = np.zeros(nBins)
    hist = hist + np.histogram(np.where(pokeHSV*mask),nBins)[0]
    hist = hist / sum(hist)
    # Use Euclidean distance to compare this histogram with the others
    dists = np.zeros(nPokes)
    for potMatch in range(0,nPokes):
        dists[potMatch] = np.linalg.norm(hist-histArr[potMatch,],2)
        print 'diff between ' + str(poke) + ' and ' + str(potMatch)
    print 'dists for element ' + str(poke) 
    #print hist
    best = np.argmin(dists)
    print 'the best match for ' + str(poke) + ' is ' + str(best) + '.'
