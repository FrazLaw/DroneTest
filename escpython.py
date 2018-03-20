# This program is an updated version from the site: http://www.instructables.com/id/Driving-an-ESCBrushless-Motor-Using-Raspberry-Pi/
# All values are specific to the Turnigy 30A Multistar 2-6S ESC 

# This program will let you test your ESC and brushless motor.

# Make sure your battery is not connected if you are going to calibrate it at first.

# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
import keyboard #Using module keyboard
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library

ESC=4  #Connect the ESC in this GPIO pin 

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0) 

max_value = 2000 #Still to be assessed 
min_value = 1025  #This is the initial value the ESC must reach before it begins working
print "For first time launch, select calibrate, make sure the battery isn't connected"
print "Type the exact word for the function you want"
print "calibrate OR manual OR control OR arm OR stop"

def manual_drive(): #You will use this function to program your ESC if required
    print "You have selected manual option so give a value between 0 and you max value"    
    while True:
        inp = raw_input()
        if inp == "stop":
            stop()
            break
		elif inp == "control":
			control()
			break
		elif inp == "arm":
			arm()
			break	
        else:
            pi.set_servo_pulsewidth(ESC,inp)
                
def calibrate():   #This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = raw_input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, min_value)
            print "Wierd eh! Special tone"
            time.sleep(7)
            print "Wait for it ...."
            time.sleep (5)
            print "Im working on it, DONT WORRY JUST WAIT....."
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print "Arming ESC now..."
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print "See.... uhhhhh"
            control() # You can change this to any other function you want
            
def control(): 
    print "I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'"
    time.sleep(1)
    speed = 1100    # change your speed if you want to.... it should be between 700 - 2000
    print "Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed"
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = raw_input()
        
        if inp == "q":
            speed -= 100    # decrementing the speed like hell
            print "speed = %d" % speed
        elif inp == "e":    
            speed += 100    # incrementing the speed like hell
            print "speed = %d" % speed
        elif inp == "d":
            speed += 10     # incrementing the speed 
            print "speed = %d" % speed
        elif inp == "a":
            speed -= 10     # decrementing the speed
            print "speed = %d" % speed
        elif inp == "stop":
            stop()          #going for the stop function
            break
        elif inp == "manual":
            manual_drive()
            break
		elif inp == "arm":
			arm()
			break	
        else:
            print "WHAT DID I SAID!! Press a,q,d or e"

def startsequence():
	#automatic start sequence
	pi.set_servo_pulsewidth(ESC, min_value) #1025
	time.sleep(1)
	speed = 1010
	while True:
		pi.set_servo_pulsewidth(ESC, speed)
		sleep(1)
		print "ESC is ready for control"
		try: #used try so that if user pressed other than the given key error will not be shown
			if keyboard.is_pressed('q'):#if key 'up' is pressed
				speed += 10
				break#finishing the loop
			elif keyboard.is_prssed('a'):
				speed -= 10
			else:
				pass
		except:
			stop() #if user pressed other than the given key the loop will break
	
def arm(): #This is the arming procedure of an ESC 
    print "Connect the battery and press Enter"
    inp = raw_input()    
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        control() 
        
def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

	
#This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.    
#inp = raw_input()
#if inp == "manual":
#    manual_drive()
#elif inp == "calibrate":
#    calibrate()
#elif inp == "arm":
#    arm()
#elif inp == "control":
#    control()
#elif inp == "stop":
#    stop()
#else :
#    print "Error. Reached else clause, restart program."

