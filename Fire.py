import os
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)
import cv2
import numpy as np
import imutils
from twilio.rest import Client

import time

video = cv2.VideoCapture("fire2.mp4")

flag=True

account_sid = 'AC4f074c7a17a9cadb518a1470dc9ed3e1'
auth_token = '1cc7afd9d30cca04b196c0754550f94e'
client = Client(account_sid, auth_token)

while True:
    (result, frame) = video.read()
     
   
    
   
    #cv2.ShowImage('real',window)
   
    if not result:
        break
 
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
 
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
 #....................
 
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    print("I found {} black shapes".format(len(cnts)))
    #cv2.imshow("nMask", mask)
 
# loop over the contours
    for c in cnts:
	# draw the contour and show it
        cv2.drawContours(mask, [c], -1, (0, 255, 0), 2)
        #cv2.imshow("Image", mask)
    
    
 
 
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)
    
    #cv2.imshow("output", output)
   
    if int(no_red) > 20000:
        print ('Fire detected')
        if flag==True:
            flag= False
            message = client.messages \
                .create(
                     body="fire detected.......",
                     from_='+14025528616',
                     to='+8801630830400'
                 )

            print(message.sid)
            
        
    #if(cv2.waitKey(1) == ord('q')):
     #   break
 
cv2.destroyAllWindows()
video.release()
