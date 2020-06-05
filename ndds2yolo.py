""" convert ndds JSON bbox to yolo bbox txt format """

import os
import sys
import time
import json
import shutil
import getpass
import cv2 as cv
import numpy as np

username = getpass.getuser()
osName = os.name
if osName == 'posix':
    os.system('clear')
else:
    os.system('cls')

def convert(box):
    
    """ method1 """
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    
    """ method2 """
    # w = box[1] - box[0]
    # h = box[3] - box[2]
    # x = (box[0] + (w/2))
    # y = (box[2] + (h/2))
    
    return (x,y,w,h)


def ndds2yolo(jsonfile, outputfile, img):

    with open(str(jsonfile)) as attributes:
        data = json.load(attributes)

    # erase old bbox files
    open(outputfile, 'w').close()
    for obj in range(len(data["objects"])):
        
        print("detected object id", obj, "& class", data["objects"][obj]["class"])    
        for item in data["objects"][obj]:
            
            if item == "bounding_box":
                
                # print(item, ":", data["objects"][obj][item])
                
                # ndds coordinate format is (Y, X) instead of (X, Y)
                x1 = float(data["objects"][obj][item]["top_left"][1])
                y1 = float(data["objects"][obj][item]["top_left"][0])
        
                x2 = float(data["objects"][obj][item]["bottom_right"][1])
                y2 = float(data["objects"][obj][item]["bottom_right"][0])

                xmin = min(x1, x2)
                xmax = max(x1, x2)
                ymin = min(y1, y2)
                ymax = max(y1, y2)

                xy = (xmin, xmax, ymin, ymax)
                # print("ndds_bbox", xy)
        
                # convert ndds to yolo format
                x, y, w, h = convert(xy)
                bbox = (obj, x, y, w, h)

                # write yolo bbox to txt format
                with open(outputfile, 'a') as f:
                    f.write('{} {} {} {} {}'.format(bbox[0], bbox[1], bbox[2], bbox[3], bbox[4]))
                    f.write("\n")

                # remember yolo (x,y) is at center of the box 
                x = round(x - w/2)
                y = round(y - h/2)
                w = round(x + w)
                h = round(y + h)
                print("yolo_bbox (x, y, w, h)", x, y, w, h)

                # visualize bbox              
                img = cv.rectangle(img, (x, y), (w , h), (255, 0, 255), 2)
                cv.imshow('yolo bbox', img)

    return (x, y, w, h)





if __name__ == "__main__":
    
    startTime = time.time()
    
    # path to dir
    path = os.path.dirname(__file__)
    path = path + '/../../../Unreal Projects/Dataset_Synthesizer/Source/NVCapturedData/banjuDRNewMap/'
    saveFolder = path + "names"
    

    # MAIN loop
    for i in range(99):
        
        if i<10:
            fileName = "00000" + str(i)
        else:
            fileName = "0000" + str(i)

        # read image
        image = cv.imread(path + fileName + ".png")

        # paths
        jsonfile = path + fileName + ".json"
        outputfile = path + "names/" + fileName + ".txt"
        
        # convert to yolo format
        ndds2yolo(jsonfile, outputfile, image)
        
        # comment this if you don't want to display yolo bbox
        cv.waitKey(50)
        
        # move color images to same folder as bbox
        shutil.move((path + fileName + ".png"), saveFolder)
        
    finishedTime = time.time()
    print('\nfinished in', round(finishedTime-startTime, 2), 'second(s)')