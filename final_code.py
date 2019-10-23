import socket
import curses
import serial
import struct
import time
import RPi.GPIO as GPIO
import cv2
import numpy as np
import imutils
from twilio.rest import Client



GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)

motor= serial.Serial('/dev/ttyUSB0',9600)
GPIO.setup(15, GPIO.OUT) # fire output to servo..........
GPIO.setup(40,GPIO.IN) #sonar input......
GPIO.setup(37,GPIO.IN) 
GPIO.setup(38,GPIO.IN)


host = ''
port = 5574

storedValue = ""

# sending messege..........
account_sid = 'AC4f074c7a17a9cadb518a1470dc9ed3e1'
auth_token = '1cc7afd9d30cca04b196c0754550f94e'
client = Client(account_sid, auth_token)



def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind comlete.")
    return s

def setupConnection():
    s.listen(2) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def UP():
    motor.write(b'3')
    return 'up'
    

def DOWN():
    motor.write(b'4')
    return 'down'

def LEFT():
    motor.write(b'6')
    return 'left'

def RIGHT():
    motor.write(b'5')
    return 'right'

def PUMP_on():
    motor.write(b'8')
    return 'pump_on'

def PUMP_off():
    motor.write(b'9')
    return 'pump off'
def CLEFT():
    return 'cam left'

def CRIGHT():
    return 'cam right'

def dataTransfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        #(result, frame) = video.read()
        #if not result :
            #v=fire_detection_messege(frame) 
        
        data = conn.recv(1024) # receive the data
        data = data.decode('utf-8')
        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        print(command)
        if command == 'w':
            reply = UP()
        elif command == 's':
            reply = DOWN()
        elif command == 'a':
            reply = LEFT()
        elif command == 'd':
            reply = RIGHT()
        elif command == 'p':
            reply = PUMP_on()
        elif command == 'o':
            reply = PUMP_off()
        elif command == 'e':
            reply = CLEFT()
        elif command == 'r':
            reply = CRIGHT()
        elif command == 'q':
            print("Our server is shutting down.")
            s.close()
            break
        else:
            reply = 'Unknown Command'
        # Send the reply back to the client
        print(reply)
        conn.sendall(str.encode(reply))
        print("Data has been sent!")
    conn.close()



#fire detection code...........


def fire_detection_messege(frame) :
    global flag
    while True:
        (result, frame) = video.read()
        #cv2.namedWindow('real',cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('real', 500,500)
        #cv2.imshow('real',frame)
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
            GPIO.output(15,GPIO.HIGH)
##            if flag==True:
##                flag= False
##                message = client.messages \
##                    .create(
##                         body="fire detected.location : eee building,kuet",
##                         from_='+14025528616',
##                         to='+8801630830400'
##                     )
##
##                print(message.sid)
                
##                   return 1
        else:
            GPIO.output(15,GPIO.LOW)
             
    


def sonarwork(sonar) :
    sonar1 = GPIO.input(40)
    if(sonar==0) :
       motor.write(b'3')
       time.sleep(1)
       if(sonar1==0) :
           motor.write(b'3')
           time.sleep(1)
           motor.write(b'5')
           time.sleep(1)
           
       
    if(sonar==1) :
        motor.write(b'7')
        time.sleep(2)
        motor.write(b'4')
        time.sleep(2)
        
        random_number = randint(0, 2)
        print(random_number)
        if random_number ==0 :
            motor.write(b'5')
            time.sleep(2)
            motor.write(b'3')
            time.sleep(2)
            motor.write(b'6')
            time.sleep(2)
            if(sonar1==1 ) :
                sonarwork(sonar1)
            
            
        else :
            motor.write(b'6')
            time.sleep(2)
            motor.write(b'3')
            time.sleep(2)
            motor.write(b'5')
            time.sleep(2)
            if(sonar1==1) :
                sonarwork(sonar1)
    



video = cv2.VideoCapture(0)

while True:
    chk= (input("enter c for controller, m for autonomous\n"))
    if( chk == 'c') :
        try:
            s = setupServer()
            conn=setupConnection()
            dataTransfer(conn)
        except:
            break
    if (chk=='m') :
        try:

            
            while True:
                
                #(result, frame) = video.read()
                #cv2.namedWindow('real',cv2.WINDOW_NORMAL)
                #cv2.resizeWindow('real', 500,500)
                #cv2.imshow('real',frame)
                #if not result:
                 #   break
                print('aaa')
                #v=fire_detection_messege(frame) 
                sonar = GPIO.input(40)
                print(sonar)
                sonarwork(sonar)
                time.sleep(2)
                input1 = GPIO.input(37)
                input2 = GPIO.input(38)
                
                if(input1==1 and input2==1) :
                    motor.write(b'6')
                elif (input1==0 and input2==1) :
                    motor.write(b,'5')
                elif(input1==1 and input2==0) :
                    motor.write(3)
                print("aaa")
                continue 
        except:
            break
     

