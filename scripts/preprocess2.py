"""
 * Copyright (c) 2019, Autonomous Networks Research Group. All rights reserved.
 *     contributors:
 *      Pradipta Ghosh, March 2019
 *      Wenda Chen, March 2019
 *      Bhaskar Krishnamachari, March 2019
 *     Read license file in main directory for more details
"""

import os
import time
import cv2 as cv

def task(onefile, pathin, pathout):


    filelist=[]
    filelist.append(onefile)

    #store the data&time info
    snapshot_time = filelist[0].partition('_')[2]
    time.sleep(10)


    for filename in filelist:
        # open the target jpeg 
        src = cv.imread(os.path.join(pathin, filename))
        src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

        # Histogram Equalization to improve the contrast of image
        #dst = cv.equalizeHist(src)

        # store the processed image
        cv.imwrite(os.path.join(pathout,'processed2_'+snapshot_time), src)


    return [os.path.join(pathout,'processed2_'+snapshot_time)]



def main():
    filelist= 'camera2_20190222.jpeg'
    outpath = os.path.join(os.path.dirname(__file__), "generated_files/")
    outfile = task(filelist, outpath, outpath)
    return outfile

if __name__ == '__main__':

    #Suppose the file structure is apac/detection_app/camera1_input/camera1_20190222.jpeg
    filelist= 'camera2_20190222.jpeg'
    task(filelist, '/home/erick/detection_app/camera2_input', '/home/erick/detection_app')


