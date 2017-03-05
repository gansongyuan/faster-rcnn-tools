import cv2
import os

#mouse event
CV_EVENT_MOUSEMOVE=0
CV_EVENT_LBUTTONDOWN=1
CV_EVENT_RBUTTONDOWN=2
CV_EVENT_MBUTTONDOWN=3
CV_EVENT_LBUTTONUP=4
CV_EVENT_RBUTTONUP=5
CV_EVENT_MBUTTONUP=6
CV_EVENT_LBUTTONDBLCLK=7
CV_EVENT_RBUTTONDBLCLK=8
CV_EVENT_MBUTTONDBLCLK=9

#workMode ---- click times
#0 ----  nothing
#1 ----  click once
#2 ----  click twice
workMode = 0
p1 = [0,0]
p2 = [0,0]

def OnMouse(event, x, y, flags, image):
    global workMode
    global p1
    global p2
    image_tmp = image.copy()
    if workMode == 0:
        if event == 1:
            #start paintting
            print 'start paintting'
            workMode += 1
            p1[0] = p2[0] = x
            p1[1] = p2[1] = y
            a = tuple(p1)
            b = tuple(p2)
            cv2.rectangle(image_tmp, a, b, (0, 255, 0), 2)
            cv2.imshow('input_image', image_tmp)
        elif event == 0:
            cv2.imshow('input_image', image_tmp)
    elif workMode == 1:
        if event == 0:
            #paintting
            p2[0] = x
            p2[1] = y
            a = tuple(p1)
            b = tuple(p2)
            cv2.rectangle(image_tmp, a, b, (0, 255, 0), 2)
            cv2.imshow('input_image', image_tmp)

            print 'paintting'
        elif event == 1:
            #stop paintting
            p2[0] = x
            p2[1] = y
            a = tuple(p1)
            b = tuple(p2)
            cv2.rectangle(image_tmp, a, b, (0, 255, 0), 2)
            cv2.imshow('input_image', image_tmp)

            print 'stop paintting'
            workMode += 1
        elif event == 2:
            #cancle paintting
            print 'cancle paintting'
            cv2.imshow('input_image', image_tmp)
            workMode -= 1

    elif workMode == 2:
        if event == 1:
            #save lable and load next image
            print 'save lable and load next image'
            workMode += 1
        elif event == 2:
            #cacle to last step
            print 'cancle to last step'
            workMode -= 1
    else:
        print '????should not be here'

cv2.namedWindow('input_image')
folder = '/home/gsy/robot1/image1/'
lable_filename = '/home/gsy/robot1/robot1.txt'

for i in range(10,100):
    workMode = 0
    filename = folder + str(i) + '.jpg'
    image = cv2.imread(filename)
    cv2.imshow('input_image', image)

    cv2.setMouseCallback('input_image',OnMouse, image)

    while workMode != 3:
        cv2.waitKey(10)
        pass

    lable_file = open(lable_filename, 'a+')
    lable_file.write(filename + ' ' + str(p1[0]) + ' ' + str(p1[1]) + ' ' + str(p2[0]) + ' ' + str(p2[1]) + '\n')
    lable_file.close()