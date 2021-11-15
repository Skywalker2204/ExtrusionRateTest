#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 08:33:47 2021

@author: lukashentschel
"""

import serial.tools.list_ports as ports
import serial
import time

DEBUG =False

class SerialCtrl():
    def __init__(self):
        self.com_list=[]
        self.connected = False
        
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
            self.ser.timeout = 0.1
        
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
            
    def checkSerialPort(self):
        try:
            if self.ser.isOpen() and self.ser.inWaiting():
                recentPacket=self.ser.readline()
            else:
                recentPacket=''
            return recentPacket.decode('utf-8').rstrip('\n') 
        except:
            pass
        
    def startStream(self, code):
        while not self.connected:
            try:
                self.ser.write(code)
                time.sleep(1)
                if self.checkSerialPort().startswith('ok'):
                    self.connected = True
            except Exception as e:
                print("Starting issues: "+e)
                
        
    def SerialSync(self, gui):
        self.threading = True
        gui.data.initScale()
        while self.threading:
            try:
                gui.data.RowMsg = self.checkSerialPort()
                msg = gui.data.DecodeMsg()
                gui.conn.label_isttemp["text"]=gui.data.dataDict.get('temperature')[-1]
                gui.conn.updateConnGUI(msg)
                
                gui.data.runScale()
                if self.threading == False:
                    break
            except Exception as e:
                print(e)

            if self.threading == False:
                break
            time.sleep(0.5)
            
                   
        
if __name__ == '__main__':
    S = SerialCtrl()
