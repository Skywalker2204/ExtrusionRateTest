
from Extrusiontest_GUI import RootGUI, ComGUI
from Serial_Com_ctrl import SerialCtrl
from Data_com import DataMaster

RootMaster = RootGUI()
MyData = DataMaster()
MySerial = SerialCtrl()

ComMaster = ComGUI(RootMaster.root, MySerial, MyData)

RootMaster.root.mainloop()
