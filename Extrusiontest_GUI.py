
import sys
import glob


import time
try:
    import tkinter as tk
except:
    import Tkinter as tk


class RootGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Printer Communication")
        self.root.geometry("360x120")
        self.root.config(bg="white")
        
class ComGUI():
    def __init__(self,root,serial):
        self.root = root
        self.serial = serial
        self. frame = tk.LabelFrame(root, text="COM Manager", padx=5, pady=5, 
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
        
        if self.bnt_connect["text"] in "Connect":
            self.serial.SerialOpen(self)
            if self.serial.ser.status:
                self.bnt_connect["text"]="Disconnect"
                self.bnt_refresh["state"]="disable"
                self.drop_baud["state"]="disable"
                self.drop_com["state"]="disable"
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
    RootGUI().root.mainloop()
        
          