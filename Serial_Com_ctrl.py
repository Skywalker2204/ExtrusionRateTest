#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 08:33:47 2021

@author: lukashentschel
"""

import serial.tools.list_ports as ports
import serial

DEBUG =True

class SerialCtrl():
    def __init__(self):
        self.com_list=[]
        
    def getCOMList(self):
        self.com_list=[i.device for i in list(ports.comports())]
        self.com_list.insert(0, "-")
        
        return self.com_list
    
    def SerialOpen(self, gui):

        try:
            self.ser.is_open
        except:
            PORT = gui.clicked_com.get()
            BAUD = gui.clicked_bd.get()
            self.ser = serial.Serial()
            self.ser.baudrate = BAUD
            self.ser.port = PORT
            self.ser.timeout = 1
        
        try:
            if self.ser.is_open:
                self.ser.status = True
            else:
                PORT = gui.clicked_com.get()
                BAUD = gui.clicked_bd.get()
                self.ser = serial.Serial()
                self.ser.baudrate = BAUD
                self.ser.port = PORT
                self.ser.timeout = 0.1
                self.ser.open()
                self.ser.status = True
        except:
            self.ser.status = False

            
    def SerialClose(self):
        
        try:
            self.ser.is_open
            self.ser.close()
            self.ser.status = False
        except:
            self.ser.status = False
 
            
        
if __name__ == '__main__':
    S = SerialCtrl()
