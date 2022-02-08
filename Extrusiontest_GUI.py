
import sys
import glob

import threading
import time
try:
    import tkinter as tk
except:
    import Tkinter as tk
    
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np

DEBUG = True

class RootGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Printer Communication")
        self.root.geometry("1025x850")
        self.root.config(bg="white")
        
        
class ComGUI():
    def __init__(self,root,serial, serial2, data):
        self.root = root
        self.serial = serial
        self.serial2 = serial2 #for the secound serial port from the printer
        self.data = data
        
        self._init_Frame()
        
        self.conn = ConnGUI(self.root, self.serial, self.serial2, self.data)
        time.sleep(2)
        self.dis = DisGUI(self.root, self.serial, self.data)
        
    def _init_Frame(self):
        
        #for the printer communication
        self.frame = tk.LabelFrame(self.root, text="COM Manager", padx=5, pady=5, 
                                 bg="white")
        self.label_printer= tk.Label(self.frame, text="Printer COM",bg="white",
                                 width=15, anchor="w")
        self.label_com = tk.Label(self.frame, 
                               text="Avaliable Ports:", bg="white", width=15, 
                               anchor="w")
        self.label_bd = tk.Label(self.frame, 
                               text="Baude Rate:", bg="white", width=15, 
                               anchor="w")
        self.clicked_com, self.drop_com = self.ComOptions(self.serial)
        self.clicked_bd, self.drop_baud = self.BaudOptions()
        
        #For the scale communiciaton 
        self.label_scale = tk.Label(self.frame, text="Scale COM",bg="white",
                                 width=15, anchor="w")
        self.clicked_scale_com, self.drop_scale_com = self.ComOptions(
            self.serial2)
        self.clicked_scale_bd, self.drop_scale_baud = self.BaudOptions(
            default=6)
        
        self.bnt_refresh = tk.Button(self.frame, text="Refresh", width=10, 
                                     command=self.com_refresh)
        self.bnt_connect = tk.Button(self.frame, text="Connect", 
                                     width=10, state="disable", 
                                     command=self.serial_connect) 
        self.publish()
        
    def ComOptions(self, serial, clicked=False):
        com_ports=self.serial.getCOMList()
        if not clicked: clicked=tk.StringVar()
        clicked.set(com_ports[0])
        drop = tk.OptionMenu(self.frame, clicked, *com_ports, 
                                      command=self.connect_ctrl)
        drop.config(width=10)
        return clicked, drop
        
        
    def BaudOptions(self, clicked=False, default=-1):
        
        if not clicked: clicked=tk.StringVar()
        bds = ["-", "300", "600", "1200", "2400", "4800", "9600", "14400", 
               "19200", "28800", "38400", "56000", "57600", "115200", 
               "128000", "256000"]
        clicked.set(bds[default])
        drop = tk.OptionMenu(self.frame, clicked, *bds, 
                                       command = self.connect_ctrl)
        drop.config(width=10)
        return clicked, drop
        
        
    def publish(self):
        self.frame.grid(row=0, column=0, rowspan=3, columnspan=3, 
                        padx=5, pady=5)
        
        self.label_printer.grid(column=1, row=0)
        self.label_scale.grid(column=2, row=0)
        
        self.label_com.grid(column=0, row=1)
        self.label_bd.grid(column=0, row=2)
        
        self.drop_com.grid(column=1, row=1)
        self.drop_baud.grid(column=1, row=2)
        
        self.drop_scale_com.grid(column=2, row=1)
        self.drop_scale_baud.grid(column=2, row=2)
        
        self.bnt_refresh.grid(column=3, row =1)
        self.bnt_connect.grid(column=3, row =2)
        
        
    def connect_ctrl(self, widget):
        check = [self.clicked_com.get(), self.clicked_bd.get(), 
                 self.clicked_scale_com.get(), self.clicked_scale_bd.get()]
        if '-' in check:
            state = "disable"
        else:
            state = "active"
  
        self.bnt_connect["state"] = state
        pass
    
    
    def com_refresh(self):
        self.drop_com.destroy()
        self.drop_scale_com.destroy()
        _, self.drop_com=self.ComOptions(self.serial, clicked=self.clicked_com)
        _, self.drop_scale_com=self.ComOptions(self.serial2,
                                               clicked=self.clicked_scale_com)
        self.drop_com.grid(column=1, row=1)
        self.drop_scale_com.grid(column=2, row=1)
        self.connect_ctrl([])
        
    
    def serial_connect(self):
        if DEBUG:
            self.root.startTime=time.time()
            
            self.serial.t0 = threading.Thread(
                target= self.serial.EmulateSerialSync, args=(self, ), 
                daemon=True)
            self.serial.t0.start()
        
        elif self.bnt_connect["text"] in "Connect":
            self.serial.SerialOpen(self.clicked_com, self.clicked_bd)
            self.serial2.SerialOpen(self.clicked_scale_com,
                                    self.clicked_scale_bd)
            if self.serial.ser.status and self.serial2.ser.status:
                self.bnt_connect["text"]="Disconnect"
                self.bnt_refresh["state"]="disable"
                self.drop_baud["state"]="disable"
                self.drop_com["state"]="disable"
                self.drop_scale_baud["state"]="disable"
                self.drop_scale_com["state"]="disable"
                
                
                self.root.startTime=time.time()
                self.serial.t0 = threading.Thread(
                    target = self.serial.SerialSyncPrinter, args=(self, ),
                    daemon= True)
                self.serial.t1 = threading.Thread(
                    target = self.serial.SerialSyncScale, args=(self, ),
                    daemon= True)
                self.serial.t0.start()
                self.serial.t1.start()
                
            else:
                ErrorMsg = f"Failure to establish UART connection using {self.clicked_com.get()}"
                tk.messagebox.showerror("showerror", ErrorMsg)
                
        else:
            self.serial.threading = False
            self.serial.SerialClose()
            self.bnt_connect["text"]="Connect"
            self.bnt_refresh["state"]="active"
            self.drop_baud["state"]="active"
            self.drop_com["state"]="active"
        pass
    

