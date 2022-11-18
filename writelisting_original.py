import pyautogui
import csv

import time
import mss
import cv2
import numpy as np

bbox=[177,2939,700,400]
mouse_w=[2817,291]
mouse_p=[3704,808]

lines=[]
with open('listing.txt', 'r') as csvfile:
    lines = csvfile.readlines()

with mss.mss() as sct:
       
        for i in range(0,len(lines)-45):

            monitor = {"top": bbox[0], "left": bbox[1], "width": bbox[2], "height": bbox[3]}

            
            pyautogui.click(x=mouse_w[0] , y=mouse_w[1])
            time.sleep(2)
            pyautogui.typewrite(lines[i])
            #pyautogui.click(x=mouse_p[0] , y=mouse_p[1])
            pyautogui.press('enter')

            sct_img = sct.grab(monitor)
            img=np.array(sct_img)        
            hsv=cv2.cvtColor(img, cv2.cv2.COLOR_BGR2HSV)
            dst = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
            no_green = cv2.countNonZero(dst)

            print('The number of green pixels is: ' + str(no_green))
            if no_green>10:
                print (lines[i])
                output = "GD{}_".format(str(lines[i]))+"sct-{top}x{left}_{width}x{height}.png".format(**monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
                #pyautogui.click(x=mouse[0] , y=mouse[1])
            else:
                None
                #pyautogui.click(x=mouse[0] , y=mouse[1])
            
            time.sleep(2)
            pyautogui.click(clicks=2)    
            pyautogui.press('delete')


