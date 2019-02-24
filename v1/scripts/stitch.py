import os
import numpy as np
import cv2
import time


# merge two images and return the merged one
def merge(i1, i2):

	a = i1
	b = i2
	H = match(a, b)
	#print ("Homography is : ", H)
	xh = np.linalg.inv(H)
	#print ("Inverse Homography :", xh)
	ds = np.dot(xh, np.array([a.shape[1], a.shape[0], 1]));
	ds = ds/ds[-1]
	#print ("final ds=>", ds)
	f1 = np.dot(xh, np.array([0,0,1]))
	f1 = f1/f1[-1]
	xh[0][-1] += abs(f1[0])
	xh[1][-1] += abs(f1[1])
	ds = np.dot(xh, np.array([a.shape[1], a.shape[0], 1]))
	offsety = abs(int(f1[1]))
	offsetx = abs(int(f1[0]))
	dsize = (int(ds[0])+offsetx, int(ds[1]) + offsety)

	# warp the first image
	tmp = cv2.warpPerspective(a, xh, dsize)
	#cv2.imshow("warped", tmp)
	#cv2.waitKey()

	#merge the two images
	tmp[offsety:b.shape[0]+offsety, offsetx:b.shape[1]+offsetx] = b
	#cv2.imshow("merged", tmp)
	#cv2.waitKey()
	return tmp


# find matches between i1 and i2
def match(i1, i2):

	# create SURF object
	surf = cv2.xfeatures2d.SURF_create()

	# create FLANN object
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
	search_params = dict(checks=50)
	flann = cv2.FlannBasedMatcher(index_params, search_params)

	# matches between image1 and image2
	imageSet1 = getSURFFeatures(i1, surf)
	imageSet2 = getSURFFeatures(i2, surf)

	matches = flann.knnMatch(
		imageSet2['des'],	
		imageSet1['des'],
		k=2
		)
	good = []
	for i , (m, n) in enumerate(matches):
		if m.distance < 0.7*n.distance:
			good.append((m.trainIdx, m.queryIdx))

	# find good matches and compute the H matrix using good matches
	if len(good) > 4:
		pointsCurrent = imageSet2['kp']
		pointsPrevious = imageSet1['kp']

		matchedPointsCurrent = np.float32(
			[pointsCurrent[i].pt for (__, i) in good]
		)
		matchedPointsPrev = np.float32(
			[pointsPrevious[i].pt for (i, __) in good]
			)

		H, s = cv2.findHomography(matchedPointsCurrent, matchedPointsPrev, cv2.RANSAC, 4)
		return H
	return None


# compute SURF features
def getSURFFeatures(im, surf):
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	kp, des = surf.detectAndCompute(gray, None)
	return {'kp':kp, 'des':des}




def task(filelist, pathin, pathout):

	#store the data&time info
    snapshot_time = filelist[0].partition('_')[2]
    time.sleep(5)

	# read the two processed images and resize
    image1_path = os.path.join(pathin, filelist[0])
    image2_path = os.path.join(pathin, filelist[1])

    image1 = cv2.resize(cv2.imread(image1_path),(480, 320))
    image2 = cv2.resize(cv2.imread(image2_path),(480, 320))	

    # merge two files into one
    merged = merge(image1, image2)
    cv2.imwrite(os.path.join(pathout,'merged_'+snapshot_time), merged)
    return [os.path.join(pathout,'merged_'+snapshot_time)]



def main():
    filelist= ['processed1_20190222.jpeg', 'processed2_20190222.jpeg']
    outpath = os.path.join(os.path.dirname(__file__), "generated_files/")
    outfile = task(filelist, outpath, outpath)
    return outfile


if __name__ == '__main__':

    filelist= ['processed1_20190222.jpeg', 'processed2_20190222.jpeg']
    task(filelist, '/home/erick/detection_app', '/home/erick/detection_app')






	
