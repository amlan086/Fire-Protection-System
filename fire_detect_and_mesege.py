import cv2
import numpy as np
import imutils
from twilio.rest import Client

video = cv2.VideoCapture("E:/workspace/iee/dataset_vedio/fire2.mp4")

flag=False

account_sid = 'ACed7c7773770c9ae93a1008e943df1fd2'
auth_token = '1be653b7f167ea204092adf659efecc8'
client = Client(account_sid, auth_token)

while True:
    (flag, frame) = video.read()
    cv2.namedWindow('real',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('real', 500,500)
    cv2.imshow('real',frame)
    if not flag:
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
    cv2.imshow("nMask", mask)
 
# loop over the contours
    for c in cnts:
	# draw the contour and show it
        cv2.drawContours(mask, [c], -1, (0, 255, 0), 2)
        cv2.imshow("Image", mask)
    
    
 
 
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)
    cv2.namedWindow('output',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('output', 500,500)
    cv2.imshow("output", output)
   
    if int(no_red) > 20000:
        print ('Fire detected')
        if flag==True:
            message = client.messages \
                .create(
                     body="fire detected.......",
                     from_='+13344599682',
                     to='+8801517038460'
                 )

            print(message.sid)
            flag= False
        
    if(cv2.waitKey(1) == ord('q')):
        break
 
cv2.destroyAllWindows()
video.release()
