
import sys
import glob


import time
try:
    import tkinter as tk
except:
    import Tkinter as tk

DEBUG = True

class RootGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Printer Communication")
        self.root.geometry("420x120")
        self.root.config(bg="white")
        
class ComGUI():
    def __init__(self,root,serial):
        self.root = root
        self.serial = serial
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
        
        self.clicked_bd.set(bds[0])
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
            self.conn = ConnGUI(self.root, self.serial)
            pass
        
        if self.bnt_connect["text"] in "Connect":
            self.serial.SerialOpen(self)
            if self.serial.ser.status:
                self.bnt_connect["text"]="Disconnect"
                self.bnt_refresh["state"]="disable"
                self.drop_baud["state"]="disable"
                self.drop_com["state"]="disable"
                
                self.conn = ConnGUI(self.root, self.serial)
            else:
                ErrorMsg = f"Failure to establish UART connection using {self.clicked_com.get()}"
                tk.messagebox.showerror("showerror", ErrorMsg)
                
        else:
            self.serial.SerialClose()
            self.bnt_connect["text"]="Connect"
            self.bnt_refresh["state"]="active"
            self.drop_baud["state"]="active"
            self.drop_com["state"]="active"
        pass

class ConnGUI():
    def __init__(self, root, serial):
        self.root = root
        self.serial = serial
        
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
        
        self.entry_temp = tk.Entry(self.frame, bd=5, width= 15)
        self.entry_ext_len = tk.Entry(self.frame, bd=5, width=10)
        self.entry_ext_speed = tk.Entry(self.frame, bd=5, width=15)
        
        self.bnt_temp = tk.Button(self.frame, text="OFF", width=2, 
                                     command=self.SetTemperature, 
                                     bg='red')
        self.bnt_ext = tk.Button(self.frame, text="GO", 
                                     width=2, command=self.Extrusion)
        
        self.ConnGUIOpen()
        self.setDefalut()
        pass
    
    def ConnGUIOpen(self):
        self.root.geometry('800x120')
        self.frame.grid(row=0, column=4, rowspan=4, columnspan=5, 
                        padx=5, pady=5)
        
        self.label_temp.grid(row=0, column=0)
        self.label_ext.grid(row=1, column=0, rowspan = 2)
        
        self.label_isttemp.grid(row=0, column=1)
        self.label_ext_len.grid(row=1, column=1)
        self.label_ext_speed.grid(row=1, column=2)
        
        self.entry_temp.grid(row=0, column=2)
        self.entry_ext_len.grid(row=2, column=1)
        self.entry_ext_speed.grid(row=2, column=2)
        
        self.bnt_temp.grid(row=0, column=3)
        self.bnt_ext.grid(row=2, column=3)
        
    def setDefalut(self):
        self.entry_ext_speed.insert(-1, '1000')
        self.entry_ext_len.insert(-1, '100')
        self.entry_temp.insert(-1, '200')
        
    def SetTemperature(self):
        pass
    
    def Extrusion(self):
        pass


        
        
        
"""        
def get_serial_ports():
        com_ports=list(ports.comports())
        return com_ports

def sendGcode(code, ser):
    for line in code.split('\n'):
        ser.write(line)
        time.sleep(1)
        
def write_Extrusion_Gcode(length, speed, purge=8):
    code = 'G1 E{} F1000\n'.format(purge)
    code += 'G4 S1\n'
    code += 'G1 E{} F{}\n'.format(length, speed)
    return code 

def get_Temperature(ser, i=1):
    sendGcode('M105 S'+str(int(i)), ser)

"""       
if __name__ == '__main__':
    RootGUI()
    ComGUI()
    ConnGUI()
        
          