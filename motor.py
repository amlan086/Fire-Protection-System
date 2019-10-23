import curses
import serial
import struct
import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)


motor= serial.Serial('/dev/ttyUSB0',9600)
GPIO.setup(15, GPIO.IN)

############################

screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)



while True:
            
                
#global sonar
#sonar = GPIO.input(15)
        
        char = screen.getch()
        if char == ord('q'):
                motor.write(b'7')
                break
        elif char == curses.KEY_UP:
                print ("up")
                motor.write(b'3')
                
        elif char == curses.KEY_DOWN:
                print ("down")
                motor.write(b'4')
        elif char == curses.KEY_RIGHT:
                print ("right")
                motor.write(b'5')
        elif char == curses.KEY_LEFT:
                print ("left")
                motor.write(b'6')
                
        elif char == curses.KEY_HOME:
                 print("aaaa")       
                     

            #Close down curses properly, inc turn echo back on!









#############################
# let it initialize



# send the first int in binary format

#motor.write(b'3')
      
    
    
    
        
