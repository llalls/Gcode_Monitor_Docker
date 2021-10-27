import os
import csv
import cv2
import numpy as np
from threading import Lock
from PIL import Image

lock = Lock()
image_compare_list = []

def drawContour(img, contours):
    for c in contours:
        area = cv2.contourArea(c)
        if area > 5000:
            #opencv drawContour's color as rule of BGR
            cv2.drawContours(img, c, -1, (0, 0, 255), 3)
    return img


def load_gcode_image(pil_img):
    gcode_bgr_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    #cv2.imwrite('cameraImage2.jpg', gcode_bgr_img) # save image

    return gcode_bgr_img

def load_camera_image():
    camera_hsv_img = cv2.imread('cameraImage1.jpg')

    return camera_hsv_img


def imageThreshed(image):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([110, 50, 50]) # mask of blue(110, 50, 50) ~ (130, 255, 255)
    upper_blue = np.array([130, 255, 255])
    image_threshed = cv2.inRange(image_hsv, lower_blue, upper_blue)
    
    _, contours, hierarchy = cv2.findContours(image_threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = contours[0]
    return cnt


def image_compare(gcode_base64, rotate_time, position_x, position_y, position_z):

    gcode_bgr_img = load_gcode_image(gcode_base64)
    camera_hsv_img = load_camera_image()


    gcode_cnt = imageThreshed(gcode_bgr_img)
    camera_cnt = imageThreshed(camera_hsv_img)

    ret = cv2.matchShapes(gcode_cnt, camera_cnt, 1, 0.0)
    print("Similarity : " + str(ret))

    
    find_best_ret(rotate_time, position_x, position_y, position_z, ret)


def get_gcodeImage_filename(filename):
    gcodeImage_filename = filename
    print("GcodeImage_name_save : " + str(gcodeImage_filename))


def find_best_ret(rotate_time, position_x, position_y, position_z, ret):
    global image_compare_list
    buffer = [str(rotate_time), str(position_x), str(position_y), str(position_z), str(ret)]

    rotate_time = int(rotate_time)

    if(rotate_time < 1):
        image_compare_list.append(buffer)
    else:
        ret = float(ret)
        list_buffer = float(str(image_compare_list[0][4]))

        if(ret < list_buffer):
            image_compare_list.pop()
            image_compare_list.append(buffer)


def get_image_compare_list():
    global image_compare_list

    return image_compare_list

def clear_image_compare_list():
    global image_compare_list
    image_compare_list = []

    print('clear: ' + str(len(image_compare_list)))

def save_csv_file(filename, position_x, position_y, position_z, ret):
    csv_list = [str(filename), str(position_x), str(position_y), str(position_z), str(ret)]

    with open('image_compare_list.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_list)

    print('save csv success')

