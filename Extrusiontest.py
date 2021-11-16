
from Extrusiontest_GUI import RootGUI, ComGUI
from Serial_Com_ctrl import SerialCtrl
from Data_com import DataMaster

RootMaster = RootGUI()
MyData = DataMaster()
MySerial = SerialCtrl()

ComMaster = ComGUI(RootMaster.root, MySerial, MyData)

def on_closing():
    MyData.cleanAndExit()
    ComMaster.dis.killChart()
    MySerial.threading=False
    RootMaster.root.destroy()

RootMaster.root.protocol("WM_DELETE_WINDOW", on_closing)
RootMaster.root.mainloop()
