from os import setregid
import serial
import datetime
import time

# results[0]: True/False - Cup with hot water detected
# results[1].x: 0-100 - x-Coordinates of the detected cup
# results[1].y: 0-100 - y-Coordinates of the detected cup
# results[2].x: 0-100 - x-Size of the detected cup
# results[2].y: 0-100 - y-Size of the detected cup

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
	message = "Greifer auf\n" 
	ser.write(str.encode(message))
	message = "Wachposition\n" 
	ser.write(str.encode(message))
	#servo = [30, 90, 90, 110, 80]
	#message = "Drive to\n" 
	#ser.write(str.encode(message))
	#print("Catch 1: ", ser.readline().decode('utf-8').rstrip(),"\n")
	#print("Catch 2: ", ser.readline().decode('utf-8').rstrip(),"\n")
	#for i in range(0, len(servo)):
	#	message = str(servo[i]) + "\n"
	#	print("Gesendet: ", message)
	#	ser.write(str.encode(message))
	#	print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
	time.sleep(2)
	return False, ser

def robotPickup(ser):
	servo = [1, 2, 3, 4, 5] 
	message = "Send position\n" 
	ser.write(str.encode(message))
	received = ser.readline().decode('utf-8').rstrip()
	if received != "Send position wurde erkannt.":
		correct = False
		while correct != True:
			received = ser.readline().decode('utf-8').rstrip()
			print("Vielleicht falsch: ", received)
			if received != "Send position wurde erkannt.":
				correct = True
	print(received)

	for i in range(0, len(servo)):
		servo[i] = ser.readline().decode('utf-8').rstrip()
		print("Ausgangspositionen: ", servo[i])

	message = "Greifen\n" 
	ser.write(str.encode(message))
	finished = ser.readline().decode('utf-8').rstrip() #waiting for finished-message
	if finished != "Roboter ist fertig":
		correct = False
		while correct != True:
			received = ser.readline().decode('utf-8').rstrip()
			print("Vielleicht falsch: ", received)
			if received != "Roboter ist fertig":
				correct = True
	print(finished)

	message = "Drive to\n"
	ser.write(str.encode(message))
	received = ser.readline().decode('utf-8').rstrip()
	if message != "Drive to wurde erkannt. Es wird die Position angefahren.":
		correct = False
		while correct != True:
			received = ser.readline().decode('utf-8').rstrip()
			print("Vielleicht falsch: ", received)
			if received != "Drive to wurde erkannt. Es wird die Position angefahren.":
				correct = True
	print(message)
	
	for i in range(0, len(servo)):
		message = servo[i] + "\n"
		ser.write(str.encode(message))
		print("Gesendet: ", servo[i], "\n")
		print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
	current_time = datetime.datetime.today()
	return current_time

def robotMove(results, ser):
	print("Sollte sich bewegen")
	if results[2].x < 70 and results[2].y < 70:
		if results[1].x < 20:
			message = "StarkLinks\n" 
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
		elif results[1].x < 25:
			message = "Links\n" 
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
		elif results[1].x < 30:
			message = "LeichtLinks\n" 
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
		elif results[1].x > 60:
			message = "StarkRechts\n" 
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
		elif results[1].x > 40:
			message = "Rechts\n" 
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
		elif results[1].x > 35:
			message = "LeichtRechts\n" 
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
		else:
			message = "StopHor\n"
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
		if results[1].y > 50:
			message = "Hoch\n" 
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
		elif results[1].y < 50:
			message = "Runter\n" 
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
		else:
			message = "StopVer\n" 
			print("Gesendet: ", message)
			ser.write(str.encode(message))
			print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")

def robotDispose(ser):
	message = "Teebeutel weg\n" 
	print("Gesendet: ", message)
	ser.write(str.encode(message))
	print("Empfangen: ", ser.readline().decode('utf-8').rstrip(),"\n")
	current_time = datetime.datetime.today()
	return current_time

def robotDeinit(ser):
	message = "Base 0\n" 
	ser.write(str.encode(message))
	message = "Greifer auf\n" 
	ser.write(str.encode(message))