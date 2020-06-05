""" convert ndds JSON bbox to yolo bbox txt format """

import os
import sys
import time
import json
import getpass
import cv2 as cv
import numpy as np

username = getpass.getuser()
osName = os.name
if osName == 'posix':
    os.system('clear')
else:
    os.system('cls')

""" source: https://stackoverflow.com/questions/56115874/how-to-convert-bounding-box-x1-y1-x2-y2-to-yolo-style-x-y-w-h """
def convert(size, box):
    # box(x1, x2, y1, y2)
    
    """ method1 """
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    # x = x*dw
    # w = w*dw
    # y = y*dh
    # h = h*dh
    
    """ method2 """
    # w = box[1] - box[0]
    # h = box[3] - box[2]
    # x = (box[0] + (w/2))
    # y = (box[2] + (h/2))
    
    return (x,y,w,h)


""" Ashesh Vasalya v.1 """
def ndds2yolo(fileName, camera_setting, outputfile, img):

    with open(str(fileName)) as attributes:
        data = json.load(attributes)

    with open(str(camera_setting)) as settings:
        camData = json.load(settings)

    for object in range(len(data["objects"])):
        
        print("detected object", object, data["objects"][object]["class"])
        for item in data["objects"][object]:
            
            if item == "bounding_box":
                
                # print(item, ":", data["objects"][object][item])
                
                # read bounding box coordinates
                # ndds coordinate format is (Y, X) instead of (X, Y)
                x1 = float(data["objects"][object][item]["top_left"][1])
                y1 = float(data["objects"][object][item]["top_left"][0])
        
                x2 = float(data["objects"][object][item]["bottom_right"][1])
                y2 = float(data["objects"][object][item]["bottom_right"][0])

                xmin = min(x1, x2)
                xmax = max(x1, x2)
                ymin = min(y1, y2)
                ymax = max(y1, y2)

                xy = (xmin, xmax, ymin, ymax)
                # print("ndds_bbox", xy)
                
                # image size
                w = camData["camera_settings"][0]["captured_image_size"]["width"]                
                h = camData["camera_settings"][0]["captured_image_size"]["height"]                
                
                # convert ndds to yolo format
                x, y, w, h = convert((w, h), xy)
                # print("yolo_bbox", x, y, w, h)

                # visualize bbox remember yolo (x,y) is at center of the box               
                img = cv.rectangle(img, ( int(x-w/2), int(y-h/2) ), ( int((x+w/2)) , int((y+h/2)) ), (255, 0, 255), 2)
                cv.imshow('yolo bbox', img)

                # write yolo bbox to txt format
                bbox = (x, y, w, h)
                with open(outputfile, 'a') as f:
                    for item in bbox:
                        f.write("%f\n" % item)

                
    return (x, y, w, h)





if __name__ == "__main__":
    
    startTime = time.time()
    
    # path to dir
    path = os.path.dirname(__file__)
    path = path + '/../../../Unreal Projects/Dataset_Synthesizer/Source/NVCapturedData/banjuDRNewMap/'
    yolobboxTxt = path + "yolobbox" + ".txt"

    #remove old file
    if os.path.exists(yolobboxTxt):
        print("deleting old file")
        os.remove(yolobboxTxt)
    else:
        pass

    # MAIN loop
    for i in range(99):
        
        if i<10:
            file = "00000" + str(i)
        else:
            file = "0000" + str(i)
                
        json_file = path + file + ".json"
        camera_file = path + "_camera_settings.json"

        # read image
        color = cv.imread(path + file + ".png")
        
        # convert to yolo format
        ndds2yolo(json_file, camera_file, yolobboxTxt, color)
        
        # comment this if you don't want to display yolo bbox
        cv.waitKey(50)
        
    finishedTime = time.time()
    print('\nfinished in', round(finishedTime-startTime, 2), 'second(s)')
    