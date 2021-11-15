import serial
import time

ser_printer = serial.Serial('/dev/ttyUSB0', 2560bytesize=8,
                            timeout=2, stopbits=serial.STOPBITS_ONE)
time.sleep(30)
buffer_bytes = ser_printer.inWaiting()
response = ser_printer.readlines()

print(response)
for r in response:
    print(str(r))
ser_printer.write(str.encode('M105\r\n'))
time.sleep(0.1)
response = ser_printer.readline()
print(response)

