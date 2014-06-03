import numpy as np
import cv2
import os
import re

NPTS = 128

def getDescriptorKp(img_file, npts):
    img = cv2.imread(img_file, 0)    #0 = read black and white
    surf = cv2.SIFT(nfeatures=npts)
    kp, des = surf.detectAndCompute(img, None)
    return des, kp, img

def load_pics(path):
    #get all images
    #find all the png files in the current path
    images = [os.path.join(path,f) for f in os.listdir(path) if os.path.splitext(f)[1] == '.png']
    desc_list = []
    kp_list = []
    classy = []
    img_list = []

    for pic in images:
        desc, kp, img = getDescriptorKp(pic, NPTS)
        #sometimes not all 32 descriptors are returned because there's not enough, in which case we just pad up to 32 descriptors * 128 values/desc
        desc_list.append(desc)
        kp_list.append(kp)
        img_list.append(img)

        #figure what pokemon it is from the file name
        match = re.search(r"pokemon-(\d+)-", pic).group(1)
        classy.append(int(match))

    #remove the first row of dummy values
    desc_list = np.delete(desc_list, 0, 0)

    return desc_list, kp_list, classy, img_list

def match_images(desc1, kp1, desc2, kp2):
    """Given two images, returns the matches"""
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2) #2
    kp_pairs = filter_matches(kp1, kp2, raw_matches)
    return kp_pairs


def filter_matches(kp1, kp2, matches, ratio = 0.75):
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            m = m[0]
            if(m.queryIdx >= len(kp1) or m.trainIdx >= len(kp2)):
                continue
            mkp1.append( kp1[m.queryIdx] )
            mkp2.append( kp2[m.trainIdx] )
    kp_pairs = zip(mkp1, mkp2)
    return kp_pairs


def explore_match(win, img1, img2, kp_pairs, status = None, H = None):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
    vis[:h1, :w1] = img1
    vis[:h2, w1:w1+w2] = img2
    vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    if H is not None:
        corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
        cv2.polylines(vis, [corners], True, (255, 255, 255))

    if status is None:
        status = np.ones(len(kp_pairs), np.bool_)
    p1 = np.int32([kpp[0].pt for kpp in kp_pairs])
    p2 = np.int32([kpp[1].pt for kpp in kp_pairs]) + (w1, 0)

    green = (0, 255, 0)
    red = (0, 0, 255)
    white = (255, 255, 255)
    kp_color = (51, 103, 236)
    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            col = green
            cv2.circle(vis, (x1, y1), 2, col, -1)
            cv2.circle(vis, (x2, y2), 2, col, -1)
        else:
            col = red
            r = 2
            thickness = 3
            cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
            cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
            cv2.line(vis, (x2-r, y2-r), (x2+r, y2+r), col, thickness)
            cv2.line(vis, (x2-r, y2+r), (x2+r, y2-r), col, thickness)
    vis0 = vis.copy()
    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            cv2.line(vis, (x1, y1), (x2, y2), green)

    cv2.imshow(win, vis)



def draw_matches(window_name, kp_pairs, img1, img2):
    """Draws the matches for """
    mkp1, mkp2 = zip(*kp_pairs)

    p1 = np.float32([kp.pt for kp in mkp1])
    p2 = np.float32([kp.pt for kp in mkp2])

    if len(kp_pairs) >= 4:
        H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
        #print '%d / %d  inliers/matched' % (numpy.sum(status), len(status))
    else:
        H, status = None, None
        #print '%d matches found, not enough for homography estimation' % len(p1)

    if len(p1):
        explore_match(window_name, img1, img2, kp_pairs, status, H)


def main(path):
    #load training data
    X_train_desc, X_train_kp, y_train, train_img = load_pics(path)

    #load test data in the 'hidden/' sub-folder 
    X_test_desc, X_test_kp, y_test, test_img = load_pics(os.path.join(path, 'hidden/'))

    guesses = []
    for target,kp1,poke_id1, img1 in zip(X_test_desc, X_test_kp, y_test, test_img):
        longest_kp = 0
        guess_id = -1
        for suspect, kp2, poke_id2, img2 in zip(X_train_desc, X_train_kp, y_train, train_img):
            kp_pairs = match_images(target, kp1, suspect, kp2)
            if(len(kp_pairs) > longest_kp):
                guess_id = poke_id2
                longest_kp = len(kp_pairs)
                draw_matches('matches', kp_pairs, img1, img2)
                cv2.waitKey()
                cv2.destroyAllWindows()

        guesses.append(guess_id)

    print "Number correct: " + str(np.sum(guesses == y_test))

if __name__=="__main__":
    main('./../sample/test/')














