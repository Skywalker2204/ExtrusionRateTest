
import sys
import glob
import serial.tools.list_ports as ports

import time

def get_serial_ports():
        com_ports=list(ports.comports())
        return com_ports

def sendGcode(code, ser):
    for line in code.split('\n'):
        ser.write(line)
        time.sleep(1)
        
if __name__ == '__main__':
    for i in get_serial_ports():
        print(i.device)
        
            