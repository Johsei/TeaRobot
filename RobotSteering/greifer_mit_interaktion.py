#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
  ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
  ser.flush()
  while True:
    test = input ("Eingabe bitte: ")
    print("Eingabe war: ", test)
    test2 = test + "\n"
    #print(test2)
    test_as_bytes = str.encode(test2)
    ser.write(test_as_bytes)
    line  = ser.readline().decode('utf-8').rstrip()
    print(line + "\n")
