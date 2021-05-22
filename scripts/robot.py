from os import setregid
import serial
import datetime
import time

def robotInit():
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.flush()
	time.sleep(10)
	#message = "Send position\n" 
	#ser.write(str.encode(message))
	#servo = [1, 2, 3, 4, 5] 
	#for i in range(0, 4):
	#	servo[i] = ser.readline().decode('utf-8').rstrip()
	#	print(servo[i])
	#message = "Greifen\n"
	#ser.write(str.encode(message))
	#read = ser.readline().decode('utf-8').rstrip()
	#print("Es wurde empfangen: ", read) 
	#message = "Greifen\n" 
	#test_as_bytes = str.encode(message)
	#ser.write(test_as_bytes)
	#line  = ser.readline().decode('utf-8').rstrip()
	#print(line + "\n")
	#time.sleep(5)
	return False, ser
	

def robotPickup(ser):
	message = "Send position\n" 
	ser.write(str.encode(message))
	servo = [1, 2, 3, 4, 5] 
	for i in range(0, 4):
		servo[i] = ser.readline().decode('utf-8').rstrip()
		print(servo[i])
	message = "Greifen\n" 
	ser.write(str.encode(message))
	finished = ser.readline().decode('utf-8').rstrip() #waiting for finished-message
	print(finished)
	message = "Drive to\n" 
	ser.write(str.encode(message))
	for i in range(0, 4):
		message = servo[i] + "\n"
		ser.write(str.encode(message))
		print("Gesendet: ", servo[i], "\n")
		print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
	current_time = datetime.datetime.today()
	return current_time

def robotMove(results, ser):
	# results[0]: True/False - Cup with hot water detected
	# results[1].x: 0-100 - x-Coordinates of the detected cup
	# results[1].y: 0-100 - y-Coordinates of the detected cup
	# results[2].x: 0-100 - x-Size of the detected cup
	# results[2].y: 0-100 - y-Size of the detected cup
	if results[2].x < 30 and results[2].y < 30:
		if results[1].x > 50:
			message = "Links" 
			ser.write(str.encode(message))
		elif results[1].x < 50:
			message = "Rechts" 
			ser.write(str.encode(message))
		else:
			message = "StopHor"
			ser.write(str.encode(message))
		if results[1].y > 50:
			message = "Hoch" 
			ser.write(str.encode(message))
		elif results[1].y < 50:
			message = "Runter" 
			ser.write(str.encode(message))
		else:
			message = "StopVer" 
			ser.write(str.encode(message))

def robotDispose(ser):
	print("Teebeutel wird entsorgt")

def robotDeinit(ser):
	message = "Base0" 
	ser.write(str.encode(message))
	message = "Greifer auf" 
	ser.write(str.encode(message))