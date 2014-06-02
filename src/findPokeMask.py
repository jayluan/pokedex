import cv2
import numpy as np

# Find the mask corresponding to the actual pokemon, so we don't do stuff with
# the bounding box.
def findPokeMask(pokeIm):
    if len(pokeIm.shape) > 2:
        grayPoke = cv2.cvtColor(pokeIm,cv2.COLOR_RGB2GRAY)
    else:
        grayPoke = pokeIm
    m,n = grayPoke.shape
    retMask = np.zeros((m,n))
    # First, find all first/last row elements, then columns
    for i in range(0,m):
        nonZeros = grayPoke[i,].nonzero()[0]
        if len(nonZeros):
            retMask[i,nonZeros[0]:nonZeros[len(nonZeros)-1]] = 1
    for i in range(0,n):
        nonZeros = grayPoke[0:m,i].nonzero()[0]
        if len(nonZeros):
            retMask[nonZeros[0]:nonZeros[len(nonZeros)-1],i] = 1
    return retMask



