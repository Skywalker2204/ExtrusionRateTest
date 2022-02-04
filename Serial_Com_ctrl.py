#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 08:33:47 2021

@author: lukashentschel
"""

import serial.tools.list_ports as ports
import serial
import time

try:
    import tkinter as tk
except:
    import Tkinter as tk

from random import uniform

DEBUG =False

class SerialCtrl():
    def __init__(self):
        self.com_list=[]
        self.connected = False
        self.startCode = b"M155 S1\r\n"
        
    def getCOMList(self):
        self.com_list=[i.device for i in list(ports.comports())]
        self.com_list.insert(0, "-")
        
        return self.com_list
    
    def SerialOpen(self, clicked_com, clicked_bd):

        try:
            self.ser.is_open
        except:
            PORT = clicked_com.get()
            BAUD = clicked_bd.get()
            self.ser = serial.Serial()
            self.ser.baudrate = BAUD
            self.ser.port = PORT
            self.ser.timeout = 0.1
        
        try:
            if self.ser.is_open:
                self.ser.status = True
            else:
                PORT = clicked_com.get()
                BAUD = clicked_bd.get()
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
        
    def startPrinterStream(self):
        try:
            self.ser.write(self.startCode)
            time.sleep(0.2)
            if self.checkSerialPort().startswith('ok'):
                self.connected=True
                print('Tempearture Stream started')
        except Exception as e:
            print("Starting issues: "+e)
            self.connected = False
            
        
    def SerialSyncPrinter(self, gui):
        self.threading = True
        while self.threading:
            try:
                gui.data.RowMsg = self.checkSerialPort()
                msg = gui.data.DecodeMsg(time.time()-gui.root.startTime)
                if not self.connected: self.startStream() 
                    
                gui.conn.label_isttemp["text"]=gui.data.dataDict.get('temperature')[-1][1]
                gui.conn.updateConnGUI(msg)
                
                if self.threading == False:
                    break
            except Exception as e:
                print(e)
            
            if self.threading == False:
                break
            time.sleep(0.5)
            
            
    def SerialSyncScale(self, gui):
        self.threading = True
        self.init_scale()
        while self.threading:
            try:
                gui.data.RowMsgScale = self.checkSerialPort()
                msg = gui.data.DecodeMsgScale(time.time()-gui.root.startTime)
                    
                gui.conn.updateConnGUI(msg)
                
                if self.threading == False:
                    break
            except Exception as e:
                print(e)
            
            gui.dis.updateChart()
            if self.threading == False:
                break
            time.sleep(0.5)
        
    
    def init_scale(self):
        self.serial.ser.wirte('t')
        load = self.popupmsg('Enter the loaded weigth', 'Scale Calibration')
        self.serial.ser.write(load)
        
        
    def popupmsg(self, msg, title):
        root = tk.Tk()
        root.title(title)
        load = tk.StringVar()
        
        label = tk.Label(root, text=msg)
        entry = tk.Entry(root, textvariable=load, bd=1, width= 5)
        B1 = tk.Button(root, text="Okay", command = root.destroy)
        
        label.pack(side="top", fill="x", pady=10)
        entry.pack()
        B1.pack()
        
        root.mainloop()
        return load.get()
        
        
        
    def EmulateSerialSync(self, gui):
        self.threading = True
        print(self.popupmsg('Enter the loaded weigth', 'Scale Calibration'))
        while self.threading:
            try:
                gui.data.dataDict['temperature'].append(
                    [time.time()-gui.root.startTime, uniform(150, 200)])
                gui.data.dataDict['force'].append(
                    [time.time()-gui.root.startTime, uniform(5, 15)])
                msg = 'just a simulation'
                    
                gui.conn.label_isttemp["text"]=int(gui.data.dataDict.get(
                    'temperature')[-1][1])
                gui.conn.updateConnGUI(msg)
                

                if self.threading == False:
                    break
            except Exception as e:
                print(e)
            
            gui.dis.updateChart()
            if self.threading == False:
                break
            time.sleep(0.5)
            print(gui.data.dataDict.get('temperature')[-1][0])
            
                   
        
if __name__ == '__main__':
    S = SerialCtrl()
