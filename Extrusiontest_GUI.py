
import sys
import glob

import threading
import time
try:
    import tkinter as tk
except:
    import Tkinter as tk
    
    

DEBUG = False

class RootGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Printer Communication")
        self.root.geometry("420x120")
        self.root.config(bg="white")
        
class ComGUI():
    def __init__(self,root,serial, data):
        self.root = root
        self.serial = serial
        self.data = data
        
        self.frame = tk.LabelFrame(root, text="COM Manager", padx=5, pady=5, 
                                 bg="white")
        self.label_com = tk.Label(self.frame, 
                               text="Avaliable Ports:", bg="white", width=15, 
                               anchor="w")
        self.label_bd = tk.Label(self.frame, 
                               text="Baude Rate:", bg="white", width=15, 
                               anchor="w")
        self.ComOptions()
        self.BaudOptions()
        
        self.bnt_refresh = tk.Button(self.frame, text="Refresh", width=10, 
                                     command=self.com_refresh)
        self.bnt_connect = tk.Button(self.frame, text="Connect", 
                                     width=10, state="disable", 
                                     command=self.serial_connect)
        self.publish()
        
    def ComOptions(self):
        com_ports=self.serial.getCOMList()
        self.clicked_com = tk.StringVar()
        self.clicked_com.set(com_ports[0])
        self.drop_com = tk.OptionMenu(self.frame, self.clicked_com, *com_ports, 
                                      command=self.connect_ctrl)
        self.drop_com.config(width=10)
        
    def BaudOptions(self):
        
        self.clicked_bd = tk.StringVar()
        bds = ["-", "300", "600", "1200", "2400", "4800", "9600", "14400", 
               "19200", "28800", "38400", "56000", "57600", "115200", 
               "128000", "256000"]
        
        self.clicked_bd.set(bds[-1])
        self.drop_baud = tk.OptionMenu(self.frame, self.clicked_bd, *bds, 
                                       command = self.connect_ctrl)
        self.drop_baud.config(width=10)
        
        
    def publish(self):
        self.frame.grid(row=0, column=0, rowspan=3, columnspan=3, 
                        padx=5, pady=5)
        self.label_com.grid(column=1, row=2)
        self.label_bd.grid(column=1, row=3)
        
        self.drop_com.grid(column=2, row=2)
        self.drop_baud.grid(column=2, row=3)
        
        self.bnt_refresh.grid(column=3, row =2)
        self.bnt_connect.grid(column=3, row =3)
        
    def connect_ctrl(self, widget):
        if '-' in self.clicked_com.get() or "-" in self.clicked_bd.get():
            state = "disable"
        else:
            state = "active"
  
        self.bnt_connect["state"] = state
        pass
    
    def com_refresh(self):
        self.drop_com.destroy()
        self.ComOptions()
        self.drop_com.grid(column=2, row=2)
        self.connect_ctrl([])
    
    def serial_connect(self):
        if DEBUG:
            self.conn = ConnGUI(self.root, self.serial, self.data)
            pass
        
        if self.bnt_connect["text"] in "Connect":
            self.serial.SerialOpen(self)
            if self.serial.ser.status:
                self.bnt_connect["text"]="Disconnect"
                self.bnt_refresh["state"]="disable"
                self.drop_baud["state"]="disable"
                self.drop_com["state"]="disable"
                
                self.conn = ConnGUI(self.root, self.serial, self.data)
                
                self.serial.t1 = threading.Thread(
                    target = self.serial.SerialSync, args=(self, ),
                    daemon= True)
                self.serial.t1.start()
                time.sleep(20) 
                self.serial.startStream(self.data.startStream)
                
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
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data=data
        self.numLog = 0
        
        
        self.frame = tk.LabelFrame(root, text="Printer Controller", 
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
        
        self.logWindow(root)
        
        self.ConnGUIOpen()
        self.setDefalut()
        
        #self.root.after(1, self.updateConnGUI())
        pass
    
    
    def ConnGUIOpen(self):
        self.root.geometry('1100x360')
        self.frame.grid(row=0, column=4, rowspan=3, columnspan=5, 
                        padx=5, pady=5)
        
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
        
        self.dataCanvas.grid(row=4, column=0, columnspan=6, rowspan=5)
        self.vsb.grid(row=4, column=6, rowspan=5, sticky='ns')
        
        
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
        self.numLog += 1
        text = str(self.numLog) + '\t' + msg
        tk.Label(self.dataFrame, text=text,
                         font=('Calibri', '10'), bg='white',
                 anchor='w', justify=tk.LEFT).pack()
                
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
        


        
             
if __name__ == '__main__':
    RootGUI()
    ComGUI()
    ConnGUI()
        
          
