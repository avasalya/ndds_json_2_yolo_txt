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


def convert(box, img):
    
    # https://stackoverflow.com/questions/56115874/how-to-convert-bounding-box-x1-y1-x2-y2-to-yolo-style-x-y-w-h

    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]

    dw = 1/img.shape[0]
    dh = 1/img.shape[1]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    
    return (x, y, w, h)


def draw_box(x, y, w, h, img):

    dw = img.shape[0]
    dh = img.shape[1]
    w_ = int(w*dw)
    h_ = int(h*dh)
    x_ = int(x*dw)
    y_ = int(y*dh)

    # remember yolo (x,y) is at center of the box 
    x_ = int(x_- w_/2)
    y_ = int(y_- h_/2)
    w_ = x_ + w_
    h_ = y_ + h_

    print("image space yolo_bbox (x, y, w, h)", x_, y_, w_, h_)

    img = cv.rectangle(img, (x_, y_), (w_, h_), (255, 0, 255), 2)

    cv.imshow('yolo bbox', img)



def ndds2yolo(jsonfile, outputfile, img):

    with open(str(jsonfile)) as attributes:
        data = json.load(attributes)

    # erase old bbox files
    open(outputfile, 'w').close()

    # extract bounding box
    for obj in range(len(data["objects"])):
        
        print("detected object id", obj, "& class", data["objects"][obj]["class"])    
        for item in data["objects"][obj]:
            
            if item == "bounding_box":
                
                # print(item, ":", data["objects"][obj][item])
                
                # ndds coordinates format is (Y, X) instead of (X, Y)
                x1 = float(data["objects"][obj][item]["top_left"][1])
                y1 = float(data["objects"][obj][item]["top_left"][0])
        
                x2 = float(data["objects"][obj][item]["bottom_right"][1])
                y2 = float(data["objects"][obj][item]["bottom_right"][0])

                xmin = min(x1, x2)
                xmax = max(x1, x2)
                ymin = min(y1, y2)
                ymax = max(y1, y2)

                xy = (xmin, xmax, ymin, ymax)
                print("ndds_bbox", xy)
        
                # convert ndds to yolo format
                x, y, w, h = convert(xy, img)
                bbox = (obj, x, y, w, h)
                print("normalized yolo_bbox (x, y, w, h)", x, y, w, h)

                # write yolo bbox to txt format
                with open(outputfile, 'a') as f:
                    f.write('{} {} {} {} {}'.format(bbox[0], bbox[1], bbox[2], bbox[3], bbox[4]))
                    f.write("\n")

                # visualize bbox  (YOLO normalizes image space to fit between [0, 1])      
                draw_box(x, y, w, h, img)

    return (x, y, w, h)





if __name__ == "__main__":
    
    startTime = time.time()
    
    # path to dir
    path = os.path.dirname(__file__)
    path = path + '/../../../Unreal Projects/Dataset_Synthesizer/Source/NVCapturedData/banjuDRNewMap/'
    
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
        outputfile = path + "bboxtxt/" + fileName + ".txt"
        
        # convert to yolo format
        ndds2yolo(jsonfile, outputfile, image)
        
        # comment this if you don't want to visualize yolo bbox
        cv.waitKey(50)
        
    finishedTime = time.time()
    print('\nfinished in', round(finishedTime-startTime, 2), 'second(s)')


    """ use only when required """
    # separate files into respective folders and move color images to same folder as bbox
    # shutil.move((path + fileName + ".png"), path + "bboxtxt")
    # shutil.move((path + fileName + ".cs" +".png"), path + "cs")
    # shutil.move((path + fileName + ".is" +".png"), path + "is")
    # shutil.move((path + fileName + ".depth" +".png"), path + "depth")
    # shutil.move((path + fileName + ".depth.16" +".png"), path + "depth16")
    # shutil.move((path + fileName + ".depth.cm.8" +".png"), path + "depthcm8")
    # shutil.move((path + fileName + ".depth.cm.16" +".png"), path + "depthcm16")
    # shutil.move((path + fileName + ".depth.mm.16" +".png"), path + "depthmm16")