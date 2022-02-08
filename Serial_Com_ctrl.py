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

DEBUG =True

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

        self.popupmsg('Scale Calibration', self)

        
        
    def popupmsg(self, title, serial):
        class popup():
            def __init__(self, title, serial, wait=1000):
                self.root = tk.Tk()
                self.serial=serial
                
                self._init_window(title)
                self._numLog=0
                
                
            def _init_window(self, title):
                self.root.title(title)
                self.dataCanvas = tk.Canvas(self.root, width = 600,
                                            heigh=120, bg='white')
                self.vsb = tk.Scrollbar(self.root, orient='vertical', 
                                command=self.dataCanvas.yview)
                self.dataCanvas.config(yscrollcommand=self.vsb.set)
        
                self.dataFrame=tk.Frame(self.dataCanvas, bg='white')
                self.dataCanvas.create_window((10,0), window=self.dataFrame,
                                      anchor='nw')
        
                self.entry = tk.Entry(self.root, bd=1, width= 50)
                self.B1 = tk.Button(self.root, text="Send", 
                                    command = self.send_command)
                self.B2 = tk.Button(self.root, text="Update Log", 
                                    command = self.updateLog)
        
                self.entry.grid(row=0, column=0)
                self.B1.grid(row=0, column=1)
                self.B2.grid(row=0, column=2, columnspan = 2)
                self.dataCanvas.grid(row=1, column=0, columnspan=3)
                self.vsb.grid(row = 1, column=3)

            def send_command(self):
                entry = self.entry.get()
                
                print(entry)
                if entry != '':
                    self.writeLog('Send: ' + entry)
                    if not DEBUG:
                        self.serial.ser.write(bytes(entry, 'utf-8'))
                else:
                    self.writeLog('Unkown command: ' + entry)
                self.entry.delete(0,tk.END)
                
            def writeLog(self,msg):
                text = str(self._numLog)
                tk.Label(self.dataFrame, text=text+msg, bg='white').pack()
                self._numLog +=1
                
            def updateLog(self, wait=100):
                if DEBUG:
                    msg = 'this is a simulation!'
                    if self._numLog > 100:
                        msg='End calibration:'
                else:
                    msg = self.checkSerialPort()
                    
                self.writeLog(msg)
                
                self.root.after(wait, self.updateLog)
                
                reg =self.dataCanvas.bbox('all')
                self.dataCanvas.config(scrollregion=reg)
                self.dataCanvas.yview(tk.MOVETO, 1)
                
                if msg.find("End calibration") != -1:
                    self.root.destroy()

        popup=popup(title, serial)
        popup.root.after(100, popup.updateLog)
        popup.root.mainloop()
   
        
    def EmulateSerialSync(self, gui):
        
        self.popupmsg('Scale Calibration', self)
        self.threading = True
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
