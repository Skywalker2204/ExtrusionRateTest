
from Extrusiontest_GUI import RootGUI, ComGUI
from Serial_Com_ctrl import SerialCtrl

RootMaster = RootGUI()
MySerial = SerialCtrl()

ComMaster = ComGUI(RootMaster.root, MySerial)

RootMaster.root.mainloop()
            