class ConnGUI():
    def __init__(self, root, serial, serial2, data):
        self.root = root
        self.serial = serial
        self.serial2 = serial2
        self.data=data
        self.numLog = 0
        
        
        self.frame = tk.LabelFrame(root, text="Printer Controller", 
                                padx=5, pady=5, bg='white')
        
        self.scaleFrame = tk.LabelFrame(root, text="Scale Control", 
                                        padx=5, pady=5, bg='white')
        
        self.label_temp = tk.Label(self.frame, text='Temperature:', 
                                    bg='white', anchor="w", width=15)
        self.label_ext = tk.Label(self.frame, text='Extrusion:', 
                                    bg='white', anchor ="w", width=15)

        self.label_isttemp = tk.Label(self.frame, text="--", 
                                    bg='white', fg='red', width=10)
        self.label_ext_len = tk.Label(self.frame, text='Length', 
                                    bg='white', width=10)
        self.label_ext_speed = tk.Label(self.frame, text='Volume Flow Rate', 
                                    bg='white', width=15)
        
        self.label_Gcode = tk.Label(self.frame, text='GCode:', 
                                    bg='white', width=15, anchor="w")
        
        self.temp = tk.StringVar()
        self.ext_len = tk.StringVar()
        self.ext_speed = tk.StringVar()
        self.Gcode = tk.StringVar()
        
        self.entry_temp = tk.Entry(self.frame, textvariable=self.temp, 
                                   bd=1, width= 5)
        self.entry_ext_len = tk.Entry(self.frame, textvariable=self.ext_len,
                                      bd=1, width=5)
        self.entry_ext_speed = tk.Entry(self.frame, textvariable=self.ext_speed,
                                        bd=1, width=5)
        self.entry_Gcode = tk.Entry(self.frame, textvariable=self.Gcode,
                                    bd=2, width = 25)
        
        self.bnt_temp = tk.Button(self.frame, text="ON", width=2, 
                                     command=self.SetTemperature, 
                                     bg='red')
        self.bnt_ext = tk.Button(self.frame, text="GO", 
                                     width=2, command=self.Extrusion)
        
        self.bnt_Gcode = tk.Button(self.frame, text="Send", 
                                     width=2, command=self.sendGcode)
        
        self.bnt_tare = tk.Button(self.scaleFrame, text="Tare", width=3, 
                                  command=self.tare)
        self.bnt_calibrateScale = tk.Button(self.scaleFrame,
                                            text="Calibration", width=8, 
                                  command=self.setReferenceValue)
        self.logWindow(root)
        self.ConnGUIOpen()
        self.setDefalut()
        
        #self.root.after(1, self.updateConnGUI())
        pass
    
    
    def ConnGUIOpen(self):
        self.frame.grid(row=0, column=3, rowspan=3, columnspan=3, 
                        padx=2, pady=2)
        
        self.label_Gcode.grid(row=0, column=0)
        self.entry_Gcode.grid(row=0, column=1, columnspan=2)
        
        self.label_temp.grid(row=1, column=0)
        self.label_ext.grid(row=2, column=0, rowspan = 2)
        
        self.label_isttemp.grid(row=1, column=1)
        self.label_ext_len.grid(row=2, column=1)
        self.label_ext_speed.grid(row=2, column=2)
        
        self.entry_temp.grid(row=1, column=2)
        self.entry_ext_len.grid(row=3, column=1)
        self.entry_ext_speed.grid(row=3, column=2)
        
        self.bnt_Gcode.grid(row=0, column=3)
        self.bnt_temp.grid(row=1, column=3)
        self.bnt_ext.grid(row=3, column=3)
        
        self.dataCanvas.grid(row=5, column=0, columnspan=8, padx=5)
        self.vsb.grid(row=5, column=8, rowspan=5, sticky='ns')
        
        self.scaleFrame.grid(row=0, column=7, rowspan=3,
                             columnspan=2, padx=2, pady=2)
        
        self.bnt_tare.grid(row=0, column=0)
        self.bnt_calibrateScale.grid(row=1, column=0)
        
        
    def setDefalut(self):
        self.entry_ext_speed.insert(-1, '20')
        self.entry_ext_len.insert(-1, '100')
        self.entry_temp.insert(-1, '200')
        
        
    def logWindow(self, root):
        self.dataCanvas = tk.Canvas(root, width = 1000, heigh=120, bg='white')
        self.vsb = tk.Scrollbar(root, orient='vertical', 
                                command=self.dataCanvas.yview)
        self.dataCanvas.config(yscrollcommand=self.vsb.set)
        
        self.dataFrame=tk.Frame(self.dataCanvas, bg='white')
        self.dataCanvas.create_window((10,0), window=self.dataFrame,
                                      anchor='nw')
        
        
    def updateConnGUI(self, msg):
        if msg!='':
            self.numLog += 1
            textList = msg.split(':')
            textList.insert(0,str(self.numLog))
            for i,t in enumerate(textList):
                tk.Label(self.dataFrame, text=t, font=('Calibri', '10'),
                     bg='white', anchor='w', justify=tk.LEFT).grid(
                row=self.numLog, column=i)
                
            self.dataCanvas.config(scrollregion=self.dataCanvas.bbox('all'))


    def SetTemperature(self):    
        if 'red' in self.bnt_temp['bg']:
            code = 'M104 S{}\r\n'.format(self.temp.get())
            self.bnt_temp.configure(bg='green')
        else:
            code = 'M104 S0 \r\n'
            self.bnt_temp.configure(bg='red')
        if DEBUG:
            print(code)
        else:
            self.serial.ser.write(bytes(code, 'utf-8'))
            time.sleep(0.5)
        pass
    
    
    def Extrusion(self):
        speed = int(self.ext_speed.get())/(1.75*1.75)*240
        code = 'G1 E{} F{}\r\n'.format(self.ext_len.get(), int(speed))
        if DEBUG:
            print(code)
        else:
            self.serial.ser.write(bytes(code, 'utf-8'))
        time.sleep(1)
        

    def sendGcode(self):
        code= self.Gcode.get()+'\r\n'
        if DEBUG:
            print(code)
        else:
            self.serial.ser.write(bytes(code, 'utf-8'))
        time.sleep(1)
        self.Gcode.set('')
        
    def tare(self):
        if DEBUG:
            print('TARE!')
        else:
            self.serial2.ser.write('t')
        pass
    
    def setReferenceValue(self):
        if DEBUG:
            print('Calibration!')
        else:
            self.serial2.ser.write('c')
        pass
        
        
class DisGUI():
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data

        self.disFrame = tk.LabelFrame(self.root, text="Display Frame", padx=5, pady=5,
                                      bg='white')
        self.disFrame.grid(padx=5, column=0, row=3, columnspan=8, sticky='nw')
        self.AddChart()

    def AddChart(self):
        self.fig = []
        self.fig.append(plt.Figure(figsize=(12,6), dpi=80))
        self.fig.append(self.fig[-1].add_subplot(111))
        self.fig.append(FigureCanvasTkAgg(self.fig[0], 
                                          master= self.disFrame))
        self.fig[-1].get_tk_widget().grid(column=0, row=0, sticky='n')
        pass
    
    def killChart(self):
        self.fig.pop()
        
    def updateChart(self):
        try:
            dat = np.array(self.data.dataDict.get('force'))
            self.fig[1].plot(dat[:,0], dat[:,1], color='green', linewidth=1)
            self.fig[1].grid(color='b', linestyle='-', linewidth=0.2)
            self.fig[0].canvas.draw()
        except Exception as e:
            print(f'Display dont work due to: {e}')
        pass
      
             
if __name__ == '__main__':
    RootGUI()
    ComGUI()
    ConnGUI()
    DisGUI()
        
          
